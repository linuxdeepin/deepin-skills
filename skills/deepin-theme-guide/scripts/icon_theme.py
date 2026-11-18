"""Discover real icon references, generate named assets and audit file coverage."""
from __future__ import annotations

import configparser
import hashlib
import json
import os
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from dde_backend import ThemeError
from vector_design import EXTRA_TEMPLATES, render_icon, semantic
from vector_assets import validate_svg

NAME_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.+-]{0,159}$")
GROUPS = {"apps": "Applications", "places": "Places", "status": "Status", "mimetypes": "MimeTypes", "devices": "Devices", "actions": "Actions"}
COMMON = {
    "places": "folder user-home user-trash user-trash-full folder-download folder-documents folder-pictures folder-music folder-videos folder-desktop folder-publicshare folder-templates network-workgroup network-server",
    "devices": "computer drive-harddisk drive-removable-media drive-optical media-optical media-flash media-flash-sd media-floppy multimedia-player audio-headphones audio-speakers audio-input-microphone input-keyboard input-mouse camera-photo camera-video phone printer scanner battery video-display network-wired network-wireless",
    "actions": "document-new document-open document-save document-save-as document-print edit-copy edit-cut edit-paste edit-delete edit-undo edit-redo edit-find edit-select-all go-home go-next go-previous go-up go-down view-refresh view-list-details view-grid zoom-in zoom-out system-search application-exit window-close media-playback-start media-playback-pause media-playback-stop media-skip-forward media-skip-backward",
    "status": "dialog-warning dialog-error dialog-information dialog-question security-high security-medium security-low audio-volume-high audio-volume-medium audio-volume-low audio-volume-muted network-offline network-transmit-receive network-wireless-signal-excellent network-wireless-signal-good network-wireless-signal-ok network-wireless-signal-weak battery-full battery-good battery-low battery-caution battery-empty battery-full-charging folder-open folder-visiting process-working changes-prevent changes-allow",
    "mimetypes": "text-x-generic text-plain text-html text-x-script text-x-python text-x-csrc application-x-zerosize application-pdf application-zip application-x-archive application-x-executable application-x-sharedlib application-json application-octet-stream x-office-document x-office-spreadsheet x-office-presentation image-x-generic audio-x-generic video-x-generic inode-directory",
}
TEMPLATES = {"app", "folder", "document", "browser", "terminal", "settings", "home", "trash", "download", "warning", "info", "music", "image", "computer", "store", "monitor", "drive", "network", "volume", "security", "video", "printer", "keyboard", "mouse", "battery", "assistant", "copy", "search", "close", "arrow", "play"}
TEMPLATES |= EXTRA_TEMPLATES
DESIGN_POLICIES = ("restyle-apps", "custom-apps")


def safe_name(value):
    if not isinstance(value, str) or not NAME_RE.fullmatch(value) or value in (".", ".."):
        raise ThemeError("图标名称不能含路径、控制字符或不受支持的字符：%r" % value)
    return value


def data_home():
    root = Path(os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local/share"))
    if not root.is_absolute():
        raise ThemeError("XDG_DATA_HOME 必须是绝对路径")
    return Path(os.path.normpath(str(root)))


def data_dirs():
    roots = [data_home()] + [Path(p) for p in os.environ.get("XDG_DATA_DIRS", "/usr/local/share:/usr/share").split(":") if p]
    return list(dict.fromkeys(str(p) for p in roots if p.is_absolute()))


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def parse_desktop(path):
    raw = Path(path).read_bytes()
    if len(raw) > 1024 * 1024:
        raise ThemeError("desktop 文件超过 1 MiB")
    text = raw.decode("utf-8")
    # Some distributed launchers repeat a translated label. Tolerate only that
    # harmless metadata case and expose it, while ambiguous operational keys
    # (including Icon) or repeated sections must still fail closed.
    current, groups, keys, warnings = None, set(), set(), []
    for line in text.splitlines():
        group = re.fullmatch(r"\s*\[([^]]+)\]\s*", line)
        if group:
            current = group.group(1)
            if current in groups:
                raise ThemeError("启动器分组重复：" + current)
            groups.add(current)
        elif current and not line.lstrip().startswith(("#", ";")) and "=" in line:
            key = line.split("=", 1)[0].strip()
            identity = (current, key)
            if identity in keys:
                if re.fullmatch(r"(?:Name|GenericName|Comment|Keywords)\[[^]]+\]", key):
                    warnings.append("重复翻译字段使用最后值：" + key)
                else:
                    raise ThemeError("启动器键重复：" + key)
            keys.add(identity)
    cfg = configparser.ConfigParser(interpolation=None, strict=False)
    cfg.optionxform = str
    cfg.read_string(text)
    if not cfg.has_section("Desktop Entry"):
        raise ThemeError("缺少 Desktop Entry")
    cfg.uos_warnings = warnings
    return cfg, text, hashlib.sha256(raw).hexdigest()


def generated_override(path, cfg):
    """True for a launcher copy this skill wrote into the user's applications dir.

    Such copies are transient activation artifacts: their Icon values are
    absolute paths inside an installed icon theme. Scanning them as if they
    were real launchers bakes a package's overlay into the next inventory and
    makes the inventory stale as soon as the overlay is rolled back or replaced.
    """
    try:
        Path(path).resolve().relative_to((data_home() / "applications").resolve())
    except (OSError, ValueError):
        return False
    icons = []
    for section in cfg.sections():
        if section != "Desktop Entry" and not section.startswith("Desktop Action "):
            continue
        raw = cfg[section].get("Icon")
        if raw:
            icons.append(raw)
    if not icons:
        return False
    roots = {os.path.normpath(str(data_home() / "icons")), os.path.normpath(str(Path.home() / ".icons"))}
    for raw in icons:
        target = Path(raw)
        if not target.is_absolute() or target.is_symlink():
            return False
        for candidate in target.parents:
            if (candidate / "index.theme").is_file():
                if os.path.normpath(str(candidate.parent)) in roots:
                    break
                return False
        else:
            return False
    return True


def inventory(scope="desktop", app_dirs=None, base_theme="bloom", icon_roots=None):
    if scope not in ("applications", "desktop", "base-theme", "explicit"):
        raise ThemeError("icon.scope 必须是 applications、desktop、base-theme 或 explicit")
    roots = [str(Path(p).expanduser().absolute()) for p in app_dirs] if app_dirs is not None else [str(Path(p) / "applications") for p in data_dirs()]
    targets, entries, exceptions, errors, masked = {}, [], [], [], set()

    def add(name, group, origin):
        safe_name(name)
        target = targets.setdefault(name, {"name": name, "group": group, "origins": []})
        if origin not in target["origins"]:
            target["origins"].append(origin)

    if scope != "explicit":
        for root_text in roots:
            root = Path(root_text)
            if not root.is_dir():
                if app_dirs is not None:
                    errors.append({"path": root_text, "reason": "指定的应用目录不存在"})
                continue
            for path in sorted(root.rglob("*.desktop")):
                desktop_id = path.relative_to(root).as_posix().replace("/", "-")
                if desktop_id in masked:
                    continue
                try:
                    safe_name(desktop_id)
                    cfg, text, checksum = parse_desktop(path)
                    if generated_override(path, cfg):
                        continue  # Transparent: the real launcher below still wins.
                    masked.add(desktop_id)  # A user Hidden=true entry masks system entries.
                    main = cfg["Desktop Entry"]
                    if main.get("Hidden", "false").lower() == "true" or main.get("Type", "Application") != "Application":
                        continue
                    entry = {"desktop_id": desktop_id, "source": str(path), "sha256": checksum,
                             "name": main.get("Name", desktop_id), "no_display": main.get("NoDisplay", "false").lower() == "true", "parse_warnings": cfg.uos_warnings, "icons": []}
                    sections = ["Desktop Entry"] + ["Desktop Action " + action for action in main.get("Actions", "").split(";") if action]
                    for section in sections:
                        if not cfg.has_section(section):
                            continue
                        value = cfg[section].get("Icon", "")
                        if not value:
                            if section == "Desktop Entry":
                                exceptions.append({"desktop_id": desktop_id, "section": section, "reason": "missing_icon"})
                            continue
                        ref = {"section": section, "value": value}
                        if Path(value).is_absolute():
                            alias = "uos-app-" + hashlib.sha256((desktop_id + "\0" + section).encode()).hexdigest()[:16]
                            ref.update({"kind": "absolute", "target": alias})
                            add(alias, "apps", desktop_id)
                            exceptions.append({"desktop_id": desktop_id, "section": section, "reason": "absolute_icon", "value": value, "target": alias})
                        else:
                            try:
                                safe_name(value)
                            except ThemeError:
                                ref.update({"kind": "unsupported", "target": None})
                                exceptions.append({"desktop_id": desktop_id, "section": section, "reason": "unsupported_icon_reference", "value": value})
                            else:
                                ref.update({"kind": "named", "target": value})
                                add(value, "apps", desktop_id)
                        entry["icons"].append(ref)
                    entries.append(entry)
                except (OSError, UnicodeError, configparser.Error, ThemeError) as exc:
                    errors.append({"path": str(path), "reason": str(exc)})
    if scope in ("desktop", "base-theme"):
        for group, names in COMMON.items():
            for name in names.split():
                add(name, group, "common-desktop")
    base_roots = []
    if scope == "base-theme":
        safe_name(base_theme)
        search = icon_roots if icon_roots is not None else [str(Path(p) / "icons") for p in data_dirs()] + [str(Path.home() / ".icons")]
        for root in search:
            theme = Path(root) / base_theme
            if not (theme / "index.theme").is_file():
                continue
            base_roots.append(str(theme))
            for path in sorted(theme.rglob("*")):
                if not path.is_file() or path.suffix.lower() not in (".svg", ".png", ".xpm") or "cursors" in path.relative_to(theme).parts:
                    continue
                try:
                    group = next((p for p in path.relative_to(theme).parts if p in GROUPS), "status")
                    add(path.stem, group, "base-theme:" + base_theme)
                except ThemeError as exc:
                    errors.append({"path": str(path), "reason": str(exc)})
        if not base_roots:
            errors.append({"reason": "未找到基准图标主题", "theme": base_theme})
    result = {"format": "uos-icon-inventory", "version": 1, "scope": scope, "application_dirs": roots if scope != "explicit" else [],
              "base_theme": base_theme if scope == "base-theme" else None, "base_roots": base_roots,
              "targets": sorted(targets.values(), key=lambda item: item["name"]), "entries": entries, "exceptions": exceptions, "errors": errors}
    result["digest"] = digest(result)
    return result


def validate_inventory(value):
    if not isinstance(value, dict) or value.get("format") != "uos-icon-inventory" or value.get("version") != 1:
        raise ThemeError("图标清单格式不支持")
    if digest({k: v for k, v in value.items() if k != "digest"}) != value.get("digest"):
        raise ThemeError("图标清单摘要不匹配")
    targets = value.get("targets")
    if not isinstance(targets, list) or len(targets) > 20000:
        raise ThemeError("图标清单超过 20000 个名称或格式错误")
    for field in ("entries", "exceptions", "errors", "application_dirs", "base_roots"):
        if not isinstance(value.get(field), list):
            raise ThemeError("图标清单字段格式无效：" + field)
    if value.get("scope") not in ("explicit", "applications", "desktop", "base-theme"):
        raise ThemeError("图标清单范围无效")
    seen = set()
    for target in targets:
        if not isinstance(target, dict):
            raise ThemeError("图标目标必须是对象")
        name = safe_name(target.get("name"))
        if name in seen or target.get("group") not in GROUPS:
            raise ThemeError("图标清单存在重复名称或未知分类")
        if not isinstance(target.get("origins"), list) or not target["origins"] or any(not isinstance(item, str) for item in target["origins"]):
            raise ThemeError("图标目标来源格式无效")
        seen.add(name)
    entry_ids = set()
    for entry in value["entries"]:
        if not isinstance(entry, dict):
            raise ThemeError("启动器清单项格式无效")
        desktop_id = safe_name(entry.get("desktop_id"))
        if desktop_id in entry_ids or not desktop_id.endswith(".desktop"):
            raise ThemeError("启动器 ID 重复或无效")
        entry_ids.add(desktop_id)
        if not isinstance(entry.get("source"), str) or not Path(entry["source"]).is_absolute() or not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("sha256"))):
            raise ThemeError("启动器路径或摘要无效")
        if not isinstance(entry.get("icons"), list):
            raise ThemeError("启动器引用格式无效")
        for ref in entry["icons"]:
            if not isinstance(ref, dict) or ref.get("kind") not in ("named", "absolute", "unsupported") or not isinstance(ref.get("section"), str) or not isinstance(ref.get("value"), str):
                raise ThemeError("启动器图标引用无效")
            if ref["kind"] in ("named", "absolute") and safe_name(ref.get("target")) not in seen:
                raise ThemeError("启动器目标未包含在图标清单中")
    if any(not isinstance(item, dict) or not isinstance(item.get("reason"), str) for item in value["exceptions"]):
        raise ThemeError("图标例外格式无效")
    return value


def guess_template(name):
    lowered = name.lower()
    precise = semantic(name)
    if precise:
        return precise
    rules = (("trash", "trash"), ("folder", "folder"), ("home", "home"), ("terminal", "terminal"),
             ("assistant", "assistant"), ("uosai", "assistant"), ("chatgpt", "assistant"),
             ("browser", "browser"), ("firefox", "browser"), ("chrom", "browser"),
             ("file-manager", "folder"), ("store", "store"), ("monitor", "monitor"),
             ("computer", "computer"), ("display", "computer"), ("disk", "drive"), ("drive", "drive"), ("usb", "drive"),
             ("network", "network"), ("wifi", "network"), ("volume", "volume"), ("speaker", "volume"),
             ("security", "security"), ("password", "security"), ("lock", "security"),
             ("battery", "battery"), ("keyboard", "keyboard"), ("mouse", "mouse"), ("print", "printer"),
             ("music", "music"), ("audio", "music"), ("image", "image"), ("photo", "image"),
             ("video", "video"), ("player", "video"), ("movie", "video"), ("download", "download"),
             ("warning", "warning"), ("error", "warning"), ("information", "info"),
             ("settings", "settings"), ("preferences", "settings"), ("control-center", "settings"),
             ("copy", "copy"), ("paste", "copy"), ("search", "search"), ("find", "search"),
             ("close", "close"), ("delete", "trash"), ("playback-start", "play"),
             ("go-", "arrow"), ("document", "document"), ("text-", "document"), ("application-", "document"), ("office", "document"))
    return next((template for key, template in rules if key in lowered), "app")


def render(name, template, label, primary, secondary, style, legacy_renderer=None, badge=False):
    return render_icon(name, template, primary, secondary, style, label=label)


def base_artwork(names, base_theme):
    """Retain recognizable local SVGs for unknown names, with provenance in the manifest."""
    wanted = set(names)
    if not wanted:
        return {}
    candidates = {}
    roots = [Path(p) / "icons" / base_theme for p in data_dirs()] + [Path.home() / ".icons" / base_theme]
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*.svg"):
            if path.stem not in wanted or "cursors" in path.parts:
                continue
            rank = 0 if "48" in path.parts or "48x48" in path.parts else 1 if "scalable" in path.parts else 2
            if path.stem not in candidates or rank < candidates[path.stem][0]:
                candidates[path.stem] = (rank, path)
    result = {}
    for name, (_, path) in candidates.items():
        try:
            validate_svg(path)
            result[name] = path
        except (OSError, ThemeError):
            continue
    return result


def build(root, package_id, name, description, cfg, primary, secondary, legacy_files, legacy_renderer):
    scope = cfg["scope"]
    if cfg.get("inventory"):
        value = validate_inventory(json.loads(Path(cfg["inventory"]).expanduser().read_text(encoding="utf-8")))
        if value["scope"] != scope:
            raise ThemeError("设计规范范围与图标清单范围不一致")
    else:
        value = inventory(scope, cfg.get("application_dirs"), cfg.get("base_theme", "bloom"))
    targets = {item["name"]: item for item in value["targets"]}
    for template in cfg["names"]:
        category = next((group for group, names in COMMON.items() if template in names.split()), "status" if "symbolic" in template else "apps")
        group, names = legacy_files.get(template, (category, (template,)))
        for icon_name in names:
            targets.setdefault(icon_name, {"name": icon_name, "group": group, "origins": ["explicit"]})
    for icon_name, override in cfg["overrides"].items():
        targets.setdefault(icon_name, {"name": icon_name, "group": "apps", "origins": ["override"]})
    # Expand only the documented category aliases. An exact application-name
    # override wins, regardless of JSON key order.
    overrides = dict(cfg["overrides"])
    override_keys = {key: key for key in overrides}
    for category, item in cfg["overrides"].items():
        for alias in legacy_files.get(category, (None, ()))[1]:
            if alias in targets and alias not in overrides:
                overrides[alias] = item
                override_keys[alias] = category
    if not targets or len(targets) > 20000:
        raise ThemeError("图标目标清单为空或超过 20000 个名称")
    value["targets"] = sorted(targets.values(), key=lambda item: item["name"])
    value["digest"] = digest({k: v for k, v in value.items() if k != "digest"})
    theme = Path(root) / "icons" / package_id
    for group in GROUPS:
        (theme / "scalable" / group).mkdir(parents=True)
        for size in (16, 24):
            (theme / str(size) / group).mkdir(parents=True)
    sections = "".join(f"[scalable/{group}]\nSize=48\nType=Scalable\nMinSize=16\nMaxSize=512\nContext={context}\n\n" for group, context in GROUPS.items())
    fixed = [f"{size}/{group}" for size in (16, 24) for group in GROUPS]
    sections += "".join(f"[{size}/{group}]\nSize={size}\nType=Fixed\nContext={context}\n\n" for size in (16, 24) for group, context in GROUPS.items())
    (theme / "index.theme").write_text(f"[Icon Theme]\nName={name}\nComment={description}\nInherits=bloom,hicolor\nDirectories=" + ",".join(fixed + ["scalable/" + group for group in GROUPS]) + "\n\n" + sections, encoding="utf-8")
    unknown = [target["name"] for target in value["targets"] if guess_template(target["name"]) == "app" and not overrides.get(target["name"])]
    preserved = base_artwork(unknown, cfg.get("base_theme", "bloom")) if cfg.get("unknown", "preserve") == "preserve" else {}
    generated = []
    for target in value["targets"]:
        icon_name, group = safe_name(target["name"]), target["group"]
        semantic_name = target["origins"][0].removesuffix(".desktop") if icon_name.startswith("uos-app-") else icon_name
        override = overrides.get(icon_name, {})
        template = override.get("template", guess_template(semantic_name))
        label = override.get("label", "")
        path = theme / "scalable" / group / (icon_name + ".svg")
        provenance = None
        if override.get("source") or icon_name in preserved:
            source = Path(override["source"]) if override.get("source") else preserved[icon_name]
            validate_svg(source)
            path.write_bytes(source.read_bytes())
            template = "custom" if override.get("source") else "preserved"
            if template == "preserved":
                provenance = {"theme": cfg.get("base_theme", "bloom"), "path": str(source.resolve()), "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
        else:
            path.write_text(render_icon(semantic_name, template, primary, secondary, cfg["style"], group, label=label), encoding="utf-8")
        variants = []
        for size in (16, 24):
            variant = theme / str(size) / group / (icon_name + ".svg")
            custom_variant = override.get("variants", {}).get(str(size))
            if custom_variant:
                validate_svg(custom_variant)
                variant.write_bytes(Path(custom_variant).read_bytes())
            elif template in {"custom", "preserved"}:
                variant.write_bytes(path.read_bytes())
            else:
                variant.write_text(render_icon(semantic_name, template, primary, secondary, cfg["style"], group, size), encoding="utf-8")
            variants.append(str(variant.relative_to(root)))
        generated.append({"name": icon_name, "file": str(path.relative_to(root)), "variants": variants, "template": template, "generic": template == "app", **({"provenance": provenance} if provenance else {}), **({"override_key": override_keys[icon_name]} if icon_name in override_keys else {})})
    (Path(root) / "icon-inventory.json").write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = coverage(root, value, generated)
    (Path(root) / "icon-coverage.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"path": f"icons/{package_id}", "generated": cfg, "scope": scope, "inventory": "icon-inventory.json", "coverage": "icon-coverage.json", "assets": generated}


def coverage(root, value, assets):
    provided = {item["name"] for item in assets if (Path(root) / item["file"]).is_file()}
    requested = {item["name"] for item in value["targets"]}
    missing = sorted(requested - provided)
    absolute = [item for item in value["exceptions"] if item["reason"] == "absolute_icon"]
    return {"scope": value["scope"], "target_names": len(requested), "provided_names": len(requested & provided),
            "file_coverage_percent": round(100 * len(requested & provided) / len(requested), 2) if requested else 0,
            "missing_names": missing, "scan_errors": value["errors"], "exceptions": value["exceptions"],
            "generic_names": [item["name"] for item in assets if item["generic"]],
            "requires_launcher_overrides": len(absolute), "files_complete": not missing and not value["errors"],
            "entries_without_icon": sum(item["reason"] == "missing_icon" for item in value["exceptions"]),
            "full_desktop_claim_allowed": False, "visual_verified": False,
            "note": "文件名称覆盖率不代表加载命中率、所有应用内部图标或视觉验收。绝对路径启动器需要显式用户级覆盖。"}


def design_coverage(root, value, assets, policy="restyle-apps"):
    """Measure supplied designs independently of filename and toolkit coverage.

    Use actual launcher references, including actions and absolute-path aliases;
    the asset's directory/category is not a reliable application denominator.
    Explicit samples check only their selected names and retain that scope.
    """
    if policy not in DESIGN_POLICIES:
        raise ThemeError("icon.design_policy must be restyle-apps or custom-apps")
    references = {}
    for entry in value["entries"]:
        for ref in entry["icons"]:
            if ref.get("target"):
                references.setdefault(ref["target"], set()).add(entry["desktop_id"])
    if value["scope"] == "explicit":
        for target in value["targets"]:
            references.setdefault(target["name"], set())
    provided = {item["name"]: item for item in assets}
    counts = dict.fromkeys(("custom", "generated", "preserved", "placeholders", "missing"), 0)
    pending = []
    for name, desktop_ids in sorted(references.items()):
        asset = provided.get(name)
        template = asset.get("template") if asset else None
        reason = None
        if not asset or not (Path(root) / asset["file"]).is_file():
            kind, reason = "missing", "missing_asset"
        elif template == "preserved":
            kind, reason = "preserved", "preserved_original"
        elif template == "app" or asset.get("generic"):
            kind, reason = "placeholders", "placeholder"
        elif template == "custom":
            kind = "custom"
        elif template in TEMPLATES:
            kind = "generated"
            if policy == "custom-apps":
                reason = "custom_source_required"
        else:
            kind, reason = "missing", "unclassified_design"
        counts[kind] += 1
        if reason:
            pending.append({"name": name, "reason": reason, "template": template,
                            "desktop_ids": sorted(desktop_ids)})
    return {"policy": policy, "scope": value["scope"], "target_names": len(references),
            "completed_names": len(references) - len(pending), "counts": counts,
            "design_complete": not pending, "pending_names": [item["name"] for item in pending],
            "pending": pending, "visual_verified": False,
            "note": "Design coverage checks asset provenance and type, not visual quality or embedded application images."}
