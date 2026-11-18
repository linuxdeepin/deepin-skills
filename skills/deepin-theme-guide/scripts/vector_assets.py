"""Bounded static SVG validation shared by icons, cursors and preserved base assets."""
import re
from pathlib import Path
import xml.etree.ElementTree as ET

from dde_backend import ThemeError

ELEMENTS = {"svg", "g", "path", "rect", "circle", "ellipse", "line", "polyline", "polygon", "defs", "text", "title", "desc",
            "linearGradient", "radialGradient", "stop", "clipPath", "mask", "use", "filter", "feGaussianBlur", "feMerge", "feMergeNode",
            "feOffset", "feFlood", "feComposite", "feBlend", "feColorMatrix"}


def validate_svg(path):
    data = Path(path).read_bytes()
    if len(data) > 1024*1024 or b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ThemeError("SVG 过大或含文档实体")
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ThemeError("SVG 无法解析：%s" % path) from exc
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        raise ThemeError("根节点不是 SVG")
    for index, element in enumerate(root.iter()):
        if index > 10000 or element.tag.split("}")[-1] not in ELEMENTS:
            raise ThemeError("SVG 包含不受支持的元素或过多节点")
        for key, value in element.attrib.items():
            key = key.split("}")[-1].lower()
            if key.startswith("on") or (key == "href" and not re.fullmatch(r"#[A-Za-z0-9_.:-]+", value)):
                raise ThemeError("SVG 包含外部引用或事件属性")
            without_local = re.sub(r"url\(\s*#[A-Za-z0-9_.:-]+\s*\)", "", value, flags=re.I)
            if re.search(r"url\s*\(|@import|expression\s*\(", without_local, re.I):
                raise ThemeError("SVG 包含外部资源或动态表达式")
    return root
