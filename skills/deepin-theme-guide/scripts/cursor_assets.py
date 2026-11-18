"""Bounded PNG decoder and standard raw ARGB Xcursor writer/validator."""
from __future__ import annotations

import ctypes as C
import ctypes.util
from pathlib import Path
import struct
import zlib

from dde_backend import ThemeError

IMAGE_TYPE = 0xFFFD0002


def decode_png(path):
    data = Path(path).read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) > 4 * 1024 * 1024:
        raise ThemeError("光标 PNG 文件头或大小无效")
    offset, header, compressed, palette, alpha = 8, None, bytearray(), None, b""
    ended = False
    while offset + 12 <= len(data):
        length = struct.unpack_from(">I", data, offset)[0]
        tag = data[offset + 4:offset + 8]
        block = data[offset + 8:offset + 8 + length]
        if len(block) != length or offset + 12 + length > len(data):
            raise ThemeError("PNG 块越界")
        crc = struct.unpack_from(">I", data, offset + 8 + length)[0]
        if zlib.crc32(tag + block) & 0xFFFFFFFF != crc:
            raise ThemeError("PNG CRC 校验失败")
        if tag == b"IHDR":
            if header is not None or offset != 8 or length != 13:
                raise ThemeError("PNG IHDR 无效")
            header = struct.unpack(">IIBBBBB", block)
        elif tag == b"IDAT":
            compressed.extend(block)
        elif tag == b"PLTE":
            palette = block
        elif tag == b"tRNS":
            alpha = block
        elif tag == b"IEND":
            ended = True
            break
        elif tag not in (b"sRGB", b"gAMA", b"cHRM", b"pHYs", b"bKGD", b"tEXt", b"iTXt", b"zTXt", b"tIME") and not tag[0] & 32:
            raise ThemeError("PNG 包含未知关键块")
        offset += length + 12
    if not header or not ended:
        raise ThemeError("PNG 不完整")
    width, height, depth, color_type, compression, filtering, interlace = header
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(color_type)
    if not channels or depth != 8 or compression or filtering or interlace or not (1 <= width <= 128 and 1 <= height <= 128):
        raise ThemeError("内置光标编译仅接受不交错的 8 位 PNG，尺寸不超过 128")
    if alpha and color_type != 3:
        raise ThemeError("带 tRNS 的灰度/RGB PNG 请先转为 RGBA PNG")
    stride = width * channels
    expected = height * (stride + 1)
    decoder = zlib.decompressobj()
    try:
        raw = decoder.decompress(bytes(compressed), expected + 1)
    except zlib.error as exc:
        raise ThemeError("PNG 压缩数据无效") from exc
    if len(raw) != expected or not decoder.eof or decoder.unconsumed_tail or decoder.unused_data:
        raise ThemeError("PNG 解压长度不匹配")
    rows, previous = [], bytearray(stride)
    for y in range(height):
        start = y * (stride + 1)
        method = raw[start]
        row = bytearray(raw[start + 1:start + stride + 1])
        if method > 4:
            raise ThemeError("PNG 行过滤器无效")
        for x in range(stride):
            left = row[x - channels] if x >= channels else 0
            up = previous[x]
            corner = previous[x - channels] if x >= channels else 0
            if method == 1:
                predictor = left
            elif method == 2:
                predictor = up
            elif method == 3:
                predictor = (left + up) // 2
            elif method == 4:
                p = left + up - corner
                choices = (abs(p - left), abs(p - up), abs(p - corner))
                predictor = (left, up, corner)[choices.index(min(choices))]
            else:
                predictor = 0
            row[x] = (row[x] + predictor) & 255
        rows.append(row)
        previous = row
    pixels = []
    for row in rows:
        for x in range(0, stride, channels):
            sample = row[x:x + channels]
            if color_type == 6:
                r, g, b, a = sample
            elif color_type == 2:
                r, g, b = sample
                a = 255
            elif color_type in (0, 4):
                r = g = b = sample[0]
                a = sample[1] if color_type == 4 else 255
            else:
                index = sample[0]
                if not palette or index * 3 + 3 > len(palette):
                    raise ThemeError("PNG 调色板越界")
                r, g, b = palette[index * 3:index * 3 + 3]
                a = alpha[index] if index < len(alpha) else 255
            pixels.append((a << 24) | (((r * a + 127) // 255) << 16) | (((g * a + 127) // 255) << 8) | ((b * a + 127) // 255))
    return width, height, pixels


def write_xcursor(path, frames):
    chunks, toc = [], []
    offset = 16 + len(frames) * 12
    if not frames or len(frames) > 16:
        raise ThemeError("光标尺寸数量无效")
    for frame in frames:
        width, height, pixels = decode_png(frame["png"])
        size, x, y = frame["size"], frame["xhot"], frame["yhot"]
        if not (0 <= x < width and 0 <= y < height):
            raise ThemeError("光标热点越界")
        chunk = struct.pack("<9I", 36, IMAGE_TYPE, size, 1, width, height, x, y, 0)
        chunk += struct.pack("<%dI" % len(pixels), *pixels)
        toc.append(struct.pack("<3I", IMAGE_TYPE, size, offset))
        chunks.append(chunk)
        offset += len(chunk)
    Path(path).write_bytes(struct.pack("<4I", 0x72756358, 16, 0x10000, len(toc)) + b"".join(toc + chunks))


def validate_xcursor(path):
    data = Path(path).read_bytes()
    if len(data) < 16 or len(data) > 4 * 1024 * 1024:
        raise ThemeError("Xcursor 文件大小无效")
    magic, header, version, count = struct.unpack_from("<4I", data)
    if magic != 0x72756358 or header != 16 or version != 0x10000 or not 1 <= count <= 16 or 16 + 12 * count > len(data):
        raise ThemeError("Xcursor 文件头或目录无效")
    frames, end = [], header + count * 12
    for i in range(count):
        typ, size, offset = struct.unpack_from("<3I", data, header + i * 12)
        if typ != IMAGE_TYPE or offset < end or offset + 36 > len(data):
            raise ThemeError("Xcursor 图像块无效；必须是标准 ARGB 图像块")
        hlen, ctyp, csize, ver, width, height, x, y, delay = struct.unpack_from("<9I", data, offset)
        if (hlen, ctyp, csize, ver) != (36, IMAGE_TYPE, size, 1) or not (1 <= width <= 128 and 1 <= height <= 128 and x < width and y < height):
            raise ThemeError("Xcursor 尺寸、热点或块版本无效")
        end = offset + 36 + width * height * 4
        if end > len(data):
            raise ThemeError("Xcursor 像素数据越界")
        frames.append({"size": size, "width": width, "height": height, "xhot": x, "yhot": y, "delay": delay})
    return frames


class Image(C.Structure):
    _fields_ = [(key, C.c_uint) for key in ("version", "size", "width", "height", "xhot", "yhot", "delay")] + [("pixels", C.POINTER(C.c_uint32))]


class Images(C.Structure):
    _fields_ = [("nimage", C.c_int), ("images", C.POINTER(C.POINTER(Image))), ("name", C.c_char_p)]


def load_images(path=None, theme=None, name=None, size=32):
    """Read-only loader proof. A theme lookup alone can silently fall back."""
    library = C.util.find_library("Xcursor")
    if not library:
        return {"available": False, "reason": "未找到 libXcursor"}
    try:
        lib = C.CDLL(library)
        lib.XcursorFilenameLoadImages.argtypes = [C.c_char_p, C.c_int]
        lib.XcursorFilenameLoadImages.restype = C.POINTER(Images)
        lib.XcursorLibraryLoadImages.argtypes = [C.c_char_p, C.c_char_p, C.c_int]
        lib.XcursorLibraryLoadImages.restype = C.POINTER(Images)
        lib.XcursorImagesDestroy.argtypes = [C.POINTER(Images)]
        ptr = lib.XcursorFilenameLoadImages(str(path).encode(), size) if path else lib.XcursorLibraryLoadImages(name.encode(), theme.encode(), size)
        if not ptr:
            return {"available": True, "loaded": False}
        try:
            if not 1 <= ptr.contents.nimage <= 16:
                raise ThemeError("libXcursor 返回的帧数无效")
            frames = []
            for i in range(ptr.contents.nimage):
                image = ptr.contents.images[i].contents
                if not 1 <= image.width <= 128 or not 1 <= image.height <= 128:
                    raise ThemeError("libXcursor 返回的尺寸无效")
                pixels = [image.pixels[j] for j in range(image.width * image.height)]
                import hashlib
                frames.append({"size": image.size, "width": image.width, "height": image.height, "xhot": image.xhot, "yhot": image.yhot,
                               "pixels_sha256": hashlib.sha256(struct.pack("<%dI" % len(pixels), *pixels)).hexdigest()})
            return {"available": True, "loaded": True, "frames": frames}
        finally:
            lib.XcursorImagesDestroy(ptr)
    except (OSError, AttributeError) as exc:
        return {"available": False, "reason": str(exc)}
