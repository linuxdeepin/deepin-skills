"""Journaled user desktop-entry Icon overrides; never execute launcher content."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import tempfile

from dde_backend import ThemeError
from icon_theme import data_home, parse_desktop, safe_name


def target_path(desktop_id):
    safe_name(desktop_id)
    if not desktop_id.endswith(".desktop"):
        raise ThemeError("启动器 ID 必须以 .desktop 结尾")
    root = data_home() / "applications"
    path = root / desktop_id
    try:
        path.absolute().relative_to(Path.home().resolve())
    except ValueError as exc:
        raise ThemeError("启动器覆盖目录必须位于当前用户 HOME 内") from exc
    if any(item.is_symlink() for item in (path, *path.parents)):
        raise ThemeError("启动器目标或父目录不能是符号链接")
    return path


def value(text, section):
    current, found = None, []
    for line in text.splitlines():
        group = re.fullmatch(r"\s*\[([^]]+)\]\s*", line)
        if group:
            current = group.group(1)
        elif current == section:
            key = re.match(r"\s*Icon\s*=\s*(.*?)\s*$", line)
            if key:
                found.append(key.group(1))
    if len(found) != 1:
        raise ThemeError("启动器图标键缺失或重复")
    return found[0]


def replace(text, section, icon):
    current, lines = None, []
    value(text, section)
    for line in text.splitlines(keepends=True):
        group = re.fullmatch(r"\s*\[([^]]+)\]\s*", line.strip())
        if group:
            current = group.group(1)
        if current == section:
            match = re.match(r"(\s*Icon\s*=\s*)(.*?)(\r?\n)?$", line)
            if match:
                line = match.group(1) + icon + (match.group(3) or "")
        lines.append(line)
    return "".join(lines)


def checksum(text):
    return hashlib.sha256(text.encode()).hexdigest()


def atomic_text(path, text, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".theme-icon-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class LauncherOverrides:
    def plan(self, inventory, adopted=None):
        # `adopted` maps desktop_id -> a still-applied launcher operation from an
        # earlier activation. A switch of themes must be able to take over our
        # own override file instead of demanding a rollback first: the file is
        # then treated as an ordinary pre-existing user override whose original
        # text is the current one, so this plan's rollback restores the older
        # theme and the older journal keeps owning the true baseline.
        adopted = adopted or {}
        operations, errors = [], []
        for entry in inventory["entries"]:
            refs = [ref for ref in entry["icons"] if ref["kind"] == "absolute"]
            if not refs:
                continue
            try:
                target = target_path(entry["desktop_id"])
                _, source, source_hash = parse_desktop(entry["source"])
                if source_hash != entry["sha256"]:
                    raise ThemeError("原启动器已变化，请重新扫描生成")
                exists = target.exists()
                current = target.read_text(encoding="utf-8") if exists else None
                takeover = None
                if exists and target.resolve() != Path(entry["source"]).resolve():
                    previous = adopted.get(entry["desktop_id"])
                    if not previous or checksum(current) != previous.get("after_hash"):
                        raise ThemeError("出现新的用户启动器覆盖，保留现值")
                    takeover = previous
                base = current if takeover else source
                after = base
                keys = []
                for ref in refs:
                    safe_name(ref["target"])
                    before = value(base, ref["section"])
                    if takeover is None and before != ref["value"]:
                        raise ThemeError("启动器图标键与扫描记录不一致")
                    after = replace(after, ref["section"], ref["target"])
                    keys.append({"section": ref["section"], "before": before, "after": ref["target"]})
                operations.append({"desktop_id": entry["desktop_id"], "source": entry["source"], "source_hash": source_hash,
                                   "created": not exists, "override": bool(takeover), "keys": keys,
                                   "before_hash": checksum(base), "after_hash": checksum(after), "status": "pending",
                                   "adopted_from": (takeover or {}).get("change_id")})
            except (OSError, ValueError, ThemeError) as exc:
                errors.append({"desktop_id": entry["desktop_id"], "error": str(exc)})
        return {"operations": operations, "errors": errors, "execute_ready": not errors,
                "note": "只在用户 applications 目录创建/调整 Icon 键；Exec 内容不执行，不修改系统启动器。"}

    def apply(self, plan, checkpoint):
        if plan["errors"]:
            raise ThemeError("启动器覆盖计划包含错误")
        for op in plan["operations"]:
            path = target_path(op["desktop_id"])
            _, source, source_hash = parse_desktop(op["source"])
            if source_hash != op["source_hash"] or (op["created"] and path.exists()):
                raise ThemeError("启动器在计划后变化")
            text = path.read_text(encoding="utf-8") if op.get("override") else source
            if checksum(text) != op["before_hash"]:
                raise ThemeError("用户启动器在计划后变化")
            for key in op["keys"]:
                text = replace(text, key["section"], key["after"])
            op["status"] = "started"
            checkpoint()
            mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
            atomic_text(path, text, mode)
            if checksum(path.read_text(encoding="utf-8")) != op["after_hash"]:
                raise ThemeError("启动器覆盖读回失败")
            op["status"] = "applied"
            checkpoint()

    def rollback(self, plan, execute=False, checkpoint=lambda: None):
        results = []
        for op in reversed(plan["operations"]):
            if op["status"] not in ("started", "applied", "conflict", "restore_failed"):
                continue
            try:
                path = target_path(op["desktop_id"])
                if not path.exists() and op["created"]:
                    status = "restored"
                else:
                    text = path.read_text(encoding="utf-8")
                    if op["created"]:
                        safe = checksum(text) == op["after_hash"]
                        status = "can_restore" if safe else "conflict"
                        if safe and execute:
                            path.unlink()
                            status = "restored"
                    else:
                        changed = False
                        for key in op["keys"]:
                            current = value(text, key["section"])
                            if current == key["before"]:
                                continue
                            if current != key["after"]:
                                raise ThemeError("用户修改了启动器图标，保留现值")
                            text = replace(text, key["section"], key["before"])
                            changed = True
                        status = "can_restore" if changed else "restored"
                        if changed and execute:
                            atomic_text(path, text, path.stat().st_mode & 0o777)
                            status = "restored"
                item = {"desktop_id": op["desktop_id"], "status": status}
            except (OSError, ValueError, ThemeError) as exc:
                item = {"desktop_id": op["desktop_id"], "status": "conflict", "error": str(exc)}
            if execute:
                op["status"] = item["status"]
                checkpoint()
            results.append(item)
        return results

    def verify(self, inventory):
        results = []
        for entry in inventory["entries"]:
            refs = [ref for ref in entry["icons"] if ref["kind"] == "absolute"]
            if not refs:
                continue
            try:
                path = target_path(entry["desktop_id"])
                text = path.read_text(encoding="utf-8")
                matches = all(value(text, ref["section"]) == ref["target"] for ref in refs)
            except (OSError, ThemeError):
                matches = False
            results.append({"desktop_id": entry["desktop_id"], "matches": matches})
        return {"ok": all(item["matches"] for item in results), "results": results}
