"""Original vector artwork and semantic states; no network, fonts or image model required."""
from __future__ import annotations

import re
from xml.sax.saxutils import escape

STYLES = {"crafted", "ink", "neon", "outline", "solid"}
EXTRA_TEMPLATES = {"calculator", "calendar", "chat", "mail", "camera", "clock", "archive", "code", "game", "contacts", "spreadsheet", "presentation", "refresh", "save", "cut", "pause", "stop", "undo", "redo", "question", "sun", "location", "scan", "paint", "language", "phone", "optical"}

# Coordinates use a 32-unit optical grid. App surfaces use a separate 64-unit grid.
GLYPHS = {
    "folder": '<path d="M3 10V7a2 2 0 0 1 2-2h8l3 4h11a2 2 0 0 1 2 2v2H3z" fill="currentColor" opacity=".55" stroke="none"/><path d="M3 12h26l-3 14H6z" fill="currentColor" stroke="none"/>',
    "document": '<path d="M8 3h11l6 6v20H8z"/><path d="M19 3v7h6M12 16h9m-9 5h9"/>',
    "browser": '<circle cx="16" cy="16" r="12"/><path d="M4 16h24M16 4c-8 7-8 17 0 24 8-7 8-17 0-24"/>',
    "terminal": '<rect x="3" y="5" width="26" height="23" rx="4"/><path d="m9 12 5 4-5 4m9 1h6"/>',
    "settings": '<path d="m13 3-1 4-4 2-4-1-2 5 3 3v4l-2 3 4 4 4-1 4 2 1 3h5l1-4 4-2 4 1 2-5-3-3v-4l2-3-4-4-4 1-4-2-1-3z" transform="translate(1 -1) scale(.94)"/><circle cx="16" cy="16" r="5"/>',
    "home": '<path d="m3 14 13-10 13 10M6 12v16h20V12M13 28V18h7v10"/>',
    "trash": '<path d="M8 9h16l-1 19H9zM5 8h22M12 8V4h8v4M13 13v10m6-10v10"/>',
    "download": '<path d="M16 3v18m-7-7 7 7 7-7M5 24v5h22v-5"/>',
    "warning": '<path d="M16 3 30 28H2z"/><path d="M16 12v7m0 4v1"/>',
    "info": '<circle cx="16" cy="16" r="12"/><path d="M16 14v10m0-16v1"/>',
    "music": '<path d="M13 23V8l13-3v16M13 12l13-3"/><circle cx="8.5" cy="24" r="4.5" fill="currentColor" stroke="none"/><circle cx="21.5" cy="22" r="4.5" fill="currentColor" stroke="none"/>',
    "image": '<rect x="3" y="4" width="26" height="24" rx="4"/><circle cx="11" cy="12" r="3"/><path d="m5 25 8-8 5 5 5-8 5 9"/>',
    "computer": '<rect x="3" y="4" width="26" height="19" rx="3"/><path d="M16 23v6M9 29h14"/>',
    "monitor": '<rect x="3" y="4" width="26" height="24" rx="4"/><path d="M6 19h5l4-9 5 13 3-6h4"/>',
    "store": '<path d="M5 11h22v17H5zM3 11l4-7h18l4 7M11 16c0 7 10 7 10 0"/>',
    "drive": '<path d="m4 13 4-8h16l4 8v14H4zM4 18h24"/><path d="M21 23h3"/>',
    "network": '<path d="M3 11c7-8 19-8 26 0M7 17c5-6 13-6 18 0m-14 6c3-3 7-3 10 0"/><circle cx="16" cy="28" r="1.5" fill="currentColor" stroke="none"/>',
    "volume": '<path d="M3 12h6l8-7v22l-8-7H3zM22 10c6 3 6 9 0 12M21 14c2 1 2 3 0 4"/>',
    "security": '<path d="m16 3 11 5v9c0 7-7 11-11 13C12 28 5 24 5 17V8z"/><path d="m10 16 4 4 8-9"/>',
    "video": '<rect x="3" y="4" width="26" height="24" rx="5"/><path d="m13 10 9 6-9 6z" fill="currentColor" stroke="none"/>',
    "printer": '<path d="M8 11V3h16v8M8 23H3V11h26v12h-5M8 18h16v11H8zM12 23h8"/>',
    "keyboard": '<rect x="2" y="7" width="28" height="20" rx="4"/><path d="M7 12h1m5 0h1m5 0h1m5 0h1M7 17h1m5 0h1m5 0h1m5 0h1M9 22h14"/>',
    "mouse": '<rect x="8" y="2" width="16" height="28" rx="8"/><path d="M16 3v8M8 13h16"/>',
    "assistant": '<path d="M7 8h18v19H7zM16 3v5M3 14v8m26-8v8M12 21h8"/><circle cx="12" cy="14" r="1"/><circle cx="20" cy="14" r="1"/>',
    "copy": '<rect x="10" y="10" width="18" height="19" rx="3"/><path d="M7 22H3V3h18v4"/>',
    "search": '<circle cx="13" cy="13" r="9"/><path d="m20 20 9 9"/>',
    "close": '<path d="m7 7 18 18M25 7 7 25"/>',
    "play": '<path d="m9 4 20 12L9 28z" fill="currentColor" stroke="none"/>',
    "pause": '<path d="M10 6v20M22 6v20" stroke-width="6"/>',
    "stop": '<rect x="6" y="6" width="20" height="20" rx="2" fill="currentColor" stroke="none"/>',
    "calculator": '<rect x="6" y="2" width="20" height="28" rx="4"/><path d="M10 7h12v6H10zM11 19h1m8 0h1m-10 6h1m8 0h1"/>',
    "calendar": '<rect x="3" y="5" width="26" height="24" rx="4"/><path d="M3 12h26M10 2v6m12-6v6M9 18h3m8 0h3m-14 6h3m8 0h3"/>',
    "chat": '<path d="M28 15c0 7-6 11-13 11H6l-4 4 2-10C-2 8 9 2 17 4c6 1 11 5 11 11z"/><path d="M9 15h.1m7 0h.1m7 0h.1"/>',
    "mail": '<rect x="3" y="6" width="26" height="21" rx="4"/><path d="m4 8 12 10L28 8M4 25l8-9m16 9-8-9"/>',
    "camera": '<path d="M3 9h6l3-5h8l3 5h6v18H3z"/><circle cx="16" cy="18" r="6"/>',
    "clock": '<circle cx="16" cy="16" r="13"/><path d="M16 7v10l7 4"/>',
    "archive": '<rect x="4" y="5" width="24" height="24" rx="3"/><path d="M3 4h26v6H3zM13 15h6v5h-6z"/>',
    "code": '<path d="m9 9-7 7 7 7m14-14 7 7-7 7M19 4l-6 24"/>',
    "game": '<path d="M9 9h14c5 0 10 18 5 19l-8-6h-8l-8 6C-1 27 4 9 9 9z"/><path d="M10 13v7m-3-4h6m9-2h.1m3 4h.1"/>',
    "contacts": '<circle cx="16" cy="10" r="6"/><path d="M5 29v-3c0-11 22-11 22 0v3z"/>',
    "spreadsheet": '<path d="M5 3h22v26H5zM5 11h22M5 19h22M13 11v18m7-18v18"/>',
    "presentation": '<path d="M3 4h26v20H3zM16 24v6M10 30h12M8 17l6-6 4 4 6-8"/>',
    "refresh": '<path d="M27 11A12 12 0 0 0 6 7l-3 5m0-7v7h7M5 21a12 12 0 0 0 21 4l3-5m0 7v-7h-7"/>',
    "save": '<path d="M5 3h19l5 5v21H3V3zM9 3v9h13V3M9 29V18h14v11"/>',
    "cut": '<circle cx="7" cy="24" r="4"/><circle cx="25" cy="24" r="4"/><path d="m10 21 15-18M22 21 7 3"/>',
    "undo": '<path d="m10 5-7 7 7 7M3 12h15c13 0 13 16 0 16"/>',
    "redo": '<path d="m22 5 7 7-7 7m7-7H14C1 12 1 28 14 28"/>',
    "question": '<circle cx="16" cy="16" r="13"/><path d="M11 11c0-7 12-7 10 0-1 4-5 3-5 8m0 5v.1"/>',
    "sun": '<circle cx="16" cy="16" r="7"/><path d="M16 2v3m0 22v3M2 16h3m22 0h3M6 6l2 2m16 16 2 2M6 26l2-2M24 8l2-2"/>',
    "location": '<path d="M26 12c0 9-10 18-10 18S6 21 6 12c0-13 20-13 20 0z"/><circle cx="16" cy="12" r="4"/>',
    "scan": '<path d="M4 21 9 7l19 11M3 20h26v9H3zM8 24h16"/>',
    "paint": '<path d="m19 3 10 6-13 12-5-3zM10 19c-6-1-2 8-8 10 12 3 18-5 8-10z"/>',
    "language": '<path d="M3 7h16M11 3v4M6 7c1 8 7 12 13 15M17 7C15 16 9 22 3 24m14 5 6-16 7 16m-10-5h7"/>',
    "phone": '<rect x="8" y="2" width="16" height="28" rx="3"/><path d="M13 6h6m-4 20h2"/>',
    "optical": '<circle cx="16" cy="16" r="13"/><circle cx="16" cy="16" r="3"/><path d="m7 7 6 6m6 6 6 6"/>',
    "app": '<path d="m16 4 12 7v14l-12 7-12-7V11z"/><path d="m4 11 12 7 12-7M16 18v14"/>',
}


def semantic(name):
    n = re.sub(r"(?:-symbolic|-dark)+$", "", name.lower())
    if n in ("chatgpt", "uosaiassistant") or "assistant" in n:
        return "assistant"
    exact = {"application-exit": "close", "view-refresh": "refresh", "document-save": "save", "document-save-as": "save", "edit-cut": "cut", "edit-undo": "undo", "edit-redo": "redo", "media-playback-pause": "pause", "media-playback-stop": "stop", "dialog-question": "question", "changes-allow": "security", "changes-prevent": "security", "process-working": "clock", "deepin-draw": "paint", "deepin-global-translation": "language", "deepin-ocr": "scan", "org.gnome.simplescan": "scan", "kwalletmanager": "security", "dde-shell": "computer", "deepin-dde": "computer", "linyaps": "store", "redshift": "sun", "gvim": "code", "media-flash-sd": "drive", "media-flash": "drive", "media-optical": "optical", "media-floppy": "save", "inode-directory": "folder"}
    if n in exact:
        return exact[n]
    rules = [("calculator", "calculator"), ("calendar", "calendar"), ("wechat", "chat"), ("telegram", "chat"), ("chat", "chat"), ("mail", "mail"), ("camera", "camera"), ("clock", "clock"), ("archive", "archive"), ("zip", "archive"), ("spreadsheet", "spreadsheet"), ("presentation", "presentation"), ("vscode", "code"), ("code", "code"), ("editor", "document"), ("contacts", "contacts"), ("album", "image"), ("recorder", "music"), ("gomoku", "game"), ("lianliankan", "game"), ("scanner", "scan"), ("location", "location"), ("phone", "phone")]
    return next((template for key, template in rules if key in n), None)


def state_glyph(name, template):
    """State affects geometry, rather than just allocating different filenames."""
    n = name.lower()
    if template == "arrow":
        angle = 90 if any(x in n for x in ("down", "bottom")) else 270 if any(x in n for x in ("up", "top")) else 180 if any(x in n for x in ("left", "previous", "first", "rtl")) else 0
        return f'<g transform="rotate({angle} 16 16)"><path d="M4 16h24m-9-9 9 9-9 9"/></g>'
    if template == "battery":
        numeric = re.search(r"battery-(\d{3})", n)
        level = min(100, int(numeric[1])) / 100 if numeric else next((v for key, v in [("empty", 0), ("caution", .12), ("low", .25), ("good", .65), ("full", 1)] if key in n), .75)
        fill = f'<rect x="5" y="10" width="{20 * level:.2f}" height="12" rx="1" fill="currentColor" stroke="none"/>' if level else ''
        charge = '<path d="m18 8-6 9h5l-3 8 8-12h-6z" fill="#FFFFFF" stroke="#182330" stroke-width=".7"/>' if "charging" in n or "plugged" in n else ''
        return '<path d="M2 7h25v18H2zM27 12h3v8h-3"/>' + fill + charge
    if template == "volume":
        shell = '<path d="M3 12h6l8-7v22l-8-7H3z"/>'
        waves = '<path d="m22 12 7 8m0-8-7 8"/>' if "muted" in n else '<path d="M22 13c3 1 3 5 0 6"/>'
        if "medium" in n:
            waves += '<path d="M25 10c5 3 5 9 0 12"/>'
        elif "high" in n or not any(v in n for v in ("low", "medium", "muted")):
            waves += '<path d="M25 8c8 4 8 12 0 16"/>'
        return shell + waves
    if template == "network" and any(x in n for x in ("signal", "offline", "network-wireless")):
        count = 0 if "offline" in n else 1 if "weak" in n else 2 if "ok" in n else 3 if "good" in n else 4
        paths = ['<circle cx="16" cy="28" r="1.5" fill="currentColor" stroke="none"/>', '<path d="M11 22q5-5 10 0"/>', '<path d="M7 17q9-9 18 0"/>', '<path d="M3 11q13-13 26 0"/>']
        return ''.join(f'<g opacity="{1 if i < count else .2}">{p}</g>' for i, p in enumerate(paths)) + ('<path d="m8 5 19 22"/>' if not count else '')
    if template == "trash" and "full" in n:
        return GLYPHS["trash"] + '<path d="m10 4 3-3 4 3 4-2 2 4"/>'
    if template == "security" and "changes-" in n:
        shackle = '<path d="M10 14V8c0-8 12-8 12 0v6"/>' if "prevent" in n else '<path d="M10 14V8c0-8 12-8 12 0"/>'
        return shackle + '<rect x="6" y="14" width="20" height="16" rx="3"/><path d="M16 20v4"/>'
    if template == "network" and "wired" in n:
        return '<path d="M8 3h16v14H8zM12 3v7m4-7v7m4-7v7M16 17v12M4 29h24"/>'
    return GLYPHS.get(template, GLYPHS["app"])


def mix(color, other, weight):
    a, b = [tuple(int(c.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) for c in (color, other)]
    return "#" + ''.join(f'{round(x*(1-weight)+y*weight):02X}' for x, y in zip(a, b))


def accent_color(template, primary):
    # Family color is deliberate; a dark system accent must not become an invisible glyph.
    colors = {"folder": "#F1AD43", "browser": "#4C91F4", "terminal": "#5669D8", "calculator": "#31B7AA", "calendar": "#EC716B", "music": "#C166DE", "image": "#D774A4", "video": "#8067DF", "assistant": "#35B58F", "chat": "#43B887", "store": "#F1924C", "document": "#5D9CDC", "settings": "#79899F", "mail": "#4DABCD", "game": "#9363D8"}
    return colors.get(template, mix(primary, "#6FA8DE", .45))


def crafted_object(template, small):
    """Recognizable objects have their own silhouette and internal hierarchy."""
    if template == "folder":
        return '<path d="M7 18V12a5 5 0 0 1 5-5h14l7 8h17a5 5 0 0 1 5 5v32H7z" fill="#B57926"/><path d="M10 19h37v27H10z" fill="#FFF1CE"/><path d="M5 24h54l-6 30H10z" fill="url(#surface)"/><path d="M7 25h50" stroke="#FFE5A9" stroke-width="1.4"/>'
    if template == "browser":
        return '<circle cx="32" cy="34" r="27" fill="#08172A" opacity=".16"/><circle cx="32" cy="31" r="27" fill="url(#surface)"/><path d="M11 28C16 4 51 8 55 28 43 15 24 23 22 38 14 39 9 34 11 28z" fill="#C9E9FF"/><path d="M54 29c3 23-26 38-42 17 16 9 30-4 30-17z" fill="#2D53B3"/><circle cx="32" cy="31" r="10" fill="#EDF8FF"/>'
    if template == "terminal":
        return '<rect x="5" y="10" width="54" height="47" rx="9" fill="#101A2C"/><rect x="5" y="8" width="54" height="12" rx="6" fill="url(#surface)"/><path d="m16 28 10 7-10 7m15 2h13" fill="none" stroke="#E9F5FF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>' + ('' if small else '<circle cx="47" cy="14" r="1.5" fill="#CCD9FF"/><circle cx="52" cy="14" r="1.5" fill="#CCD9FF"/>')
    if template == "calculator":
        return '<rect x="10" y="4" width="44" height="55" rx="10" fill="url(#surface)"/><rect x="16" y="10" width="32" height="13" rx="3" fill="#D3F4EC"/><path d="M16 30h12m-6-6v12m13-6h12M18 43l8 8m0-8-8 8m18-6h10m-10 5h10" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round"/>'
    if template == "music":
        return '<circle cx="37" cy="32" r="25" fill="#35324C"/><circle cx="37" cy="32" r="17" fill="none" stroke="#BDA3D3" stroke-opacity=".35"/><rect x="5" y="5" width="45" height="54" rx="12" fill="url(#surface)"/><path d="M23 40V19l17-4v22M23 23l17-4" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round"/><ellipse cx="18" cy="42" rx="6" ry="4" fill="#FFFFFF"/><ellipse cx="35" cy="39" rx="6" ry="4" fill="#FFFFFF"/>'
    if template == "store":
        return '<path d="M10 18h44l4 39H6z" fill="url(#surface)"/><path d="M22 23V14c0-14 20-14 20 0v9" fill="none" stroke="#83451D" stroke-width="3" stroke-linecap="round"/><path d="M15 19h34" stroke="#FFE7C5" stroke-width="1"/>' + ('' if small else '<path d="M18 31c5 14 23 14 28 0" fill="none" stroke="#FFF6E9" stroke-width="2.5" stroke-linecap="round"/>')
    return None


def render_icon(name, template, primary, secondary, style="crafted", group="apps", size=64, label=""):
    small = size <= 24
    glyph = state_glyph(name, template)
    a = accent_color(template, primary)
    symbolic = "symbolic" in name.lower() or group in {"actions", "status"}
    sw = 2.4 if small else 1.9
    symbolic_color = {"ink": "#9D8055", "neon": "#3298AB"}.get(style, "#738196")
    shape_color = "#E7EAF0" if name.endswith("-dark") else symbolic_color if symbolic else "#FFF9EC" if style == "ink" else "#D3FBFF" if style == "neon" else "#FFFFFF"
    defs = ''
    surface = ''
    if not symbolic and style not in {"outline", "solid"}:
        if style == "ink":
            defs = '<linearGradient id="surface" x2=".85" y2="1"><stop stop-color="#3C4149"/><stop offset="1" stop-color="#121820"/></linearGradient>'
            surface = '<path d="M13 5h37l9 9v37l-8 8H13l-8-8V13z" fill="url(#surface)" stroke="#9D875B" stroke-width="1"/><path d="m10 16 6-6h32M10 19v27" stroke="#C4AB73" stroke-opacity=".3" fill="none"/>'
            if not small:
                surface += '<path d="m48 11 4 2-6 34-3 4 1-8z" fill="#E7E1CC" opacity=".13"/><rect x="46" y="46" width="9" height="9" rx="1" fill="#B63D3C"/><path d="M49 48v5m3-5v5m-4-3h5" stroke="#FFE4BE" stroke-width=".7"/>'
        elif style == "neon":
            bright = mix(primary, "#85FBFF", .5)
            defs = f'<linearGradient id="surface" x2=".8" y2="1"><stop stop-color="#25364E"/><stop offset="1" stop-color="#101727"/></linearGradient><linearGradient id="rim" x2="1" y2="1"><stop stop-color="{bright}"/><stop offset="1" stop-color="{secondary}"/></linearGradient>'
            surface = '<rect x="5" y="5" width="54" height="54" rx="14" fill="url(#surface)" stroke="url(#rim)" stroke-width="1.6"/>'
            if not small:
                surface += '<path d="M17 9h23M9 17v8M47 55h4l4-4" stroke="url(#rim)" stroke-width="1" opacity=".7" fill="none"/>'
        else:
            defs = f'<linearGradient id="surface" x2=".5" y2="1"><stop stop-color="{mix(a, "#FFFFFF", .16)}"/><stop offset="1" stop-color="{mix(a, "#0A1A35", .25)}"/></linearGradient>'
            surface = '<rect x="5" y="7" width="54" height="54" rx="14" fill="#08172A" opacity=".16"/><rect x="5" y="4" width="54" height="54" rx="14" fill="url(#surface)"/><path d="M19 5h26c8 0 13 6 13 14" fill="none" stroke="#FFFFFF" stroke-opacity=".32" stroke-width="1"/>'
    if symbolic:
        transform = "translate(4 4) scale(1.75)"
    elif surface:
        transform = "translate(14 13) scale(1.12)" if small else "translate(13 12) scale(1.18)"
    else:
        transform = "translate(5 5) scale(1.7)"
        shape_color = mix(primary, "#90C6E9", .4) if style == "outline" else a
    fill = shape_color if style == "solid" else "none"
    artwork = f'<g transform="{transform}" color="{shape_color}" fill="{fill}" stroke="{shape_color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>'
    if style == "crafted" and not symbolic:
        object_art = crafted_object(template, small)
        if object_art:
            surface, artwork = '', object_art
    # Labels are opt-in; default assets do not depend on installed fonts or tiny initials.
    if label and not small:
        artwork += f'<text x="32" y="54" font-family="sans-serif" font-size="8" text-anchor="middle" fill="{shape_color}">{escape(label)}</text>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 64 64"><defs>{defs}</defs>{surface}{artwork}</svg>\n'
