"""Small, allowlisted DDE appearance adapter; Python standard library only."""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse


class ThemeError(Exception):
    pass


ENDPOINTS = (
    ("org.deepin.dde.Appearance1", "/org/deepin/dde/Appearance1"),
    ("com.deepin.daemon.Appearance", "/com/deepin/daemon/Appearance"),
)
FIELDS = {"icon_theme": "IconTheme", "cursor_theme": "CursorTheme",
          "cursor_size": "CursorSize", "accent_color": "QtActiveColor"}


def run(argv):
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", timeout=4,
                              env={**os.environ, "LC_ALL": "C.UTF-8"})
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ThemeError("命令不可用或超时：%s" % exc) from exc
    if proc.returncode:
        raise ThemeError((proc.stderr or proc.stdout).strip()[:1600])
    return proc.stdout.strip()


def scalar(output):
    """Decode only gdbus' scalar reply grammar. Never evaluate executable input."""
    value = output.strip()
    if value == "()":
        return None
    if not value.startswith("(") or not value.endswith(")"):
        raise ThemeError("无法解析 D-Bus 返回值：%s" % value[:160])
    value = value[1:-1].strip()
    if value.endswith(","):
        value = value[:-1].strip()
    if value.startswith("<") and value.endswith(">"):
        value = value[1:-1].strip()
    value = re.sub(r"^(?:u?int(?:16|32|64)|byte|double)\s+", "", value)
    if value in ("true", "false"):
        return value == "true"
    try:
        result = ast.literal_eval(value)
    except (ValueError, SyntaxError) as exc:
        raise ThemeError("不支持的 D-Bus 标量返回值：%s" % value[:160]) from exc
    if type(result) not in (str, int, float, bool):
        raise ThemeError("期望单个标量返回值")
    return result


def text_variant(value):
    # gdbus parses GVariant strings, not shell strings. JSON string escaping is
    # valid for the string values sent here; subprocess never invokes a shell.
    return json.dumps(value, ensure_ascii=False)


def file_path(value):
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ThemeError("壁纸必须是本地文件路径或 file:// URI")
    parsed = urlparse(value)
    if parsed.scheme:
        if parsed.scheme != "file" or parsed.netloc not in ("", "localhost"):
            raise ThemeError("只接受本地壁纸；请先把图片保存到本机")
        return Path(unquote(parsed.path)).resolve()
    return Path(value).expanduser().resolve()


def image_dimensions(path):
    """Read (width, height) from PNG/JPEG/WebP/BMP headers; None when unknown.

    Headers are parsed directly so the skill keeps its standard-library-only
    dependency policy. Unparseable but recognizable files stay valid assets.
    """
    try:
        with Path(path).open("rb") as fh:
            data = fh.read(512 * 1024)
    except OSError:
        return None, None
    try:
        if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24 and data[12:16] == b"IHDR":
            width, height = struct.unpack(">II", data[16:24])
            return width or None, height or None
        if data.startswith(b"\xff\xd8"):
            index = 2
            while index + 9 <= len(data):
                if data[index] != 0xFF:
                    index += 1
                    continue
                marker = data[index + 1]
                if marker in (0xD8, 0x01, 0xFF) or 0xD0 <= marker <= 0xD7:
                    index += 2
                    continue
                if marker == 0xDA:
                    break
                length = int.from_bytes(data[index + 2:index + 4], "big")
                if length < 2:
                    break
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    height = int.from_bytes(data[index + 5:index + 7], "big")
                    width = int.from_bytes(data[index + 7:index + 9], "big")
                    return width or None, height or None
                index += 2 + length
        if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
            chunk = data[12:16]
            if chunk == b"VP8X" and len(data) >= 30:
                return (1 + int.from_bytes(data[24:27], "little"),
                        1 + int.from_bytes(data[27:30], "little"))
            if chunk == b"VP8 " and data[23:26] == b"\x9d\x01\x2a" and len(data) >= 30:
                return (int.from_bytes(data[26:28], "little") & 0x3FFF,
                        int.from_bytes(data[28:30], "little") & 0x3FFF)
            if chunk == b"VP8L" and data[20:21] == b"\x2f" and len(data) >= 25:
                bits = int.from_bytes(data[21:25], "little")
                return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
        if data.startswith(b"BM") and len(data) >= 26:
            width = int.from_bytes(data[18:22], "little", signed=True)
            height = int.from_bytes(data[22:26], "little", signed=True)
            return abs(width) or None, abs(height) or None
    except (struct.error, IndexError):
        pass
    return None, None


def image_info(value):
    path = file_path(value)
    if not path.is_file() or path.stat().st_size > 128 * 1024 * 1024:
        raise ThemeError("壁纸不存在、不是普通文件或大于 128 MiB")
    try:
        with path.open("rb") as fh:
            header = fh.read(32)
            if not (header.startswith(b"\x89PNG\r\n\x1a\n") or
                    header.startswith(b"\xff\xd8\xff") or
                    (header.startswith(b"RIFF") and header[8:12] == b"WEBP") or
                    header.startswith(b"BM")):
                raise ThemeError("只接受可识别文件头的 PNG、JPEG、WebP 或 BMP 壁纸")
            fh.seek(0)
            digest = hashlib.sha256()
            for block in iter(lambda: fh.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as exc:
        raise ThemeError("无法读取壁纸：%s" % exc) from exc
    width, height = image_dimensions(path)
    return {"path": str(path), "sha256": digest.hexdigest(), "bytes": path.stat().st_size,
            "width": width, "height": height}


def equivalent(kind, left, right):
    if left == right:
        return True
    if kind == "wallpaper" and isinstance(left, str) and isinstance(right, str):
        try:
            if file_path(left) == file_path(right):
                return True
            return image_info(left)["sha256"] == image_info(right)["sha256"]
        except (ThemeError, OSError):
            return False
    if kind == "accent_color" and isinstance(left, str) and isinstance(right, str):
        return left.lower() == right.lower()
    return False


class DDE:
    def __init__(self, runner=run):
        self.runner = runner
        self.service = self.path = self.interface = None
        self.methods = {}
        self.properties = {}
        self.errors = []

    def connect(self):
        if self.service:
            return self
        for service, path in ENDPOINTS:
            try:
                xml = self.runner(["gdbus", "introspect", "--session", "--dest", service,
                                   "--object-path", path, "--xml"])
                root = ET.fromstring(xml)
                interface = root if root.tag == "interface" else root.find("interface[@name='%s']" % service)
                if interface is None or interface.get("name") != service:
                    raise ThemeError("目标对象未暴露预期的外观接口")
                self.service, self.path, self.interface = service, path, service
                self.methods = {
                    node.get("name"): (
                        "".join(a.get("type", "") for a in node.findall("arg") if a.get("direction", "in") == "in"),
                        "".join(a.get("type", "") for a in node.findall("arg") if a.get("direction") == "out"),
                    ) for node in interface.findall("method")
                }
                self.properties = {p.get("name"): {"type": p.get("type"), "access": p.get("access", "read")}
                                   for p in interface.findall("property")}
                return self
            except (ThemeError, ET.ParseError) as exc:
                self.errors.append({"service": service, "error": str(exc)})
        raise ThemeError("无法连接当前用户的 DDE 外观服务；检查图形登录会话、gdbus 和 D-Bus。详情：" + json.dumps(self.errors, ensure_ascii=False))

    def method(self, name, incoming, outgoing=""):
        return self.methods.get(name) == (incoming, outgoing)

    def prop(self, name, signature, writable=False):
        p = self.properties.get(name, {})
        return (p.get("type") == signature and p.get("access") in ("read", "readwrite")
                and (not writable or p.get("access") == "readwrite"))

    def call(self, member, *args):
        return scalar(self.runner(["gdbus", "call", "--session", "--dest", self.service,
                                   "--object-path", self.path, "--method", member, *args]))

    def get(self, name):
        return self.call("org.freedesktop.DBus.Properties.Get", text_variant(self.interface), text_variant(name))

    def capabilities(self, monitor=None):
        pair = self.method("GetActiveColors", "", "s") and self.method("SetActiveColors", "s")
        wp = (self.method("GetCurrentWorkspaceBackgroundForMonitor", "s", "s") and
              self.method("SetCurrentWorkspaceBackgroundForMonitor", "ss")) if monitor else (
              self.method("GetCurrentWorkspaceBackground", "", "s") and
              self.method("SetCurrentWorkspaceBackground", "s"))
        return {"wallpaper": bool(wp),
                "icon_theme": self.method("Set", "ss") and self.method("List", "s", "s") and self.prop("IconTheme", "s"),
                "cursor_theme": self.method("Set", "ss") and self.method("List", "s", "s") and self.prop("CursorTheme", "s"),
                "cursor_size": self.prop("CursorSize", "i", True),
                "accent_color": bool(pair or (not self.service.endswith("Appearance1") and self.prop("QtActiveColor", "s", True))),
                "accent_pair": bool(pair)}

    def read(self, kind, target=None):
        if kind == "wallpaper":
            if target:
                return self.call(self.interface + ".GetCurrentWorkspaceBackgroundForMonitor", text_variant(target))
            return self.call(self.interface + ".GetCurrentWorkspaceBackground")
        if kind == "accent_color" and target == "pair":
            return self.call(self.interface + ".GetActiveColors")
        if kind in FIELDS:
            return self.get(FIELDS[kind])
        raise ThemeError("未知设置类型：%s" % kind)

    def write(self, kind, target, value):
        if kind == "wallpaper":
            if target:
                return self.call(self.interface + ".SetCurrentWorkspaceBackgroundForMonitor", text_variant(value), text_variant(target))
            return self.call(self.interface + ".SetCurrentWorkspaceBackground", text_variant(value))
        if kind in ("icon_theme", "cursor_theme"):
            return self.call(self.interface + ".Set", text_variant("icon" if kind == "icon_theme" else "cursor"), text_variant(value))
        if kind == "accent_color" and target == "pair":
            return self.call(self.interface + ".SetActiveColors", text_variant(value))
        if kind in ("cursor_size", "accent_color"):
            variant = "<%s>" % ("int32 %d" % value if kind == "cursor_size" else text_variant(value))
            return self.call("org.freedesktop.DBus.Properties.Set", text_variant(self.interface), text_variant(FIELDS[kind]), variant)
        raise ThemeError("不允许写入此设置")

    def wait_for(self, kind, target, value):
        deadline = time.monotonic() + 3
        while True:
            current = self.read(kind, target)
            if equivalent(kind, current, value):
                return current
            if time.monotonic() >= deadline:
                raise ThemeError("接口已返回，但读回值不匹配；当前值：%s" % current)
            time.sleep(0.2)

    def endpoint(self):
        return {"service": self.service, "path": self.path, "interface": self.interface}

    def inspect(self, monitor=None):
        caps = self.capabilities(monitor)
        settings, failures = {}, []
        for kind in FIELDS.keys() | {"wallpaper"}:
            if not caps.get(kind):
                settings[kind] = None
                continue
            target = monitor if kind == "wallpaper" else "pair" if kind == "accent_color" and caps["accent_pair"] else None
            try:
                settings[kind] = self.read(kind, target)
            except ThemeError as exc:
                settings[kind] = None
                failures.append({"field": kind, "error": str(exc)})
        for name in ("GlobalTheme", "GtkTheme", "WallpaperURIs", "WallpaperURls"):
            if self.prop(name, "s"):
                try:
                    settings[name] = self.get(name)
                except ThemeError:
                    pass
        return {"backend": self.endpoint(), "capabilities": caps, "settings": settings,
                "monitor": monitor or "primary", "wallpaper_scope": "current_workspace",
                "read_errors": failures}

    def catalog(self, kind="all"):
        groups = ("icon", "cursor", "background") if kind == "all" else (kind,)
        result, errors = {}, []
        for group in groups:
            try:
                if not self.method("List", "s", "s"):
                    raise ThemeError("当前接口不支持主题枚举")
                raw = self.call(self.interface + ".List", text_variant(group))
                entries = json.loads(raw)
                if not isinstance(entries, list):
                    raise ThemeError("List 未返回 JSON 数组")
                normalized = []
                for entry in entries:
                    if isinstance(entry, str):
                        normalized.append({"id": entry})
                    elif isinstance(entry, dict):
                        lower = {k.lower(): v for k, v in entry.items()}
                        identity = lower.get("id")
                        if isinstance(identity, str) and identity:
                            normalized.append({"id": identity, "name": lower.get("name", identity),
                                               "path": lower.get("path"), "preview": lower.get("thumbnail")})
                result[group] = normalized
            except (ThemeError, ValueError, TypeError) as exc:
                result[group] = []
                errors.append({"kind": group, "error": str(exc)})
        return {"catalog": result, "errors": errors}


def environment():
    release = {}
    try:
        for line in Path("/etc/os-release").read_text().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                if k in ("ID", "VERSION_ID", "PRETTY_NAME"):
                    release[k] = v.strip('"')
    except OSError:
        pass
    return {"os": release, "desktop": os.environ.get("XDG_CURRENT_DESKTOP"),
            "session_type": os.environ.get("XDG_SESSION_TYPE"), "uid": os.getuid(),
            "gdbus": shutil.which("gdbus"),
            "session_bus_present": bool(os.environ.get("DBUS_SESSION_BUS_ADDRESS")),
            "display_present": bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))}
