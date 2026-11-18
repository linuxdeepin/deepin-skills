#!/usr/bin/env python3
"""Read-only cursor evidence and journalable, allowlisted user setting writes."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile
import time

from dde_backend import DDE, ThemeError, scalar, text_variant
from cursor_assets import load_images, validate_xcursor

INI_KEYS = (("kcminputrc", "Mouse", "cursorTheme"),
            ("dde-appearance/deepin-themes/custom/index.theme", "DefaultTheme", "CursorTheme"),
            ("dde-appearance/deepin-themes/custom/index.theme", "DarkTheme", "CursorTheme"))
SCHEMAS = ("com.deepin.dde.appearance", "org.deepin.dde.appearance")


def command(argv, input_text=None):
    try:
        result = subprocess.run(argv, input=input_text, text=True, capture_output=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ThemeError("光标设置工具不可用或超时：%s" % exc) from exc
    if result.returncode:
        raise ThemeError((result.stderr or result.stdout).strip()[:1000])
    return result.stdout.strip()


def config_path(relative):
    if relative not in {item[0] for item in INI_KEYS}:
        raise ThemeError("未知光标配置路径")
    root = Path(os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config"))
    path = root / relative
    if not root.is_absolute() or any(item.is_symlink() for item in (path, *path.parents)):
        raise ThemeError("配置路径必须为绝对路径且不能含符号链接")
    return path


def ini_value(text, section, key):
    found, current = [], None
    for line in text.splitlines():
        match = re.fullmatch(r"\s*\[([^]]+)\]\s*", line)
        if match:
            current = match.group(1)
        elif current == section:
            match = re.match(r"\s*" + re.escape(key) + r"\s*=\s*(.*?)\s*$", line)
            if match:
                found.append(match.group(1))
    if len(found) > 1:
        raise ThemeError("配置包含重复光标键，停止自动改写")
    return found[0] if found else None


def replace_ini(text, section, key, value):
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        raise ThemeError("光标配置值无效")
    lines, current, replaced = [], None, False
    for line in text.splitlines(keepends=True):
        match = re.fullmatch(r"\s*\[([^]]+)\]\s*", line.strip())
        if match:
            current = match.group(1)
        if current == section:
            match = re.match(r"(\s*" + re.escape(key) + r"\s*=\s*)(.*?)(\r?\n)?$", line)
            if match:
                line = match.group(1) + value + (match.group(3) or "")
                replaced = True
        lines.append(line)
    if not replaced:
        raise ThemeError("原光标配置键已不存在，停止改写")
    return "".join(lines)


class CursorRuntime:
    def __init__(self, runner=command):
        self.runner = runner

    def discover(self):
        operations, errors = [], []
        if shutil.which("gsettings"):
            try:
                schemas = self.runner(["gsettings", "list-schemas"]).splitlines()
                for schema in SCHEMAS:
                    if schema in schemas and "cursor-theme" in self.runner(["gsettings", "list-keys", schema]).splitlines():
                        op = {"kind": "gsettings", "schema": schema, "key": "cursor-theme"}
                        op["before"] = self.read(op)
                        operations.append(op)
            except ThemeError as exc:
                errors.append(str(exc))
        for filename, section, key in INI_KEYS:
            try:
                path = config_path(filename)
                if not path.is_file():
                    continue
                op = {"kind": "ini", "file": filename, "section": section, "key": key}
                value = self.read(op)
                if value is not None:
                    op["before"] = value
                    operations.append(op)
            except (ThemeError, OSError) as exc:
                errors.append(str(exc))
        if os.environ.get("XDG_SESSION_TYPE") == "x11" and os.environ.get("DISPLAY") and shutil.which("xrdb"):
            try:
                op = {"kind": "xrdb", "key": "Xcursor.theme"}
                op["before"] = self.read(op)
                operations.append(op)
            except ThemeError as exc:
                errors.append(str(exc))
        return operations, errors

    def check_op(self, op):
        kind = op.get("kind")
        if kind == "ini" and (op.get("file"), op.get("section"), op.get("key")) in INI_KEYS:
            return
        if kind == "gsettings" and op.get("schema") in SCHEMAS and op.get("key") == "cursor-theme":
            return
        if kind == "xrdb" and op.get("key") == "Xcursor.theme" and os.environ.get("XDG_SESSION_TYPE") == "x11" and os.environ.get("DISPLAY"):
            return
        raise ThemeError("未知或当前会话不支持的光标配置操作")

    def read(self, op):
        self.check_op(op)
        if op["kind"] == "ini":
            path = config_path(op["file"])
            if not path.is_file() or path.stat().st_size > 1024 * 1024:
                raise ThemeError("光标配置文件不可读或过大")
            return ini_value(path.read_text(encoding="utf-8"), op["section"], op["key"])
        if op["kind"] == "gsettings":
            return scalar("(%s,)" % self.runner(["gsettings", "get", op["schema"], op["key"]]))
        text = self.runner(["xrdb", "-query"])
        values = re.findall(r"^Xcursor\.theme\s*:\s*(.*?)\s*$", text, re.M)
        if len(values) > 1:
            raise ThemeError("X 资源包含重复的 Xcursor.theme")
        return values[0] if values else None

    def write(self, op, value):
        self.check_op(op)
        if value is not None and (not isinstance(value, str) or not value or len(value) > 512 or any(ord(c) < 32 for c in value)):
            raise ThemeError("光标主题值无效")
        if op["kind"] == "gsettings":
            if value is None:
                raise ThemeError("GSettings 恢复值不能缺失")
            self.runner(["gsettings", "set", op["schema"], op["key"], text_variant(value)])
        elif op["kind"] == "ini":
            path = config_path(op["file"])
            original = path.read_text(encoding="utf-8")
            updated = replace_ini(original, op["section"], op["key"], value)
            fd, temp = tempfile.mkstemp(prefix=".cursor-", dir=str(path.parent))
            try:
                with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
                    handle.write(updated)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.chmod(temp, stat.S_IMODE(path.stat().st_mode))
                if path.read_text(encoding="utf-8") != original:
                    raise ThemeError("配置文件并发变化，保留现值")
                os.replace(temp, path)
            finally:
                if os.path.exists(temp):
                    os.unlink(temp)
        elif value is not None:
            self.runner(["xrdb", "-merge"], "Xcursor.theme:\t%s\n" % value)
        else:
            # Restore key absence while retaining all other current resources.
            original = self.runner(["xrdb", "-query"])
            updated = "\n".join(line for line in original.splitlines() if not re.match(r"^Xcursor\.theme\s*:", line)) + "\n"
            if self.runner(["xrdb", "-query"]) != original:
                raise ThemeError("X 资源并发变化，保留现值")
            self.runner(["xrdb", "-load"], updated)
        if self.read(op) != value:
            raise ThemeError("光标配置写入后读回不匹配")

    def plan(self, theme):
        operations, errors = self.discover()
        for op in operations:
            op.update({"after": theme, "status": "unchanged" if op["before"] == theme else "pending"})
        return {"operations": operations, "errors": errors, "execute_ready": not errors,
                "scope": "only_existing_DDE_keys_and_X11_Xcursor.theme"}

    def apply(self, plan, checkpoint):
        if plan.get("errors"):
            raise ThemeError("光标配置诊断失败，请先处理错误")
        for op in plan["operations"]:
            if op["status"] == "unchanged":
                continue
            current = self.read(op)
            if current == op["after"]:
                op["status"] = "applied"
                checkpoint()
                continue
            if current != op["before"]:
                raise ThemeError("光标配置在计划后改变")
            op["status"] = "started"
            checkpoint()
            self.write(op, op["after"])
            op["status"] = "applied"
            checkpoint()

    def rollback(self, plan, execute=False, checkpoint=lambda: None):
        results = []
        for op in reversed(plan["operations"]):
            if op["status"] not in ("started", "applied", "conflict", "restore_failed"):
                continue
            try:
                current = self.read(op)
                if current == op["before"]:
                    status = "restored"
                elif current != op["after"]:
                    status = "conflict"
                elif execute:
                    self.write(op, op["before"])
                    status = "restored"
                else:
                    status = "can_restore"
                item = {"kind": op["kind"], "key": op["key"], "status": status}
            except (ThemeError, OSError) as exc:
                item = {"kind": op["kind"], "key": op["key"], "status": "restore_failed", "error": str(exc)}
            results.append(item)
            if execute:
                op["status"] = item["status"]
                checkpoint()
        return results

    def inspect(self, expected, cursor_dir=None, observe_seconds=0, backend=None):
        if not 0 <= observe_seconds <= 30:
            raise ThemeError("观察时间必须在 0 到 30 秒之间")
        samples = []
        started = time.monotonic()
        while True:
            ops, errors = self.discover()
            layers = [{"kind": op["kind"], "location": op.get("file", op.get("schema", "X resource manager")), "section": op.get("section"), "value": op["before"], "matches": op["before"] == expected} for op in ops]
            legacy_layers = list(layers)
            # Native DDE switching updates XSettings and the WM, while obsolete
            # GSettings and xrdb values may remain. Check the actual live layers.
            if isinstance(backend, DDE) and os.environ.get("XDG_SESSION_TYPE") == "x11":
                layers = []
                errors = []
                for service, path, member, args in (
                    ("org.deepin.dde.XSettings1", "/org/deepin/dde/XSettings1", "org.deepin.dde.XSettings1.GetString", ["Gtk/CursorThemeName"]),
                    ("com.deepin.wm", "/com/deepin/wm", "org.freedesktop.DBus.Properties.Get", ["com.deepin.wm", "cursorTheme"]),
                ):
                    try:
                        value = scalar(command(["gdbus", "call", "--session", "--dest", service, "--object-path", path, "--method", member,
                                                *(text_variant(arg) for arg in args)]))
                        layers.append({"kind": "live", "location": service, "value": value, "matches": value == expected})
                    except ThemeError as exc:
                        errors.append(str(exc))
            if backend:
                try:
                    value = backend.read("cursor_theme")
                    layers.insert(0, {"kind": "dde", "value": value, "matches": value == expected})
                except ThemeError as exc:
                    errors.append(str(exc))
            samples.append({"elapsed_seconds": round(time.monotonic() - started, 2), "layers": layers,
                            "legacy_layers": legacy_layers, "errors": errors})
            remaining = observe_seconds - (time.monotonic() - started)
            if remaining <= 0:
                break
            time.sleep(min(2, remaining))
        lookup = []
        if cursor_dir:
            for path in sorted((Path(cursor_dir) / "cursors").iterdir()):
                if not path.is_file() or path.is_symlink():
                    continue
                for size in sorted({frame["size"] for frame in validate_xcursor(path)}):
                    direct = load_images(path=path, size=size)
                    themed = load_images(theme=expected, name=path.name, size=size)
                    matches = bool(direct.get("loaded") and themed.get("loaded") and direct["frames"] == themed["frames"])
                    lookup.append({"name": path.name, "size": size, "matches": matches, "loader_available": direct["available"]})
        consistent = all(sample["layers"] and not sample["errors"] and all(layer["matches"] for layer in sample["layers"]) for sample in samples)
        return {"expected": expected, "configuration_consistent": consistent, "samples": samples,
                "named_lookup_matches": all(item["matches"] for item in lookup) if lookup else None,
                "named_lookup": lookup, "visual_confirmation": "not_observed",
                "hot_reload": "native_DDE_XSettings_and_WM_checked" if isinstance(backend, DDE) and os.environ.get("XDG_SESSION_TYPE") == "x11" else "not_observed",
                "note": "X11 检查 DDE、实时 XSettings 与窗口管理器；legacy_layers 单列旧配置。按名加载仍不能代替当前指针的视觉观察。"}


def main():
    parser = argparse.ArgumentParser(description="只读光标配置与按名加载诊断")
    parser.add_argument("--theme", required=True)
    parser.add_argument("--cursor-dir")
    parser.add_argument("--observe-seconds", type=float, default=0)
    args = parser.parse_args()
    try:
        backend, dde_error = None, None
        try:
            backend = DDE().connect()
        except ThemeError as exc:
            dde_error = str(exc)
        result = CursorRuntime().inspect(args.theme, args.cursor_dir, args.observe_seconds, backend)
        result["dde_error"] = dde_error
        result["ok"] = not dde_error and result["configuration_consistent"] and result["named_lookup_matches"] is not False
    except (ThemeError, OSError, ValueError) as exc:
        result = {"ok": False, "error": str(exc)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
