"""Semantic plans and recoverable journals. Stored plans never contain commands."""
from __future__ import annotations

import contextlib
import copy
import fcntl
import hashlib
import json
import os
import re
import tempfile
import time
import uuid
from pathlib import Path

from dde_backend import DDE, ThemeError, equivalent, image_info

REQUEST_KEYS = {"wallpaper", "monitor", "icon_theme", "cursor_theme", "cursor_size",
                "accent_color", "accent_color_dark", "reason"}
KINDS = {"wallpaper", "icon_theme", "cursor_theme", "cursor_size", "accent_color"}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def identity():
    # The address is hashed, never returned to a cloud model verbatim.
    bits = [str(os.getuid()), os.environ.get("DBUS_SESSION_BUS_ADDRESS", ""),
            os.environ.get("DISPLAY", ""), os.environ.get("WAYLAND_DISPLAY", "")]
    try:
        bits.append(Path("/proc/sys/kernel/random/boot_id").read_text().strip())
    except OSError:
        pass
    return digest(bits)


def validate_request(request):
    if not isinstance(request, dict) or set(request) - REQUEST_KEYS:
        raise ThemeError("请求必须是 JSON 对象，且只能使用文档中列出的字段")
    if not any(k in request for k in KINDS):
        raise ThemeError("请至少指定一个主题修改项")
    for key, value in request.items():
        if key == "cursor_size":
            if type(value) is not int or not 16 <= value <= 128:
                raise ThemeError("cursor_size 必须是 16 到 128 的整数；实际尺寸以读回值为准")
        elif not isinstance(value, str) or not value or len(value) > 4096 or any(ord(c) < 32 for c in value):
            raise ThemeError("%s 必须是非空、无控制字符的字符串" % key)
    for key in ("accent_color", "accent_color_dark"):
        if key in request and not re.fullmatch(r"#[0-9A-Fa-f]{6}", request[key]):
            raise ThemeError("%s 必须使用 #RRGGBB 格式" % key)
    if "accent_color_dark" in request and "accent_color" not in request:
        raise ThemeError("accent_color_dark 必须与 accent_color 一起指定")
    if "monitor" in request and "wallpaper" not in request:
        raise ThemeError("monitor 只用于指定壁纸的目标显示器")
    return dict(request)


class Store:
    def __init__(self, root=None):
        self.root = Path(root) if root is not None else Path(os.environ.get(
            "XDG_STATE_HOME") or str(Path.home() / ".local/state")) / "uos-theme-personalize"
        self.root = self.root.absolute()

    def ensure(self):
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        if self.root.is_symlink() or self.root.stat().st_uid != os.getuid():
            raise ThemeError("状态目录必须属于当前用户，且不能是符号链接")
        self.root.chmod(0o700)

    @contextlib.contextmanager
    def locked(self):
        self.ensure()
        fd = os.open(str(self.root / ".lock"), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        try:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise ThemeError("另一个主题操作正在运行，请等待其结束") from exc
            yield
        finally:
            os.close(fd)

    def path(self, item_id):
        if not isinstance(item_id, str) or not re.fullmatch(r"(?:plan|change)-[a-f0-9]{16}", item_id):
            raise ThemeError("计划或变更 ID 格式无效")
        return self.root / (item_id + ".json")

    def save(self, item):
        self.ensure()
        target = self.path(item["id"])
        fd, temp = tempfile.mkstemp(prefix=".write-", dir=str(self.root))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(item, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(temp, target)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)

    def load(self, item_id):
        try:
            path = self.path(item_id)
            if path.is_symlink():
                raise ThemeError("拒绝读取符号链接状态文件")
            item = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ThemeError("状态记录不存在或损坏：%s" % item_id) from exc
        if not isinstance(item, dict) or item.get("id") != item_id:
            raise ThemeError("状态记录 ID 不匹配")
        if item.get("session") != identity():
            raise ThemeError("记录属于其他用户或登录会话；请在原会话恢复，或重新生成计划")
        if item_id.startswith("plan-") and digest(item.get("spec")) != item.get("hash"):
            raise ThemeError("计划内容已改变，必须重新生成计划")
        return item


class Theme:
    def __init__(self, backend=None, store=None):
        self.backend = backend if backend is not None else DDE()
        self.store = store if store is not None else Store()

    def plan(self, request):
        request = validate_request(request)
        self.backend.connect()
        monitor = request.get("monitor")
        inspected = self.backend.inspect(monitor)
        capabilities = inspected["capabilities"]
        settings = inspected["settings"]
        catalog = self.backend.catalog()
        ops, blocked, assets = [], [], []
        for kind in ("wallpaper", "icon_theme", "cursor_theme", "cursor_size", "accent_color"):
            if kind not in request:
                continue
            if not capabilities.get(kind):
                blocked.append({"field": kind, "reason": "当前接口缺少可验证、可恢复的读写能力"})
                continue
            before = settings.get(kind)
            if before is None or (isinstance(before, str) and not before):
                blocked.append({"field": kind, "reason": "无法读取原值，不能建立恢复点"})
                continue
            after, target = request[kind], None
            if kind == "wallpaper":
                asset = image_info(after)
                assets.append(asset)
                after, target = Path(asset["path"]).as_uri(), monitor
                if not isinstance(before, str):
                    raise ThemeError("壁纸原值不是 URI")
            elif kind in ("icon_theme", "cursor_theme"):
                group = "icon" if kind == "icon_theme" else "cursor"
                known = {v["id"] for v in catalog["catalog"].get(group, [])}
                if after not in known:
                    blocked.append({"field": kind, "reason": "主题 ID 不在当前 DDE 返回的可用资源清单中", "requested": after})
                    continue
            elif kind == "accent_color":
                if capabilities.get("accent_pair"):
                    target = "pair"
                    parts = str(before).split(",")
                    if len(parts) != 2 or not all(re.fullmatch(r"#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?", p) for p in parts):
                        blocked.append({"field": kind, "reason": "原活动色不是可恢复的浅色/深色颜色对"})
                        continue
                    # An unspecified dark color is preserved, never overwritten.
                    after = request["accent_color"] + "," + request.get("accent_color_dark", parts[1])
                elif "accent_color_dark" in request:
                    blocked.append({"field": kind, "reason": "旧接口只有单个活动色，不支持单独设置深色活动色"})
                    continue
            op = {"kind": kind, "target": target, "before": before, "after": after,
                  "status": "unchanged" if equivalent(kind, before, after) else "pending"}
            ops.append(op)
        spec = {"request": request, "backend": self.backend.endpoint(), "operations": ops,
                "assets": assets, "blocked": blocked, "scope": "current_user/current_workspace"}
        plan = {"id": "plan-" + uuid.uuid4().hex[:16], "version": 1, "session": identity(),
                "created_at": int(time.time()), "expires_at": int(time.time()) + 1800,
                "state": "prepared", "hash": digest(spec), "spec": spec}
        with self.store.locked():
            self.store.save(plan)
        return {"ok": not blocked, "plan": plan, "execute_ready": not blocked,
                "note": "仅生成计划并保存本地恢复信息，尚未修改桌面；壁纸限当前工作区。"}

    def _check_backend(self, record):
        self.backend.connect()
        if record != self.backend.endpoint():
            raise ThemeError("当前外观服务已改变，请重新生成计划")

    def _validate_op(self, op):
        kind, target = op.get("kind"), op.get("target")
        if kind not in KINDS:
            raise ThemeError("记录包含未知操作")
        if target is not None and (not isinstance(target, str) or not target or len(target) > 4096):
            raise ThemeError("目标参数无效")
        if kind not in ("wallpaper", "accent_color") and target is not None:
            raise ThemeError("此设置不支持目标参数")
        if kind == "accent_color" and target not in (None, "pair"):
            raise ThemeError("活动色目标无效")
        for key in ("before", "after"):
            value = op.get(key)
            if kind == "cursor_size":
                if type(value) is not int or not 1 <= value <= 1024:
                    raise ThemeError("光标尺寸记录无效")
            elif not isinstance(value, str) or not value or len(value) > 8192 or "\x00" in value:
                raise ThemeError("设置值记录无效")
            if kind == "wallpaper" and not value.startswith(("file://", "/")):
                raise ThemeError("拒绝非本地壁纸 URI")

    def _recover(self, change):
        """Restore only operations whose values still match what this change wrote."""
        results = []
        for op in reversed(change["operations"]):
            if op["status"] not in ("applied", "started", "restore_failed", "conflict"):
                continue
            self._validate_op(op)
            kind, target = op["kind"], op["target"]
            try:
                current = self.backend.read(kind, target)
                if equivalent(kind, current, op["before"]):
                    op["status"] = "restored"
                    op.pop("error", None)
                elif equivalent(kind, current, op["after"]):
                    # Journal already records the original value before this write.
                    self.backend.write(kind, target, op["before"])
                    self.backend.wait_for(kind, target, op["before"])
                    op["status"] = "restored"
                    op.pop("error", None)
                else:
                    op["status"] = "conflict"
                    op["error"] = "当前值被其他操作修改，保留现值，未覆盖"
            except ThemeError as exc:
                op["status"] = "restore_failed"
                op["error"] = str(exc)
            results.append({"kind": kind, "status": op["status"], "error": op.get("error")})
            self.store.save(change)
        unresolved = any(op["status"] in ("applied", "started", "restore_failed", "conflict")
                         for op in change["operations"])
        change["state"] = "needs_attention" if unresolved else "rolled_back"
        self.store.save(change)
        return results

    def apply(self, plan_id, execute=False):
        with self.store.locked():
            plan = self.store.load(plan_id)
            if not plan_id.startswith("plan-"):
                raise ThemeError("apply 只接受计划 ID")
            spec = plan["spec"]
            if plan["state"] != "prepared" or time.time() > plan["expires_at"]:
                raise ThemeError("计划已执行、执行中或超过 30 分钟有效期，请重新生成")
            if spec["blocked"]:
                raise ThemeError("请求含不可执行项，请调整请求后重新生成完整计划")
            self._check_backend(spec["backend"])
            for asset in spec["assets"]:
                if image_info(asset["path"])["sha256"] != asset["sha256"]:
                    raise ThemeError("壁纸文件在规划后发生变化，请重新生成计划")
            for op in spec["operations"]:
                self._validate_op(op)
                if not equivalent(op["kind"], self.backend.read(op["kind"], op["target"]), op["before"]):
                    raise ThemeError("%s 原值已变化，计划过期，请重新生成" % op["kind"])
                # Recheck the catalog at execution time, since themes can be removed.
                if op["kind"] in ("icon_theme", "cursor_theme"):
                    group = "icon" if op["kind"] == "icon_theme" else "cursor"
                    if op["after"] not in {v["id"] for v in self.backend.catalog(group)["catalog"].get(group, [])}:
                        raise ThemeError("主题资源已不可用，请重新生成计划")
            if not execute:
                return {"ok": True, "dry_run": True, "plan_id": plan_id, "operations": spec["operations"]}
            if os.geteuid() == 0:
                raise ThemeError("请以图形登录用户执行，不要使用 sudo 或 root")
            change = {"id": "change-" + uuid.uuid4().hex[:16], "version": 1,
                      "session": identity(), "plan_id": plan_id, "backend": spec["backend"],
                      "created_at": int(time.time()), "state": "applying", "operations": copy.deepcopy(spec["operations"])}
            self.store.save(change)
            plan["state"], plan["change_id"] = "executing", change["id"]
            self.store.save(plan)
            try:
                for op in change["operations"]:
                    if op["status"] == "unchanged":
                        continue
                    op["status"] = "started"
                    self.store.save(change)
                    self.backend.write(op["kind"], op["target"], op["after"])
                    op["observed"] = self.backend.wait_for(op["kind"], op["target"], op["after"])
                    op["status"] = "applied"
                    self.store.save(change)
            except ThemeError as exc:
                change["error"] = str(exc)
                recovered = self._recover(change)
                plan["state"] = "failed"
                self.store.save(plan)
                return {"ok": False, "dry_run": False, "change": change, "recovery": recovered}
            change["state"], plan["state"] = "applied", "applied"
            self.store.save(change)
            self.store.save(plan)
            return {"ok": True, "dry_run": False, "change": change}

    def verify(self, change_id):
        with self.store.locked():
            change = self.store.load(change_id)
            if not change_id.startswith("change-"):
                raise ThemeError("verify 只接受变更 ID")
            self._check_backend(change["backend"])
            results = []
            for op in change["operations"]:
                self._validate_op(op)
                expected = op["before"] if op["status"] in ("restored", "pending") else op["after"]
                try:
                    current = self.backend.read(op["kind"], op["target"])
                    matches = equivalent(op["kind"], current, expected)
                    results.append({"kind": op["kind"], "matches": matches, "current": current,
                                    "expected": expected, "status": op["status"]})
                except ThemeError as exc:
                    results.append({"kind": op["kind"], "matches": False, "error": str(exc)})
            settled = all(op["status"] in ("applied", "unchanged", "restored", "pending")
                          for op in change["operations"])
            return {"ok": settled and all(r["matches"] for r in results), "change_id": change_id,
                    "state": change["state"], "results": results,
                    "note": "验证的是接口读回值；图标刷新、应用兼容性与视觉效果仍需桌面观察。"}

    def rollback(self, change_id, execute=False):
        with self.store.locked():
            change = self.store.load(change_id)
            if not change_id.startswith("change-"):
                raise ThemeError("rollback 只接受变更 ID")
            self._check_backend(change["backend"])
            if not execute:
                preview = []
                for op in reversed(change["operations"]):
                    if op["status"] in ("applied", "started", "restore_failed", "conflict"):
                        self._validate_op(op)
                        current = self.backend.read(op["kind"], op["target"])
                        safe = equivalent(op["kind"], current, op["after"]) or equivalent(op["kind"], current, op["before"])
                        preview.append({"kind": op["kind"], "from": current, "to": op["before"], "can_restore": safe})
                return {"ok": all(r["can_restore"] for r in preview), "dry_run": True,
                        "change_id": change_id, "operations": preview}
            if os.geteuid() == 0:
                raise ThemeError("请以图形登录用户恢复，不要使用 sudo 或 root")
            results = self._recover(change)
            return {"ok": change["state"] == "rolled_back", "dry_run": False,
                    "change_id": change_id, "state": change["state"], "results": results}
