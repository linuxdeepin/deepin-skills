"""User-level Deepin screensaver adapter using the installed DConfig CLI."""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

from dde_backend import ThemeError


APP = "org.deepin.screensaver"
CURRENT = "org.deepin.screensaver"
CUSTOM = "org.deepin.customscreensaver"


def _run(argv):
    try:
        result = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                                timeout=5, env={**os.environ, "LC_ALL": "C.UTF-8"})
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ThemeError("DConfig 命令不可用或超时：%s" % exc) from exc
    if result.returncode:
        raise ThemeError((result.stderr or result.stdout).strip()[:1600])
    return result.stdout.strip()


class ScreenSaver:
    def __init__(self, runner=_run):
        self.runner = runner

    def connect(self):
        if not shutil.which("dde-dconfig"):
            raise ThemeError("当前系统没有 dde-dconfig，无法安全配置屏保")
        return self

    def component_available(self):
        return bool(shutil.which("deepin-screensaver")) and any(
            (Path(base) / "deepin-screensaver/modules/deepin-custom-screensaver").is_file()
            for base in ("/usr/lib", "/usr/lib64", "/usr/lib/x86_64-linux-gnu", "/usr/lib/aarch64-linux-gnu"))

    def get(self, resource, key):
        raw = self.runner(["dde-dconfig", "get", "-a", APP, "-r", resource, "-k", key])
        # Values are JSON strings/numbers/bools in the DConfig CLI. Avoid eval.
        import json
        try:
            value = json.loads(raw)
            # Deepin 25's CLI serializes numeric DConfig values as JSON strings.
            if key in ("intervalTime", "playMode") and isinstance(value, str) and re.fullmatch(r"-?[0-9]+", value):
                return int(value)
            return value
        except (TypeError, ValueError) as exc:
            raise ThemeError("无法解析屏保配置 %s/%s：%s" % (resource, key, raw[:120])) from exc

    def set(self, resource, key, value):
        # dde-dconfig takes a native command-line value; quoting a string as
        # JSON would make the quote characters part of the stored path.
        if isinstance(value, bool):
            encoded = "true" if value else "false"
        else:
            encoded = str(value)
        self.runner(["dde-dconfig", "set", "-a", APP, "-r", resource, "-k", key, "-v", encoded])

    def inspect(self):
        self.connect()
        values = {}
        errors = []
        for resource, key in ((CURRENT, "currentScreenSaver"), (CUSTOM, "slideshowPath"),
                              (CUSTOM, "intervalTime"), (CUSTOM, "playMode")):
            try:
                values[key] = self.get(resource, key)
            except ThemeError as exc:
                values[key] = None
                errors.append({"resource": resource, "key": key, "error": str(exc)})
        return {"available": not errors, "values": values, "errors": errors,
                "custom_component": self.component_available()}

    def plan(self, path, interval=30, play_mode=0, activate=True):
        self.connect()
        folder = Path(path).expanduser()
        if folder.is_symlink() or not folder.is_dir():
            raise ThemeError("屏保图片目录必须是当前用户可读的普通目录")
        folder = folder.resolve()
        files = [item for item in folder.iterdir() if not item.is_symlink() and item.is_file() and item.suffix.lower() in
                 {".png", ".jpg", ".jpeg", ".bmp"}]
        if not files:
            raise ThemeError("屏保图片目录为空，或没有 PNG/JPEG/BMP 图片")
        if type(interval) is not int or not 3 <= interval <= 3600:
            raise ThemeError("屏保轮播间隔必须在 3 到 3600 秒之间")
        if type(play_mode) is not int or play_mode not in (0, 1):
            raise ThemeError("屏保播放模式必须为 0 或 1")
        inspected = self.inspect()
        if not inspected["available"] or not inspected["custom_component"]:
            raise ThemeError("缺少可用的 Deepin 自定义屏保组件或无法读取原配置：%s" % inspected["errors"])
        current = inspected["values"]
        if any(type(current[key]) is not typ for key, typ in (("currentScreenSaver", str), ("slideshowPath", str), ("intervalTime", int), ("playMode", int))):
            raise ThemeError("屏保原配置类型无效，无法建立恢复点")
        return {"resource": {"currentScreenSaver": current.get("currentScreenSaver"),
                              "slideshowPath": current.get("slideshowPath"),
                              "intervalTime": current.get("intervalTime"),
                              "playMode": current.get("playMode")},
                "target": {"currentScreenSaver": "deepin-custom-screensaver" if activate else current.get("currentScreenSaver"),
                           "slideshowPath": str(folder), "intervalTime": int(interval), "playMode": int(play_mode)},
                "files": [str(item) for item in sorted(files)],
                "note": "Deepin 自定义屏保读取图片目录；当前技能不生成可执行屏保程序。"}

    def apply(self, plan, checkpoint=None):
        self.connect()
        before, target = plan["resource"], plan["target"]
        if not Path(target["slideshowPath"]).is_dir():
            raise ThemeError("屏保目录在计划后不存在")
        for key, old in before.items():
            if self.get(CURRENT if key == "currentScreenSaver" else CUSTOM, key) != old:
                raise ThemeError("屏保原配置已变化，请重新预览")
        changed = []
        plan["started"] = []
        try:
            for key in ("slideshowPath", "intervalTime", "playMode", "currentScreenSaver"):
                if target[key] is None or target[key] == before.get(key):
                    continue
                plan["started"].append(key)
                if checkpoint:
                    checkpoint()
                self.set(CUSTOM if key != "currentScreenSaver" else CURRENT, key, target[key])
                if self.get(CUSTOM if key != "currentScreenSaver" else CURRENT, key) != target[key]:
                    raise ThemeError("屏保配置 %s 读回值不匹配" % key)
                changed.append(key)
        except ThemeError:
            self.rollback({"resource": before, "target": target})
            raise
        return {"before": before, "target": target, "changed": changed}

    def rollback(self, plan, execute=True):
        self.connect()
        before, target = plan["resource"], plan["target"]
        results = []
        keys = plan.get("started", [key for key in ("slideshowPath", "intervalTime", "playMode", "currentScreenSaver") if before.get(key) != target.get(key)])
        for key in reversed(keys):
            old, expected = before.get(key), target.get(key)
            if old is None or expected is None:
                continue
            resource = CUSTOM if key != "currentScreenSaver" else CURRENT
            try:
                current = self.get(resource, key)
                if current == old:
                    results.append({"key": key, "status": "already_restored"})
                elif current != expected:
                    results.append({"key": key, "status": "conflict", "current": current})
                elif not execute:
                    results.append({"key": key, "status": "can_restore", "current": current, "to": old})
                else:
                    self.set(resource, key, old)
                    if self.get(resource, key) != old:
                        raise ThemeError("读回值不匹配")
                    results.append({"key": key, "status": "restored"})
            except ThemeError as exc:
                results.append({"key": key, "status": "failed", "error": str(exc)})
        return results
