"""Plan capture, guarded execution, verification and rollback."""
from __future__ import annotations

import copy
import difflib
import functools
import hashlib
import os
import re
import shutil
import stat
import tempfile
import time
import sys
import subprocess
import select
from pathlib import Path

from tune_catalog import operations_for, profile_available, PROFILE_META
from tune_probe import read_text, run
from tune_state import TuningError, digest, identity, uuid_hex
from tune_desktop import Desktop, DISPLAY
from tune_policies import settings_ops, constraints

BEGIN = "# BEGIN deepin-system-tuning\n"
END = "# END deepin-system-tuning\n"
MAX_FILE = 1024 * 1024
PLAN_TTL = 30 * 60
CONTEXT_KEYS = {"intent", "power_source", "priority",
                "allow_service_restart", "active_app", "notes", "settings"}


def _sha(content):
    return hashlib.sha256((content or "").encode("utf-8")).hexdigest()


def _normalize(value):
    return (value or "").strip()


def _clone(value):
    return copy.deepcopy(value)


def _locked(function):
    @functools.wraps(function)
    def wrapper(store, *args, **kwargs):
        with store.locked():
            return function(store, *args, **kwargs)
    return wrapper


class System:
    """Controlled adapter for the small set of operations in the catalog."""

    def __init__(self, snapshot, runner=None):
        self.snapshot = snapshot
        self.home = Path(snapshot.get("home") or Path.home()).expanduser()
        self.runner = runner or run
        self.capabilities = snapshot.get("capabilities") or {}
        self.euid = os.geteuid()
        self.privileged = bool(self.capabilities.get("privileged")) or self.euid == 0
        self.tools = snapshot.get("tools") or {}

    # ------------------------------------------------------------- commands
    def _run(self, argv, timeout=8.0, priv=False):
        command = [str(item) for item in argv]
        if priv:
            if not self.privileged:
                raise TuningError("该操作需要 root 或免交互 sudo")
            if self.euid != 0:
                command = ["sudo", "-n"] + command
        result = self.runner(command, timeout=timeout,
                             env={"PATH": "/usr/sbin:/usr/bin:/sbin:/bin"})
        if not isinstance(result, dict):
            raise TuningError("命令适配器返回了无效结果")
        return result

    def _ok(self, argv, timeout=8.0, priv=False):
        result = self._run(argv, timeout=timeout, priv=priv)
        if not result.get("ok"):
            raise TuningError((result.get("err") or result.get("out") or "命令执行失败")[:500])
        return result.get("out", "")

    def validate_control(self, argv):
        if not isinstance(argv, list) or not argv or not all(isinstance(item, str) for item in argv):
            raise TuningError("服务控制命令格式无效")
        if argv[:2] not in (["systemctl", "reload"], ["systemctl", "restart"]):
            raise TuningError("服务控制命令不在白名单内")
        unit = argv[2] if len(argv) == 3 else ""
        reloadable = (
            unit == "NetworkManager.service"
            or re.fullmatch(r"postgresql(@[0-9]+-main)?\.service", unit)
            or unit in ("mariadb.service", "mysql.service")
        )
        if argv[1] == "reload" and not reloadable:
            raise TuningError("不允许重载该服务：%s" % unit)
        if argv[1] == "restart" and not re.fullmatch(r"postgresql(@[0-9]+-main)?\.service|mariadb\.service|mysql\.service", unit):
            raise TuningError("不允许重启该服务：%s" % unit)
        return list(argv)

    def validate_config(self, argv):
        if not isinstance(argv, list) or argv not in (
            ["mysqld", "--validate-config"],
            ["mysqld", "--help", "--verbose"],
            ["mariadbd", "--help", "--verbose"],
        ):
            raise TuningError("数据库配置校验命令不在白名单内")
        return list(argv)

    # ---------------------------------------------------------------- paths
    def validate_target(self, path, scope):
        if not isinstance(path, str) or not path or "\x00" in path:
            raise TuningError("目标路径无效")
        normalized = os.path.normpath(path)
        if not normalized.startswith("/") or ".." in Path(normalized).parts:
            raise TuningError("目标路径必须是规范化的绝对路径")
        if scope == "user":
            expected = (self.home / ".config/environment.d/90-deepin-tuning.conf").absolute()
            if Path(normalized) != expected:
                raise TuningError("用户配置只允许写入环境变量片段")
            return Path(normalized)
        allowed = (
            r"/etc/sysctl\.d/90-deepin-tuning\.conf",
            r"/etc/modprobe\.d/90-deepin-tuning\.conf",
            r"/etc/NetworkManager/conf\.d/90-deepin-tuning\.conf",
            r"/etc/security/limits\.d/90-deepin-tuning\.conf",
            r"/etc/postgresql/[^/]+/main/conf\.d/90-deepin-tuning\.conf",
            r"/etc/mysql/(?:mariadb\.conf\.d|conf\.d)/90-deepin-tuning\.cnf",
        )
        if not any(re.fullmatch(pattern, normalized) for pattern in allowed):
            raise TuningError("目标路径不在本技能允许的系统配置范围内")
        return Path(normalized)

    def read_target(self, path, scope):
        target = self.validate_target(path, scope)
        if target.is_symlink():
            raise TuningError("拒绝操作符号链接：%s" % path)
        try:
            info = target.stat()
        except FileNotFoundError:
            return {"exists": False, "content": "", "mode": None, "sha256": None}
        except PermissionError:
            if not self.privileged:
                raise TuningError("没有权限读取目标文件")
            content = self._ok(["cat", str(target)], priv=True)
            if "\x00" in content:
                raise TuningError("目标文件包含 NUL，拒绝处理")
            return {"exists": True, "content": content, "mode": None, "sha256": _sha(content)}
        except OSError as exc:
            raise TuningError("无法读取目标文件：%s" % exc) from exc
        if not stat.S_ISREG(info.st_mode):
            raise TuningError("目标不是普通文件：%s" % path)
        if info.st_size > MAX_FILE:
            raise TuningError("目标文件超过 1 MiB，拒绝处理")
        try:
            content = target.read_text(encoding="utf-8")
        except PermissionError:
            if not self.privileged:
                raise TuningError("没有权限读取目标文件")
            content = self._ok(["cat", str(target)], priv=True)
        except (OSError, UnicodeDecodeError) as exc:
            raise TuningError("无法读取 UTF-8 配置：%s" % exc) from exc
        if "\x00" in content:
            raise TuningError("目标文件包含 NUL，拒绝处理")
        return {
            "exists": True,
            "content": content,
            "mode": stat.S_IMODE(info.st_mode),
            "sha256": _sha(content),
        }

    def write_target(self, path, scope, content, mode="0644"):
        target = self.validate_target(path, scope)
        if target.is_symlink():
            raise TuningError("拒绝写入符号链接：%s" % path)
        if "\x00" in content:
            raise TuningError("配置内容包含 NUL")
        file_mode = int(str(mode), 8)
        if scope == "user":
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            fd, temporary = tempfile.mkstemp(prefix=".deepin-tuning-", dir=str(target.parent))
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    handle.write(content)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.chmod(temporary, file_mode)
                os.replace(temporary, target)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
            return
        parent = target.parent
        if not parent.exists():
            self._ok(["install", "-d", "-m", "0755", str(parent)], priv=True)
        if self.euid == 0:
            fd, temporary = tempfile.mkstemp(prefix=".deepin-tuning-", dir=str(parent))
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    handle.write(content)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.chmod(temporary, file_mode)
                os.replace(temporary, target)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
            return
        directory = tempfile.mkdtemp(prefix="deepin-tuning-", dir="/tmp")
        temporary = Path(directory) / "content"
        try:
            temporary.write_text(content, encoding="utf-8")
            temporary.chmod(0o600)
            self._ok(["install", "-m", "%04o" % file_mode, "--", str(temporary), str(target)], priv=True)
        finally:
            shutil.rmtree(directory, ignore_errors=True)

    def remove_target(self, path, scope):
        target = self.validate_target(path, scope)
        if target.is_symlink():
            target.unlink()
            return
        if not target.exists():
            return
        if scope == "user" or self.euid == 0:
            target.unlink()
        else:
            self._ok(["rm", "-f", str(target)], priv=True)

    def desktop_adapter(self, op):
        session = (self.snapshot.get("desktop_native") or {}).get("session") or os.environ.get("XDG_SESSION_TYPE", "")
        expected = op["target"].get("session")
        if session and expected and session != expected:
            raise TuningError("桌面会话类型已变化，无法操作原会话设置")
        adapter = Desktop(lambda argv, timeout=4: self._run(argv, timeout=timeout,
                          priv=op.get("requires_root", False)), session=expected or session)
        if op["target"].get("backend") == "dconfig":
            spec = adapter.dconfig_spec(op["target"]["setting"])
            if spec and "global" in adapter.metadata(spec).get("flags", []) and not op.get("requires_root"):
                raise TuningError("dconfig 作用域已变化或缺少系统级权限声明，请重新探测和生成计划")
        return adapter

    # ---------------------------------------------------------- gsettings
    def gsettings_get(self, schema, key):
        if not self.tools.get("gsettings"):
            return None
        result = self._run(["gsettings", "get", schema, key], timeout=5)
        return _normalize(result.get("out")) if result.get("ok") else None

    def gsettings_set(self, schema, key, value):
        self._ok(["gsettings", "set", schema, key, value], timeout=5)

    # ------------------------------------------------------------- sysctl
    def read_sysctl(self, key):
        text = read_text("/proc/sys/" + key.replace(".", "/"), "").strip()
        try:
            return int(text)
        except ValueError:
            return text or None

    # ------------------------------------------------------------ services
    def service_state(self, unit):
        enabled = None
        active = None
        if not self.tools.get("systemctl"):
            return {"enabled": None, "active": None}
        result = self._run(["systemctl", "is-enabled", unit], timeout=4)
        output = _normalize(result.get("out"))
        enabled = "enabled" if result.get("ok") else (
            output if output in ("disabled", "static", "masked", "indirect", "generated") else "disabled")
        result = self._run(["systemctl", "is-active", unit], timeout=4)
        output = _normalize(result.get("out"))
        active = "active" if result.get("ok") else (
            output if output in ("inactive", "failed", "activating", "deactivating") else "inactive")
        return {"enabled": enabled, "active": active}

    def service_restart_marker(self, unit):
        if not unit or not self.tools.get("systemctl"):
            return None
        result = self._run(["systemctl", "show", unit, "-p",
                            "ActiveEnterTimestampMonotonic", "--value"], timeout=4)
        if not result.get("ok"):
            return None
        return _normalize(result.get("out")) or None

    # ----------------------------------------------------- power backends
    def power_profile(self):
        if not self.tools.get("powerprofilesctl"):
            return None
        result = self._run(["powerprofilesctl", "get"], timeout=4)
        return _normalize(result.get("out")) if result.get("ok") else None

    def tuned_profile(self):
        if not self.tools.get("tuned-adm"):
            return None
        result = self._run(["tuned-adm", "active"], timeout=4)
        if not result.get("ok"):
            return None
        text = _normalize(result.get("out"))
        return text.split(":", 1)[1].strip() if ":" in text else text or None

    def preview_rollback_commands(self, op):
        kind = op["kind"]
        if kind == "desktop":
            commands = self.desktop_adapter(op).preview(op["target"], op["before"]["value"], op["before"])
            return [["sudo", "-n"] + cmd for cmd in commands] if op.get("requires_root") and self.euid != 0 else commands
        if kind == "gsettings":
            return [["gsettings", "set", op["target"]["schema"], op["target"]["key"], op["before"]["repr"]]]
        if kind in ("file", "modprobe"):
            before = op["before"]
            if before.get("exists"):
                install = ["install", "-m", "%04o" % (before.get("mode") or 0o644),
                           "<original-content>", op["target"]["path"]]
                commands = [(["sudo", "-n"] + install) if op["target"].get("scope") == "system" and self.euid != 0 else install]
            else:
                remove = ["rm", "-f", op["target"]["path"]]
                commands = [(["sudo", "-n"] + remove) if op["target"].get("scope") == "system" and self.euid != 0 else remove]
            if op["desired"].get("reload"):
                commands.append(["sudo", "-n"] + op["desired"]["reload"] if self.euid != 0 else op["desired"]["reload"])
            if op.get("restart_required") and op["desired"].get("restart"):
                commands.append(["sudo", "-n"] + op["desired"]["restart"] if self.euid != 0 else op["desired"]["restart"])
            return commands
        if kind == "sysctl":
            before = op["before"]
            commands = []
            if before["file"].get("exists"):
                commands.append(["install", "-m", "%04o" % (before["file"].get("mode") or 0o644),
                                 "<original-content>", op["target"]["path"]])
                commands.append(["sudo", "-n", "sysctl", "-p", op["target"]["path"]] if self.euid != 0
                                else ["sysctl", "-p", op["target"]["path"]])
            else:
                commands.append(["rm", "-f", op["target"]["path"]])
            pairs = ["%s=%s" % (key, value) for key, value in before.get("runtime", {}).items()
                     if value is not None]
            if pairs:
                commands.append(["sudo", "-n", "sysctl", "-w"] + pairs if self.euid != 0
                                else ["sysctl", "-w"] + pairs)
            return commands
        if kind == "service":
            before = op["before"]
            unit = op["target"]["unit"]
            commands = []
            if before.get("enabled") == "disabled":
                commands.append(["sudo", "-n", "systemctl", "disable", unit] if self.euid != 0 else ["systemctl", "disable", unit])
            elif before.get("enabled") == "enabled":
                commands.append(["sudo", "-n", "systemctl", "enable", unit] if self.euid != 0 else ["systemctl", "enable", unit])
            if before.get("active") == "inactive":
                commands.append(["sudo", "-n", "systemctl", "stop", unit] if self.euid != 0 else ["systemctl", "stop", unit])
            elif before.get("active") == "active":
                commands.append(["sudo", "-n", "systemctl", "start", unit] if self.euid != 0 else ["systemctl", "start", unit])
            return commands
        if kind == "power_profile":
            return [["powerprofilesctl", "set", op["before"]["profile"]]]
        if kind == "tuned_profile":
            return [["sudo", "-n", "tuned-adm", "profile", op["before"]["profile"]] if self.euid != 0
                    else ["tuned-adm", "profile", op["before"]["profile"]]]
        return []

    def restore_preview(self, op):
        current = self.capture_before(op)
        before = op.get("before")
        after = op.get("after")
        result = {"current": current, "before": before, "after": after}
        if op["kind"] == "sysctl":
            current_file = (current or {}).get("file") or {}
            before_file = (before or {}).get("file") or {}
            result["diff"] = _text_diff(current_file.get("content", ""), before_file.get("content", ""))
        elif op["kind"] in ("file", "modprobe"):
            result["diff"] = _text_diff((current or {}).get("content", ""),
                                        (before or {}).get("content", ""))
        return result

    def module_parameter(self, module, parameter):
        return read_text("/sys/module/%s/parameters/%s" % (module, parameter), "").strip() or None

    # ------------------------------------------------------- pre/post state
    def capture_before(self, op):
        kind = op["kind"]
        if kind == "desktop":
            adapter = self.desktop_adapter(op)
            adapter.validate(op["target"], op["desired"]["value"])
            return adapter.read(op["target"])
        if kind == "gsettings":
            target = op["target"]
            value = self.gsettings_get(target["schema"], target["key"])
            if value is None:
                raise TuningError("无法读取 gsettings %s %s" % (target["schema"], target["key"]))
            return {"repr": value}
        if kind in ("file", "modprobe"):
            target = op["target"]
            state = self.read_target(target["path"], target["scope"])
            if kind == "modprobe":
                state["module_parameters"] = {
                    module + "." + key: self.module_parameter(module, key)
                    for module, key, _ in _module_expectations(op)
                }
            return state
        if kind == "sysctl":
            target = op["target"]
            keys = op["desired"].get("loaded_entries") or op["desired"]["entries"]
            return {
                "file": self.read_target(target["path"], target["scope"]),
                "runtime": {key: self.read_sysctl(key) for key in keys},
            }
        if kind == "service":
            return self.service_state(op["target"]["unit"])
        if kind == "power_profile":
            value = self.power_profile()
            if value is None:
                raise TuningError("无法读取 power-profiles-daemon 当前配置")
            return {"profile": value}
        if kind == "tuned_profile":
            value = self.tuned_profile()
            if value is None:
                raise TuningError("无法读取 tuned 当前配置")
            return {"profile": value}
        if kind == "advisory":
            return None
        raise TuningError("未知操作类型：%s" % kind)

    def after_state(self, op, before):
        kind = op["kind"]
        if kind == "desktop":
            after = {"value": op["desired"]["value"]}
            if "default" in before:
                after.update(default=False, signature=before["signature"])
            if "monitor" in before:
                after["monitor"] = before["monitor"]
            if "explicit" in before:
                after["explicit"] = True
            return after
        if kind == "gsettings":
            return {"repr": op["desired"]["repr"]}
        if kind in ("file", "modprobe"):
            content = managed_content(before.get("content", ""), op["desired"]["block"],
                                      merge_existing=True,
                                      remove_keys=op["desired"].get("remove_keys"))
            mode = before.get("mode") if before.get("exists") and before.get("mode") is not None else int(op["desired"].get("mode", "0644"), 8)
            return {"exists": True, "content": content, "mode": mode, "sha256": _sha(content)}
        if kind == "sysctl":
            content = managed_content(before["file"].get("content", ""),
                                      ["%s = %s" % (key, value) for key, value in sorted(op["desired"]["entries"].items())],
                                      merge_existing=True)
            mode = before["file"].get("mode") if before["file"].get("exists") and before["file"].get("mode") is not None else int(op["desired"].get("mode", "0644"), 8)
            return {"file": {"exists": True, "content": content,
                             "mode": mode, "sha256": _sha(content)},
                    "runtime": sysctl_entries_from_content(content)}
        if kind == "service":
            return dict(op["desired"])
        if kind in ("power_profile", "tuned_profile"):
            return dict(op["desired"])
        return None

    # ------------------------------------------------------------ commands
    def preview_commands(self, op):
        kind = op["kind"]
        if kind == "desktop":
            commands = self.desktop_adapter(op).preview(op["target"], op["desired"]["value"])
            return [["sudo", "-n"] + cmd for cmd in commands] if op.get("requires_root") and self.euid != 0 else commands
        if kind == "gsettings":
            return [["gsettings", "set", op["target"]["schema"], op["target"]["key"], op["desired"]["repr"]]]
        if kind in ("file", "modprobe"):
            mode = (op.get("after") or {}).get("mode")
            install = ["install", "-m", "%04o" % (mode or int(op["desired"].get("mode", "0644"), 8)),
                       "<managed-content>", op["target"]["path"]]
            commands = [(["sudo", "-n"] + install) if op["target"].get("scope") == "system" and self.euid != 0 else install]
            if op["desired"].get("reload"):
                commands.append(["sudo", "-n"] + op["desired"]["reload"] if self.euid != 0 else op["desired"]["reload"])
            if op["desired"].get("validate"):
                commands.append(["sudo", "-n"] + op["desired"]["validate"] if self.euid != 0 else op["desired"]["validate"])
            if op["desired"].get("restart"):
                commands.append(["sudo", "-n"] + op["desired"]["restart"] if self.euid != 0 else op["desired"]["restart"])
            return commands
        if kind == "sysctl":
            return [["sudo", "-n", "sysctl", "-p", op["target"]["path"]] if self.euid != 0 else
                    ["sysctl", "-p", op["target"]["path"]]]
        if kind == "service":
            unit = op["target"]["unit"]
            desired = op["desired"]
            commands = []
            if desired.get("enabled") is True:
                commands.append(["sudo", "-n", "systemctl", "enable", unit] if self.euid != 0 else ["systemctl", "enable", unit])
            if desired.get("enabled") is False:
                commands.append(["sudo", "-n", "systemctl", "disable", unit] if self.euid != 0 else ["systemctl", "disable", unit])
            if desired.get("active") is True:
                commands.append(["sudo", "-n", "systemctl", "start", unit] if self.euid != 0 else ["systemctl", "start", unit])
            if desired.get("active") is False:
                commands.append(["sudo", "-n", "systemctl", "stop", unit] if self.euid != 0 else ["systemctl", "stop", unit])
            return commands
        if kind == "power_profile":
            return [["powerprofilesctl", "set", op["desired"]["profile"]]]
        if kind == "tuned_profile":
            return [["sudo", "-n", "tuned-adm", "profile", op["desired"]["profile"]] if self.euid != 0 else
                    ["tuned-adm", "profile", op["desired"]["profile"]]]
        return []


def _normalize_sysctl_value(value):
    text = str(value).strip()
    try:
        return int(text)
    except ValueError:
        return text.strip("'\"")


def sysctl_entries_from_content(content):
    entries = {}
    for line in (content or "").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", key):
            continue
        entries[key] = _normalize_sysctl_value(value)
    return entries


def _text_diff(current, before):
    lines = list(difflib.unified_diff((current or "").splitlines(),
                                      (before or "").splitlines(),
                                      fromfile="current", tofile="before", lineterm=""))
    text = "\n".join(lines)
    return text[:4000] + ("\n... (truncated)" if len(text) > 4000 else "")


def _config_key(line):
    stripped = line.strip()
    if stripped.startswith("#") or stripped.startswith("["):
        return stripped
    if "=" in stripped:
        return stripped.split("=", 1)[0].strip()
    if stripped.startswith("options "):
        parts = stripped.split()
        return "options " + parts[1] if len(parts) > 1 else stripped
    return " ".join(stripped.split()[:3])


def _merge_lines(existing, new_lines, remove_keys=None):
    remove_keys = set(remove_keys or ())
    result = [line for line in existing if _config_key(line) not in remove_keys]
    positions = {}
    for index, line in enumerate(result):
        positions.setdefault(_config_key(line), index)
    for line in new_lines:
        key = _config_key(line)
        if key in positions:
            result[positions[key]] = line
        else:
            positions[key] = len(result)
            result.append(line)
    return result


def managed_content(original, block, merge_existing=False, remove_keys=None):
    if not isinstance(block, list) or not block:
        raise TuningError("配置块为空")
    for line in block:
        if not isinstance(line, str) or "\x00" in line or "\n" in line:
            raise TuningError("配置行必须是单行字符串")
    if BEGIN in original or END in original:
        if original.count(BEGIN) != 1 or original.count(END) != 1:
            raise TuningError("现有托管标记不完整，拒绝修改")
        start = original.index(BEGIN)
        end = original.index(END, start + len(BEGIN))
        if end < start:
            raise TuningError("现有托管标记顺序异常")
        if merge_existing:
            existing = original[start + len(BEGIN):end]
            block = _merge_lines(existing.splitlines(), block, remove_keys=remove_keys)
        block_text = BEGIN + "\n".join(block).rstrip("\n") + "\n" + END
        return original[:start] + block_text + original[end + len(END):]
    block_text = BEGIN + "\n".join(block).rstrip("\n") + "\n" + END
    if not original:
        return block_text
    prefix = original.rstrip("\n")
    return prefix + "\n\n" + block_text if prefix else block_text


def op_key(op):
    kind = op["kind"]
    if kind == "desktop":
        return (kind, op["target"]["setting"], op["target"].get("monitor"))
    if kind == "gsettings":
        return (kind, op["target"]["schema"], op["target"]["key"])
    if kind in ("file", "modprobe", "sysctl"):
        return (kind, op["target"]["path"])
    if kind == "service":
        return (kind, op["target"]["unit"])
    if kind in ("power_profile", "tuned_profile"):
        return (kind, op["target"]["backend"])
    return (kind, op["title"])


def _merge_blocks(blocks):
    result = []
    seen = {}
    for block in blocks:
        for line in block:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#") or stripped.startswith("["):
                key = stripped
            elif "=" in stripped:
                key = stripped.split("=", 1)[0].strip()
            elif stripped.startswith("options "):
                parts = stripped.split()
                key = "options " + parts[1] if len(parts) > 1 else stripped
            else:
                key = " ".join(stripped.split()[:3])
            if key in seen and seen[key] != stripped:
                raise TuningError("配置键冲突：%s" % key)
            if key not in seen:
                seen[key] = stripped
                result.append(stripped)
    return result


def merge_operations(operations):
    merged = []
    conflicts = []
    index = {}
    for op in operations:
        key = op_key(op)
        if key not in index:
            op = _clone(op)
            op.setdefault("profiles", [op["profile"]])
            index[key] = op
            merged.append(op)
            continue
        current = index[key]
        if op["kind"] == "advisory":
            continue
        try:
            if op["kind"] in ("file", "modprobe"):
                if op["desired"].get("mode") != current["desired"].get("mode"):
                    raise TuningError("配置模式冲突")
                if op["desired"].get("reload") != current["desired"].get("reload"):
                    raise TuningError("服务重载目标冲突")
                if op["desired"].get("restart") != current["desired"].get("restart"):
                    raise TuningError("服务重启目标冲突")
                current["desired"]["block"] = _merge_blocks(
                    [current["desired"]["block"], op["desired"]["block"]])
                remove_keys = set(current["desired"].get("remove_keys") or ()) | set(op["desired"].get("remove_keys") or ())
                if remove_keys:
                    current["desired"]["remove_keys"] = sorted(remove_keys)
            elif op["kind"] == "sysctl":
                entries = dict(current["desired"]["entries"])
                changed = dict(current["desired"].get("changed_entries") or {})
                for name, value in op["desired"]["entries"].items():
                    if name in entries and entries[name] != value:
                        raise TuningError("sysctl 值冲突：%s" % name)
                    entries[name] = value
                changed.update(op["desired"].get("changed_entries") or {})
                current["desired"]["entries"] = entries
                current["desired"]["changed_entries"] = changed
            elif op["kind"] == "gsettings":
                if op["desired"] != current["desired"]:
                    raise TuningError("gsettings 值冲突：%s" % current["target"]["key"])
            elif op["kind"] == "service":
                if op["desired"] != current["desired"]:
                    raise TuningError("服务状态冲突：%s" % current["target"]["unit"])
            else:
                if op["desired"] != current["desired"]:
                    raise TuningError("电源后端目标冲突")
            if op["profile"] not in current["profiles"]:
                current["profiles"].append(op["profile"])
        except TuningError as exc:
            conflicts.append({
                "key": list(key),
                "profiles": sorted(set([current.get("profile"), op.get("profile")])),
                "reason": str(exc),
            })
    return merged, conflicts


def validate_context(context):
    if context is None:
        return {}
    if not isinstance(context, dict) or set(context) - CONTEXT_KEYS:
        raise TuningError("上下文只能包含 intent、power_source、priority、allow_service_restart、active_app、notes、settings")
    for key, value in context.items():
        if key == "settings":
            if not isinstance(value, dict):
                raise TuningError("settings 必须是设置对象")
            continue
        if key == "allow_service_restart":
            if not isinstance(value, bool):
                raise TuningError("%s 必须是布尔值" % key)
        elif not isinstance(value, str) or len(value) > 512 or any(ord(char) < 32 for char in value):
            raise TuningError("%s 必须是较短的普通字符串" % key)
    if context.get("power_source") not in (None, "ac", "battery", "unknown"):
        raise TuningError("power_source 只能是 ac、battery 或 unknown")
    return dict(context)


@_locked
def create_plan(store, snapshot, profiles, context=None, user_only=False, runner=None):
    context = validate_context(context)
    profiles = [profile for profile in profiles if profile]
    profiles = list(dict.fromkeys(profiles))
    if not profiles:
        raise TuningError("至少选择一个配置方案")
    for profile in profiles:
        if profile not in PROFILE_META:
            raise TuningError("未知配置方案：%s" % profile)
        available, reason = profile_available(profile, snapshot)
        if not available:
            raise TuningError("%s 不可用：%s" % (profile, reason))
    operations = []
    warnings = []
    for profile in profiles:
        for op in operations_for(profile, snapshot, context):
            op = _clone(op)
            op["profile"] = profile
            operations.append(op)
    explicit = settings_ops(snapshot, context.get("settings", {}))
    override_keys = {op_key(op) for op in explicit}
    operations = [op for op in operations if op_key(op) not in override_keys] + explicit
    if user_only:
        kept = [op for op in operations if not op.get("requires_root")]
        removed = len(operations) - len(kept)
        operations = kept
        if removed:
            warnings.append("user-only 已跳过 %d 个需要 root 的系统级操作。" % removed)
    operations, conflicts = merge_operations(operations)
    policy_conflicts, policy_warnings = constraints(operations, snapshot)
    if any(op.get("display_guard") for op in operations) and snapshot.get("desktop_native", {}).get("display_pending"):
        policy_conflicts.append({"key": ["display-staging"], "profiles": [], "reason": "控制中心存在尚未提交的显示改动，先完成或撤销这些改动"})
    conflicts += policy_conflicts
    warnings += policy_warnings
    # Mode / topology changes run after other writes and always under a watchdog.
    def dependency_order(op):
        key = op.get("target", {}).get("setting")
        if key in ("display.auto_brightness", "power.brightness_drop_percent"):
            return -2
        if key in ("power.mode", "power.saving"):
            return -1
        return 1 if op.get("display_guard") else 0
    operations.sort(key=dependency_order)
    system = System(snapshot, runner=runner)
    blocked = []
    for index, op in enumerate(operations):
        op["id"] = "op-%03d" % (index + 1)
        if op["kind"] == "advisory":
            op["executable"] = False
            op["reason"] = op.get("reason") or "仅建议"
            continue
        try:
            if not op.get("executable", True):
                raise TuningError(op.get("reason") or "设置能力不可用")
            if op["kind"] in ("file", "modprobe", "sysctl"):
                system.validate_target(op["target"]["path"], op["target"]["scope"])
            if op["requires_root"] and not system.privileged:
                raise TuningError("需要 root 或免交互 sudo")
            if op["kind"] == "gsettings" and not system.tools.get("gsettings"):
                raise TuningError("gsettings 不可用")
            if op["kind"] == "sysctl" and not system.tools.get("sysctl"):
                raise TuningError("sysctl 不可用")
            if op["kind"] == "service" and not system.tools.get("systemctl"):
                raise TuningError("systemctl 不可用")
            if op["kind"] == "power_profile" and not system.tools.get("powerprofilesctl"):
                raise TuningError("powerprofilesctl 不可用")
            if op["kind"] == "tuned_profile" and not system.tools.get("tuned-adm"):
                raise TuningError("tuned-adm 不可用")
            before = system.capture_before(op)
            after = system.after_state(op, before)
            if op["kind"] == "sysctl":
                loaded = after.get("runtime") or {}
                op["desired"]["loaded_entries"] = loaded
                before["runtime"] = {key: system.read_sysctl(key) for key in loaded}
            op["before"] = before
            op["after"] = after
        except (TuningError, OSError) as exc:
            op["executable"] = False
            op["reason"] = str(exc)
            blocked.append({"id": op["id"], "title": op["title"], "reason": str(exc)})
    if conflicts:
        warnings.append("存在方案冲突；执行前请只保留一个冲突方案。")
    if any(op.get("reboot_required") for op in operations):
        warnings.append("包含驱动参数：写入后需要重启才会生效，脚本不会自动重启。")
    if any(op.get("restart_required") for op in operations):
        warnings.append("包含需要重启服务的参数；执行时需显式 --allow-service-restart 才会重启。")
    if any(op.get("relogin_required") for op in operations):
        warnings.append("包含环境变量或 limits 配置：当前登录会话需要重新登录后才能继承。")
    has_writes = any(op["kind"] != "advisory" for op in operations)
    partial_ready = bool(has_writes and not conflicts and any(
        op.get("executable") for op in operations if op["kind"] != "advisory"))
    execute_ready = bool(has_writes and not conflicts and not blocked)
    spec = {
        "profiles": profiles,
        "context": context,
        "baseline": snapshot.get("metrics"),
        "operations": operations,
        "conflicts": conflicts,
        "warnings": warnings,
        "execute_ready": execute_ready,
        "partial_ready": partial_ready,
        "user_only": bool(user_only),
        "blocked": blocked,
        "requires_reboot": any(op.get("reboot_required") for op in operations),
        "requires_relogin": any(op.get("relogin_required") for op in operations),
        "requires_service_restart": any(op.get("restart_required") for op in operations),
    }
    plan = {
        "id": "plan-" + uuid_hex(),
        "hash": digest(spec),
        "created_at": int(time.time()),
        "expires_at": int(time.time()) + PLAN_TTL,
        "session": identity(),
        "uid": os.getuid(),
        "hardware": snapshot.get("hardware_hash"),
        "environment": {
            "home": snapshot.get("home"),
            "classification": snapshot.get("classification"),
            "capabilities": snapshot.get("capabilities"),
        },
        "spec": spec,
    }
    with store.locked():
        store.plan(plan)
    return plan


def plan_view(plan, snapshot, runner=None):
    """Public, read-only view of a plan; never includes captured file bodies."""
    return _plan_view(plan, True, System(snapshot, runner=runner))


def safe_preview_commands(system, op):
    if not op.get("executable", True):
        return {"commands": []}
    try:
        return {"commands": system.preview_commands(op)}
    except (TuningError, OSError, ValueError, KeyError) as exc:
        return {"commands": [], "preview_error": str(exc)}


def _plan_view(plan, dry_run, system):
    spec = plan["spec"]
    return {
        "ok": bool(spec.get("execute_ready")),
        "dry_run": dry_run,
        "plan_id": plan["id"],
        "profiles": spec["profiles"],
        "hardware": plan.get("hardware"),
        "expires_at": plan.get("expires_at"),
        "execute_ready": spec["execute_ready"],
        "partial_ready": spec.get("partial_ready", False),
        "blocked": spec["blocked"],
        "conflicts": spec["conflicts"],
        "warnings": spec["warnings"],
        "requires_reboot": spec["requires_reboot"],
        "requires_relogin": spec["requires_relogin"],
        "requires_service_restart": spec["requires_service_restart"],
        "operations": [
            {
                "id": op["id"],
                "profile": op["profile"],
                "profiles": op.get("profiles", [op["profile"]]),
                "category": op["category"],
                "kind": op["kind"],
                "title": op["title"],
                "description": op["description"],
                "requires_root": op.get("requires_root", False),
                "relogin_required": op.get("relogin_required", False),
                "restart_required": op.get("restart_required", False),
                "reboot_required": op.get("reboot_required", False),
                "executable": op.get("executable", True),
                "reason": op.get("reason"),
                "target": op.get("target"),
                "desired": op.get("desired"),
                **safe_preview_commands(system, op),
            }
            for op in spec["operations"]
        ],
    }


@_locked
def apply_plan(store, plan_id, snapshot, execute=False, allow_service_restart=False,
               allow_partial=False, runner=None):
    plan = store.load(plan_id)
    system = System(snapshot, runner=runner)
    if plan.get("hardware") != snapshot.get("hardware_hash"):
        raise TuningError("硬件指纹已变化，必须重新生成计划")
    if plan.get("expires_at", 0) < int(time.time()):
        raise TuningError("计划已过期，必须重新生成")
    if not execute:
        return _plan_view(plan, True, system)
    spec = plan["spec"]
    if not spec.get("execute_ready"):
        if not (allow_partial and spec.get("partial_ready")):
            raise TuningError("计划包含冲突或不可执行项；请先移除冲突并确认 blocked 原因，"
                              "或显式使用 --allow-partial 只执行可执行项")
    for active in store.latest():
        if active.get("display_guard", {}).get("state") == "armed":
            raise TuningError("已有待确认的显示变更；先确认或等待回滚")
    operations = copy.deepcopy(spec["operations"])
    if any(op.get("display_guard") for op in operations) and snapshot.get("desktop_native", {}).get("display_pending"):
        return {"ok": False, "dry_run": False, "plan_id": plan_id, "state": "conflict",
                "error": "控制中心存在尚未提交的显示改动，先完成或撤销后重新生成计划"}
    # Check every precondition before writing anything.
    for op in operations:
        if op["kind"] == "advisory" or not op.get("executable", True):
            continue
        if op.get("requires_root") and not system.privileged:
            return {"ok": False, "dry_run": False, "plan_id": plan_id, "state": "blocked",
                    "error": "执行环境缺少 root 或免交互 sudo：%s" % op["title"]}
        try:
            if op.get("display_guard") and system.desktop_adapter(op).bus.get(DISPLAY, "HasChanged"):
                raise TuningError("控制中心存在尚未提交的显示改动")
            current = system.capture_before(op)
        except (TuningError, OSError) as exc:
            return {"ok": False, "dry_run": False, "plan_id": plan_id, "state": "conflict",
                    "error": "无法重新读取原值：%s" % exc}
        if current != op.get("before"):
            return {"ok": False, "dry_run": False, "plan_id": plan_id, "state": "conflict",
                    "error": "计划生成后原值发生变化：%s" % op["title"]}
    change = {
        "id": "change-" + uuid_hex(),
        "plan_id": plan_id,
        "state": "applying",
        "created_at": int(time.time()),
        "uid": os.getuid(),
        "hardware": snapshot.get("hardware_hash"),
        "home": snapshot.get("home"),
        "session": identity(),
        "boot_id": (snapshot.get("host") or {}).get("boot_id") or _current_boot_id(),
        "tools": snapshot.get("tools"),
        "capabilities": snapshot.get("capabilities"),
        "profiles": spec["profiles"],
        "context": spec["context"],
        "baseline": spec.get("baseline"),
        "operations": operations,
    }
    with store.locked():
        store.change(change)
    if any(op.get("display_guard") and (op.get("before") or {}).get("value") != op["desired"]["value"] and op.get("executable") for op in operations):
        change["display_guard_required"] = True
        store.change(change)
    results = []
    failure = None
    for op in change["operations"]:
        if op["kind"] == "advisory" or not op.get("executable", True):
            op["status"] = "skipped"
            results.append({"id": op["id"], "title": op["title"], "status": "skipped",
                            "detail": op.get("reason")})
            store.change(change)
            continue
        try:
            if op.get("display_guard") and system.desktop_adapter(op).bus.get(DISPLAY, "HasChanged"):
                raise TuningError("执行前控制中心产生未提交的显示改动")
            current = system.capture_before(op)
        except (TuningError, OSError) as exc:
            current = None
            op["status"] = "conflict"
            op["detail"] = "无法重新读取原值：%s" % exc
        own_side_effect = (op["kind"] == "desktop" and current == op.get("after") and
                           op["target"]["setting"] in ("power.mode", "power.saving") and any(
                               item.get("changed") and item["kind"] == "desktop" and
                               item["target"]["setting"] in ("power.mode", "power.saving")
                               for item in change["operations"]))
        if op.get("status") == "conflict" or (current != op.get("before") and not own_side_effect):
            if current is not None:
                op["status"] = "conflict"
                op["detail"] = "执行前原值再次变化，保留现值"
            results.append({"id": op["id"], "title": op["title"],
                            "status": "conflict", "detail": op.get("detail")})
            store.change(change)
            failure = op
            break
        if op.get("restart_required"):
            unit = _restart_unit(op)
            if unit:
                try:
                    op["restart_marker"] = system.service_restart_marker(unit)
                except (TuningError, OSError):
                    op["restart_marker"] = None
        if op.get("relogin_required"):
            try:
                op["inherited_before"] = _current_inherited_values(op)
            except (TuningError, OSError):
                op["inherited_before"] = None
        if op.get("display_guard") and change.get("display_guard_required") and not change.get("display_guard"):
            change["display_guard"] = {"state": "armed", "deadline": time.time() + 30}
            store.change(change)
            try:
                start_display_guard(store, change)
            except OSError as exc:
                op.update(status="failed", detail="无法启动显示恢复进程：" + str(exc))
                failure = op
                store.change(change)
                break
        op["status"] = "applying"
        store.change(change)
        try:
            status, detail = _apply_operation(system, op, allow_service_restart)
            if own_side_effect and status == "unchanged":
                status, detail = "applied", "同次电源操作引发联动变化，纳入原值恢复"
        except (TuningError, OSError) as exc:
            status, detail = "failed", str(exc)
        if status.startswith("applied") and op.get("display_guard"):
            op["unconfirmed_status"] = status
            status = "applied_pending_confirmation"
        op["status"] = status
        op["detail"] = detail
        op["changed"] = status in ("applied", "applied_pending_restart",
                                   "applied_pending_reboot", "applied_pending_relogin",
                                   "applied_pending_runtime", "applied_pending_confirmation")
        results.append({"id": op["id"], "title": op["title"], "status": status, "detail": detail})
        store.change(change)
        if status == "failed":
            failure = op
            break
    if failure:
        if change.get("display_guard"):
            change["display_guard"]["state"] = "cancelled"
        restored = _restore_all(system, change, allow_service_restart, force=False)
        any_failed = any(item["status"] in ("failed", "conflict") for item in restored)
        change["state"] = "needs_attention" if any_failed else "failed"
        change["rollback"] = restored
        store.change(change)
        return {
            "ok": False,
            "dry_run": False,
            "change_id": change["id"],
            "state": change["state"],
            "results": results,
            "rollback": restored,
            "error": failure.get("detail") or "执行失败，已尝试恢复",
        }
    pending = [op["status"] for op in change["operations"]
               if op["status"].startswith("applied_pending")]
    skipped = [op["id"] for op in change["operations"]
               if op["status"] == "skipped" and op["kind"] != "advisory"]
    complete = not pending and not skipped
    change["state"] = "applied" if complete else "applied_pending"
    change["complete"] = complete
    change["pending"] = pending
    store.change(change)
    return {
        "ok": True,
        "dry_run": False,
        "change_id": change["id"],
        "state": change["state"],
        "complete": complete,
        "pending": pending,
        "skipped": skipped,
        "results": results,
        "requires_reboot": spec.get("requires_reboot", False),
        "requires_relogin": spec.get("requires_relogin", False),
        "requires_service_restart": spec.get("requires_service_restart", False),
        "display_guard": change.get("display_guard"),
        "confirm_command": [sys.executable, str(Path(__file__).with_name("tune.py")), "confirm-display", "--change-id", change["id"]] if change.get("display_guard", {}).get("state") == "armed" else None,
        "warnings": spec.get("warnings", []),
    }


def _apply_operation(system, op, allow_service_restart):
    kind = op["kind"]
    if kind == "desktop":
        adapter = system.desktop_adapter(op)
        if adapter.read(op["target"])["value"] == op["desired"]["value"]:
            return "unchanged", None
        adapter.write(op["target"], op["desired"]["value"], signature=op["before"].get("signature"))
        wait_desktop(adapter, op["target"], op["desired"]["value"])
        if not op.get("runtime_verifiable", True):
            return "applied_pending_runtime", "dconfig 已写入；当前接口只能验证配置，不能证明消费者已加载"
        if op.get("relogin_required"):
            return "applied_pending_relogin", "缩放已读回；已运行的客户端可能需重新登录"
        return "applied", None
    if kind == "gsettings":
        current = system.gsettings_get(op["target"]["schema"], op["target"]["key"])
        desired = op["desired"]["repr"]
        if current == desired:
            return "unchanged", None
        system.gsettings_set(op["target"]["schema"], op["target"]["key"], desired)
        if system.gsettings_get(op["target"]["schema"], op["target"]["key"]) != desired:
            return "failed", "gsettings 读回值与目标不一致"
        return "applied", None
    if kind in ("file", "modprobe"):
        before = op["before"]
        after = op["after"]
        current = system.read_target(op["target"]["path"], op["target"]["scope"])
        mode = after.get("mode") or int(op["desired"].get("mode", "0644"), 8)
        if current.get("sha256") == after.get("sha256") and current.get("mode") == mode:
            if kind == "modprobe" or op.get("reboot_required"):
                return "applied_pending_reboot", "配置文件已存在；驱动参数仍需重启才确认"
            if op.get("restart_required"):
                if not op["desired"].get("restart") or not allow_service_restart:
                    return "applied_pending_restart", "配置文件已存在；需 --allow-service-restart 才能重启服务"
                try:
                    if op["desired"].get("validate"):
                        system._ok(system.validate_config(op["desired"]["validate"]), timeout=30, priv=True)
                    system._ok(system.validate_control(op["desired"]["restart"]), timeout=30, priv=True)
                except TuningError as exc:
                    return "failed", "数据库配置校验或服务重启失败：%s" % exc
                op["restart_done"] = True
                if op.get("relogin_required"):
                    return "applied_pending_relogin", "配置已写入；重新登录后生效"
                return "applied", None
            if op.get("relogin_required"):
                return "applied_pending_relogin", "配置文件已存在；当前登录会话仍需重新登录"
            return "unchanged", None
        system.write_target(op["target"]["path"], op["target"]["scope"], after["content"],
                            "%04o" % mode)
        check = system.read_target(op["target"]["path"], op["target"]["scope"])
        if check.get("sha256") != after.get("sha256"):
            return "failed", "配置文件写后摘要不一致"
        if kind == "modprobe" or op.get("reboot_required"):
            return "applied_pending_reboot", "驱动参数在重启后生效"
        reload_result = None
        if op["desired"].get("reload"):
            try:
                reload_result = system._ok(system.validate_control(op["desired"]["reload"]),
                                           timeout=15, priv=True)
            except TuningError as exc:
                reload_result = "failed: %s" % exc
        if op.get("restart_required"):
            if op["desired"].get("restart") and allow_service_restart:
                try:
                    if op["desired"].get("validate"):
                        system._ok(system.validate_config(op["desired"]["validate"]), timeout=30, priv=True)
                    system._ok(system.validate_control(op["desired"]["restart"]), timeout=30, priv=True)
                except TuningError as exc:
                    return "failed", "数据库配置校验或服务重启失败：%s" % exc
                op["restart_done"] = True
            elif op["desired"].get("restart"):
                return "applied_pending_restart", "配置已写入；需 --allow-service-restart 才能重启服务"
            else:
                return "applied_pending_restart", "配置已写入；需要重启服务后才完全生效"
        if op.get("relogin_required"):
            return "applied_pending_relogin", "配置已写入；重新登录后生效"
        if isinstance(reload_result, str) and reload_result.startswith("failed"):
            return "applied_pending_restart", "配置已写入；服务重载失败，可稍后手动重载"
        return "applied", None
    if kind == "sysctl":
        after = op["after"]
        desired = after.get("runtime") or op["desired"]["entries"]
        current_file = system.read_target(op["target"]["path"], op["target"]["scope"])
        current = {key: system.read_sysctl(key) for key in desired}
        if current_file.get("sha256") == after["file"].get("sha256") and current == desired:
            return "unchanged", None
        system.write_target(op["target"]["path"], op["target"]["scope"], after["file"]["content"],
                            "%04o" % (after["file"].get("mode") or 0o644))
        try:
            system._ok(["sysctl", "-p", op["target"]["path"]], timeout=10, priv=True)
        except TuningError as exc:
            return "failed", "sysctl 应用失败：%s" % exc
        current = {key: system.read_sysctl(key) for key in desired}
        if current != desired:
            return "failed", "sysctl 运行值读回不一致：%s" % current
        return "applied", None
    if kind == "service":
        unit = op["target"]["unit"]
        desired = op["desired"]
        current = system.service_state(unit)
        if current.get("enabled") == ("enabled" if desired.get("enabled") else "disabled") and (
            desired.get("active") is None or current.get("active") == ("active" if desired.get("active") else "inactive")
        ):
            return "unchanged", None
        if desired.get("enabled") is True and current.get("enabled") != "enabled":
            system._ok(["systemctl", "enable", unit], timeout=10, priv=True)
        if desired.get("enabled") is False and current.get("enabled") == "enabled":
            system._ok(["systemctl", "disable", unit], timeout=10, priv=True)
        if desired.get("active") is True and current.get("active") != "active":
            system._ok(["systemctl", "start", unit], timeout=20, priv=True)
        if desired.get("active") is False and current.get("active") == "active":
            system._ok(["systemctl", "stop", unit], timeout=20, priv=True)
        check = system.service_state(unit)
        if desired.get("enabled") is not None and check.get("enabled") != ("enabled" if desired["enabled"] else "disabled"):
            return "failed", "服务启用状态读回不一致"
        if desired.get("active") is not None and check.get("active") != ("active" if desired["active"] else "inactive"):
            return "failed", "服务运行状态读回不一致"
        return "applied", None
    if kind == "power_profile":
        current = system.power_profile()
        desired = op["desired"]["profile"]
        if current == desired:
            return "unchanged", None
        system._ok(["powerprofilesctl", "set", desired], timeout=10)
        if system.power_profile() != desired:
            return "failed", "power-profiles-daemon 读回不一致"
        return "applied", None
    if kind == "tuned_profile":
        current = system.tuned_profile()
        desired = op["desired"]["profile"]
        if current == desired:
            return "unchanged", None
        system._ok(["tuned-adm", "profile", desired], timeout=20, priv=True)
        if system.tuned_profile() != desired:
            return "failed", "tuned 读回不一致"
        return "applied", None
    if kind == "advisory":
        return "skipped", op.get("reason")
    return "failed", "未知操作类型"


def _restore_all(system, change, allow_service_restart, force=False):
    results = []
    for op in reversed(change["operations"]):
        attempted = op.get("changed") or op.get("status") in ("applying", "failed")
        if not attempted:
            continue
        if op.get("rollback_status") in ("restored", "unchanged"):
            continue
        if op["kind"] == "advisory":
            continue
        try:
            status, detail = _restore_operation(system, op, allow_service_restart,
                                                force=force, change=change)
        except (TuningError, OSError) as exc:
            status, detail = "failed", str(exc)
        op["rollback_status"] = status
        results.append({"id": op["id"], "title": op["title"], "status": status, "detail": detail})
    return results


def _restart_unit(op):
    command = (op.get("desired") or {}).get("restart") or []
    return command[2] if len(command) > 2 else ""


def _service_restart_observed(system, op):
    if op.get("restart_done"):
        return True
    unit = _restart_unit(op)
    marker = op.get("restart_marker")
    if not unit or marker is None:
        return False
    current = system.service_restart_marker(unit)
    return current is not None and current != marker


def _env_assignments(content):
    values = {}
    for line in (content or "").splitlines():
        text = line.strip()
        if not text or text.startswith("#") or "=" not in text:
            continue
        key, value = text.split("=", 1)
        key = key.strip()
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            values[key] = value.strip().strip("'\"")
    return values


def _nofile_limits(content):
    limits = {}
    for line in (content or "").splitlines():
        parts = line.split()
        if len(parts) != 4 or parts[2] != "nofile" or parts[0].startswith("#"):
            continue
        try:
            limits[parts[1]] = int(parts[3])
        except ValueError:
            continue
    return limits


def _desired_inherited_values(op):
    path = (op.get("target") or {}).get("path") or ""
    block = "\n".join((op.get("desired") or {}).get("block") or [])
    if "/environment.d/" in path:
        return _env_assignments(block)
    if "/limits.d/" in path:
        return _nofile_limits(block)
    return None


def _current_inherited_values(op):
    desired = _desired_inherited_values(op)
    if desired is None:
        return None
    path = (op.get("target") or {}).get("path") or ""
    if "/environment.d/" in path:
        return {key: os.environ.get(key) for key in desired}
    import resource
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    return {"soft": soft, "hard": hard}


def _relogin_values_still_inherited(op):
    desired = _desired_inherited_values(op)
    if not desired:
        return False, None
    baseline = op.get("inherited_before")
    if isinstance(baseline, dict):
        changed = {key: value for key, value in desired.items() if baseline.get(key) != value}
    else:
        changed = dict(desired)
    if not changed:
        return False, None
    current = _current_inherited_values(op) or {}
    still = sorted(key for key, value in changed.items() if current.get(key) == value)
    if not still:
        return False, None
    path = (op.get("target") or {}).get("path") or ""
    if "/environment.d/" in path:
        return True, "环境变量 " + ", ".join(still)
    return True, "limits " + ", ".join("%s=%s" % (key, current[key]) for key in still)


def _relogin_restore_pending(op, change):
    inherited, detail = _relogin_values_still_inherited(op)
    if inherited:
        op["relogin_marker"] = identity()
        return True, detail
    current_session = identity()
    if op.get("relogin_resolved_session") == current_session:
        return False, None
    marker = op.get("relogin_marker")
    if marker:
        if current_session == marker:
            return True, "当前登录会话仍可能继承调优值"
        op["relogin_resolved_session"] = current_session
        op.pop("relogin_marker", None)
        return False, None
    applied_session = (change or {}).get("session")
    if applied_session and current_session != applied_session:
        op["relogin_marker"] = current_session
        return True, "当前登录会话可能已继承调优值"
    return False, None


def _restore_file_service(system, op, allow_service_restart, change=None):
    reload_error = None
    if op["desired"].get("reload"):
        try:
            system._ok(system.validate_control(op["desired"]["reload"]), timeout=15, priv=True)
        except TuningError as exc:
            reload_error = str(exc)
    if op.get("restart_required"):
        if not op["desired"].get("restart") or not allow_service_restart:
            detail = "配置已恢复；需 --allow-service-restart 才能重启服务"
            if reload_error:
                detail += "；服务重载失败：%s" % reload_error
            return "restored_pending_restart", detail
        try:
            if op["desired"].get("validate"):
                system._ok(system.validate_config(op["desired"]["validate"]), timeout=30, priv=True)
            system._ok(system.validate_control(op["desired"]["restart"]), timeout=30, priv=True)
        except TuningError as exc:
            return "failed", "数据库配置校验或服务重启失败：%s" % exc
        unit = _restart_unit(op)
        state = system.service_state(unit)
        if state.get("active") != "active":
            return "failed", "服务重启后未运行：%s" % unit
        op["restart_done"] = True
    elif reload_error:
        return "restored_pending_restart", "配置文件已恢复；服务重载失败：%s" % reload_error
    if op.get("relogin_required"):
        pending, detail = _relogin_restore_pending(op, change)
        if pending:
            return "restored_pending_relogin", (
                "配置文件已恢复；%s，需重新登录后恢复" % detail)
    return "restored", None


def _restore_operation(system, op, allow_service_restart, force=False, change=None):
    kind = op["kind"]
    if kind == "desktop":
        adapter = system.desktop_adapter(op)
        current = adapter.read(op["target"])
        before = op["before"]
        if current != before:
            if not force and current != op["after"]:
                return "conflict", "桌面设置或默认继承状态已被其他程序修改，保留现值"
            adapter.write(op["target"], before["value"], reset=before.get("default", False) or before.get("explicit") is False, signature=before.get("signature"), restoring=True)
            wait_desktop(adapter, op["target"], before["value"])
            if adapter.read(op["target"]) != before:
                return "failed", "桌面原值或默认继承状态恢复验证失败"
        if op.get("relogin_required") and (change or {}).get("session") == identity():
            return "restored_pending_relogin", "缩放配置已恢复，客户端可能需重新登录"
        if not op.get("runtime_verifiable", True):
            return "restored_pending_runtime", "dconfig 原值及默认继承状态已恢复；消费者运行态未确认"
        return "restored", None
    if kind == "gsettings":
        before = op["before"]["repr"]
        current = system.gsettings_get(op["target"]["schema"], op["target"]["key"])
        if current == before:
            return "unchanged", None
        if not force and current != op["desired"]["repr"]:
            return "conflict", "当前值已被其他程序修改，保留现值"
        system.gsettings_set(op["target"]["schema"], op["target"]["key"], before)
        return ("restored", None) if system.gsettings_get(op["target"]["schema"], op["target"]["key"]) == before else ("failed", "gsettings 恢复读回不一致")
    if kind in ("file", "modprobe"):
        before = op["before"]
        current = system.read_target(op["target"]["path"], op["target"]["scope"])
        if before.get("exists"):
            if current.get("sha256") == before.get("sha256") and (
                    current.get("mode") == before.get("mode") or before.get("mode") is None):
                if kind == "modprobe" or op.get("reboot_required"):
                    return _restore_reboot_state(system, op, change)
                return _restore_file_service(system, op, allow_service_restart, change=change)
        elif not current.get("exists"):
            if kind == "modprobe" or op.get("reboot_required"):
                return _restore_reboot_state(system, op, change)
            return _restore_file_service(system, op, allow_service_restart, change=change)
        if not force and current.get("sha256") != op["after"].get("sha256"):
            return "conflict", "文件在计划执行后被修改，保留现值"
        if before.get("exists"):
            system.write_target(op["target"]["path"], op["target"]["scope"], before["content"],
                                "%04o" % (before.get("mode") or 0o644))
        else:
            system.remove_target(op["target"]["path"], op["target"]["scope"])
        check = system.read_target(op["target"]["path"], op["target"]["scope"])
        if (before.get("exists") and check.get("sha256") != before.get("sha256")) or (
            not before.get("exists") and check.get("exists")
        ):
            return "failed", "文件恢复读回不一致"
        if kind == "modprobe" or op.get("reboot_required"):
            return _restore_reboot_state(system, op, change)
        return _restore_file_service(system, op, allow_service_restart, change=change)
    if kind == "sysctl":
        before = op["before"]
        desired_keys = list((op.get("after") or {}).get("runtime") or op["desired"]["entries"])
        before_runtime = before.get("runtime") or {}
        current = system.read_target(op["target"]["path"], op["target"]["scope"])
        current_runtime = {key: system.read_sysctl(key) for key in desired_keys}
        file_matches_before = current.get("sha256") == before["file"].get("sha256")
        if file_matches_before and all(
                before_runtime.get(key) in (None, current_runtime.get(key)) for key in desired_keys):
            return "unchanged", None
        if not force and not file_matches_before and current.get("sha256") != op["after"]["file"].get("sha256"):
            return "conflict", "sysctl 文件在计划执行后被修改，保留现值"
        if not force:
            after_runtime = (op.get("after") or {}).get("runtime") or {}
            for key in desired_keys:
                current_value = current_runtime.get(key)
                if after_runtime.get(key) is not None and current_value not in (
                        after_runtime.get(key), before_runtime.get(key)):
                    return "conflict", "sysctl 运行值 %s 已被其他程序修改，保留现值" % key
        warnings = []
        if before["file"].get("exists") and not file_matches_before:
            system.write_target(op["target"]["path"], op["target"]["scope"], before["file"]["content"],
                                "%04o" % (before["file"].get("mode") or 0o644))
            try:
                system._ok(["sysctl", "-p", op["target"]["path"]], timeout=10, priv=True)
            except TuningError as exc:
                warnings.append("原文件已恢复，但 sysctl -p 失败：%s" % exc)
        elif not before["file"].get("exists") and current.get("exists"):
            system.remove_target(op["target"]["path"], op["target"]["scope"])
        pairs = ["%s=%s" % (key, before_runtime[key]) for key in desired_keys
                 if before_runtime.get(key) is not None]
        if pairs:
            try:
                system._ok(["sysctl", "-w"] + pairs, timeout=10, priv=True)
            except TuningError as exc:
                warnings.append("运行值恢复失败：%s" % exc)
        runtime = {key: system.read_sysctl(key) for key in desired_keys}
        if any(before_runtime.get(key) not in (None, runtime.get(key)) for key in desired_keys):
            return "failed", "sysctl 运行值恢复读回不一致"
        return ("restored", "; ".join(warnings) if warnings else None)
    if kind == "service":
        before = op["before"]
        current = system.service_state(op["target"]["unit"])
        if all(current.get(key) == value for key, value in before.items() if value is not None):
            return "unchanged", None
        expected = {"enabled": "enabled" if op["desired"].get("enabled") else "disabled"}
        if op["desired"].get("active") is not None:
            expected["active"] = "active" if op["desired"]["active"] else "inactive"
        if not force and any(current.get(key) != value for key, value in expected.items()):
            return "conflict", "服务状态已被其他程序修改，保留现值"
        if before.get("active") == "inactive" and current.get("active") == "active":
            system._ok(["systemctl", "stop", op["target"]["unit"]], timeout=20, priv=True)
        if before.get("enabled") == "disabled":
            system._ok(["systemctl", "disable", op["target"]["unit"]], timeout=10, priv=True)
        elif before.get("enabled") == "enabled":
            system._ok(["systemctl", "enable", op["target"]["unit"]], timeout=10, priv=True)
        if before.get("active") == "active":
            system._ok(["systemctl", "start", op["target"]["unit"]], timeout=20, priv=True)
        check = system.service_state(op["target"]["unit"])
        if before.get("enabled") is not None and check.get("enabled") != before["enabled"]:
            return "failed", "服务启用状态恢复读回不一致"
        if before.get("active") is not None and check.get("active") != before["active"]:
            return "failed", "服务运行状态恢复读回不一致"
        return "restored", None
    if kind == "power_profile":
        before = op["before"]["profile"]
        current = system.power_profile()
        if current == before:
            return "unchanged", None
        if not force and current != op["desired"]["profile"]:
            return "conflict", "电源配置已被其他程序修改，保留现值"
        system._ok(["powerprofilesctl", "set", before], timeout=10)
        return ("restored", None) if system.power_profile() == before else ("failed", "电源配置恢复读回不一致")
    if kind == "tuned_profile":
        before = op["before"]["profile"]
        current = system.tuned_profile()
        if current == before:
            return "unchanged", None
        if not force and current != op["desired"]["profile"]:
            return "conflict", "tuned 配置已被其他程序修改，保留现值"
        system._ok(["tuned-adm", "profile", before], timeout=20, priv=True)
        return ("restored", None) if system.tuned_profile() == before else ("failed", "tuned 恢复读回不一致")
    return "skipped", "未知操作类型"


def _module_expectations(op):
    result = []
    for line in op.get("desired", {}).get("block", []):
        parts = line.split()
        if len(parts) < 3 or parts[0] != "options":
            continue
        module = parts[1]
        for item in parts[2:]:
            if "=" in item:
                key, value = item.split("=", 1)
                result.append((module, key, value))
    return result


_MODULE_TRUE = {"1", "y", "yes", "on", "true", "enabled"}
_MODULE_FALSE = {"0", "n", "no", "off", "false", "disabled"}


def _normalize_module_value(value):
    """Map sysfs boolean spellings (Y/N, 0/1) to one comparable value."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in _MODULE_TRUE:
        return True
    if text in _MODULE_FALSE:
        return False
    try:
        return int(text)
    except ValueError:
        return text


def _restore_reboot_state(system, op, change):
    boot_id = (change or {}).get("boot_id")
    if not boot_id or _current_boot_id() == boot_id:
        return "restored_pending_reboot", "驱动配置已恢复；尚未检测到系统重启"
    expected = (op.get("before") or {}).get("module_parameters") or {}
    if not expected:
        return "restored_pending_reboot", "驱动配置已恢复；重启后仍无法确认模块运行参数"
    missing = []
    mismatch = []
    for name, value in sorted(expected.items()):
        module, _, parameter = name.partition(".")
        actual = system.module_parameter(module, parameter)
        if value is None or actual is None:
            missing.append(name)
        elif _normalize_module_value(actual) != _normalize_module_value(value):
            mismatch.append("%s=%s（原值 %s）" % (name, actual, value))
    if mismatch:
        return "restored_pending_reboot", (
            "驱动配置已恢复，但重启后模块参数仍为调优值，需再次重启：%s" % ", ".join(mismatch))
    if missing:
        return "restored_pending_reboot", (
            "驱动配置已恢复；重启后无法读取模块参数：%s" % ", ".join(missing))
    return "restored", "驱动配置已恢复；已重启并确认模块参数回到原值"


def _current_boot_id():
    return read_text("/proc/sys/kernel/random/boot_id", "").strip() or None


@_locked
def verify_change(store, change_id, runner=None):
    change = store.load(change_id)
    system = System({
        "home": change.get("home") or str(Path.home()),
        "tools": change.get("tools") or {
            "gsettings": shutil.which("gsettings") is not None,
            "systemctl": shutil.which("systemctl") is not None,
            "powerprofilesctl": shutil.which("powerprofilesctl") is not None,
            "tuned-adm": shutil.which("tuned-adm") is not None,
        },
        "capabilities": change.get("capabilities") or {
            "privileged": os.geteuid() == 0 or _sudo_ok(),
        },
    }, runner=runner)
    results = []
    skipped = []
    for op in change["operations"]:
        if op["kind"] == "advisory":
            results.append({"id": op["id"], "title": op["title"], "status": "skipped",
                            "matches": None, "effective": "skipped",
                            "detail": op.get("reason")})
            continue
        if op.get("status") == "skipped":
            skipped.append(op["id"])
            results.append({"id": op["id"], "title": op["title"], "status": "skipped",
                            "matches": None, "effective": "skipped",
                            "detail": op.get("reason") or op.get("detail")})
            continue
        if not op.get("after"):
            results.append({"id": op["id"], "title": op["title"], "status": "not_applied",
                            "matches": False, "effective": "not_applied",
                            "detail": op.get("reason") or op.get("detail")})
            continue
        try:
            current = system.capture_before(op)
        except TuningError as exc:
            results.append({"id": op["id"], "title": op["title"], "status": "unreadable",
                            "matches": False, "effective": "unreadable", "detail": str(exc)})
            continue
        kind = op["kind"]
        config_matches = False
        runtime_matches = None
        effective = "mismatch"
        detail = None
        result = {"module_parameters": {}}
        if kind == "desktop":
            config_matches = current == op.get("after") or (op.get("status") == "unchanged" and current == op.get("before"))
            runtime_matches = config_matches if op.get("runtime_verifiable", True) else None
            effective = "active" if config_matches else "mismatch"
            if config_matches and not op.get("runtime_verifiable", True):
                effective = "configured_unverified"
                detail = "已验证 dconfig 值；未验证消费者运行态"
            elif config_matches and op.get("status") == "applied_pending_confirmation":
                effective = "pending_confirmation"
            elif config_matches and op.get("relogin_required") and change.get("session") == identity():
                effective = "pending_relogin"
        elif kind == "gsettings":
            config_matches = current.get("repr") == op["desired"]["repr"]
            runtime_matches = config_matches
            effective = "active" if config_matches else "mismatch"
        elif kind in ("file", "modprobe"):
            expected_mode = op["after"].get("mode")
            config_matches = (
                current.get("sha256") == op["after"].get("sha256")
                and (expected_mode is None or current.get("mode") == expected_mode)
            )
            status = op.get("status")
            if kind == "modprobe" or status == "applied_pending_reboot" or op.get("reboot_required"):
                rebooted = bool(change.get("boot_id") and _current_boot_id() != change.get("boot_id"))
                if not config_matches:
                    effective = "mismatch"
                elif not rebooted:
                    effective = "pending_reboot"
                    detail = "配置一致；尚未检测到系统重启"
                else:
                    missing = []
                    mismatch = []
                    for module, key, value in _module_expectations(op):
                        name = module + "." + key
                        actual = system.module_parameter(module, key)
                        result["module_parameters"][name] = actual
                        if actual is None:
                            missing.append(name)
                        elif _normalize_module_value(actual) != _normalize_module_value(value):
                            mismatch.append("%s=%s（目标 %s）" % (name, actual, value))
                    if mismatch:
                        effective = "mismatch"
                        runtime_matches = False
                        detail = "重启后模块参数不一致：" + ", ".join(mismatch)
                    elif missing:
                        effective = "pending_reboot"
                        detail = "已重启，但无法读取模块参数：" + ", ".join(missing)
                    else:
                        effective = "active"
                        runtime_matches = True
                        detail = "已重启并读回模块参数"
            elif op.get("restart_required"):
                unit = _restart_unit(op)
                running = True
                if unit:
                    running = system.service_state(unit).get("active") == "active"
                restarted = bool(op.get("restart_done")) or _service_restart_observed(system, op)
                if not config_matches:
                    effective = "mismatch"
                    runtime_matches = False
                elif unit and not running:
                    was_running = op.get("restart_marker") not in (None, "", "0")
                    if restarted or was_running:
                        effective = "mismatch"
                        runtime_matches = False
                        detail = "配置一致，但服务当前未运行：%s" % unit
                    else:
                        effective = "pending_restart"
                        detail = "配置一致；服务尚未启动"
                elif status == "applied_pending_restart" and not restarted:
                    effective = "pending_restart"
                    detail = "配置一致；尚未确认服务重启"
                else:
                    effective = "active"
                    runtime_matches = True
                    if unit:
                        detail = "服务已重启并运行"
            elif status == "applied_pending_restart":
                effective = "pending_restart" if config_matches else "mismatch"
            elif status == "applied_pending_relogin":
                relogged = bool(change.get("session") and identity() != change.get("session"))
                effective = ("active" if relogged else "pending_relogin") if config_matches else "mismatch"
                detail = "已检测到新登录会话" if relogged and config_matches else None
            else:
                effective = "active" if config_matches else "mismatch"
        elif kind == "sysctl":
            current_file = current.get("file") or {}
            expected_file = op["after"]["file"]
            config_matches = (
                current_file.get("sha256") == expected_file.get("sha256")
                and (expected_file.get("mode") is None or current_file.get("mode") == expected_file.get("mode"))
            )
            runtime_matches = current.get("runtime") == (op["after"].get("runtime") or op["desired"]["entries"])
            config_matches = bool(config_matches and runtime_matches)
            effective = "active" if config_matches else "mismatch"
        elif kind == "service":
            expected = {}
            if op["desired"].get("enabled") is not None:
                expected["enabled"] = "enabled" if op["desired"]["enabled"] else "disabled"
            if op["desired"].get("active") is not None:
                expected["active"] = "active" if op["desired"]["active"] else "inactive"
            config_matches = all(current.get(key) == value for key, value in expected.items())
            runtime_matches = config_matches
            effective = "active" if config_matches else "mismatch"
        elif kind in ("power_profile", "tuned_profile"):
            config_matches = current.get("profile") == op["desired"]["profile"]
            runtime_matches = config_matches
            effective = "active" if config_matches else "mismatch"
        if effective == "pending_reboot":
            detail = detail or "配置文件一致；重启后才会加载"
        elif effective == "pending_restart":
            detail = detail or "配置文件一致；服务重启后才会完全生效"
        elif effective == "pending_relogin":
            detail = detail or "配置文件一致；当前登录会话仍需重新登录"
        matches = config_matches and effective != "mismatch"
        results.append({
            "id": op["id"], "title": op["title"],
            "status": "verified" if matches else "mismatch",
            "matches": matches,
            "runtime_matches": runtime_matches,
            "effective": effective,
            "current": current,
            "expected": op.get("after"),
            "detail": detail,
            "module_parameters": result.get("module_parameters") or {},
        })
    ok = all(item["matches"] is not False and item.get("effective") != "mismatch"
             for item in results)
    complete = not skipped and all(item.get("effective") in ("active", "skipped")
                                   for item in results)
    return {"ok": ok, "complete": complete, "change_id": change["id"],
            "state": change.get("state"), "skipped": skipped, "results": results}


@_locked
def rollback_change(store, change_id, snapshot, execute=False, allow_service_restart=False, runner=None, force=False):
    change = store.load(change_id)
    rollback_snapshot = dict(snapshot)
    if change.get("home"):
        rollback_snapshot["home"] = change["home"]
    system = System(rollback_snapshot, runner=runner)
    if change.get("hardware") != snapshot.get("hardware_hash"):
        raise TuningError("硬件指纹已变化，无法安全恢复该变更")
    if change.get("state") not in ("applied", "applied_pending", "needs_attention", "failed", "applying", "rolled_back_pending"):
        raise TuningError("该变更当前状态不能恢复：%s" % change.get("state"))
    if not execute:
        preview = []
        for op in reversed(change["operations"]):
            if not op.get("changed") and op.get("status") not in ("applying", "failed", "conflict"):
                continue
            item = {"id": op["id"], "title": op["title"], "kind": op["kind"],
                    "status": op.get("status")}
            try:
                item["commands"] = system.preview_rollback_commands(op)
                item["preview"] = system.restore_preview(op)
            except (TuningError, OSError) as exc:
                item["preview_error"] = str(exc)
            preview.append(item)
        return {"ok": True, "dry_run": True, "change_id": change_id, "operations": preview}
    if change.get("display_guard", {}).get("state") == "armed":
        change["display_guard"]["state"] = "cancelled"
        store.change(change)
    results = _restore_all(system, change, allow_service_restart, force=force)
    failed = [item for item in results if item["status"] in ("failed", "conflict")]
    pending = [item for item in results if item["status"].startswith("restored_pending")]
    if failed:
        change["state"] = "needs_attention"
    elif pending:
        change["state"] = "rolled_back_pending"
    else:
        change["state"] = "rolled_back"
    change["rollback"] = results
    with store.locked():
        store.change(change)
    return {
        "ok": not failed,
        "complete": not failed and not pending,
        "dry_run": False,
        "change_id": change["id"],
        "state": change["state"],
        "results": results,
        "pending": pending,
    }


@_locked
def restore_all(store, snapshot, execute=False, allow_service_restart=False, runner=None, force=False):
    """Roll back every active change, newest first, to the pre-skill state."""
    active = [
        item for item in store.latest()
        if item.get("state") in ("applied", "applied_pending", "needs_attention", "failed", "applying", "rolled_back_pending")
    ]
    active.sort(key=lambda item: item.get("created_at") or 0, reverse=True)
    if not active:
        return {
            "ok": True,
            "dry_run": not execute,
            "state": "already_restored",
            "changes": [],
            "message": "没有待恢复的变更记录；当前没有本技能记录的写入可以回滚",
        }
    results = []
    for change in active:
        item = {
            "change_id": change.get("id"),
            "state": change.get("state"),
            "profiles": change.get("profiles"),
        }
        try:
            result = rollback_change(store, change["id"], snapshot, execute=execute,
                                     allow_service_restart=allow_service_restart,
                                     runner=runner, force=force)
            item.update({
                "ok": result.get("ok", False),
                "complete": result.get("complete", result.get("ok", False)),
                "state": result.get("state"),
                "results": result.get("results"),
                "operations": result.get("operations"),
            })
        except (TuningError, OSError, ValueError) as exc:
            item.update({"ok": False, "error": str(exc)})
        results.append(item)
    ok = all(item.get("ok") for item in results)
    complete = all(item.get("complete", item.get("ok")) for item in results)
    return {
        "ok": ok,
        "complete": complete,
        "dry_run": not execute,
        "state": "restored" if execute and ok and complete else (
            "rolled_back_pending" if execute and ok else ("needs_attention" if execute else "preview")),
        "changes": results,
    }


def _sudo_ok():
    if not shutil.which("sudo"):
        return False
    return run(["sudo", "-n", "true"], timeout=3).get("ok", False)


def wait_desktop(adapter, target, desired):
    deadline = time.monotonic() + 2
    while True:
        if adapter.read(target)["value"] == desired:
            return
        if time.monotonic() >= deadline:
            raise TuningError("桌面设置运行态读回不一致")
        time.sleep(0.1)


def start_display_guard(store, change):
    script = Path(__file__).with_name("tune_guard.py")
    read_fd, write_fd = os.pipe()
    try:
        process = subprocess.Popen([sys.executable, str(script), "--state-dir", str(store.root),
                                    "--change-id", change["id"], "--ready-fd", str(write_fd)],
                                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   start_new_session=True, close_fds=True, pass_fds=(write_fd,))
        os.close(write_fd)
        write_fd = None
        ready, _, _ = select.select([read_fd], [], [], 3)
        if not ready or os.read(read_fd, 1) != b"1":
            process.terminate()
            process.wait(timeout=3)
            raise OSError("显示恢复进程未能完成启动握手")
        return process
    finally:
        os.close(read_fd)
        if write_fd is not None:
            os.close(write_fd)


@_locked
def confirm_display(store, change_id, runner=None):
    change = store.load(change_id)
    guard = change.get("display_guard", {})
    if guard.get("state") != "armed" or time.time() >= guard.get("deadline", 0):
        raise TuningError("没有可确认的显示变更，或确认已超时")
    if change.get("session") != identity():
        raise TuningError("必须在原登录会话确认显示变更")
    system = System({"home": change.get("home"), "tools": change.get("tools"),
                     "capabilities": change.get("capabilities")}, runner=runner)
    for op in change["operations"]:
        if op.get("status") == "applied_pending_confirmation":
            if system.capture_before(op) != op["after"]:
                raise TuningError("显示状态已变化，保留自动回滚保护")
            op["status"] = op.pop("unconfirmed_status", "applied")
    guard["state"] = "confirmed"
    change["pending"] = [op["status"] for op in change["operations"] if op.get("status", "").startswith("applied_pending")]
    change["complete"] = not change["pending"] and not any(op["kind"] != "advisory" and op.get("status") == "skipped" for op in change["operations"])
    change["state"] = "applied" if change["complete"] else "applied_pending"
    store.change(change)
    return {"ok": True, "change_id": change_id, "state": change["state"],
            "complete": change["complete"], "pending": change["pending"]}
