"""Original, outlined cursor family with independent colors and editable hotspots."""
from __future__ import annotations

CURSOR_NAMES = ("left_ptr", "hand1", "text", "watch", "crosshair", "fleur", "sb_h_double_arrow",
                "sb_v_double_arrow", "bd_double_arrow", "fd_double_arrow", "not-allowed", "help", "progress", "grab", "grabbing")
ALIASES = {
    "left_ptr": ("default", "arrow", "top_left_arrow"), "hand1": ("hand2", "pointer", "pointing_hand"),
    "text": ("xterm", "ibeam"), "watch": ("wait",), "progress": ("left_ptr_watch",),
    "crosshair": ("cross",), "fleur": ("move", "size_all", "all-scroll"),
    "sb_h_double_arrow": ("ew-resize", "h_double_arrow", "size_hor"),
    "sb_v_double_arrow": ("ns-resize", "v_double_arrow", "size_ver"),
    "bd_double_arrow": ("nwse-resize", "size_fdiag", "bottom_right_corner", "top_left_corner"),
    "fd_double_arrow": ("nesw-resize", "size_bdiag", "bottom_left_corner", "top_right_corner"),
    "not-allowed": ("forbidden", "no-drop", "crossed_circle"), "help": ("question_arrow", "whats_this"),
    "grab": ("openhand",), "grabbing": ("closedhand",),
}
HOTSPOTS = {"left_ptr": (4, 3), "hand1": (14, 3), "progress": (4, 3), "help": (4, 3), "text": (16, 16)}


def hotspot(name, size, override=None):
    x, y = override or HOTSPOTS.get(name, (16, 16))
    return min(size-1, round(x*size/32)), min(size-1, round(y*size/32))


def render_cursor(name, primary, secondary, size=32, style="crafted", colors=None):
    defaults = {"fill": "#F7FAFF", "outline": "#172130", "accent": primary}
    if style == "ink":
        defaults.update(fill="#EEE8D7", outline="#161A21", accent="#BB4245")
    elif style == "neon":
        defaults.update(fill="#E4FCFF", outline="#102335", accent="#19B9CD")
    defaults.update(colors or {})
    fill, edge, accent = (defaults[key] for key in ("fill", "outline", "accent"))
    arrow = '<path d="M4 3v23l6-6 4 9 4-2-4-9h9z"/>'
    shapes = {
        "left_ptr": arrow,
        "hand1": '<path d="M12 16V5a2 2 0 0 1 4 0v9-3c0-3 4-3 4 0v3-1c0-3 4-3 4 0v3-1c0-2 4-2 4 1v6c0 5-3 8-8 8h-3c-3 0-5-2-7-5l-5-7c-2-3 1-5 3-3l4 4z"/>',
        "text": '<path d="M11 4h10M16 4v24m-5 0h10" fill="none"/>',
        "watch": '<circle cx="16" cy="16" r="10" fill="none"/>',
        "crosshair": '<path d="M16 3v10m0 6v10M3 16h10m6 0h10" fill="none"/><circle cx="16" cy="16" r="1"/>',
        "fleur": '<path d="M16 2 11 7h3v7H7v-3l-5 5 5 5v-3h7v7h-3l5 5 5-5h-3v-7h7v3l5-5-5-5v3h-7V7h3z"/>',
        "sb_h_double_arrow": '<path d="m3 16 7-6v4h12v-4l7 6-7 6v-4H10v4z"/>',
        "not-allowed": '<circle cx="16" cy="16" r="11" fill="none"/><path d="m8 8 16 16" fill="none"/>',
        "grab": '<path d="M8 17V8c0-3 4-3 4 0v7-11c0-3 4-3 4 0v11-10c0-3 4-3 4 0v10-7c0-3 4-3 4 0v14c0 6-3 8-8 8-4 0-6-2-8-5l-4-6c-2-3 1-5 3-3z"/>',
        "grabbing": '<path d="M7 13c0-3 4-3 4 0v-3c0-3 4-3 4 0v2-3c0-3 4-3 4 0v3-1c0-3 4-3 4 0v2c0-3 4-3 4 0v8c0 6-4 9-10 9-5 0-7-2-9-6l-3-6c-1-3 2-5 4-2z"/>',
        "help": arrow,
        "progress": arrow,
    }
    if name in {"sb_v_double_arrow", "bd_double_arrow", "fd_double_arrow"}:
        angle = {"sb_v_double_arrow": 90, "bd_double_arrow": 45, "fd_double_arrow": -45}[name]
        shape = f'<g transform="rotate({angle} 16 16)">{shapes["sb_h_double_arrow"]}</g>'
    else:
        shape = shapes[name]
    # A bright outer contour and dark inner contour survive both light and dark backgrounds.
    artwork = f'<g fill="{fill}" stroke="#FFFFFF" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round">{shape}</g><g fill="{fill}" stroke="{edge}" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round">{shape}</g>'
    if name == "left_ptr":
        detail = '<path d="m7 8 9 8h-5l-4 4z" stroke="none"/>' if style != "ink" else '<path d="m7 8 2 12 4-4 5-1z" stroke="none"/>'
        artwork += f'<g fill="{accent}">{detail}</g>'
    elif name == "watch":
        artwork += f'<path d="M16 6a10 10 0 0 1 10 10" stroke="{accent}" stroke-width="3" stroke-linecap="round" fill="none"/>'
    elif name == "hand1":
        artwork += f'<path d="M15 23h7" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>'
    elif name in {"progress", "help"}:
        artwork += f'<circle cx="23" cy="23" r="7" fill="{edge}" stroke="#FFFFFF" stroke-width="1.2"/>'
        if name == "progress":
            artwork += f'<path d="M23 18a5 5 0 0 1 5 5" fill="none" stroke="{accent}" stroke-width="2.5" stroke-linecap="round"/>'
        else:
            artwork += '<path d="M21 21c0-3 5-3 4 0l-2 2m0 3v.1" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 32 32">{artwork}</svg>\n'
