"""Plans and recoverable change journals for deepin-system-tuning."""
from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path


class TuningError(Exception):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def login_session_id():
    """Return the inherited login session id, never a display/bus proxy."""
    value = (os.environ.get("XDG_SESSION_ID") or "").strip()
    if value:
        return value
    try:
        value = Path("/proc/self/sessionid").read_text(encoding="utf-8").strip()
    except OSError:
        return ""
    return "" if value in ("", "4294967295") else value


def identity():
    bits = [str(os.getuid()), login_session_id()]
    try:
        bits.append(Path("/proc/sys/kernel/random/boot_id").read_text(encoding="utf-8").strip())
    except OSError:
        pass
    return digest(bits)


class Store:
    def __init__(self, root=None):
        self.root = Path(root) if root is not None else Path(os.environ.get(
            "XDG_STATE_HOME") or str(Path.home() / ".local/state")) / "deepin-system-tuning"
        self.root = self.root.absolute()
        self._lock_depth = 0
        self._lock_fd = None

    def ensure(self):
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        if self.root.is_symlink() or self.root.stat().st_uid != os.getuid():
            raise TuningError("状态目录必须属于当前用户，且不能是符号链接")
        self.root.chmod(0o700)

    @contextlib.contextmanager
    def locked(self):
        if self._lock_depth:
            self._lock_depth += 1
            try:
                yield
            finally:
                self._lock_depth -= 1
            return
        self.ensure()
        fd = os.open(str(self.root / ".lock"), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        try:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise TuningError("另一个系统调优操作正在运行，请等待其结束") from exc
            self._lock_depth = 1
            self._lock_fd = fd
            try:
                yield
            finally:
                self._lock_depth = 0
                self._lock_fd = None
        finally:
            os.close(fd)

    def path(self, item_id):
        if not isinstance(item_id, str) or not re.fullmatch(r"(?:plan|change)-[a-f0-9]{16}", item_id):
            raise TuningError("计划或变更 ID 格式无效")
        return self.root / (item_id + ".json")

    def save(self, item):
        self.ensure()
        target = self.path(item["id"])
        fd, temporary = tempfile.mkstemp(prefix=".write-", dir=str(self.root))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(item, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, target)
            target.chmod(0o600)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def load(self, item_id):
        try:
            path = self.path(item_id)
            if path.is_symlink():
                raise TuningError("拒绝读取符号链接状态文件")
            item = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise TuningError("状态记录不存在或损坏：%s" % item_id) from exc
        if not isinstance(item, dict) or item.get("id") != item_id:
            raise TuningError("状态记录 ID 不匹配")
        if item.get("uid") != os.getuid():
            raise TuningError("状态记录属于其他用户")
        if item_id.startswith("plan-"):
            if item.get("session") != identity():
                raise TuningError("计划属于其他登录会话；请在原会话执行，或重新生成计划")
            if digest(item.get("spec")) != item.get("hash"):
                raise TuningError("计划内容已改变，必须重新生成计划")
        return item

    def plan(self, plan):
        self.save(plan)
        return plan

    def change(self, change):
        self.save(change)
        return change

    def latest(self):
        self.ensure()
        items = []
        for path in sorted(self.root.glob("change-*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                items.append(json.loads(path.read_text(encoding="utf-8")))
            except (OSError, ValueError):
                continue
        return items

    def list(self):
        self.ensure()
        return [path.name for path in sorted(self.root.glob("*.json"))]


def uuid_hex():
    import uuid
    return uuid.uuid4().hex[:16]
