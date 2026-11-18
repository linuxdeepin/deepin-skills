#!/usr/bin/env python3
"""Fetch a real desktop wallpaper for the current screen and record provenance.

The skill does not draw wallpapers. This helper reports the user's current
resolution, downloads a candidate over HTTPS, and refuses anything that would
have to be upscaled (the image must cover the screen's width and height).
Aspect ratio is advisory: the deviation is reported so the caller can prefer a
closer crop, but a usable image is never rejected for its ratio alone. Every
accepted image gets a `.source.json` sidecar with the original URL and checksum,
plus optional license and author metadata; unknown metadata stays null and does
not block downloads. `theme_pack.py create` copies both into the theme package
so the provenance survives installation.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from dde_backend import ThemeError, image_dimensions, image_info

MAX_BYTES = 64 * 1024 * 1024
TIMEOUT = 30
ASPECT_TOLERANCE = 0.02
FORMAT_VERSION = 1
CONTENT_SUFFIXES = {"image/png": ".png", "image/jpeg": ".jpg", "image/jpg": ".jpg",
                    "image/webp": ".webp", "image/bmp": ".bmp"}
SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
USER_AGENT = "uos-theme-personalize/1.0 (+local wallpaper fetch)"


def parse_xrandr(text):
    primary = fallback = None
    for line in text.splitlines():
        match = re.match(r"^(\S+) connected(?P<primary> primary)? (?P<width>\d+)x(?P<height>\d+)\+", line)
        if not match:
            continue
        entry = {"width": int(match.group("width")), "height": int(match.group("height")),
                 "output": match.group(1)}
        if match.group("primary") and primary is None:
            primary = entry
        elif fallback is None:
            fallback = entry
    return primary or fallback


def parse_wlr_randr(text):
    for block in re.split(r"(?m)^(?=\S)", text):
        header = re.match(r"^(\S+)", block)
        if not header or not re.search(r"(?m)^\s+Modes:", block):
            continue
        mode = re.search(r"(?m)^\s+(\d+)x(\d+) px.*\bcurrent\b", block)
        if mode:
            return {"width": int(mode.group(1)), "height": int(mode.group(2)), "output": header.group(1)}
    return None


def _run(argv):
    try:
        result = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", timeout=5,
                                env={**os.environ, "LC_ALL": "C"})
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout if result.returncode == 0 else None


def detect_screen(width=None, height=None):
    """Return the target screen size; explicit dimensions win over detection."""
    if width is not None or height is not None:
        if type(width) is not int or type(height) is not int or width < 320 or height < 240:
            raise ThemeError("--width/--height 必须是有效的像素整数（宽 >= 320，高 >= 240）")
        return {"width": width, "height": height, "source": "argument", "output": None}
    override = os.environ.get("UOS_THEME_SCREEN")
    if override:
        match = re.fullmatch(r"(\d{3,5})x(\d{3,5})", override.strip())
        if not match:
            raise ThemeError("UOS_THEME_SCREEN 必须是 WIDTHxHEIGHT")
        return {"width": int(match.group(1)), "height": int(match.group(2)),
                "source": "environment", "output": None}
    for argv, parser, name in ((("xrandr", "--current"), parse_xrandr, "xrandr"),
                               (("wlr-randr",), parse_wlr_randr, "wlr-randr")):
        if shutil.which(argv[0]) is None:
            continue
        text = _run(list(argv))
        if not text:
            continue
        found = parser(text)
        if found:
            return {**found, "source": name}
    dimensions = _run(["xdpyinfo"]) if shutil.which("xdpyinfo") else None
    if dimensions:
        match = re.search(r"dimensions:\s+(\d+)x(\d+) pixels", dimensions)
        if match:
            return {"width": int(match.group(1)), "height": int(match.group(2)),
                    "source": "xdpyinfo", "output": None}
    raise ThemeError("无法读取当前屏幕分辨率；请先用 xrandr 确认，并显式传入 --width/--height")


def validate_image(path, screen, tolerance=ASPECT_TOLERANCE):
    """Require at least the screen's pixels; report aspect deviation separately.

    An image whose width and height both cover the screen can always be used
    without upscaling. The aspect ratio only decides how much DDE crops or
    letterboxes, so it is reported for the caller's judgement instead of being
    rejected: pick the closest ratio available, then document the deviation.
    """
    info = dict(image_info(str(path)))
    if not info["width"] or not info["height"]:
        raise ThemeError("无法解析图片尺寸；请换用标准的 PNG/JPEG/WebP/BMP 壁纸")
    if info["width"] < screen["width"] or info["height"] < screen["height"]:
        raise ThemeError("壁纸 %dx%d 小于屏幕 %dx%d，会需要放大；请换用等于或高于屏幕分辨率的素材"
                         % (info["width"], info["height"], screen["width"], screen["height"]))
    target = screen["width"] / screen["height"]
    actual = info["width"] / info["height"]
    delta = abs(actual - target) / target
    info["aspect"] = {"ratio": round(actual, 4), "screen_ratio": round(target, 4),
                      "delta": round(delta, 4), "close": delta <= tolerance}
    if not info["aspect"]["close"]:
        info["warnings"] = ["壁纸宽高比 %.3f 与屏幕 %.3f 相差 %.1f%%，缩放填充会裁切或留边；尽量换更接近屏幕比例的素材"
                            % (actual, target, delta * 100)]
    return info


def sidecar_path(image):
    return Path(str(image) + ".source.json")


def load_provenance(image, info=None):
    """Read and verify the fetch sidecar; None when the image has none."""
    path = sidecar_path(image)
    if not path.is_file():
        return None
    if path.is_symlink():
        raise ThemeError("来源记录不能是符号链接：%s" % path)
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ThemeError("来源记录无法解析：%s" % exc) from exc
    if not isinstance(document, dict) or document.get("format") != "uos-wallpaper-source" or document.get("version") != FORMAT_VERSION:
        raise ThemeError("来源记录格式不支持：%s" % path)
    info = info or image_info(str(image))
    if document.get("sha256") != info["sha256"]:
        raise ThemeError("壁纸与来源记录的摘要不一致，请重新获取：%s" % path)
    if document.get("width") and (document.get("width"), document.get("height")) != (info["width"], info["height"]):
        raise ThemeError("壁纸与来源记录的尺寸不一致，请重新获取：%s" % path)
    return document


def _parse_url(value, field="url"):
    if not isinstance(value, str) or not value.strip() or len(value) > 2048:
        raise ThemeError("%s 无效" % field)
    parsed = urllib.parse.urlsplit(value.strip())
    if parsed.username or parsed.password:
        raise ThemeError("%s 不能包含凭据" % field)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ThemeError("%s 必须使用 https" % field)
    return value.strip()


def _suffix_for(content_type, url):
    kind = (content_type or "").split(";")[0].strip().lower()
    if kind in CONTENT_SUFFIXES:
        return CONTENT_SUFFIXES[kind]
    suffix = Path(urllib.parse.urlsplit(url).path).suffix.lower()
    return ".jpg" if suffix == ".jpeg" else suffix if suffix in SUFFIXES else None


def _probe(url):
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return {"ok": True, "final_url": response.geturl(),
                    "content_type": response.headers.get("Content-Type"),
                    "content_length": response.headers.get("Content-Length")}
    except (urllib.error.URLError, ValueError, OSError) as exc:
        return {"ok": False, "error": str(exc)[:300]}


def _download(url, destination):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "image/*"})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        final = response.geturl()
        if urllib.parse.urlsplit(final).scheme != "https":
            raise ThemeError("下载被重定向到非 https 地址，拒绝保存")
        content_type = response.headers.get("Content-Type")
        length = response.headers.get("Content-Length")
        if length and length.isdigit() and int(length) > MAX_BYTES:
            raise ThemeError("图片超过 %d MiB 上限" % (MAX_BYTES // (1024 * 1024)))
        if content_type and not content_type.lower().startswith("image/"):
            raise ThemeError("返回内容不是图片（%s）；可能下载到了网页" % content_type)
        written = 0
        with Path(destination).open("wb") as handle:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                written += len(block)
                if written > MAX_BYTES:
                    raise ThemeError("图片超过 %d MiB 上限" % (MAX_BYTES // (1024 * 1024)))
                handle.write(block)
    return {"final_url": final, "content_type": content_type, "bytes": written}


def fetch(url, output, width=None, height=None, license=None, author=None, source_page=None,
          force=False, execute=False):
    url = _parse_url(url)
    if source_page is not None:
        source_page = _parse_url(source_page, "source-page")
    screen = detect_screen(width, height)
    output = Path(output).expanduser()
    if not output.is_absolute():
        raise ThemeError("--output 必须是绝对路径")
    if output.is_symlink() or output.exists() and not force:
        raise ThemeError("输出已存在或是符号链接；确认替换请加 --force：%s" % output)
    if output.suffix.lower() not in SUFFIXES:
        raise ThemeError("输出扩展名必须是 .png/.jpg/.jpeg/.webp/.bmp")
    if license is not None and (not isinstance(license, str) or len(license) > 200 or any(ord(c) < 32 for c in license)):
        raise ThemeError("--license 必须是 200 字符以内的单行文本")
    license = (license.strip() or None) if license is not None else None
    result = {"ok": True, "dry_run": not execute, "screen": screen, "url": url, "output": str(output)}
    if not execute:
        result["probe"] = _probe(url)
        result["checks"] = ["https", "content-type: image/*", "<= %d MiB" % (MAX_BYTES // (1024 * 1024)),
                            "width >= %d" % screen["width"], "height >= %d" % screen["height"],
                            "aspect close to %.2f (advisory, %.0f%% tolerance)"
                            % (screen["width"] / screen["height"], ASPECT_TOLERANCE * 100)]
        result["note"] = ("预览只做 HEAD 探测，不保存文件；--execute 才下载。宽高必须覆盖屏幕，"
                          "宽高比只做提示，不会阻止下载。")
        sidecar = sidecar_path(output)
        result["sidecar"] = {"path": str(sidecar), "exists": sidecar.exists()}
        return result
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".wallpaper-", dir=str(output.parent))
    os.close(fd)
    temporary = Path(temporary)
    try:
        try:
            download = _download(url, temporary)
        except (urllib.error.URLError, ValueError, OSError) as exc:
            raise ThemeError("下载失败：%s" % str(exc)[:300]) from exc
        suffix = _suffix_for(download["content_type"], url)
        if suffix is None:
            raise ThemeError("无法从内容类型或 URL 判断图片格式")
        if output.suffix.lower() != suffix:
            raise ThemeError("输出扩展名应为 %s（实际内容 %s）" % (suffix, download["content_type"] or "未知"))
        info = validate_image(temporary, screen)
        os.chmod(temporary, 0o644)
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            temporary.unlink()
    document = {"format": "uos-wallpaper-source", "version": FORMAT_VERSION,
                "url": url, "final_url": download["final_url"], "content_type": download["content_type"],
                "author": author, "license": license, "source_page": source_page,
                "fetched_at": int(time.time()), "screen": {"width": screen["width"], "height": screen["height"]},
                "width": info["width"], "height": info["height"], "bytes": info["bytes"], "sha256": info["sha256"]}
    sidecar = sidecar_path(output)
    fd, source_temp = tempfile.mkstemp(prefix=".wallpaper-source-", dir=str(output.parent))
    source_temp = Path(source_temp)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(document, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(source_temp, 0o644)
        os.replace(source_temp, sidecar)
    finally:
        if source_temp.exists():
            source_temp.unlink()
    result.update({"image": info, "provenance": document, "sidecar": str(sidecar),
                   "warnings": info.get("warnings", []),
                   "note": "宽高已覆盖屏幕；宽高比仅提示裁切幅度。作者和许可仅作可选来源记录，未知可留空；来源记录会随主题包一起安装。"})
    return result


def check(path, width=None, height=None):
    screen = detect_screen(width, height)
    info = validate_image(path, screen)
    return {"ok": True, "screen": screen, "image": info, "provenance": load_provenance(path, info)}


def parser():
    top = argparse.ArgumentParser(description="为当前屏幕获取网络壁纸并记录来源")
    sub = top.add_subparsers(dest="command", required=True)
    screen = sub.add_parser("screen", help="只读报告当前屏幕分辨率")
    screen.add_argument("--width", type=int)
    screen.add_argument("--height", type=int)
    check_parser = sub.add_parser("check", help="只读校验本地图片是否适配当前屏幕")
    check_parser.add_argument("--path", required=True)
    check_parser.add_argument("--width", type=int)
    check_parser.add_argument("--height", type=int)
    fetch_parser = sub.add_parser("fetch", help="下载并校验壁纸，写入来源记录")
    fetch_parser.add_argument("--url", required=True)
    fetch_parser.add_argument("--output", required=True)
    fetch_parser.add_argument("--width", type=int)
    fetch_parser.add_argument("--height", type=int)
    fetch_parser.add_argument("--license", help="可选的许可记录；未知可省略，不阻止下载")
    fetch_parser.add_argument("--author")
    fetch_parser.add_argument("--source-page")
    fetch_parser.add_argument("--force", action="store_true")
    fetch_parser.add_argument("--execute", action="store_true")
    return top


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "screen":
            value = {"ok": True, "screen": detect_screen(args.width, args.height)}
        elif args.command == "check":
            value = check(args.path, args.width, args.height)
        else:
            value = fetch(args.url, args.output, args.width, args.height, args.license,
                          args.author, args.source_page, args.force, args.execute)
    except (ThemeError, OSError) as exc:
        value = {"ok": False, "error": str(exc)}
    print(json.dumps(value, ensure_ascii=False, indent=2))
    return 0 if value.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
