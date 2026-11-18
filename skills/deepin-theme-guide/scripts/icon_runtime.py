#!/usr/bin/env python3
"""Probe GTK and Qt named icon lookup in isolated, bounded helper processes."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile

from dde_backend import ThemeError
from icon_theme import safe_name, validate_inventory, inventory as scan_inventory, parse_desktop, design_coverage


def _probe(request):
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
    theme = Gtk.IconTheme.new()
    theme.set_custom_theme(request["theme"])
    if request.get("staged_parent"):
        theme.set_search_path([request["staged_parent"]] + theme.get_search_path())
    rows = []
    for name in request["names"]:
        for size in request["sizes"]:
            info = theme.lookup_icon(name, size, 0)
            rows.append({"name": name, "size": size, "file": info.get_filename() if info else None})
    settings = Gtk.Settings.get_default()
    return {"available": True, "resolver": "gtk3", "search_paths": theme.get_search_path(), "rows": rows,
            "default_theme": settings.get_property("gtk-icon-theme-name") if settings else None}


def lookup(theme, names, sizes=(24, 48, 96), staged_parent=None):
    names = sorted({safe_name(name) for name in names})
    if len(names) > 20000:
        raise ThemeError("图标查找名称超过 20000")
    request = {"theme": theme, "names": names, "sizes": list(sizes), "staged_parent": str(staged_parent) if staged_parent else None}
    errors = []
    for executable in dict.fromkeys((sys.executable, "/usr/bin/python3")):
        try:
            result = subprocess.run([executable, str(Path(__file__).resolve()), "--probe"], input=json.dumps(request), capture_output=True, text=True, timeout=45)
            value = json.loads(result.stdout)
            if result.returncode == 0 and value.get("available"):
                return value
            errors.append(value.get("error", "GTK helper failed"))
        except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
            errors.append(str(exc))
    return {"available": False, "resolver": None, "rows": [], "errors": errors,
            "note": "没有可用的 GTK3/PyGObject 查找接口，只能报告文件覆盖，不能宣称实际命中已验证。"}


def qt_lookup(theme, names, staged_parent=None):
    request = {"theme": theme, "names": sorted(names), "sizes": [24, 48, 96],
               "staged_parent": str(staged_parent) if staged_parent else None}
    try:
        if not shutil.which("g++") or not shutil.which("pkg-config"):
            raise ThemeError("无可用的 Qt6 编译工具；未验证 Qt 实际命中")
        flags = subprocess.run(["pkg-config", "--cflags", "--libs", "Qt6Gui"], capture_output=True, text=True, timeout=5, check=True)
        with tempfile.TemporaryDirectory(prefix="uos-qt-icon-") as temp:
            executable = str(Path(temp) / "probe")
            subprocess.run(["g++", "-std=c++17", "-fPIC", str(Path(__file__).with_name("qt_icon_probe.cpp")), "-o", executable,
                            *shlex.split(flags.stdout)], capture_output=True, text=True, timeout=30, check=True)
            result = subprocess.run([executable], input=json.dumps(request), capture_output=True, text=True,
                                    timeout=45, env={**os.environ, "QT_LOGGING_RULES": "qt.gui.icon.loader.debug=true"})
            value = json.loads(result.stdout)
            if result.returncode or not value.get("available"):
                raise ThemeError("Qt 图标查找辅助进程失败")
            return value
    except (OSError, ValueError, subprocess.SubprocessError, ThemeError) as exc:
        return {"available": False, "resolver": "qt6", "rows": [], "errors": [str(exc)]}


def inspect(package_root, manifest, staged=False, launcher_plan=None):
    component = manifest["components"].get("icon")
    if not component:
        raise ThemeError("包内无图标组件")
    package_root = Path(package_root)
    if not component.get("inventory"):
        # Old packages have no target inventory, so cannot prove full coverage.
        return {"available": False, "scope_complete": False, "design_complete": False, "technical_scope_complete": False,
                "legacy_package": True, "reason": "旧包没有图标目标清单，请创建新 ID 的图标包"}
    inventory = validate_inventory(json.loads((package_root / component["inventory"]).read_text(encoding="utf-8")))
    names = [item["name"] for item in inventory["targets"]]
    theme_root = package_root / component["path"] if staged else Path(component["installed_path"])
    resolved = lookup(manifest["id"], names, staged_parent=theme_root.parent if staged else None)
    rows = []
    for row in resolved["rows"]:
        filename = row["file"]
        path = Path(filename).resolve() if filename else None
        expected = {str((theme_root / directory / group / (row["name"] + ".svg")).resolve()) for directory in ("scalable", "16", "24") for group in ("apps", "places", "status", "mimetypes", "devices", "actions")}
        status = "own_theme" if filename and str(path) in expected else "fallback" if filename else "unresolved"
        rows.append({**row, "status": status})
    missing = sorted({row["name"] for row in rows if row["status"] != "own_theme"})
    qt = qt_lookup(manifest["id"], names, staged_parent=theme_root.parent if staged else None)
    roots = [theme_root.resolve()]
    mirror = Path(os.environ.get("HOME", str(Path.home()))) / ".icons" / manifest["id"]
    if not staged and mirror.is_dir():
        roots.append(mirror.resolve())
    for row in qt["rows"]:
        row["own_theme"] = bool(row.get("rendered") and row.get("files")) and all(
            any(root in Path(filename).parents for root in roots) for filename in row["files"])
    qt["lookup_verified"] = bool(qt["available"] and len(qt["rows"]) == len(names) * 3
                                  and all(row["own_theme"] for row in qt["rows"]))
    absolute = [item for item in inventory["exceptions"] if item["reason"] == "absolute_icon"]
    unresolved_exceptions = [item for item in inventory["exceptions"] if item["reason"] not in ("absolute_icon", "missing_icon")]
    launcher_ready = bool(launcher_plan) and not launcher_plan.get("errors")
    # A plan alone does not prove activation. During staging it only explains scope.
    if not staged and absolute:
        from launcher_overrides import LauncherOverrides
        launcher_ready = LauncherOverrides().verify(inventory)["ok"]
    current_errors = []
    fresh = scan_inventory(inventory["scope"], inventory["application_dirs"], inventory.get("base_theme") or "bloom")
    current = {item["desktop_id"]: item for item in fresh["entries"]}
    original_ids = {item["desktop_id"] for item in inventory["entries"]}
    for desktop_id in sorted(current.keys() - original_ids):
        current_errors.append(desktop_id + ": new_application")
    for error in fresh["errors"]:
        # Default XDG directories may not exist; only errors also absent at
        # generation time need attention. A missing unused directory is harmless.
        if error.get("reason") != "指定的应用目录不存在":
            current_errors.append(str(error))
    uncovered = {item["name"] for item in fresh["targets"]} - set(names)
    current_errors.extend(name + ": new_icon_name" for name in sorted(uncovered))
    for entry in inventory["entries"]:
        try:
            effective = current.get(entry["desktop_id"])
            if effective is None:
                current_errors.append(entry["desktop_id"] + ": removed_or_hidden")
                continue
            _, text, checksum = parse_desktop(effective["source"])
            if checksum != entry["sha256"]:
                # Undo only the precise Icon substitutions for this entry when
                # comparing hashes; one valid override cannot hide other edits.
                from launcher_overrides import replace, value, checksum as text_hash
                for ref in entry["icons"]:
                    if ref["kind"] == "absolute" and value(text, ref["section"]) == ref["target"]:
                        text = replace(text, ref["section"], ref["value"])
                checksum = text_hash(text)
            if checksum != entry["sha256"]:
                current_errors.append(entry["desktop_id"] + ": source_changed")
        except (OSError, ValueError, ThemeError) as exc:
            current_errors.append(entry["desktop_id"] + ": " + str(exc))
    expected_pairs = {(name, size) for name in names for size in (24, 48, 96)}
    verified = resolved["available"] and bool(rows) and not missing and {(row["name"], row["size"]) for row in rows} == expected_pairs
    runtime_verified = verified and qt["lookup_verified"]
    technical_scope_complete = runtime_verified and not inventory["errors"] and not current_errors and not unresolved_exceptions and (not absolute or launcher_ready)
    design = design_coverage(package_root, inventory, component["assets"],
                             component.get("generated", {}).get("design_policy", "restyle-apps"))
    scope_complete = technical_scope_complete and design["design_complete"]
    return {"available": resolved["available"], "resolver": resolved.get("resolver"), "scope": inventory["scope"],
            "lookup_pairs": len(rows), "own_theme_pairs": sum(row["status"] == "own_theme" for row in rows),
            "lookup_verified": verified, "scope_complete": bool(scope_complete), "missing_or_fallback_names": missing,
            "runtime_verified": runtime_verified, "qt_runtime": qt,
            "technical_scope_complete": bool(technical_scope_complete),
            "design_complete": design["design_complete"], "icon_design": design,
            "gtk_default_theme": resolved.get("default_theme"),
            "absolute_launcher_entries": absolute, "launcher_overrides_verified": launcher_ready if absolute else None,
            "entries_without_icon": sum(item["reason"] == "missing_icon" for item in inventory["exceptions"]),
            "other_exceptions": unresolved_exceptions, "inventory_errors": inventory["errors"], "source_changes": current_errors,
            "errors": resolved.get("errors", []), "rows": rows, "visual_verified": False,
            "limits": ["GTK3 与 Qt6 分别验证；均不能证明沙箱或已运行应用缓存已刷新", "名称覆盖不包括应用内嵌图片和未扫描的私有资源", "占位图需要补画，保留素材不计为原创重绘"]}


if __name__ == "__main__":
    if sys.argv[1:] != ["--probe"]:
        raise SystemExit("请通过 theme_pack.py icon-audit 或 verify 调用")
    try:
        request = json.load(sys.stdin)
        result = _probe(request)
    except Exception as exc:
        result = {"available": False, "error": str(exc)}
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["available"] else 2)
