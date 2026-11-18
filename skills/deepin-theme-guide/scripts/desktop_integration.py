"""Deepin native theme cards and journalled custom wallpaper registration."""
from __future__ import annotations

import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import zlib

from dde_backend import DDE, ThemeError, file_path, image_info


def cover_png(path, color):
    """Small valid preview without adding a Pillow dependency."""
    rgb = bytes.fromhex(color.lstrip("#"))
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    Path(path).write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 320, 180, 8, 2, 0, 0, 0))
                          + chunk(b"IDAT", zlib.compress((b"\0" + rgb * 320) * 180)) + chunk(b"IEND", b""))


def write_global_theme(folder, manifest, wallpaper_uri=None):
    """Only include requested components; never inherit unrelated user settings."""
    import shutil
    folder = Path(folder)
    folder.mkdir(parents=True)
    components = manifest["components"]
    palette = manifest.get("palette") or {}
    wallpaper = components.get("wallpaper")
    if wallpaper:
        source = file_path(wallpaper_uri) if wallpaper_uri else None
        if source and source.is_file():
            shutil.copyfile(source, folder / ("cover" + source.suffix))
            example = "cover" + source.suffix
        else:
            example = wallpaper_uri or "cover.png"
    else:
        example = "cover.png"
    if example == "cover.png" and not (folder / example).exists():
        cover_png(folder / example, palette.get("dark", "#20242B"))
    lines = ["[Deepin Theme]", "Name=" + manifest["name"], "Comment=" + manifest["description"],
             "Example=" + example, "DefaultTheme=DefaultTheme", "DarkTheme=DarkTheme", "Hidden=false"]
    for section, mode in [("DefaultTheme", "light"), ("DarkTheme", "dark")]:
        lines += ["", "[" + section + "]"]
        if components.get("icon"):
            lines.append("IconTheme=" + manifest["id"])
        if (components.get("cursor") or {}).get("compiled"):
            lines.append("CursorTheme=" + manifest["id"])
        if wallpaper_uri:
            lines.append("Wallpaper=" + wallpaper_uri)
        if palette:
            lines.append("ActiveColor=" + palette[mode])
    (folder / "index.theme").write_text("\n".join(lines) + "\n", encoding="utf-8")


class NativeWallpaper:
    """Use the same user-owned system service API as Control Center, including FD passing."""
    def __init__(self):
        self.executable = None

    def call(self, mode, **values):
        if self.executable is None:
            errors = []
            for executable in dict.fromkeys((sys.executable, "/usr/bin/python3")):
                try:
                    self._call(executable, {"mode": "probe"})
                    self.executable = executable
                    break
                except ThemeError as exc:
                    errors.append(str(exc))
            if self.executable is None:
                raise ThemeError("无法连接原生壁纸导入接口（需要系统 Python 的 Gio/PyGObject）：" + "; ".join(errors))
        return self._call(self.executable, {"mode": mode, **values})

    def _call(self, executable, request):
        try:
            proc = subprocess.run([executable, str(Path(__file__).resolve()), "--native-helper"],
                                  input=json.dumps(request), text=True, capture_output=True, timeout=20)
            value = json.loads(proc.stdout)
        except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
            raise ThemeError("原生壁纸辅助进程失败：%s" % exc) from exc
        if proc.returncode or not value.get("ok"):
            raise ThemeError(value.get("error", proc.stderr[:1000]))
        return value

    def plan(self, source):
        info = image_info(str(source))
        before = self.call("list")["files"]
        matches = []
        for filename in before:
            try:
                if image_info(filename)["sha256"] == info["sha256"]:
                    matches.append(filename)
            except (ThemeError, OSError):
                continue
        return {"source": info, "before": before, "path": matches[0] if matches else None,
                "created": False, "status": "existing" if matches else "pending"}

    def apply(self, plan, checkpoint):
        if plan["status"] == "existing":
            return
        if image_info(plan["source"]["path"])["sha256"] != plan["source"]["sha256"]:
            raise ThemeError("壁纸在导入前已变化")
        plan["status"] = "started"
        checkpoint()
        value = self.call("save", path=plan["source"]["path"])
        plan["path"] = str(file_path(value["path"]))
        plan["created"] = plan["path"] not in plan["before"]
        plan["sha256"] = image_info(plan["path"])["sha256"]
        plan["status"] = "imported"
        checkpoint()

    def remove(self, plan):
        # An interrupted save can be found by content; never delete prior entries.
        if plan.get("status") == "started" and not plan.get("path"):
            for filename in self.call("list")["files"]:
                if filename not in plan["before"] and image_info(filename)["sha256"] == plan["source"]["sha256"]:
                    plan.update(path=filename, created=True, sha256=plan["source"]["sha256"])
                    break
        if not plan.get("created") or plan.get("status") == "removed":
            return
        filename = plan["path"]
        if Path(filename).exists() and image_info(filename)["sha256"] != plan["sha256"]:
            raise ThemeError("原生壁纸内容已被修改，保留文件：" + filename)
        if not Path(filename).exists() and filename not in self.call("list")["files"]:
            plan["status"] = "removed"
            return
        self.call("delete", path=filename)
        if filename in self.call("list")["files"]:
            raise ThemeError("原生壁纸删除后仍在列表中：" + filename)
        plan["status"] = "removed"


def desktop_status(record):
    """Listing evidence, independent of which resources are currently selected."""
    backend = DDE().connect()
    catalogs = backend.catalog()
    if record.get("desktop_integration"):
        global_catalog = backend.catalog("globaltheme")
        catalogs["catalog"].update(global_catalog["catalog"])
        catalogs["errors"].extend(global_catalog["errors"])
    expected = {"globaltheme": record["id"]} if record.get("desktop_integration") else {}
    for kind, field in [("icon", "icon"), ("cursor", "cursor")]:
        component = record["manifest"]["components"].get(field)
        if component and (kind != "cursor" or component.get("compiled")):
            expected[kind] = record["id"]
    wallpaper = record.get("native_wallpaper")
    rows = [{"kind": kind, "id": identity, "listed": any(
        item["id"] == identity for item in catalogs["catalog"].get(kind, []))} for kind, identity in expected.items()]
    if wallpaper and wallpaper.get("path"):
        # Deepin 25's wallpaper page reads Daemon1 directly; Appearance1's
        # background list can remain cached after a native import notification.
        files = NativeWallpaper().call("list")["files"]
        uri = Path(wallpaper["path"]).as_uri()
        rows.append({"kind": "background", "id": uri, "listed": wallpaper["path"] in files,
                     "source": "Daemon1.GetCustomWallPapers",
                     "session_catalog_listed": any(item["id"] == uri for item in catalogs["catalog"].get("background", []))})
    return {"available": True, "ok": bool(rows) and all(row["listed"] for row in rows),
            "resources": rows, "errors": catalogs["errors"], "visual_verified": False}


def _native_helper(request):
    import pwd
    import xml.etree.ElementTree as ET
    import gi
    gi.require_version("Gio", "2.0")
    from gi.repository import Gio, GLib
    connection = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
    endpoint = None
    for service, path in [("org.deepin.dde.Daemon1", "/org/deepin/dde/Daemon1"),
                          ("com.deepin.daemon.Daemon", "/com/deepin/daemon/Daemon")]:
        try:
            result = connection.call_sync(service, path, "org.freedesktop.DBus.Introspectable", "Introspect",
                                          None, GLib.VariantType.new("(s)"), Gio.DBusCallFlags.NONE, 5000, None)
            node = ET.fromstring(result.unpack()[0]).find("interface[@name='%s']" % service)
            methods = {m.get("name"): "".join(a.get("type", "") for a in m.findall("arg") if a.get("direction", "in") == "in") for m in node.findall("method")}
            if methods.get("SaveCustomWallPaper") in ("shs", "ss") and methods.get("GetCustomWallPapers") == "s" and methods.get("DeleteCustomWallPaper") == "ss":
                endpoint = (service, path, methods)
                break
        except Exception:
            continue
    if endpoint is None:
        raise ThemeError("系统未暴露可导入、列举和删除的自定义壁纸接口")
    service, path, methods = endpoint
    username = pwd.getpwuid(os.getuid()).pw_name
    mode = request["mode"]
    def call(member, parameters, reply=None):
        return connection.call_sync(service, path, service, member, parameters,
                                    GLib.VariantType.new(reply) if reply else None, Gio.DBusCallFlags.NONE, 10000, None).unpack()
    if mode == "probe":
        return {"ok": True, "service": service}
    if mode == "list":
        return {"ok": True, "files": call("GetCustomWallPapers", GLib.Variant("(s)", (username,)), "(as)")[0]}
    if mode == "delete":
        call("DeleteCustomWallPaper", GLib.Variant("(ss)", (username, request["path"])))
        return {"ok": True}
    if mode != "save":
        raise ThemeError("未知原生壁纸操作")
    info = image_info(request["path"])
    if methods["SaveCustomWallPaper"] == "shs":
        descriptors = Gio.UnixFDList.new()
        with open(info["path"], "rb") as handle:
            index = descriptors.append(handle.fileno())
            result, _ = connection.call_with_unix_fd_list_sync(service, path, service, "SaveCustomWallPaper",
                GLib.Variant("(shs)", (username, index, "custom")), GLib.VariantType.new("(s)"),
                Gio.DBusCallFlags.NONE, 10000, descriptors, None)
            filename = result.unpack()[0]
    else:
        filename = call("SaveCustomWallPaper", GLib.Variant("(ss)", (username, info["path"])), "(s)")[0]
    if not filename:
        raise ThemeError("壁纸服务未返回导入路径")
    return {"ok": True, "path": filename}


if __name__ == "__main__":
    try:
        if sys.argv[1:] != ["--native-helper"]:
            raise ThemeError("请通过 theme_pack.py 调用")
        result = _native_helper(json.load(sys.stdin))
    except Exception as exc:
        result = {"ok": False, "error": str(exc)}
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["ok"] else 2)
