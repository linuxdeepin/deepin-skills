#!/usr/bin/env python3
"""Generate, validate, install and activate a user-level UOS theme package.

The model supplies a small JSON design specification; this script owns file
formats, resource validation, installation locations, DDE writes and rollback.
It never runs generated text as shell code or writes system files directly.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
import xml.etree.ElementTree as ET
from functools import wraps
from pathlib import Path

from dde_backend import DDE, ThemeError, equivalent, image_info
from screensaver_backend import ScreenSaver
from cursor_assets import load_images, validate_xcursor, write_xcursor
from cursor_runtime import CursorRuntime
from icon_theme import build as build_icons, coverage as icon_coverage, design_coverage, inventory as icon_inventory, validate_inventory, safe_name, TEMPLATES, DESIGN_POLICIES, data_home
from icon_runtime import inspect as inspect_icons
from launcher_overrides import LauncherOverrides
from desktop_integration import NativeWallpaper, desktop_status, write_global_theme
from vector_design import STYLES
from vector_assets import validate_svg
from cursor_design import CURSOR_NAMES, ALIASES as CURSOR_ALIASES, hotspot as cursor_hotspot, render_cursor
from wallpaper_source import ASPECT_TOLERANCE, detect_screen, load_provenance

try:
    from theme_state import Store, identity
except ImportError:  # pragma: no cover - direct import from a different cwd
    from .theme_state import Store, identity

PACKAGE_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,31}$")
COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
SCREENSAVER_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp"}
ICON_NAMES = ("folder", "document", "browser", "terminal", "settings", "home",
              "trash", "download", "warning", "info", "music", "image")
ICON_FILES = {
    "folder": ("places", ("folder",)),
    "document": ("mimetypes", ("text-x-generic", "application-x-zerosize")),
    "browser": ("apps", ("web-browser", "firefox", "chromium", "deepin-browser")),
    "terminal": ("apps", ("utilities-terminal", "deepin-terminal")),
    "settings": ("apps", ("preferences-system", "dde-control-center", "deepin-control-center")),
    "home": ("places", ("user-home",)),
    "trash": ("places", ("user-trash", "user-trash-full")),
    "download": ("places", ("folder-download",)),
    "warning": ("status", ("dialog-warning",)),
    "info": ("status", ("dialog-information",)),
    "music": ("mimetypes", ("audio-x-generic",)),
    "image": ("mimetypes", ("image-x-generic",)),
}



def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_relative(path: Path, root: Path) -> str:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ThemeError("包内路径越界：%s" % path) from exc
    if any(part in ("", ".", "..") for part in relative.parts):
        raise ThemeError("包内路径无效：%s" % path)
    return relative.as_posix()


def safe_id(value, field="package id"):
    if not isinstance(value, str) or not PACKAGE_RE.fullmatch(value):
        raise ThemeError("%s 必须是 2 到 32 位小写字母、数字和连字符" % field)
    return value


def color(value, field):
    if not isinstance(value, str) or not COLOR_RE.fullmatch(value):
        raise ThemeError("%s 必须使用 #RRGGBB 格式" % field)
    return value.upper()


def source_path(value, field, suffixes=None):
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ThemeError("%s 必须是本地文件路径" % field)
    source = Path(value).expanduser()
    if source.is_symlink():
        raise ThemeError("%s 不允许符号链接" % field)
    path = source.resolve()
    if not path.is_file():
        raise ThemeError("%s 不存在或不是普通文件：%s" % (field, path))
    if suffixes and path.suffix.lower() not in suffixes:
        raise ThemeError("%s 的格式不受支持：%s" % (field, path.suffix))
    if path.stat().st_size > 128 * 1024 * 1024:
        raise ThemeError("%s 大于 128 MiB" % field)
    return path


def svg_icon(name, primary, secondary, style="crafted"):
    from vector_design import render_icon
    return render_icon(name, name, primary, secondary, style)


def svg_cursor(name, primary, secondary, size=32):
    return render_cursor(name, primary, secondary, size)


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_record(path, value):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.parent.is_symlink() or path.is_symlink():
        raise ThemeError("拒绝符号链接状态路径")
    fd, temporary = tempfile.mkstemp(prefix=".write-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def package_locked(function):
    @wraps(function)
    def locked(*args, **kwargs):
        if not kwargs.get("execute", args[1] if len(args) > 1 else False):
            return function(*args, **kwargs)
        with Store().locked():
            return function(*args, **kwargs)
    return locked


def spec_defaults(spec):
    if not isinstance(spec, dict):
        raise ThemeError("主题规范必须是 JSON 对象")
    package_id = safe_id(spec.get("id"), "主题 id")
    if set(spec) - {"id", "name", "description", "palette", "icon", "cursor", "screensaver", "wallpaper", "required_components"}:
        raise ThemeError("主题规范包含未知字段")
    required = spec.get("required_components", [])
    if not isinstance(required, list) or any(item not in ("icon", "cursor", "wallpaper", "screensaver", "palette") for item in required):
        raise ThemeError("required_components 只能列出 icon,cursor,wallpaper,screensaver,palette")
    missing = [item for item in required if item not in spec or (item == "screensaver" and not (isinstance(spec[item], dict) and spec[item].get("images")))]
    if missing:
        raise ThemeError("用户要求的组件缺失：" + ",".join(missing))
    for key in ("palette", "icon", "cursor", "screensaver"):
        if key in spec and not isinstance(spec[key], dict):
            raise ThemeError("%s 必须是 JSON 对象；不需要的组件请省略" % key)
    allowed = {"palette": {"light", "dark", "apply_accent"}, "icon": {"style", "names", "scope", "inventory", "application_dirs", "base_theme", "overrides", "unknown", "design_policy"},
               "cursor": {"size", "sizes", "states", "compiler", "style", "colors", "overrides"}, "screensaver": {"images", "interval", "play_mode", "activate"}}
    for key, fields in allowed.items():
        if set(spec.get(key, {})) - fields:
            raise ThemeError("%s 包含不支持的字段" % key)
    if not any(key in spec for key in ("palette", "icon", "cursor", "wallpaper")) and not spec.get("screensaver", {}).get("images"):
        raise ThemeError("请至少指定一个组件或活动色")
    palette = spec.get("palette") or {}
    if type(palette.get("apply_accent", True)) is not bool:
        raise ThemeError("palette.apply_accent 必须是布尔值")
    light, dark = color(palette.get("light", "#3B82F6"), "palette.light"), color(palette.get("dark", "#60A5FA"), "palette.dark")
    icon = spec.get("icon") if isinstance(spec.get("icon"), dict) else {}
    cursor = spec.get("cursor") if isinstance(spec.get("cursor"), dict) else {}
    screensaver = spec.get("screensaver") if isinstance(spec.get("screensaver"), dict) else {}
    icons = icon.get("names", list(ICON_NAMES))
    cursors = cursor.get("states", list(CURSOR_NAMES))
    if not isinstance(icons, list) or not icons or len(icons) > 20000:
        raise ThemeError("icon.names 必须包含 1 到 20000 个图标名称")
    for icon_name in icons:
        safe_name(icon_name)
    icon_scope = icon.get("scope", "explicit" if "names" in icon else "desktop")
    if icon_scope not in ("explicit", "applications", "desktop", "base-theme"):
        raise ThemeError("icon.scope 必须是 explicit、applications、desktop 或 base-theme")
    app_dirs = icon.get("application_dirs")
    if app_dirs is not None and (not isinstance(app_dirs, list) or any(not isinstance(p, str) or not Path(p).is_absolute() for p in app_dirs)):
        raise ThemeError("icon.application_dirs 必须是绝对路径数组")
    overrides = copy.deepcopy(icon.get("overrides", {}))
    if not isinstance(overrides, dict):
        raise ThemeError("icon.overrides 必须是名称到绘制参数的对象")
    for icon_name, item in overrides.items():
        safe_name(icon_name)
        if not isinstance(item, dict) or set(item) - {"template", "label", "source", "variants"} or item.get("template", "app") not in TEMPLATES:
            raise ThemeError("图标绘制参数含未知模板或字段")
        if item.get("source"):
            item["source"] = str(source_path(item["source"], "icon.overrides.source", {".svg"}))
        variants = item.get("variants", {})
        if not isinstance(variants, dict) or set(variants) - {"16", "24"} or (variants and not item.get("source")):
            raise ThemeError("icon.overrides.variants 需要 source，并只接受 16、24 的独立 SVG")
        item["variants"] = {size: str(source_path(path, "icon.overrides.variants", {".svg"})) for size, path in variants.items()}
        label = item.get("label", "")
        if not isinstance(label, str) or len(label) > 4 or any(ord(c) < 32 for c in label):
            raise ThemeError("图标 label 必须是 0 到 4 个无控制字符的字符")
    inventory_path = icon.get("inventory")
    if inventory_path:
        inventory_path = str(source_path(inventory_path, "icon.inventory", {".json"}))
    base_theme = safe_name(icon.get("base_theme", "bloom"))
    if not isinstance(cursors, list) or not cursors or any(x not in CURSOR_NAMES for x in cursors):
        raise ThemeError("cursor.states 只能从支持的光标状态中选择")
    if "cursor" in spec and "left_ptr" not in cursors:
        raise ThemeError("可在控制中心切换的光标主题必须包含 left_ptr")
    cursor_size = cursor.get("size", 32)
    if type(cursor_size) is not int or not 16 <= cursor_size <= 128:
        raise ThemeError("cursor.size 必须是 16 到 128 的整数")
    sizes = cursor.get("sizes", sorted({24, 32, 48, cursor_size}))
    if not isinstance(sizes, list) or not sizes or len(sizes) > 8 or any(type(size) is not int or not 16 <= size <= 128 for size in sizes):
        raise ThemeError("cursor.sizes 必须包含 1 到 8 个 16–128 的整数")
    compiler = cursor.get("compiler", "auto")
    if compiler not in ("auto", "builtin", "xcursorgen"):
        raise ThemeError("cursor.compiler 必须是 auto、builtin 或 xcursorgen")
    style = icon.get("style", "crafted")
    if style not in STYLES:
        raise ThemeError("icon.style 必须是 crafted、ink、neon、outline 或 solid")
    unknown = icon.get("unknown", "preserve")
    if unknown not in ("preserve", "placeholder"):
        raise ThemeError("icon.unknown 必须是 preserve 或 placeholder")
    design_policy = icon.get("design_policy", "restyle-apps")
    if design_policy not in DESIGN_POLICIES:
        raise ThemeError("icon.design_policy must be restyle-apps or custom-apps")
    cursor_style = cursor.get("style", style if style in {"crafted", "ink", "neon"} else "crafted")
    if cursor_style not in {"crafted", "ink", "neon"}:
        raise ThemeError("cursor.style 必须是 crafted、ink 或 neon")
    cursor_colors = cursor.get("colors", {})
    if not isinstance(cursor_colors, dict) or set(cursor_colors) - {"fill", "outline", "accent"}:
        raise ThemeError("cursor.colors 只支持 fill、outline、accent")
    cursor_colors = {key: color(value, "cursor.colors." + key) for key, value in cursor_colors.items()}
    cursor_overrides = copy.deepcopy(cursor.get("overrides", {}))
    if not isinstance(cursor_overrides, dict) or set(cursor_overrides) - set(cursors):
        raise ThemeError("cursor.overrides 必须按已选择的状态提供素材")
    for state, item in cursor_overrides.items():
        if not isinstance(item, dict) or set(item) != {"source", "hotspot"}:
            raise ThemeError("自定义光标必须同时提供 source SVG 和 32 单位坐标的 hotspot")
        item["source"] = str(source_path(item["source"], "cursor.overrides.source", {".svg"}))
        svg = validate_svg(item["source"])
        point = item["hotspot"]
        if not isinstance(point, list) or len(point) != 2 or any(type(v) not in (int, float) or not 0 <= v < 32 for v in point):
            raise ThemeError("cursor hotspot 必须是 0≤x,y<32 的坐标对")
        try:
            bounds = [float(v) for v in re.split(r"[\s,]+", svg.get("viewBox", "").strip())]
        except ValueError:
            bounds = []
        if bounds != [0, 0, 32, 32]:
            raise ThemeError('自定义光标 SVG 必须使用 viewBox="0 0 32 32"，以便准确缩放热点')
    saver_images = screensaver.get("images", [])
    if not isinstance(saver_images, list) or any(not isinstance(x, str) for x in saver_images):
        raise ThemeError("screensaver.images 必须是本地图片路径数组")
    interval = screensaver.get("interval", 30)
    if type(interval) is not int or not 3 <= interval <= 3600:
        raise ThemeError("screensaver.interval 必须在 3 到 3600 秒之间")
    play_mode = screensaver.get("play_mode", 0)
    if type(play_mode) is not int or play_mode not in (0, 1):
        raise ThemeError("screensaver.play_mode 必须是 0 或 1")
    for key in ("name", "description"):
        if key in spec and (not isinstance(spec[key], str) or any(ord(c) < 32 for c in spec[key])):
            raise ThemeError("%s 必须是不含控制字符的字符串" % key)
    return {"id": package_id, "name": spec.get("name", package_id)[:80],
            "description": spec.get("description", "Generated UOS theme")[:300],
            "palette": {"light": light, "dark": dark} if "palette" in spec and palette.get("apply_accent", True) else None,
            "colors": {"light": light, "dark": dark},
            "enabled": {key: key in spec for key in ("icon", "cursor")},
            "icon": {"style": style, "names": icons, "scope": icon_scope, "inventory": inventory_path,
                     "application_dirs": app_dirs, "base_theme": base_theme, "overrides": overrides, "unknown": unknown,
                     "design_policy": design_policy},
            "cursor": {"size": cursor_size, "sizes": sorted(set(sizes)), "states": cursors, "compiler": compiler, "style": cursor_style, "colors": cursor_colors, "overrides": cursor_overrides},
            "screensaver": {"images": saver_images, "interval": interval,
                            "play_mode": play_mode,
                            "activate": bool(screensaver.get("activate", False))},
            "wallpaper": spec.get("wallpaper")}




def create_package(spec, output, force=False):
    cfg = spec_defaults(spec)
    output = Path(output).expanduser().absolute()
    if output.is_symlink():
        raise ThemeError("输出路径不能是符号链接")
    output = output.resolve()
    install_bases = [Path.home() / ".local/share/uos-theme-personalize/themes", data_home() / "icons", Path.home() / ".icons",
                     Path(os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")) / "dde-appearance/deepin-themes"]
    if any(base.resolve() == output or base.resolve() in output.parents for base in install_bases):
        raise ThemeError("不能直接生成或覆盖已安装资源目录；请在独立目录生成新 ID 的包")
    if output == Path.home() or output in Path.cwd().parents or output == Path.cwd():
        raise ThemeError("输出路径不能是用户目录或当前工作目录及其父目录")
    if output.exists():
        if not force:
            raise ThemeError("输出目录已存在；如确认替换，请显式使用 --force")
        if output.is_symlink() or not output.is_dir():
            raise ThemeError("输出路径必须是普通目录")
        try:
            previous = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ThemeError("--force 只能替换本生成器创建的主题包目录") from exc
        if not isinstance(previous, dict) or previous.get("format") != "uos-theme-package":
            raise ThemeError("--force 只能替换本生成器创建的主题包目录")
        shutil.rmtree(output)
    output.mkdir(parents=True, mode=0o700)
    package_id = cfg["id"]
    try:
        components = {"icon": None, "cursor": None, "screensaver": None, "wallpaper": None}
        warnings = []
        primary, secondary = cfg["colors"]["light"], cfg["colors"]["dark"]
        if cfg["enabled"]["icon"]:
            components["icon"] = build_icons(output, package_id, cfg["name"], cfg["description"], cfg["icon"], primary, secondary, ICON_FILES, svg_icon)
            generated_report = json.loads((output / "icon-coverage.json").read_text(encoding="utf-8"))
            if generated_report["exceptions"]:
                warnings.append("图标扫描有 %d 个例外；绝对路径需 --launcher-overrides，其他例外需单独适配。" % len(generated_report["exceptions"]))
            if generated_report["generic_names"]:
                warnings.append("%d 个图标仍为通用占位图形，需要补充素材；名称覆盖不代表设计完成。" % len(generated_report["generic_names"]))
        if cfg["enabled"]["cursor"]:
            cursor_dir = output / "cursors" / package_id
            source_dir = cursor_dir / "source"
            source_dir.mkdir(parents=True)
            (cursor_dir / "index.theme").write_text(f"[Icon Theme]\nName={cfg['name']}\nInherits=bloom\n", encoding="utf-8")
            (cursor_dir / "cursor.theme").write_text(f"[Icon Theme]\nName={cfg['name']}\nComment={cfg['description']}\nInherits=bloom\n", encoding="utf-8")
            size = cfg["cursor"]["size"]
            for name in cfg["cursor"]["states"]:
                override = cfg["cursor"]["overrides"].get(name)
                if override:
                    shutil.copyfile(override["source"], source_dir / f"{name}.svg")
                else:
                    (source_dir / f"{name}.svg").write_text(render_cursor(name, primary, secondary, size, cfg["cursor"]["style"], cfg["cursor"]["colors"]), encoding="utf-8")
            components["cursor"] = {"path": f"cursors/{package_id}", "compiled": False, "generated": cfg["cursor"]}
            rsvg, xcursorgen = shutil.which("rsvg-convert"), shutil.which("xcursorgen")
            method = cfg["cursor"]["compiler"]
            selected_compiler = "xcursorgen" if method != "builtin" and xcursorgen else "builtin"
            if method == "xcursorgen" and not xcursorgen:
                raise ThemeError("规范指定 xcursorgen，但工具不存在；可改用 auto 或 builtin")
            if rsvg:
                compiled = cursor_dir / "cursors"
                compiled.mkdir()
                for name in cfg["cursor"]["states"]:
                    frames = []
                    for nominal in cfg["cursor"]["sizes"]:
                        png = source_dir / f"{name}-{nominal}.png"
                        subprocess.run([rsvg, "-w", str(nominal), "-h", str(nominal), str(source_dir / f"{name}.svg"), "-o", str(png)], check=True, capture_output=True, timeout=8)
                        x, y = cursor_hotspot(name, nominal, cfg["cursor"]["overrides"].get(name, {}).get("hotspot"))
                        frames.append({"size": nominal, "xhot": x, "yhot": y, "png": png})
                    conf = cursor_dir / f"{name}.conf"
                    conf.write_text("".join(f"{frame['size']} {frame['xhot']} {frame['yhot']} source/{frame['png'].name}\n" for frame in frames), encoding="utf-8")
                    if selected_compiler == "xcursorgen":
                        subprocess.run([xcursorgen, str(conf), str(compiled / name)], cwd=str(cursor_dir), check=True, capture_output=True, timeout=8)
                    else:
                        write_xcursor(compiled / name, frames)
                    validate_xcursor(compiled / name)
                    for nominal in cfg["cursor"]["sizes"]:
                        loaded = load_images(path=compiled / name, size=nominal)
                        if loaded["available"] and not loaded.get("loaded"):
                            raise ThemeError("libXcursor 无法加载生成光标：%s/%s" % (name, nominal))
                    for alias in CURSOR_ALIASES[name]:
                        shutil.copyfile(compiled / name, compiled / alias)
                components["cursor"]["compiled"] = True
                components["cursor"]["compiler"] = selected_compiler
                components["cursor"]["loader_verified"] = loaded["available"]
            else:
                warnings.append("未找到 rsvg-convert，已生成光标 SVG 源文件但无法光栅化；缺少 xcursorgen 时可自动使用内置标准 ARGB 编译器。")
        saver = cfg["screensaver"]
        if saver["images"]:
            images_dir = output / "screensaver" / "images"
            images_dir.mkdir(parents=True)
            image_records = []
            for index, source in enumerate(saver["images"]):
                src = source_path(source, f"screensaver.images[{index}]", SCREENSAVER_SUFFIXES)
                image_info(str(src))
                target = images_dir / f"{index:03d}-{src.name}"
                shutil.copyfile(src, target)
                image_records.append({"file": str(target.relative_to(output)), "sha256": sha256(target), "bytes": target.stat().st_size})
            write_json(output / "screensaver" / "config.json", {"interval": saver["interval"], "play_mode": saver["play_mode"], "images": image_records})
            components["screensaver"] = {"path": "screensaver", "type": "deepin-custom-image-slideshow", "activate": saver["activate"], "interval": saver["interval"], "play_mode": saver["play_mode"], "images": image_records}
        if cfg["wallpaper"]:
            src = source_path(cfg["wallpaper"], "wallpaper", IMAGE_SUFFIXES)
            info = image_info(str(src))
            provenance = load_provenance(src, info)
            destination = output / "wallpapers" / (src.stem + "-" + sha256(src)[:16] + src.suffix.lower())
            destination.parent.mkdir(parents=True)
            shutil.copyfile(src, destination)
            component = {"file": str(destination.relative_to(output)), "sha256": sha256(destination),
                         "bytes": info["bytes"]}
            if info["width"] and info["height"]:
                component.update(width=info["width"], height=info["height"])
            if provenance:
                sidecar = destination.with_name(destination.name + ".source.json")
                write_json(sidecar, provenance)
                component.update(source=provenance, source_file=str(sidecar.relative_to(output)))
            try:
                screen = detect_screen()
            except ThemeError:
                screen = None
            if screen and info["width"] and (info["width"] < screen["width"] or info["height"] < screen["height"]):
                warnings.append("壁纸 %dx%d 低于当前屏幕 %dx%d，激活后会被拉伸；请换用等于或高于屏幕分辨率的素材。"
                                % (info["width"], info["height"], screen["width"], screen["height"]))
            elif screen and info["width"]:
                target = screen["width"] / screen["height"]
                delta = abs(info["width"] / info["height"] - target) / target
                if delta > ASPECT_TOLERANCE:
                    warnings.append("壁纸宽高比与当前屏幕相差 %.1f%%，填充时会裁切或留边；请在可选素材中优先更接近屏幕比例的一张。"
                                    % (delta * 100))
            components["wallpaper"] = component
        missing = [name for name in spec.get("required_components", [])
                   if (not cfg["palette"] if name == "palette" else not components.get(name))]
        if "cursor" in spec.get("required_components", []) and not (components.get("cursor") or {}).get("compiled"):
            missing.append("cursor（尚未编译）")
        if missing:
            raise ThemeError("用户要求的组件尚未生成完整：" + ",".join(missing))
        assets = (components.get("icon") or {}).get("assets", [])
        preserved = [a["name"] for a in assets if a["template"] == "preserved"]
        placeholders = [a["name"] for a in assets if a["generic"]]
        if preserved:
            warnings.append("%d 个名称保留本机基准 SVG，未计为原创重绘；来源见 manifest。" % len(preserved))
        icon_design = design_coverage(output, json.loads((output / "icon-inventory.json").read_text(encoding="utf-8")), assets, cfg["icon"]["design_policy"]) if assets else None
        if icon_design and not icon_design["design_complete"]:
            warnings.append("%d application icon designs are pending; see icon_design.pending. Complete activation is blocked until they are supplied." % len(icon_design["pending"]))
        write_json(output / "design-report.json", {
            "icon_style": cfg["icon"]["style"] if assets else None,
            "icon_design": icon_design,
            "icons": {"total": len(assets), "custom": [a["name"] for a in assets if a["template"] == "custom"],
                      "preserved": preserved, "placeholders": placeholders, "generated": sum(a["template"] not in ("custom", "preserved", "app") for a in assets)},
            "cursor_style": cfg["cursor"]["style"] if components.get("cursor") else None,
            "cursor_custom_states": list(cfg["cursor"]["overrides"]),
            "cursor_animation": "static",
            "visual_verified": False,
            "review": ["查看 design-preview 的明暗背景、16/24/48 图标及 24/32/48 光标", "检查应用辨识、方向与状态、热点、占位图和保留素材；技术通过不代表视觉验收"]})
        manifest = {"format": "uos-theme-package", "version": 1, "id": package_id,
                    "name": cfg["name"], "description": cfg["description"],
                    "generated_by": "uos-theme-personalize", "generated_at": int(time.time()),
                    "palette": cfg["palette"], "components": components,
                    "required_components": list(spec.get("required_components", [])),
                    "requirements": {"user_install": True, "root_required": False,
                                      "cursor_compiler": "rsvg-convert + xcursorgen or built-in raw ARGB writer",
                                      "screensaver": "deepin-custom-screensaver for image slideshow"},
                    "warnings": warnings}
        write_json(output / "manifest.json", manifest)
        (output / "palette.json").write_text(json.dumps(cfg["palette"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest["files"] = {str(path.relative_to(output)): sha256(path) for path in output.rglob("*") if path.is_file() and path != output / "manifest.json"}
        write_json(output / "manifest.json", manifest)
        return validate_package(output)
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        raise


def validate_package(package):
    requested = Path(package).expanduser()
    if requested.is_symlink():
        raise ThemeError("主题包不能是符号链接")
    root = requested.resolve()
    if not root.is_dir():
        raise ThemeError("主题包必须是普通目录")
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise ThemeError("缺少 manifest.json")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ThemeError("manifest.json 无法解析") from exc
    if not isinstance(manifest, dict):
        raise ThemeError("manifest.json 必须是 JSON 对象")
    package_id = safe_id(manifest.get("id"))
    if manifest.get("format") != "uos-theme-package" or manifest.get("version") != 1:
        raise ThemeError("不支持的主题包格式或版本")
    files, errors = [], []
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append("包内不允许符号链接：%s" % path.relative_to(root))
        elif path.is_file():
            relative = safe_relative(path, root)
            if path.stat().st_size > 128 * 1024 * 1024:
                errors.append("文件超过 128 MiB：%s" % relative)
            files.append(relative)
    if errors:
        raise ThemeError("主题包校验失败：" + "；".join(errors))
    components = manifest.get("components")
    if not isinstance(components, dict) or set(components) - {"icon", "cursor", "screensaver", "wallpaper"}:
        raise ThemeError("manifest.components 无效")
    for key, component in components.items():
        if component is not None and not isinstance(component, dict):
            raise ThemeError("组件 %s 必须是对象或 null" % key)
    palette = manifest.get("palette")
    if palette is not None:
        if not isinstance(palette, dict):
            raise ThemeError("manifest.palette 无效")
        color(palette.get("light"), "palette.light")
        color(palette.get("dark"), "palette.dark")
    icon_root = root / "icons" / package_id
    if components.get("icon") and (components["icon"].get("path") != f"icons/{package_id}" or not (icon_root / "index.theme").is_file()):
        errors.append("图标主题路径无效或缺少 index.theme")
    icon = components.get("icon") or {}
    icon_design = None
    if icon.get("inventory"):
        if icon.get("inventory") != "icon-inventory.json" or icon.get("coverage") != "icon-coverage.json":
            raise ThemeError("图标清单或覆盖报告路径无效")
        targets = validate_inventory(json.loads((root / "icon-inventory.json").read_text(encoding="utf-8")))
        assets = icon.get("assets")
        if not isinstance(assets, list) or len(assets) > 20000:
            raise ThemeError("图标资源清单无效")
        names = set()
        for asset in assets:
            name = safe_name(asset.get("name"))
            filename = asset.get("file")
            if name in names or not isinstance(filename, str) or not re.fullmatch(r"icons/" + re.escape(package_id) + r"/scalable/(apps|places|status|mimetypes|devices|actions)/" + re.escape(name) + r"\.svg", filename):
                raise ThemeError("图标资源名称重复或文件路径无效")
            names.add(name)
            path = root / filename
            if not path.is_file() or path.stat().st_size > 1024 * 1024:
                raise ThemeError("图标资源缺失或过大：%s" % filename)
            validate_svg(path)
            variants = asset.get("variants", [])
            if not isinstance(variants, list) or len(variants) > 2:
                raise ThemeError("图标小尺寸清单无效")
            for variant in variants:
                if not isinstance(variant, str) or not re.fullmatch(r"icons/" + re.escape(package_id) + r"/(16|24)/(apps|places|status|mimetypes|devices|actions)/" + re.escape(name) + r"\.svg", variant):
                    raise ThemeError("小尺寸图标路径无效")
                validate_svg(root / variant)
        computed = icon_coverage(root, targets, assets)
        recorded = json.loads((root / "icon-coverage.json").read_text(encoding="utf-8"))
        if computed != recorded:
            raise ThemeError("图标覆盖报告与实际资源不一致")
        icon_design = design_coverage(root, targets, assets, icon.get("generated", {}).get("design_policy", "restyle-apps"))
    cursor = components.get("cursor") or {}
    cursor_root = root / "cursors" / package_id
    if cursor and (cursor.get("path") != f"cursors/{package_id}" or not (cursor_root / "index.theme").is_file()):
        errors.append("光标主题路径无效或缺少 index.theme")
    if cursor:
        for source in (cursor_root / "source").glob("*.svg"):
            validate_svg(source)
    if cursor.get("compiled"):
        compiled = cursor_root / "cursors"
        if not compiled.is_dir() or not any(item.is_file() for item in compiled.iterdir()):
            errors.append("manifest 标记了已编译光标，但缺少 Xcursor 文件")
        else:
            for item in compiled.iterdir():
                if item.is_file():
                    validate_xcursor(item)
    saver = components.get("screensaver")
    if saver:
        if saver.get("path") != "screensaver" or saver.get("type") != "deepin-custom-image-slideshow" or not (root / "screensaver/images").is_dir():
            errors.append("屏保组件类型或图片目录无效")
        if type(saver.get("interval")) is not int or not 3 <= saver["interval"] <= 3600 or type(saver.get("play_mode")) is not int or saver["play_mode"] not in (0, 1):
            errors.append("屏保轮播参数无效")
        images = saver.get("images")
        if not isinstance(images, list) or not images:
            errors.append("屏保组件缺少图片清单")
        else:
            for image in images:
                if not isinstance(image, dict) or not isinstance(image.get("file"), str):
                    raise ThemeError("屏保图片记录无效")
                image_path = root / image["file"]
                if not image["file"].startswith("screensaver/images/") or safe_relative(image_path, root) != image["file"] or not image_path.is_file():
                    raise ThemeError("屏保图片路径无效")
                image_info(str(image_path))
    wallpaper = components.get("wallpaper")
    if wallpaper:
        filename = wallpaper.get("file")
        if not isinstance(filename, str) or not filename.startswith("wallpapers/") or safe_relative(root / filename, root) != filename:
            raise ThemeError("壁纸组件路径无效")
        info = image_info(str(root / filename))
        if wallpaper.get("width") and (wallpaper.get("width"), wallpaper.get("height")) != (info["width"], info["height"]):
            raise ThemeError("壁纸尺寸记录与实际文件不一致")
        source, source_file = wallpaper.get("source"), wallpaper.get("source_file")
        if source is not None or source_file is not None:
            if (not isinstance(source, dict) or source.get("format") != "uos-wallpaper-source"
                    or source.get("version") != 1 or source.get("sha256") != wallpaper.get("sha256")):
                raise ThemeError("壁纸来源记录与摘要不一致")
            if (not isinstance(source_file, str) or not source_file.startswith("wallpapers/")
                    or safe_relative(root / source_file, root) != source_file or not (root / source_file).is_file()):
                raise ThemeError("壁纸来源记录路径无效")
            if json.loads((root / source_file).read_text(encoding="utf-8")) != source:
                raise ThemeError("壁纸来源记录文件与 manifest 不一致")
    checksums = manifest.get("files")
    if not isinstance(checksums, dict) or set(checksums) != set(files) - {"manifest.json"}:
        errors.append("包内文件与摘要清单不一致")
    else:
        for filename, expected in checksums.items():
            if sha256(root / filename) != expected:
                errors.append("文件内容已变化：%s" % filename)
    if errors:
        raise ThemeError("主题包校验失败：" + "；".join(errors))
    return {"ok": True, "id": package_id, "manifest": manifest, "files": files,
            "icon_design": icon_design, "design_complete": icon_design["design_complete"] if icon_design else None,
            "icon_coverage": json.loads((root / icon["coverage"]).read_text(encoding="utf-8")) if icon.get("coverage") else None,
            "cursor_compiled": bool(cursor.get("compiled")), "warnings": manifest.get("warnings", [])}


def user_root():
    home = Path(os.environ.get("HOME") or str(Path.home())).expanduser().resolve()
    if home == Path("/") or not home.is_dir():
        raise ThemeError("无法确定用户 HOME")
    return home


def copy_tree(source, target):
    if target.exists() or target.is_symlink():
        raise ThemeError("目标已存在：%s；为避免覆盖现有主题，请使用新的 id" % target)
    check_target(target)
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    shutil.copytree(source, target, symlinks=False)


def package_state_path(package_id):
    state = Path(os.environ.get("XDG_STATE_HOME") or str(user_root() / ".local/state")) / "uos-theme-personalize" / "packages"
    if not state.is_absolute() or state.is_symlink():
        raise ThemeError("状态目录必须是绝对路径且不能是符号链接")
    return state / (safe_id(package_id) + ".json")


def managed_root(package_id):
    return user_root() / ".local/share/uos-theme-personalize/themes" / safe_id(package_id)


def icon_install_root(package_id):
    path = data_home() / "icons" / safe_id(package_id)
    check_target(path)
    return path


def global_install_root(package_id):
    root = Path(os.environ.get("XDG_CONFIG_HOME") or str(user_root() / ".config"))
    path = root / "dde-appearance/deepin-themes" / safe_id(package_id)
    check_target(path)
    return path


def check_target(target):
    home = user_root()
    try:
        target.relative_to(home)
    except ValueError as exc:
        raise ThemeError("安装目标必须位于当前用户目录") from exc
    if any(path.is_symlink() for path in (target, *target.parents) if path != home and home in path.parents):
        raise ThemeError("安装目标或父目录不能是符号链接：%s" % target)


def inventory(folder):
    if not folder.is_dir() or folder.is_symlink():
        raise ThemeError("安装目录不存在或已替换：%s" % folder)
    result = {}
    for path in folder.rglob("*"):
        if path.is_symlink():
            raise ThemeError("安装目录包含符号链接：%s" % path)
        if path.is_file():
            result[str(path.relative_to(folder))] = sha256(path)
    return result


@package_locked
def install_package(package, execute=False, desktop_integration=True):
    report = validate_package(package)
    root = Path(package).expanduser().resolve()
    package_id = report["id"]
    home = user_root()
    actions = [{"source": ".", "target": str(managed_root(package_id)), "component": "package"}]
    icon = report["manifest"]["components"].get("icon")
    cursor = report["manifest"].get("components", {}).get("cursor") or {}
    if icon or cursor.get("compiled"):
        actions.append({"source": "@assets", "target": str(icon_install_root(package_id)), "component": "icon" if icon else "cursor-primary"})
    if cursor.get("compiled"):
        # Both search orders see the SAME index, cursor.theme, icons and cursors.
        actions.append({"source": "@assets", "target": str(home / ".icons" / package_id), "component": "cursor"})
    if desktop_integration:
        actions.append({"source": "@global", "target": str(global_install_root(package_id)), "component": "globaltheme"})
    for action in actions:
        target = Path(action["target"])
        check_target(target)
        if target.exists():
            raise ThemeError("目标已存在：%s；请使用新主题 id 或先卸载" % target)
        if target == root or root in target.parents or target in root.parents:
            raise ThemeError("主题包来源与安装目录不能重叠")
    if package_state_path(package_id).exists():
        raise ThemeError("主题包已安装，请先恢复并卸载旧包")
    wallpaper = report["manifest"]["components"].get("wallpaper")
    native = NativeWallpaper()
    native_plan = native.plan(root / wallpaper["file"]) if desktop_integration and wallpaper else None
    if not execute:
        return {"ok": True, "dry_run": True, "id": package_id, "actions": actions, "native_wallpaper": native_plan,
                "desktop_integration": desktop_integration, "warnings": report["warnings"]}
    if os.geteuid() == 0:
        raise ThemeError("请以图形登录用户安装，不要使用 sudo 或 root")
    installed = []
    record = {"id": package_id, "package": str(managed_root(package_id)), "installed_at": int(time.time()),
              "actions": installed, "manifest": report["manifest"], "native_wallpaper": native_plan,
              "desktop_integration": desktop_integration, "state": "installing"}
    try:
        with tempfile.TemporaryDirectory(prefix="uos-theme-install-") as temp:
            assets = Path(temp) / "assets"
            assets.mkdir()
            if icon:
                shutil.copytree(root / icon["path"], assets, dirs_exist_ok=True)
            if cursor.get("compiled"):
                for source in (root / cursor["path"]).iterdir():
                    if source.name == "index.theme" and icon:
                        continue
                    destination = assets / source.name
                    if source.is_dir():
                        shutil.copytree(source, destination)
                    else:
                        shutil.copyfile(source, destination)
                if not (assets / "cursor.theme").exists():
                    shutil.copyfile(root / cursor["path"] / "index.theme", assets / "cursor.theme")
            save_record(package_state_path(package_id), record)
            for action in actions:
                if action["source"] == "@global":
                    if native_plan:
                        native.apply(native_plan, lambda: save_record(package_state_path(package_id), record))
                    uri = Path(native_plan["path"]).as_uri() if native_plan else None
                    write_global_theme(Path(temp) / "global", report["manifest"], uri)
                    source = Path(temp) / "global"
                else:
                    source = assets if action["source"] == "@assets" else root / action["source"]
                target = Path(action["target"])
                action["files"] = inventory(source)
                installed.append(action)
                save_record(package_state_path(package_id), record)
                copy_tree(source, target)
        validate_package(managed_root(package_id))
        record["state"] = "installed"
        save_record(package_state_path(package_id), record)
    except Exception:
        if native_plan:
            try:
                native.remove(native_plan)
            except Exception as exc:
                record.update(state="needs_attention", error=str(exc))
                save_record(package_state_path(package_id), record)
                raise ThemeError("安装失败且壁纸导入尚未恢复；保留安装记录：%s" % exc) from exc
        for action in reversed(installed):
            target = Path(action["target"])
            if target.is_dir() and not target.is_symlink():
                shutil.rmtree(target, ignore_errors=True)
            elif target.exists() or target.is_symlink():
                target.unlink()
        package_state_path(package_id).unlink(missing_ok=True)
        raise
    integration = None
    if desktop_integration:
        deadline = time.monotonic() + 15  # DDE batches directory refreshes for 10 s.
        while True:
            try:
                integration = desktop_status(record)
            except ThemeError as exc:
                integration = {"ok": False, "error": str(exc)}
            if integration["ok"] or time.monotonic() >= deadline:
                break
            time.sleep(0.25)
    return {"ok": not desktop_integration or integration["ok"], "installed": True, "dry_run": False,
            "id": package_id, "actions": actions, "desktop_integration": integration,
            "native_wallpaper": native_plan, "warnings": report["warnings"]}


def load_installed(package_id):
    path = package_state_path(package_id)
    if not path.is_file() or path.is_symlink():
        raise ThemeError("主题包尚未通过 install 安装：%s" % package_id)
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict) or record.get("id") != package_id or record.get("package") != str(managed_root(package_id)):
        raise ThemeError("安装记录格式或路径无效")
    allowed = {"package": {str(managed_root(package_id))}, "icon": {str(icon_install_root(package_id)), str(user_root() / ".local/share/icons" / package_id)},
               "cursor-primary": {str(icon_install_root(package_id))},
               "cursor": {str(user_root() / ".icons" / package_id)}}
    if any(action.get("component") == "globaltheme" for action in record.get("actions", [])):
        allowed["globaltheme"] = {str(global_install_root(package_id))}
    for action in record.get("actions", []):
        if action.get("component") not in allowed or action.get("target") not in allowed[action["component"]] or not isinstance(action.get("files"), dict):
            raise ThemeError("安装记录含有未知目标")
        check_target(Path(action["target"]))
    if not record.get("actions"):
        raise ThemeError("安装记录缺少资源清单")
    return record


def verify_installed(record):
    for action in record["actions"]:
        if inventory(Path(action["target"])) != action["files"]:
            raise ThemeError("安装资源已变化：%s；保留文件，请先处理后重试" % action["target"])
    report = validate_package(record["package"])
    if report["manifest"] != record["manifest"]:
        raise ThemeError("安装后的 manifest 与记录不一致")


@package_locked
def uninstall_package(package_id, execute=False):
    record = load_installed(package_id)
    active_path = package_state_path(package_id).with_name(package_id + ".active.json")
    if active_path.exists():
        raise ThemeError("主题包仍有激活记录；先用 rollback 恢复，再卸载")
    verify_installed(record)
    if record.get("desktop_integration"):
        backend = DDE().connect()
        current = backend.inspect()["settings"]
        wallpaper = record.get("native_wallpaper") or {}
        wallpaper_uris = [current.get("wallpaper", "")]
        for key in ("WallpaperURIs", "WallpaperURls"):
            try:
                wallpaper_uris.extend(json.loads(current.get(key, "{}" )).values())
            except (ValueError, AttributeError):
                pass
        if (current.get("icon_theme") == package_id or current.get("cursor_theme") == package_id
                or current.get("GlobalTheme", "").split(".")[0] == package_id
                or (wallpaper.get("path") and Path(wallpaper["path"]).as_uri() in wallpaper_uris)):
            raise ThemeError("该主题仍被控制中心选中或壁纸仍在某个工作区使用；先切换到其他资源再卸载")
    actions = record.get("actions", [])
    if not execute:
        return {"ok": True, "dry_run": True, "id": package_id,
                "actions": [{"remove": action["target"]} for action in actions]}
    if os.geteuid() == 0:
        raise ThemeError("请以图形登录用户卸载，不要使用 sudo 或 root")
    if record.get("native_wallpaper"):
        wallpaper = record["native_wallpaper"]
        shared = False
        if wallpaper.get("created"):
            for path in package_state_path(package_id).parent.glob("*.json"):
                if path == package_state_path(package_id) or path.stem.startswith("change-") or path.name.endswith(".active.json"):
                    continue
                other = json.loads(path.read_text(encoding="utf-8"))
                target = other.get("native_wallpaper") or {}
                if other.get("id") == path.stem and target.get("path") == wallpaper.get("path") and target.get("status") != "removed":
                    target.update(created=True, sha256=wallpaper["sha256"], status="imported")
                    save_record(path, other)
                    shared = True
                    break
        if not shared:
            NativeWallpaper().remove(wallpaper)
        save_record(package_state_path(package_id), record)
    removed = []
    for action in reversed(actions):
        target = Path(action["target"])
        if not target.exists() and not target.is_symlink():
            continue
        # Never follow a symlink from a package installation record.
        if target.is_symlink():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
        removed.append(str(target))
    package_state_path(package_id).unlink(missing_ok=True)
    return {"ok": True, "dry_run": False, "id": package_id, "removed": removed}


def screen_recovery_ok(results):
    return all(item["status"] in ("restored", "already_restored", "can_restore") for item in results)


def inspect_installed_icons(record):
    manifest = copy.deepcopy(record["manifest"])
    icon_action = next((item for item in record["actions"] if item["component"] == "icon"), None)
    if not icon_action:
        raise ThemeError("安装记录缺少图标资源")
    manifest["components"]["icon"]["installed_path"] = icon_action["target"]
    return inspect_icons(record["package"], manifest)


ACTIVE_STATUSES = ("applied", "started", "conflict", "restore_failed")

def active_fields(change):
    """Component kinds whose recovery point is still owned by this record."""
    fields = {op["kind"] for op in change.get("operations", []) if op.get("status") in ACTIVE_STATUSES}
    if (change.get("screensaver") and change["screensaver"].get("started")
            and not change.get("screensaver_restored")):
        fields.add("screensaver")
    for key, kind in (("cursor_sync", "cursor_theme"), ("launcher_overrides", "icon_theme")):
        if any(op.get("status") in ACTIVE_STATUSES for op in (change.get(key) or {}).get("operations", [])):
            fields.add(kind)
    return fields


def recover_change(change, backend, state_path, execute, components_only=None):
    mapping = {"icon": "icon_theme", "cursor": "cursor_theme", "wallpaper": "wallpaper", "accent": "accent_color", "screensaver": "screensaver"}
    if components_only and (set(components_only) - set(mapping)):
        raise ThemeError("恢复组件名称无效")
    selected = {mapping[name] for name in components_only} if components_only else set(mapping.values())
    results = []
    if "screensaver" in selected and change.get("screensaver") and change["screensaver"].get("started") and not change.get("screensaver_restored"):
        try:
            screen_results = ScreenSaver().rollback(change["screensaver"], execute=execute)
        except ThemeError as exc:
            screen_results = [{"key": "screensaver", "status": "failed", "error": str(exc)}]
        change["screensaver_recovery"] = screen_results
        if execute and screen_recovery_ok(screen_results):
            change["screensaver_restored"] = True
            save_record(state_path, change)
    else:
        screen_results = []
    for op in reversed(change["operations"]):
        if op["kind"] not in selected or op["status"] not in ("applied", "started", "conflict", "restore_failed"):
            continue
        try:
            current = backend.read(op["kind"], op["target"])
            if equivalent(op["kind"], current, op["before"]):
                status = "restored"
            elif equivalent(op["kind"], current, op["after"]):
                status = "can_restore"
                if execute:
                    backend.write(op["kind"], op["target"], op["before"])
                    backend.wait_for(op["kind"], op["target"], op["before"])
                    status = "restored"
            else:
                status = "conflict"
            result = {"kind": op["kind"], "status": status, "current": current, "to": op["before"]}
        except ThemeError as exc:
            result = {"kind": op["kind"], "status": "restore_failed", "error": str(exc)}
        if execute:
            op["status"] = result["status"]
            save_record(state_path, change)
        results.append(result)
    cursor_results = CursorRuntime().rollback(change["cursor_sync"], execute, checkpoint=lambda: save_record(state_path, change)) if "cursor_theme" in selected and change.get("cursor_sync") else []
    launcher_results = LauncherOverrides().rollback(change["launcher_overrides"], execute, checkpoint=lambda: save_record(state_path, change)) if "icon_theme" in selected and change.get("launcher_overrides") else []
    ok = screen_recovery_ok(screen_results) and all(item["status"] in ("restored", "can_restore") for item in results + cursor_results + launcher_results)
    if execute:
        remaining = any(op["status"] in ("applied", "started", "conflict", "restore_failed") for op in change["operations"])
        for key in ("cursor_sync", "launcher_overrides"):
            remaining |= bool(change.get(key) and any(op["status"] in ("applied", "started", "conflict", "restore_failed") for op in change[key]["operations"]))
        if change.get("screensaver") and change["screensaver"].get("started"):
            remaining |= not change.get("screensaver_restored", False)
        change["state"] = ("applied" if remaining else "rolled_back") if ok else "needs_attention"
        save_record(state_path, change)
        if change["state"] == "rolled_back":
            os.replace(state_path, state_path.with_name(change["id"] + ".json"))
    return {"ok": ok, "dry_run": not execute, "change_id": change["id"], "state": change.get("state"), "results": results, "screensaver": screen_results, "cursor_sync": cursor_results, "launcher_overrides": launcher_results, "restored_components": components_only}


@package_locked
def apply_package(package_id, execute=False, include_screensaver=False, components_only=None, cursor_sync=False, launcher_overrides=False, allow_partial_icons=False):
    record = load_installed(package_id)
    verify_installed(record)
    state_path = package_state_path(package_id).with_name(package_id + ".active.json")
    active = list(state_path.parent.glob("*.active.json"))
    previous = []
    for path in active:
        if path.is_symlink():
            raise ThemeError("拒绝符号链接激活记录")
        previous.append((path, json.loads(path.read_text(encoding="utf-8"))))
    for _, old in previous:
        if old.get("package_id") == package_id:
            raise ThemeError("同一主题包已有激活记录；请直接恢复该记录，或生成新 ID 的包后再切换：%s" % old["id"])
        if old.get("state") not in ("applied", "applied_pending_runtime"):
            raise ThemeError("存在未完成的激活记录；请先恢复对应变更：%s" % old["id"])
    # Launcher overrides written by an applied theme may still sit in the user's
    # applications directory; a switch takes them over instead of forcing a
    # rollback that would invalidate every installed package's app inventory.
    adopt_launchers = {}
    archived = []
    for candidate in sorted(state_path.parent.glob("change-*.json")):
        if candidate.is_symlink() or not candidate.is_file():
            continue
        try:
            old = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if old.get("state") == "superseded":
            archived.append(old)
    for _, old in previous + [(None, item) for item in archived]:
        for op in (old.get("launcher_overrides") or {}).get("operations", []):
            if op.get("status") in ACTIVE_STATUSES:
                adopt_launchers.setdefault(op["desktop_id"], {"after_hash": op.get("after_hash"), "change_id": old["id"]})
    manifest = record["manifest"]
    selected = set(components_only or ("icon", "cursor", "wallpaper", "accent"))
    if selected - {"icon", "cursor", "wallpaper", "accent"} or not selected:
        raise ThemeError("--components 只能使用 icon,cursor,wallpaper,accent")
    components = {key: value for key, value in manifest.get("components", {}).items() if key in selected or key == "screensaver"}
    palette = (manifest.get("palette") or {}) if "accent" in selected else {}
    has_dde = components.get("icon") or (components.get("cursor") or {}).get("compiled") or components.get("wallpaper") or palette
    backend = DDE().connect() if has_dde else None
    capabilities = backend.capabilities() if backend else {}
    before = {}
    target = {}
    blocked = []
    warnings = list(manifest.get("warnings", []))
    incomplete = ["cursor"] if components.get("cursor") and not components["cursor"].get("compiled") else []
    for field in selected - {"accent"}:
        if components_only is not None and not components.get(field):
            blocked.append(field + ": 包内无该组件")
    if components_only is not None and "cursor" in selected and incomplete:
        blocked.append("cursor: 尚未编译")
    for kind, field in (("icon_theme", "icon"), ("cursor_theme", "cursor")):
        component = components.get(field)
        if not component or (field == "cursor" and not component.get("compiled")):
            continue
        if not capabilities.get(kind):
            blocked.append(kind)
            continue
        before[kind] = backend.read(kind)
        target[kind] = package_id
    if palette:
        if capabilities.get("accent_pair"):
            before["accent_color"] = backend.read("accent_color", "pair")
            if not re.fullmatch(r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?,#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?", str(before["accent_color"])):
                raise ThemeError("原活动色格式无效，无法建立恢复点")
            target["accent_color"] = palette["light"].upper() + "," + palette["dark"].upper()
        else:
            blocked.append("accent_color: 当前接口不支持浅色/深色颜色对")
    wallpaper = components.get("wallpaper")
    if wallpaper:
        if capabilities.get("wallpaper"):
            path = Path(record["package"]) / wallpaper["file"]
            before["wallpaper"] = backend.read("wallpaper")
            native_wallpaper = record.get("native_wallpaper") or {}
            target["wallpaper"] = Path(native_wallpaper["path"]).as_uri() if native_wallpaper.get("path") else path.as_uri()
        else:
            blocked.append("wallpaper")
    saver = components.get("screensaver")
    saver_plan = None
    if include_screensaver and saver:
        saver_root = user_root() / ".local/share/uos-theme-personalize/themes" / package_id / "screensaver" / "images"
        saver_plan = ScreenSaver().plan(saver_root, saver.get("interval", 30), saver.get("play_mode", 0), True)
        saver_plan["started"] = []
    elif include_screensaver:
        blocked.append("screensaver: 包内无屏保组件")
    for kind, value in before.items():
        if not isinstance(value, str) or not value:
            raise ThemeError("无法读取 %s 的可恢复原值" % kind)
    if not target and not saver_plan:
        if not blocked:
            raise ThemeError("主题包没有可激活的已编译组件")
    operations = [{"kind": kind, "before": old, "after": target[kind], "target": "pair" if kind == "accent_color" else None,
                   "status": "unchanged" if equivalent(kind, old, target[kind]) else "pending"} for kind, old in before.items()]
    sync_plan = None
    if cursor_sync:
        if "cursor_theme" not in target:
            blocked.append("cursor_sync: 本次未选择已编译的光标组件")
        else:
            sync_plan = CursorRuntime().plan(package_id)
            blocked.extend(sync_plan["errors"])
    launcher_plan, icon_report, icon_preflight, icon_design = None, None, None, None
    if "icon_theme" in target:
        icon = components["icon"]
        if icon.get("coverage"):
            icon_report = json.loads((Path(record["package"]) / icon["coverage"]).read_text(encoding="utf-8"))
            inventory = validate_inventory(json.loads((Path(record["package"]) / icon["inventory"]).read_text(encoding="utf-8")))
            icon_design = design_coverage(record["package"], inventory, icon["assets"], icon.get("generated", {}).get("design_policy", "restyle-apps"))
            if launcher_overrides:
                launcher_plan = LauncherOverrides().plan(inventory, adopt_launchers)
                blocked.extend(item["error"] for item in launcher_plan["errors"])
            icon_complete = icon_report["files_complete"] and not any(item["reason"] not in ("absolute_icon", "missing_icon") for item in icon_report["exceptions"]) and (not icon_report["requires_launcher_overrides"] or launcher_overrides) and icon_design["design_complete"]
            if not icon_complete:
                incomplete.append("icon")
                if not allow_partial_icons:
                    blocked.append("Icon coverage or design is incomplete; see icon_coverage and icon_design.pending. Absolute paths require --launcher-overrides; explicitly accepted omissions require --allow-partial-icons.")
            icon_preflight = inspect_icons(record["package"], manifest, staged=True, launcher_plan=launcher_plan)
            if icon_preflight.get("source_changes"):
                blocked.append("应用清单在生成后变化，请重新扫描并生成新 ID 的包")
        else:
            incomplete.append("icon")
            warnings.append("旧图标包没有目标清单，不能验证全量覆盖。")
    elif launcher_overrides:
        blocked.append("launcher_overrides: 本次未选择图标组件")
    requested = {op["kind"] for op in operations}
    if saver_plan:
        requested.add("screensaver")
    replaced = [(path, old) for path, old in previous if requested & active_fields(old)]
    preview = {"ok": not blocked, "execute_ready": not blocked, "dry_run": not execute, "package_id": package_id, "operations": operations,
               "screensaver": saver_plan, "cursor_sync": sync_plan, "launcher_overrides": launcher_plan,
               "icon_coverage": icon_report, "icon_design": icon_design,
               "design_complete": icon_design["design_complete"] if icon_design else None,
               "icon_preflight": icon_preflight, "blocked": blocked, "warnings": warnings,
               "incomplete_components": incomplete, "scope_complete": not incomplete and not blocked, "wallpaper_scope": "primary/current_workspace",
               "supersedes": [old["id"] for _, old in replaced],
               "note": "预览与执行会各自重新读取当前值；执行记录保存本次执行前的原值。已被替代的激活记录归档，但仍可按 change ID 恢复。"}
    if not execute:
        return preview
    if blocked:
        raise ThemeError("主题包存在不可执行项，请调整后重新预览：%s" % blocked)
    if os.geteuid() == 0:
        raise ThemeError("请以图形登录用户执行，不要使用 sudo 或 root")
    change_id = "change-" + uuid.uuid4().hex[:16]
    for path, old in replaced:
        # A theme switch replaces the previous theme's recovery point with a
        # newer one; the old journal is kept intact and archived so its change
        # ID still restores the older baseline.
        old.update(state="superseded", superseded_by=change_id, superseded_at=int(time.time()))
        save_record(path, old)
        os.replace(path, path.with_name(old["id"] + ".json"))
    change = {"id": change_id, "package_id": package_id,
              "session": identity(), "created_at": int(time.time()), "state": "applying",
              "supersedes": [old["id"] for _, old in replaced],
              "backend": backend.endpoint() if backend else None, "operations": copy.deepcopy(operations), "screensaver": saver_plan, "cursor_sync": sync_plan, "launcher_overrides": launcher_plan}
    save_record(state_path, change)
    try:
        for op in change["operations"]:
            if op["status"] == "unchanged":
                continue
            if not equivalent(op["kind"], backend.read(op["kind"], op["target"]), op["before"]):
                raise ThemeError("原设置已变化，请重新预览")
            op["status"] = "started"
            save_record(state_path, change)
            backend.write(op["kind"], op["target"], op["after"])
            observed = backend.wait_for(op["kind"], op["target"], op["after"])
            op["observed"] = observed
            op["status"] = "applied"
            save_record(state_path, change)
        if saver_plan:
            change["screensaver_result"] = ScreenSaver().apply(saver_plan, checkpoint=lambda: save_record(state_path, change))
        if sync_plan:
            CursorRuntime().apply(sync_plan, checkpoint=lambda: save_record(state_path, change))
        if launcher_plan:
            LauncherOverrides().apply(launcher_plan, checkpoint=lambda: save_record(state_path, change))
        change["state"] = "applied"
        runtime_ok = True
        if "icon_theme" in target:
            change["icon_runtime"] = inspect_installed_icons(record)
            runtime_ok = change["icon_runtime"].get("runtime_verified", False)
            if not allow_partial_icons:
                runtime_ok &= change["icon_runtime"].get("scope_complete", False)
            if not change["icon_runtime"].get("scope_complete", False) and "icon" not in incomplete:
                incomplete.append("icon")
        if "cursor_theme" in target:
            cursor_dir = user_root() / ".icons" / package_id
            change["cursor_runtime"] = CursorRuntime().inspect(package_id, cursor_dir, backend=backend)
            runtime_ok &= change["cursor_runtime"]["configuration_consistent"] and change["cursor_runtime"]["named_lookup_matches"] is True
        if not runtime_ok:
            change["state"] = "applied_pending_runtime"
        save_record(state_path, change)
        return {"ok": runtime_ok, "settings_written": True, "visual_verified": False, "scope_complete": not incomplete,
                "design_complete": change.get("icon_runtime", {}).get("design_complete"),
                "dry_run": False, "change": change, "warnings": warnings,
                "note": "区分配置读回、图标/光标按名加载和视觉效果；未通过运行时验证时保留恢复点。"}
    except Exception as exc:
        change["error"] = str(exc)
        recover_change(change, backend, state_path, True)
        return {"ok": False, "dry_run": False, "change": change}


@package_locked
def rollback_package(change_id, execute=False, components_only=None):
    if not re.fullmatch(r"change-[a-f0-9]{16}", change_id):
        raise ThemeError("change ID 格式无效")
    state_root = Path(os.environ.get("XDG_STATE_HOME") or str(user_root() / ".local/state")) / "uos-theme-personalize" / "packages"
    matches = list(state_root.glob("*.active.json")) + [state_root / (change_id + ".json")]
    path = None
    for candidate in matches:
        if candidate.is_file() and not candidate.is_symlink() and json.loads(candidate.read_text(encoding="utf-8")).get("id") == change_id:
            path = candidate
            break
    if path is None:
        raise ThemeError("没有找到该主题包变更记录")
    change = json.loads(path.read_text(encoding="utf-8"))
    if change.get("state") == "rolled_back":
        return {"ok": True, "dry_run": not execute, "change_id": change_id, "state": "rolled_back", "note": "已经恢复，不会重复覆盖设置。"}
    if change.get("session") != identity():
        raise ThemeError("变更属于其他登录会话，请在原会话恢复")
    backend = DDE().connect() if change.get("backend") else None
    if backend and backend.endpoint() != change["backend"]:
        raise ThemeError("DDE 接口已改变，请在原环境恢复")
    if execute and os.geteuid() == 0:
        raise ThemeError("请以图形登录用户恢复，不要使用 sudo 或 root")
    return recover_change(change, backend, path, execute, components_only)


def verify_package(package_id, observe_seconds=0, components_only=None):
    record = load_installed(package_id)
    verify_installed(record)
    components = record["manifest"]["components"]
    selected = set(components_only or (name for name in ("icon", "cursor") if components.get(name)))
    if selected - {"icon", "cursor"} or not selected:
        raise ThemeError("verify --components 只能选择 icon,cursor；其他组件看变更中的读回值")
    result = {"ok": True, "package_id": package_id, "visual_verified": False, "scope_complete": True}
    if record.get("desktop_integration"):
        result["desktop_integration"] = desktop_status(record)
        result["ok"] &= result["desktop_integration"]["ok"]
    backend = DDE().connect()
    if "icon" in selected:
        report = inspect_installed_icons(record)
        report["dde_value"] = backend.read("icon_theme")
        report["dde_matches"] = report["dde_value"] == package_id
        result["icon_runtime"] = report
        result["ok"] &= report.get("scope_complete", False) and report["dde_matches"]
        result["design_complete"] = report.get("design_complete", False)
        result["scope_complete"] &= report.get("scope_complete", False)
    if "cursor" in selected:
        cursor = components.get("cursor") or {}
        if not cursor.get("compiled"):
            result.update({"ok": False, "scope_complete": False, "cursor_runtime": {"error": "光标未编译"}})
        else:
            report = CursorRuntime().inspect(package_id, user_root() / ".icons" / package_id, observe_seconds, backend)
            result["cursor_runtime"] = report
            result["ok"] &= report["configuration_consistent"] and report["named_lookup_matches"] is True
    return result


def parser():
    result = argparse.ArgumentParser(description="生成和应用用户级 UOS/Deepin 主题包")
    sub = result.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="检查光标编译器和自定义屏保能力，不修改设置")
    create = sub.add_parser("create", help="根据设计规范生成图标、光标源文件、屏保图片包")
    create.add_argument("--spec", required=True)
    create.add_argument("--output", required=True)
    create.add_argument("--force", action="store_true")
    create.add_argument("--summary", action="store_true", help="省略大量文件/资源清单，完整信息保存在包内")
    valid = sub.add_parser("validate", help="校验主题包")
    valid.add_argument("--package", required=True)
    valid.add_argument("--summary", action="store_true")
    preview = sub.add_parser("design-preview", help="从真实素材生成明暗背景与多尺寸预览，不安装或切换")
    preview.add_argument("--package", required=True)
    preview.add_argument("--output", required=True, help="包外 .svg 或 .png 路径")
    preview.add_argument("--names", help="逗号分隔的包内图标名称，最多 32 个")
    preview.add_argument("--force", action="store_true")
    inventory = sub.add_parser("icon-inventory", help="只读扫描应用和可选基准主题，保存图标目标清单")
    inventory.add_argument("--scope", choices=("applications", "desktop", "base-theme"), default="desktop")
    inventory.add_argument("--base-theme", default="bloom")
    inventory.add_argument("--app-dir", action="append", help="按优先级指定应用目录，可重复；默认遵循 XDG")
    inventory.add_argument("--output", required=True)
    audit = sub.add_parser("icon-audit", help="只读检查图标实际查找来源、覆盖例外和应用变化")
    source = audit.add_mutually_exclusive_group(required=True)
    source.add_argument("--package")
    source.add_argument("--id")
    audit.add_argument("--output", help="将完整逐名称/尺寸查找结果写入 JSON；终端只输出摘要")
    install = sub.add_parser("install", help="预览或安装到当前用户目录")
    install.add_argument("--package", required=True)
    install.add_argument("--execute", action="store_true")
    install.add_argument("--summary", action="store_true")
    install.add_argument("--no-desktop-integration", action="store_true", help="不注册控制中心主题或导入壁纸；图标/光标仍会安装，适合离线测试或手工完整主题引用资源")
    integrated = sub.add_parser("desktop-status", help="检查控制中心整体主题、图标、光标和原生壁纸列表可见性")
    integrated.add_argument("--id", required=True)
    activate = sub.add_parser("activate", help="预览或激活已安装主题包")
    activate.add_argument("--id", required=True)
    activate.add_argument("--execute", action="store_true")
    activate.add_argument("--screensaver", action="store_true")
    activate.add_argument("--components", help="只激活指定组件，逗号分隔：icon,cursor,wallpaper,accent")
    activate.add_argument("--cursor-sync", action="store_true", help="预览并记录同步已有 DDE 光标键和 X11 资源，不改其他配置")
    activate.add_argument("--launcher-overrides", action="store_true", help="将绝对路径 Icon 替换为命名图标，用户级覆盖纳入回滚")
    activate.add_argument("--allow-partial-icons", action="store_true", help="明确接受图标例外；结果仍报告 scope_complete=false")
    activate.add_argument("--summary", action="store_true")
    verify = sub.add_parser("verify", help="只读检查图标和光标的实际查找，不能代替视觉观察")
    verify.add_argument("--id", required=True)
    verify.add_argument("--observe-seconds", type=float, default=0)
    verify.add_argument("--components", help="只验证指定组件：icon,cursor")
    verify.add_argument("--summary", action="store_true")
    rollback = sub.add_parser("rollback", help="预览或恢复主题包变更")
    rollback.add_argument("--change-id", required=True)
    rollback.add_argument("--execute", action="store_true")
    rollback.add_argument("--components", help="只恢复选定组件：icon,cursor,wallpaper,accent,screensaver；省略恢复全部")
    uninstall = sub.add_parser("uninstall", help="预览或删除用户目录中的未激活主题包")
    uninstall.add_argument("--id", required=True)
    uninstall.add_argument("--execute", action="store_true")
    return result


def main():
    args = parser().parse_args()
    try:
        if args.command == "doctor":
            dependencies = {name: shutil.which(name) for name in ("rsvg-convert", "xcursorgen", "dde-dconfig", "deepin-screensaver")}
            try:
                screensaver = ScreenSaver().inspect()
            except ThemeError as exc:
                screensaver = {"available": False, "error": str(exc)}
            try:
                native_wallpaper = NativeWallpaper().call("probe")
            except ThemeError as exc:
                native_wallpaper = {"ok": False, "error": str(exc)}
            result = {"ok": True, "dependencies": dependencies, "cursor_compile_ready": bool(dependencies["rsvg-convert"]),
                      "cursor_compiler": "xcursorgen" if dependencies["xcursorgen"] else "builtin", "screensaver": screensaver,
                      "native_wallpaper": native_wallpaper, "qt_lookup_tools": {name: shutil.which(name) for name in ("g++", "pkg-config")}}
        elif args.command == "create":
            spec = json.loads(Path(args.spec).expanduser().read_text(encoding="utf-8"))
            result = create_package(spec, args.output, args.force)
        elif args.command == "validate":
            result = validate_package(args.package)
        elif args.command == "design-preview":
            from design_preview import sheet
            manifest = validate_package(args.package)["manifest"]
            result = sheet(args.package, manifest, args.output, args.names.split(",") if args.names else None, args.force)
        elif args.command == "icon-inventory":
            value = icon_inventory(args.scope, args.app_dir, args.base_theme)
            output = Path(args.output).expanduser().absolute()
            write_json(output, value)
            result = {"ok": not value["errors"], "output": str(output), "scope": value["scope"],
                      "applications": len(value["entries"]), "target_names": len(value["targets"]),
                      "exception_count": len(value["exceptions"]), "exceptions_sample": value["exceptions"][:20],
                      "errors": value["errors"], "digest": value["digest"]}
        elif args.command == "icon-audit":
            if args.package:
                manifest = validate_package(args.package)["manifest"]
                report = inspect_icons(Path(args.package).expanduser().resolve(), manifest, staged=True)
            else:
                record = load_installed(args.id)
                verify_installed(record)
                report = inspect_installed_icons(record)
            result = {"ok": report.get("scope_complete", False), **report}
            if args.output:
                output = Path(args.output).expanduser().absolute()
                write_json(output, result)
                result = {key: value for key, value in result.items() if key != "rows"}
                if "qt_runtime" in result:
                    result["qt_runtime"] = {key: value for key, value in result["qt_runtime"].items() if key != "rows"}
                result["output"] = str(output)
        elif args.command == "install":
            result = install_package(args.package, args.execute, not args.no_desktop_integration)
        elif args.command == "desktop-status":
            record = load_installed(args.id)
            verify_installed(record)
            result = desktop_status(record)
        elif args.command == "activate":
            result = apply_package(args.id, args.execute, args.screensaver, args.components.split(",") if args.components else None, args.cursor_sync, args.launcher_overrides, args.allow_partial_icons)
        elif args.command == "verify":
            result = verify_package(args.id, args.observe_seconds, args.components.split(",") if args.components else None)
        elif args.command == "rollback":
            result = rollback_package(args.change_id, args.execute, args.components.split(",") if args.components else None)
        elif args.command == "uninstall":
            result = uninstall_package(args.id, args.execute)
        else:
            raise ThemeError("未知命令")
    except (ThemeError, OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        result = {"ok": False, "error": str(exc)}
    if getattr(args, "summary", False):
        def compact(value):
            if isinstance(value, dict):
                return {key: {"count": len(item)} if key in ("files", "assets", "rows") and isinstance(item, (dict, list)) else {"count": len(item), "sample": item[:20]} if key in ("generic_names", "exceptions", "pending_names", "pending") and isinstance(item, list) else compact(item) for key, item in value.items()}
            return [compact(item) for item in value] if isinstance(value, list) else value
        result = compact(result)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    sys.exit(main())
