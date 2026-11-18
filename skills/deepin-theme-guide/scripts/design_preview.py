"""Build an offline contact sheet from actual package assets at their display sizes."""
from __future__ import annotations

import copy
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

from dde_backend import ThemeError
from cursor_design import hotspot
from vector_assets import validate_svg

PREFERRED = ("dde-file-manager", "deepin-browser", "deepin-terminal", "deepin-calculator", "dde-calendar", "deepin-music", "deepin-app-store", "dde-control-center", "chatgpt", "go-up", "go-down", "battery-low", "battery-full", "audio-volume-muted")


def sheet(package, manifest, output, names=None, force=False):
    root = Path(package).resolve()
    target = Path(output).expanduser().absolute()
    if root == target or root in target.resolve().parents:
        raise ThemeError("预览输出必须在包目录之外，以免改变摘要")
    if target.suffix.lower() not in (".svg", ".png") or target.is_symlink() or (target.exists() and not force):
        raise ThemeError("预览输出须为 .svg 或 .png 普通文件；覆盖时显式加 --force")
    icon = manifest["components"].get("icon") or {}
    cursor = manifest["components"].get("cursor") or {}
    byname = {a["name"]: a for a in icon.get("assets", [])}
    selected = list(dict.fromkeys(names or [name for name in PREFERRED if name in byname] or list(byname)[:12]))
    if any(name not in byname for name in selected) or len(selected) > 32:
        raise ThemeError("预览只接受包内的 1–32 个图标名称")
    states = cursor.get("generated", {}).get("states", [])
    rows = (len(selected) + 5)//6
    cursor_rows = (len(states) + 5)//6
    panel_height = 70 + rows*124 + (48 + cursor_rows*112 if states else 0)
    height = 92 + panel_height*2 + 48
    fragments = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="{height}" viewBox="0 0 1440 {height}">',
                 '<rect width="1440" height="100%" fill="#111823"/>',
                 f'<text x="28" y="36" fill="#F0F5FC" font-family="sans-serif" font-size="24">{escape(manifest["name"])} · actual-size design review</text>',
                 '<text x="28" y="66" fill="#B2C0D4" font-family="sans-serif" font-size="15">Icons: 16 / 24 / 48 px · Cursors: 24 / 32 / 48 px · red dot: hotspot · static SVG sources</text>']
    serial = 0

    def embed(source, x, y, size):
        nonlocal serial
        serial += 1
        svg = copy.deepcopy(validate_svg(source))
        ids = {node.get("id"): "asset%d_%s" % (serial, node.get("id")) for node in svg.iter() if node.get("id")}
        for node in svg.iter():
            for key, value in list(node.attrib.items()):
                if key == "id":
                    node.set(key, ids[value])
                else:
                    value = re.sub(r"url\(#([^)]*)\)", lambda m: "url(#"+ids.get(m[1], m[1])+")", value)
                    if key.split("}")[-1] == "href" and value.startswith("#"):
                        value = "#" + ids.get(value[1:], value[1:])
                    node.set(key, value)
        if not svg.get("viewBox"):
            width = re.sub(r"px$", "", svg.get("width", "64"))
            h = re.sub(r"px$", "", svg.get("height", "64"))
            svg.set("viewBox", f"0 0 {width} {h}")
        svg.attrib.update(x=str(x), y=str(y), width=str(size), height=str(size))
        fragments.append(ET.tostring(svg, encoding="unicode"))

    for panel, (background, foreground) in enumerate([("#F0F3F8", "#26354B"), ("#17212E", "#E6EEF9")]):
        top = 88 + panel*panel_height
        fragments.append(f'<rect x="16" y="{top}" width="1408" height="{panel_height-12}" rx="16" fill="{background}"/>')
        fragments.append(f'<text x="34" y="{top+30}" fill="{foreground}" font-size="17" font-family="sans-serif">{"Light" if not panel else "Dark"} background</text>')
        for i, name in enumerate(selected):
            x, y = 40 + (i % 6)*232, top + 55 + (i//6)*124
            asset = byname[name]
            for size, dx in [(16, 0), (24, 32), (48, 79)]:
                variant = next((p for p in asset.get("variants", []) if f"/{size}/" in p), asset["file"])
                embed(root / variant, x+dx, y+48-size, size)
            fragments.append(f'<text x="{x}" y="{y+73}" fill="{foreground}" font-size="11" font-family="sans-serif">{escape(name[:31])}</text>')
            fragments.append(f'<text x="{x}" y="{y+90}" fill="{foreground}" opacity=".65" font-size="10" font-family="sans-serif">{escape(asset["template"])}</text>')
        origin = top + 60 + rows*124
        if states:
            fragments.append(f'<text x="34" y="{origin}" fill="{foreground}" font-size="16" font-family="sans-serif">Cursor family</text>')
        for i, state in enumerate(states):
            x, y = 40 + (i % 6)*232, origin + 22 + (i//6)*112
            source = root / cursor["path"] / "source" / (state + ".svg")
            for size, dx in [(24, 0), (32, 39), (48, 90)]:
                embed(source, x+dx, y+48-size, size)
                point = cursor.get("generated", {}).get("overrides", {}).get(state, {}).get("hotspot")
                hx, hy = hotspot(state, size, point)
                fragments.append(f'<circle cx="{x+dx+hx}" cy="{y+48-size+hy}" r="1.1" fill="#F74758"/>')
            fragments.append(f'<text x="{x}" y="{y+73}" fill="{foreground}" font-size="11" font-family="sans-serif">{escape(state)}</text>')
    fragments += [f'<text x="28" y="{height-18}" fill="#ABBBD1" font-family="sans-serif" font-size="13">Preview is evidence for review, not an automatic quality score or proof of runtime appearance.</text>', '</svg>']
    data = ''.join(fragments)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.suffix.lower() == ".svg":
        target.write_text(data, encoding="utf-8")
    else:
        if not shutil.which("rsvg-convert"):
            raise ThemeError("PNG 预览需要已有 rsvg-convert；可输出 SVG")
        result = subprocess.run(["rsvg-convert", "-f", "png"], input=data.encode(), capture_output=True, timeout=20, check=True)
        target.write_bytes(result.stdout)
    return {"ok": True, "output": str(target), "icons": selected, "cursor_states": states, "visual_verified": False}
