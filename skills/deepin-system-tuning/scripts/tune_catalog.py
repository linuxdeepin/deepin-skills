"""Profile catalog and recommendation rules for deepin-system-tuning.

Profiles only describe semantic operations.  They do not write anything until
the CLI captures their pre-state and the user explicitly executes a plan.
"""
from __future__ import annotations

import math

from tune_policies import COMPONENTS, SCENARIOS, component_ops, op as desktop_op

PROFILE_ORDER = (
    "office",
    "programming",
    "performance",
    "render-quality",
    "render-performance",
    "gaming",
    "battery",
    "database",
)

PROFILE_META = {
    "office": {
        "label": "办公均衡",
        "summary": "均衡电源、硬件视频解码和桌面动画，优先稳定与低打扰。",
        "tradeoffs": ["不追求极限响应", "部分环境变量在重新登录后生效"],
        "requires": ["可选的 DDE 电源设置或 power-profiles-daemon"],
    },
    "programming": {
        "label": "编程开发",
        "summary": "提高 inotify、文件句柄和内存映射上限，降低交换倾向，并按电源状态选择性能策略。",
        "tradeoffs": ["更激进的脏页回写可能在断电时损失少量最近写入", "限制文件在重新登录后生效"],
        "requires": ["本地开发工具链；数据库调优请单独选择 database"],
    },
    "performance": {
        "label": "性能优先",
        "summary": "使用 DDE/power-profiles-daemon 性能模式，降低交换与缓存回收倾向，减少无线和音频省电。",
        "tradeoffs": ["功耗和温度上升", "驱动配置文件需要重启才生效"],
        "requires": ["DDE 电源、power-profiles-daemon 或 tuned 之一"],
    },
    "render-quality": {
        "label": "画质渲染",
        "summary": "保留桌面动画，启用硬件视频解码与 Mesa 着色器缓存，减少重复编译和画面卡顿。",
        "tradeoffs": ["着色器缓存占用磁盘", "环境变量只影响新启动的程序"],
        "requires": ["Mesa 或兼容的图形栈"],
    },
    "render-performance": {
        "label": "低延迟渲染",
        "summary": "关闭桌面动画，启用 Mesa GL 线程和着色器缓存，优先交互和帧时间稳定性。",
        "tradeoffs": ["关闭动画会改变桌面观感", "GL 线程对个别旧应用可能反而增加 CPU 占用"],
        "requires": ["Mesa 图形栈"],
    },
    "gaming": {
        "label": "游戏性能",
        "summary": "性能电源、max_map_count、着色器缓存；混合显卡建议按应用选择独显。",
        "tradeoffs": ["独显直连提高功耗与发热", "驱动参数重启后生效"],
        "requires": ["独立显卡时收益更明显；集显也能使用基础项"],
    },
    "battery": {
        "label": "续航优先",
        "summary": "省电电源模式、无线与音频省电、降低磁盘回写和 GL 线程开销。",
        "tradeoffs": ["响应速度下降", "驱动省电参数需要重启才生效"],
        "requires": ["笔记本电池"],
    },
    "database": {
        "label": "数据库调优",
        "summary": "按内存与存储类型为已安装的 PostgreSQL/MariaDB 生成保守的缓冲区配置；Redis/SQLite 只给建议。",
        "tradeoffs": ["多数参数需要重启数据库服务", "只读取现有配置，不自动安装数据库"],
        "requires": ["本机已安装 PostgreSQL 或 MariaDB/MySQL"],
    },
}


COMPONENT_ORDER = (
    "power-performance",
    "power-balanced",
    "power-battery",
    "graphics-quality",
    "graphics-performance",
    "dev-limits",
    "database-auto",
)

PROFILE_META.update({
    "power-performance": {
        "label": "电源：性能",
        "summary": "只切换电源后端到性能模式。",
        "tradeoffs": ["功耗和温度上升"],
        "requires": ["DDE 电源、power-profiles-daemon 或 tuned 之一"],
        "component": True,
    },
    "power-balanced": {
        "label": "电源：均衡",
        "summary": "只切换电源后端到均衡模式。",
        "tradeoffs": ["不追求极限响应"],
        "requires": ["DDE 电源、power-profiles-daemon 或 tuned 之一"],
        "component": True,
    },
    "power-battery": {
        "label": "电源：省电",
        "summary": "只切换电源后端到省电模式。",
        "tradeoffs": ["性能下降"],
        "requires": ["可用的电源后端"],
        "component": True,
    },
    "graphics-quality": {
        "label": "图形：画质",
        "summary": "只配置 VA-API、着色器缓存和动画，不改电源。",
        "tradeoffs": ["着色器缓存占用磁盘"],
        "requires": ["Mesa 或兼容图形栈"],
        "component": True,
    },
    "graphics-performance": {
        "label": "图形：低延迟",
        "summary": "只配置 VA-API、GL 线程、着色器缓存和关闭动画，不改电源。",
        "tradeoffs": ["关闭动画改变观感", "GL 线程对旧应用可能增加 CPU"],
        "requires": ["Mesa 图形栈"],
        "component": True,
    },
    "dev-limits": {
        "label": "开发限制",
        "summary": "只提高 inotify、文件句柄、映射和网络队列上限，不改电源或图形。",
        "tradeoffs": ["限制文件需重新登录", "脏页参数更激进"],
        "requires": ["无；系统项需 root"],
        "component": True,
    },
    "database-auto": {
        "label": "数据库：自动",
        "summary": "只对已安装的 PostgreSQL/MariaDB 生成参数，不改其他组件。",
        "tradeoffs": ["多数参数需重启数据库服务"],
        "requires": ["本机已安装 PostgreSQL 或 MariaDB/MySQL"],
        "component": True,
    },
})


def _op(profile, category, kind, title, description, **extra):
    result = {
        "profile": profile,
        "category": category,
        "kind": kind,
        "title": title,
        "description": description,
        "requires_root": False,
        "relogin_required": False,
        "restart_required": False,
        "reboot_required": False,
        "executable": True,
        "reason": None,
    }
    result.update(extra)
    return result


def _home(snapshot):
    return snapshot.get("home") or "~"


def _cls(snapshot):
    return snapshot.get("classification") or {}


def _power_source(snapshot, context=None):
    context = context or {}
    return context.get("power_source") or _cls(snapshot).get("power_source")


def _total_mb(snapshot):
    return (snapshot.get("memory") or {}).get("total_mb") or 0


def _clamp(value, low, high):
    return max(low, min(high, int(value)))


def _driver_env(snapshot):
    gpu = snapshot.get("gpu") or {}
    drivers = gpu.get("vaapi_drivers") or []
    gpu_class = _cls(snapshot).get("primary_gpu_class") or _cls(snapshot).get("gpu_class") or ""
    values = {}
    if "intel" in gpu_class and "iHD_drv_video.so" in drivers:
        values["LIBVA_DRIVER_NAME"] = "iHD"
    elif "intel" in gpu_class and "i965_drv_video.so" in drivers:
        values["LIBVA_DRIVER_NAME"] = "i965"
    elif "amd" in gpu_class and "radeonsi_drv_video.so" in drivers:
        values["LIBVA_DRIVER_NAME"] = "radeonsi"
    elif "nvidia" in gpu_class and "nvidia_drv_video.so" in drivers:
        values["LIBVA_DRIVER_NAME"] = "nvidia"
    return values


def _env_ops(profile, snapshot, values, title, description, category="render",
             relogin=True):
    if not values:
        return []
    target = {
        "path": _home(snapshot).rstrip("/") + "/.config/environment.d/90-deepin-tuning.conf",
        "scope": "user",
    }
    return [_op(
        profile, category, "file", title, description,
        target=target,
        desired={"block": ["%s=%s" % (key, values[key]) for key in sorted(values)],
                 "mode": "0644"},
        relogin_required=relogin,
    )]


def _power_ops(profile, snapshot, mode, psm, high):
    native = snapshot.get("desktop_native")
    if native is not None:
        available = native.get("settings", {})
        if "power.mode" in available:
            ops = [desktop_op(profile, "power.mode", mode, snapshot)]
            if psm is not None and "power.saving" in available:
                ops.append(desktop_op(profile, "power.saving", psm, snapshot))
            return ops
        # Presence of migrated schemas alone is not proof of an active backend.
        snapshot = dict(snapshot, desktop=dict(snapshot.get("desktop") or {}, power_schema=False))
    desktop = snapshot.get("desktop") or {}
    keys = set(desktop.get("power_keys") or [])
    ops = []
    if desktop.get("power_schema") and {"mode", "power-saving-mode-enabled", "high-performance-enabled"} <= keys:
        if mode is not None:
            ops.append(_op(
                profile, "power", "gsettings",
                "设置桌面电源模式", "通过 DDE 电源设置切换到目标模式；可由控制中心再次修改。",
                target={"schema": "com.deepin.dde.power", "key": "mode"},
                desired={"repr": "'%s'" % mode},
            ))
        if psm is not None:
            ops.append(_op(
                profile, "power", "gsettings",
                "设置省电模式", "控制 DDE 的省电策略开关。",
                target={"schema": "com.deepin.dde.power", "key": "power-saving-mode-enabled"},
                desired={"repr": "true" if psm else "false"},
            ))
        if high is not None:
            ops.append(_op(
                profile, "power", "gsettings",
                "设置高性能开关", "允许 DDE 在需要时使用高性能策略。",
                target={"schema": "com.deepin.dde.power", "key": "high-performance-enabled"},
                desired={"repr": "true" if high else "false"},
            ))
        return ops
    tools = snapshot.get("tools") or {}
    if tools.get("powerprofilesctl"):
        mapping = {"performance": "performance", "balance": "balanced", "powersave": "power-saver"}
        ops.append(_op(
            profile, "power", "power_profile",
            "切换 power-profiles-daemon 电源配置",
            "读取当前 profile，执行时切换到目标 profile。",
            target={"backend": "powerprofilesctl"},
            desired={"profile": mapping.get(mode or "balance", "balanced")},
        ))
        return ops
    if tools.get("tuned-adm"):
        mapping = {"performance": "throughput-performance", "balance": "balanced", "powersave": "powersave"}
        ops.append(_op(
            profile, "power", "tuned_profile",
            "切换 tuned 电源配置",
            "读取当前 tuned profile，执行时切换到目标 profile。",
            target={"backend": "tuned-adm"},
            desired={"profile": mapping.get(mode or "balance", "balanced")},
        ))
        return ops
    ops.append(_op(
        profile, "power", "advisory",
        "未检测到可用的电源后端",
        "未找到 DDE 电源 schema、power-profiles-daemon 或 tuned。可在系统设置中手动选择电源模式。",
        executable=False,
        reason="没有可安全调用的电源后端",
    ))
    return ops


def _animations_op(profile, snapshot, enabled):
    if "desktop_native" in snapshot:
        available = snapshot["desktop_native"].get("settings", {})
        return [desktop_op(profile, key, enabled, snapshot) for key in
                ("effects.fade", "effects.scale", "effects.minimize", "effects.slidingpopups") if key in available]
    desktop = snapshot.get("desktop") or {}
    schema = desktop.get("interface_schema")
    if not schema or "enable-animations" not in set(desktop.get("interface_keys") or []):
        return []
    return [_op(
        profile, "render", "gsettings",
        "桌面动画", "保留或关闭兼容桌面动画；DDE 是否完全遵循该键取决于当前 shell。",
        target={"schema": schema, "key": "enable-animations"},
        desired={"repr": "true" if enabled else "false"},
    )]


HIGHER_IS_BETTER = {
    "fs.file-max",
    "fs.inotify.max_user_watches",
    "fs.inotify.max_user_instances",
    "fs.inotify.max_queued_events",
    "vm.max_map_count",
    "net.core.somaxconn",
}


def _sysctl_ops(profile, snapshot, entries, title, description):
    current = (snapshot.get("kernel") or {}).get("sysctls") or {}
    persistent = {}
    changed = {}
    for key, value in entries.items():
        current_value = current.get(key)
        if key in HIGHER_IS_BETTER and isinstance(current_value, int) and current_value > value:
            continue
        persistent[key] = value
        if current_value != value:
            changed[key] = value
    if not persistent:
        return []
    return [_op(
        profile, "kernel", "sysctl", title, description,
        target={"path": "/etc/sysctl.d/90-deepin-tuning.conf", "scope": "system"},
        desired={"entries": persistent, "changed_entries": changed},
        requires_root=True,
    )]


def _swappiness(snapshot, fallback=10):
    if (snapshot.get("memory") or {}).get("zram"):
        return 100
    return fallback


def _service_ops(profile, snapshot, unit, enabled, active, title, description):
    service = (snapshot.get("services") or {}).get(unit) or {}
    if not service.get("exists"):
        return []
    if service.get("enabled") == ("enabled" if enabled else "disabled") and (
        active is None or service.get("active") == ("active" if active else "inactive")
    ):
        return []
    return [_op(
        profile, "service", "service", title, description,
        target={"unit": unit},
        desired={"enabled": enabled, "active": active},
        requires_root=True,
    )]


def _storage_ops(profile, snapshot):
    storage = snapshot.get("storage") or {}
    fstype = (storage.get("root") or {}).get("fstype")
    if fstype not in ("ext4", "xfs", "btrfs"):
        return []
    return _service_ops(
        profile, snapshot, "fstrim.timer", True, True,
        "启用周期 TRIM", "为 SSD/NVMe 启用 fstrim.timer；文件系统已支持 discard 时也不会重复删除数据。",
    )


def _irqbalance_ops(profile, snapshot):
    cpu = snapshot.get("cpu") or {}
    if (cpu.get("logical") or 0) < 8:
        return []
    return _service_ops(
        profile, snapshot, "irqbalance.service", True, True,
        "启用中断负载均衡", "多核机器启用 irqbalance，减少单核中断堆积。",
    )


def _thermald_ops(profile, snapshot):
    if "intel" not in ((snapshot.get("cpu") or {}).get("vendor") or "").lower():
        return []
    return _service_ops(
        profile, snapshot, "thermald.service", True, True,
        "启用 thermald", "Intel 平台启用热管理服务；未安装时不会自动安装。",
    )


def _network_ops(profile, snapshot, powersave):
    network = snapshot.get("network") or {}
    if not network.get("wifi") or network.get("manager") != "NetworkManager":
        return []
    service = (snapshot.get("services") or {}).get("NetworkManager.service") or {}
    if not service.get("exists"):
        return []
    return [_op(
        profile, "service", "file",
        "设置 Wi-Fi 省电策略", "写入 NetworkManager 配置片段并重载服务；只影响 Wi-Fi 省电，不修改连接密码。",
        target={"path": "/etc/NetworkManager/conf.d/90-deepin-tuning.conf", "scope": "system"},
        desired={
            "block": ["[connection]", "wifi.powersave = %d" % powersave],
            "mode": "0644",
            "reload": ["systemctl", "reload", "NetworkManager.service"],
        },
        requires_root=True,
    )]


def _modprobe_ops(profile, snapshot, entries, title):
    modules = (snapshot.get("kernel") or {}).get("modules") or {}
    active = []
    for entry in entries:
        module = entry.split()[1].split(".")[0]
        if modules.get(module):
            active.append(entry)
    if not active:
        return []
    return [_op(
        profile, "driver", "modprobe",
        title,
        "写入 modprobe 配置片段；不会自动重启，当前内核参数在重启后生效。",
        target={"path": "/etc/modprobe.d/90-deepin-tuning.conf", "scope": "system"},
        desired={"block": active, "mode": "0644"},
        requires_root=True,
        reboot_required=True,
    )]


def _limits_op(profile, snapshot):
    return [_op(
        profile, "kernel", "file",
        "提高用户文件句柄上限",
        "写入 PAM limits 片段；已在登录会话中的进程需要重新登录才会继承。",
        target={"path": "/etc/security/limits.d/90-deepin-tuning.conf", "scope": "system"},
        desired={
            "block": ["* soft nofile 65536", "* hard nofile 65536"],
            "mode": "0644",
        },
        requires_root=True,
        relogin_required=True,
    )]


def _session_advisory(profile, snapshot, text):
    return [_op(
        profile, "render", "advisory",
        "会话/渲染后端提示",
        text,
        executable=False,
        reason="切换 X11/Wayland 需要在登录界面重新选择会话，脚本不自动注销或改登录配置",
    )]


def _postgres_values(snapshot):
    total = _total_mb(snapshot)
    max_connections = 100
    shared = _clamp(total * 0.25, 128, 4096)
    cache = _clamp(total * 0.50, 512, 12288)
    maintenance = _clamp(total / 16, 64, 1024)
    work = _clamp(total / (max_connections * 4), 4, 64)
    return {
        "shared_buffers": "%dMB" % shared,
        "effective_cache_size": "%dMB" % cache,
        "maintenance_work_mem": "%dMB" % maintenance,
        "work_mem": "%dMB" % work,
        "max_connections": str(max_connections),
        "random_page_cost": "1.1",
        "effective_io_concurrency": "200",
        "wal_compression": "on",
        "checkpoint_completion_target": "0.9",
        "default_statistics_target": "100",
    }


def _mysql_values(snapshot, mysql):
    total = _total_mb(snapshot)
    pool = _clamp(total * 0.25, 128, 8192)
    log_size = _clamp(total / 32, 128, 1024)
    values = {
        "innodb_buffer_pool_size": "%dM" % pool,
        "innodb_log_file_size": "%dM" % log_size,
        "innodb_flush_method": "O_DIRECT",
        "innodb_flush_log_at_trx_commit": "1",
        "max_connections": "151",
        "table_open_cache": "4000",
        "tmp_table_size": "64M",
        "max_heap_table_size": "64M",
        "join_buffer_size": "4M",
    }
    product = (mysql or {}).get("product") or "unknown"
    version = list((mysql or {}).get("version_tuple") or [])
    if len(version) == 2:
        version.append(0)
    if product == "mysql" or (product == "mariadb" and version and version < [10, 6, 0]):
        values["innodb_buffer_pool_instances"] = str(
            min(8, max(1, int(math.ceil(pool / 1024.0)))))
    return values


def _database_ops(profile, snapshot):
    databases = snapshot.get("databases") or {}
    ops = []
    pg = databases.get("postgresql") or {}
    if pg.get("installed"):
        include = pg.get("include_dir")
        if include:
            target = include.rstrip("/") + "/90-deepin-tuning.conf"
            values = _postgres_values(snapshot)
            ops.append(_op(
                profile, "database", "file",
                "调优 PostgreSQL 缓冲区",
                "按内存规模生成保守的 shared_buffers、effective_cache_size、work_mem 等参数；多数参数需重启 PostgreSQL 才生效。",
                target={"path": target, "scope": "system"},
                desired={
                    "block": ["%s = %s" % (key, values[key]) for key in sorted(values)],
                    "mode": "0644",
                    "reload": ["systemctl", "reload", pg.get("unit") or "postgresql.service"],
                    "restart": ["systemctl", "restart", pg.get("unit") or "postgresql.service"],
                },
                requires_root=True,
                restart_required=True,
            ))
        else:
            ops.append(_op(
                profile, "database", "advisory",
                "PostgreSQL 未启用 conf.d",
                "现有 postgresql.conf 没有 include_dir，未写入配置以免覆盖主配置文件；可手动为 conf.d 添加 include_dir 后重试。",
                executable=False,
                reason="没有可安全写入的 PostgreSQL 配置包含目录",
            ))
    mysql = databases.get("mysql") or {}
    if mysql.get("installed") and mysql.get("include_dirs"):
        values = _mysql_values(snapshot, mysql)
        target = mysql["include_dirs"][0].rstrip("/") + "/90-deepin-tuning.cnf"
        product = mysql.get("product") or "unknown"
        version = mysql.get("version") or "未知版本"
        desired = {
            "block": ["[mysqld]"] + ["%s = %s" % (key, values[key]) for key in sorted(values)],
            "mode": "0644",
            "restart": ["systemctl", "restart", mysql.get("unit") or "mariadb.service"],
        }
        if mysql.get("validate"):
            desired["validate"] = mysql["validate"]
        version_tuple = list(mysql.get("version_tuple") or [])
        if len(version_tuple) == 2:
            version_tuple.append(0)
        if product == "mariadb" and (not version_tuple or version_tuple >= [10, 6, 0]):
            desired["remove_keys"] = ["innodb_buffer_pool_instances"]
        ops.append(_op(
            profile, "database", "file",
            "调优 %s %s 缓冲池" % (product, version),
            "已按产品/版本选择兼容参数；需要重启数据库服务才生效，脚本不会自动重启。",
            target={"path": target, "scope": "system"},
            desired=desired,
            requires_root=True,
            restart_required=True,
        ))
    redis = databases.get("redis") or {}
    if redis.get("installed"):
        ops.append(_op(
            profile, "database", "advisory",
            "Redis 参数建议",
            "Redis 的 maxmemory 与淘汰策略取决于持久化方式、是否共享实例和业务容忍度。建议人工确认后再修改，本版本不自动写入。",
            executable=False,
            reason="maxmemory 策略需要业务确认",
        ))
    sqlite = databases.get("sqlite") or {}
    if sqlite.get("installed"):
        ops.append(_op(
            profile, "database", "advisory",
            "SQLite 使用建议",
            "SQLite 是嵌入式数据库，没有系统级服务配置。开发库可评估 PRAGMA journal_mode=WAL、synchronous=NORMAL、cache_size 和 mmap_size；不要对生产库盲目关闭同步。",
            executable=False,
            reason="SQLite 由应用自身连接参数控制",
        ))
    return ops


def _base_render_env(snapshot, glthread, shader_cache=False):
    values = _driver_env(snapshot)
    primary = _cls(snapshot).get("primary_gpu_class") or _cls(snapshot).get("gpu_class") or ""
    if "intel" in primary or "amd" in primary:
        values["mesa_glthread"] = "true" if glthread else "false"
    if shader_cache:
        if "nvidia" in (_cls(snapshot).get("gpu_class") or ""):
            values["__GL_SHADER_DISK_CACHE"] = "1"
            values["__GL_SHADER_DISK_CACHE_SKIP_CLEANUP"] = "1"
        else:
            values["MESA_SHADER_CACHE_MAX_SIZE"] = "2G"
    return values


def _office(snapshot, context):
    ops = _power_ops("office", snapshot, "balance", False, True)
    ops += _env_ops("office", snapshot, _base_render_env(snapshot, True),
                    "启用硬件视频解码与 GL 线程",
                    "通过 environment.d 为新启动的图形程序提供 VA-API 驱动与 Mesa GL 线程；当前会话中的程序需重启。")
    ops += _animations_op("office", snapshot, True)
    ops += _storage_ops("office", snapshot)
    if _cls(snapshot).get("has_wayland_session") and _cls(snapshot).get("session") == "x11":
        ops += _session_advisory("office", snapshot, "本机同时提供 X11 与 Wayland 会话。办公场景可评估 Wayland；切换需在登录界面选择，脚本不会注销当前会话。")
    return ops


def _programming(snapshot, context):
    battery = _power_source(snapshot, context) == "battery"
    mode = "balance" if battery else "performance"
    ops = _power_ops("programming", snapshot, mode, False, not battery)
    ops += _env_ops("programming", snapshot, _base_render_env(snapshot, True),
                    "启用开发工具图形加速",
                    "为编辑器和浏览器启用 VA-API 与 Mesa GL 线程；新进程生效。")
    entries = {
        "fs.inotify.max_user_watches": 524288,
        "fs.inotify.max_user_instances": 8192,
        "fs.inotify.max_queued_events": 65536,
        "vm.max_map_count": 1048576,
        "vm.swappiness": _swappiness(snapshot),
        "vm.vfs_cache_pressure": 50,
        "vm.dirty_background_ratio": 5,
        "vm.dirty_ratio": 10,
        "fs.file-max": 2097152,
        "net.core.somaxconn": 4096,
    }
    ops += _sysctl_ops("programming", snapshot, entries,
                       "提高开发工具与文件监视上限",
                       "提高 inotify、文件句柄、内存映射与网络连接队列；降低交换倾向，适合大型仓库、容器和本地服务。")
    ops += _storage_ops("programming", snapshot)
    ops += _irqbalance_ops("programming", snapshot)
    ops += _thermald_ops("programming", snapshot)
    ops += _limits_op("programming", snapshot)
    if not battery:
        ops += _network_ops("programming", snapshot, 2)
    return ops


def _performance(snapshot, context):
    ops = _power_ops("performance", snapshot, "performance", False, True)
    ops += _env_ops("performance", snapshot, _base_render_env(snapshot, True),
                    "启用图形栈性能选项",
                    "启用 VA-API 和 Mesa GL 线程；新启动的程序生效。")
    ops += _sysctl_ops("performance", snapshot, {
        "vm.swappiness": _swappiness(snapshot),
        "vm.vfs_cache_pressure": 50,
        "vm.dirty_background_ratio": 5,
        "vm.dirty_ratio": 10,
    }, "降低交换与缓存回收倾向", "减少桌面和交互进程被换出，优先保持热数据；长时间高负载时内存压力会更高。")
    ops += _storage_ops("performance", snapshot)
    ops += _irqbalance_ops("performance", snapshot)
    ops += _thermald_ops("performance", snapshot)
    ops += _network_ops("performance", snapshot, 2)
    entries = ["options i915 enable_fbc=1"]
    if "iwlwifi" in ((snapshot.get("kernel") or {}).get("modules") or {}):
        entries.append("options iwlwifi power_save=0")
    if "snd_hda_intel" in ((snapshot.get("kernel") or {}).get("modules") or {}):
        entries.append("options snd_hda_intel power_save=0")
    ops += _modprobe_ops("performance", snapshot, entries, "关闭无线与音频省电")
    return ops


def _render_quality(snapshot, context):
    ops = _env_ops("render-quality", snapshot, _base_render_env(snapshot, True, shader_cache=True),
                    "启用硬件解码与着色器缓存",
                    "减少视频解码和着色器重复编译；缓存会占用用户目录磁盘空间，可在环境文件中删除后恢复。")
    ops += _animations_op("render-quality", snapshot, True)
    ops += _storage_ops("render-quality", snapshot)
    if _cls(snapshot).get("has_wayland_session") and _cls(snapshot).get("session") == "x11":
        ops += _session_advisory("render-quality", snapshot, "若追求更一致的高分屏缩放和帧同步，可评估 Wayland/Treeland 会话；切换需在登录界面完成，脚本不自动切换。")
    return ops


def _render_performance(snapshot, context):
    battery = _power_source(snapshot, context) == "battery"
    ops = _power_ops("render-performance", snapshot, "balance" if battery else "performance", False, not battery)
    ops += _env_ops("render-performance", snapshot, _base_render_env(snapshot, True, shader_cache=True),
                    "启用低延迟图形栈选项",
                    "启用 VA-API、Mesa GL 线程和着色器缓存，面向交互与帧时间稳定性。")
    ops += _animations_op("render-performance", snapshot, False)
    ops += _storage_ops("render-performance", snapshot)
    ops += _network_ops("render-performance", snapshot, 2)
    return ops


def _gaming(snapshot, context):
    cls = _cls(snapshot)
    ops = _power_ops("gaming", snapshot, "performance", False, True)
    values = _base_render_env(snapshot, True, shader_cache=True)
    ops += _env_ops("gaming", snapshot, values,
                    "启用游戏图形栈选项",
                    "启用 VA-API 和着色器缓存；不在全局强制独立显卡。")
    if (cls.get("gpu_class") or "").startswith("hybrid-"):
        ops.append(_op(
            "gaming", "render", "advisory",
            "混合显卡按应用选择渲染设备",
            "需要独显渲染时，优先使用发行版提供的 prime-run 或按应用设置 __NV_PRIME_RENDER_OFFLOAD=1；不要把所有程序都固定到独显，以免增加功耗。",
            executable=False,
            reason="全局 PRIME 环境变量会影响所有程序，需按应用配置",
        ))
    ops += _animations_op("gaming", snapshot, False)
    ops += _sysctl_ops("gaming", snapshot, {
        "vm.max_map_count": 1048576,
        "vm.swappiness": _swappiness(snapshot),
    }, "提高游戏兼容性与内存驻留", "max_map_count 对部分 Proton/兼容层游戏必要；降低交换倾向可减少卡顿。")
    ops += _storage_ops("gaming", snapshot)
    ops += _irqbalance_ops("gaming", snapshot)
    ops += _thermald_ops("gaming", snapshot)
    ops += _network_ops("gaming", snapshot, 2)
    entries = ["options i915 enable_fbc=1"]
    if "iwlwifi" in ((snapshot.get("kernel") or {}).get("modules") or {}):
        entries.append("options iwlwifi power_save=0")
    if "snd_hda_intel" in ((snapshot.get("kernel") or {}).get("modules") or {}):
        entries.append("options snd_hda_intel power_save=0")
    ops += _modprobe_ops("gaming", snapshot, entries, "关闭无线与音频省电")
    return ops


def _battery(snapshot, context):
    ops = _power_ops("battery", snapshot, "powersave", True, False)
    ops += _env_ops("battery", snapshot, _base_render_env(snapshot, False),
                    "降低图形栈持续功耗",
                    "关闭 Mesa GL 线程并保留硬件视频解码；新启动的程序生效。")
    ops += _animations_op("battery", snapshot, False)
    ops += component_ops("display-battery", snapshot)
    ops += component_ops("effects-reduced", snapshot)
    ops += component_ops("idle-battery", snapshot)
    native_keys = (snapshot.get("desktop_native") or {}).get("settings", {})
    if "power.brightness_drop_percent" in native_keys:
        ops.append(desktop_op("battery", "power.brightness_drop_percent", 0, snapshot))
    battery_sysctl = {
        "vm.laptop_mode": 5,
        "vm.dirty_writeback_centisecs": 6000,
        "vm.dirty_expire_centisecs": 12000,
    }
    if (snapshot.get("memory") or {}).get("zram"):
        battery_sysctl["vm.swappiness"] = 100
    ops += _sysctl_ops("battery", snapshot, battery_sysctl, "降低磁盘回写频率", "减少电池模式下的磁盘唤醒和写入，代价是断电时可能丢失最近约一分钟的未落盘数据。")
    ops += _network_ops("battery", snapshot, 3)
    entries = []
    modules = (snapshot.get("kernel") or {}).get("modules") or {}
    if modules.get("iwlwifi"):
        entries.append("options iwlwifi power_save=1")
    if modules.get("snd_hda_intel"):
        entries.append("options snd_hda_intel power_save=1")
    if modules.get("i915"):
        entries.append("options i915 enable_fbc=1 enable_psr=1")
    ops += _modprobe_ops("battery", snapshot, entries, "启用无线、音频与显示省电")
    return ops


def _database(snapshot, context):
    return _database_ops("database", snapshot)


def _power_component(mode, psm, high):
    def build(snapshot, context):
        return _power_ops("power-component", snapshot, mode, psm, high)
    return build


def _graphics_quality(snapshot, context):
    ops = _env_ops("graphics-quality", snapshot, _base_render_env(snapshot, True, shader_cache=True),
                   "启用硬件解码与着色器缓存",
                   "只修改图形环境变量，不改变电源或系统服务。")
    ops += _animations_op("graphics-quality", snapshot, True)
    return ops


def _graphics_performance(snapshot, context):
    ops = _env_ops("graphics-performance", snapshot, _base_render_env(snapshot, True, shader_cache=True),
                   "启用低延迟图形环境变量",
                   "只修改图形环境变量，不改变电源或系统服务。")
    ops += _animations_op("graphics-performance", snapshot, False)
    return ops


def _dev_limits(snapshot, context):
    entries = {
        "fs.inotify.max_user_watches": 524288,
        "fs.inotify.max_user_instances": 8192,
        "fs.inotify.max_queued_events": 65536,
        "vm.max_map_count": 1048576,
        "vm.swappiness": _swappiness(snapshot),
        "vm.vfs_cache_pressure": 50,
        "vm.dirty_background_ratio": 5,
        "vm.dirty_ratio": 10,
        "fs.file-max": 2097152,
        "net.core.somaxconn": 4096,
    }
    ops = _sysctl_ops("dev-limits", snapshot, entries, "提高开发工具限制",
                      "只调整内核与用户限制，不改变电源或图形环境。")
    ops += _limits_op("dev-limits", snapshot)
    ops += _storage_ops("dev-limits", snapshot)
    ops += _irqbalance_ops("dev-limits", snapshot)
    ops += _thermald_ops("dev-limits", snapshot)
    return ops


def _database_auto(snapshot, context):
    return _database_ops("database-auto", snapshot)


BUILDERS = {
    "office": _office,
    "programming": _programming,
    "performance": _performance,
    "render-quality": _render_quality,
    "render-performance": _render_performance,
    "gaming": _gaming,
    "battery": _battery,
    "database": _database,
    "power-performance": _power_component("performance", False, True),
    "power-balanced": _power_component("balance", False, True),
    "power-battery": _power_component("powersave", True, False),
    "graphics-quality": _graphics_quality,
    "graphics-performance": _graphics_performance,
    "dev-limits": _dev_limits,
    "database-auto": _database_auto,
}


# Components are independently selectable; scenarios expand to these components.
COMPONENT_ORDER += tuple(COMPONENTS)
for _id, _label in COMPONENTS.items():
    PROFILE_META[_id] = {"label": _label, "summary": _label, "component": True,
                         "tradeoffs": ["依赖当前会话接口；显示变更需限时确认"], "requires": ["DDE 桌面接口"]}
for _id, (_label, _parts) in SCENARIOS.items():
    PROFILE_META[_id] = {"label": _label, "summary": " + ".join(_parts), "scenario": True,
                         "components": _parts, "tradeoffs": ["显示变化需要限时确认；配置项可能需运行态验证"], "requires": ["对应组件能力"]}


def operations_for(profile, snapshot, context=None):
    if profile in COMPONENTS:
        return component_ops(profile, snapshot)
    if profile in SCENARIOS:
        result = []
        for component in SCENARIOS[profile][1]:
            result += operations_for(component, snapshot, context)
        if profile == "coding-smooth":
            source = _power_source(snapshot, context)
            result += _power_ops(profile, snapshot, "balance" if source == "battery" else "performance", False, source != "battery")
        if profile == "long-battery":
            result += _env_ops(profile, snapshot, _base_render_env(snapshot, False), "续航图形环境", "减少持续图形开销")
            if "power.brightness_drop_percent" in (snapshot.get("desktop_native") or {}).get("settings", {}):
                result.append(desktop_op(profile, "power.brightness_drop_percent", 0, snapshot))
        return result
    return BUILDERS[profile](snapshot, context or {})


def profile_available(profile, snapshot):
    if profile in ("database", "database-auto"):
        databases = snapshot.get("databases") or {}
        if not any((databases.get(name) or {}).get("installed") for name in ("postgresql", "mysql", "redis")):
            return False, "未检测到 PostgreSQL、MariaDB/MySQL 或 Redis 服务；SQLite 仅提供使用建议，本版本不会自动安装或初始化数据库"
    if profile in ("battery", "long-battery") and not ((snapshot.get("power") or {}).get("battery_present")):
        return False, "未检测到电池，续航配置没有实际收益"
    return True, None


def _score(profile, snapshot, context):
    cls = _cls(snapshot)
    cpu = snapshot.get("cpu") or {}
    gpu = cls.get("gpu_class") or ""
    power = _power_source(snapshot, context)
    memory_mb = _total_mb(snapshot)
    memory_gb = memory_mb / 1024.0
    intent = str(context.get("intent") or "general").lower()
    priority = str(context.get("priority") or "").lower()
    score = 50
    reasons = []

    if profile == "office":
        score = 58
        if cls.get("form_factor") == "laptop":
            score += 8
            reasons.append("笔记本形态更适合均衡功耗")
        if memory_gb < 16:
            score += 8
            reasons.append("中等内存下避免激进缓存策略")
        if intent in ("office", "document", "meeting", "video"):
            score += 18
            reasons.append("当前任务接近办公/会议场景")
        if priority == "quiet":
            score += 10
            reasons.append("偏好安静与低功耗")
        if intent == "gaming":
            score -= 12
    elif profile == "programming":
        score = 56
        if memory_gb >= 12:
            score += 12
            reasons.append("内存足以支撑编辑器、容器和本地服务")
        if memory_gb >= 24:
            score += 6
            reasons.append("大内存可进一步降低构建与缓存压力")
        if (cpu.get("logical") or 0) >= 12:
            score += 10
            reasons.append("多核 CPU 适合并行编译和容器")
        if cls.get("storage_class") == "nvme":
            score += 8
            reasons.append("NVMe 适合大量小文件与构建缓存")
        if intent in ("coding", "programming", "development", "dev"):
            score += 20
            reasons.append("当前任务明确为开发")
        if memory_gb < 8:
            score -= 15
            reasons.append("内存偏小，需避免把缓存参数调得过高")
    elif profile == "performance":
        score = 50
        if power == "ac":
            score += 15
            reasons.append("当前使用交流电，性能模式不会明显牺牲续航")
        if cls.get("form_factor") == "desktop":
            score += 8
        if (cpu.get("logical") or 0) >= 12:
            score += 8
            reasons.append("多核 CPU 可受益于性能电源策略")
        if "nvidia" in gpu or "amd" in gpu:
            score += 5
        if intent in ("performance", "gaming", "rendering", "build"):
            score += 15
            reasons.append("当前任务偏向持续负载")
        if priority == "performance":
            score += 12
            reasons.append("偏好性能优先")
        if power == "battery":
            score -= 25
            reasons.append("电池供电时性能模式会明显缩短续航")
    elif profile == "battery":
        score = 38
        if power == "battery":
            score += 32
            reasons.append("当前正在使用电池")
        if cls.get("form_factor") == "laptop":
            score += 15
            reasons.append("笔记本具备电池与移动使用场景")
        if intent in ("battery", "travel", "mobile"):
            score += 15
            reasons.append("当前任务关注续航")
        if power == "ac":
            score -= 25
            reasons.append("当前使用交流电，续航配置收益有限")
    elif profile == "gaming":
        score = 42
        if "nvidia" in gpu or "amd" in gpu:
            score += 20
            reasons.append("检测到独立/高性能 GPU")
        if gpu.startswith("hybrid-"):
            score += 8
            reasons.append("混合显卡可启用渲染卸载")
        if power == "ac":
            score += 10
        if (cls.get("display_refresh") or 0) >= 120:
            score += 8
            reasons.append("高刷新率屏幕受益于低延迟设置")
        if intent == "gaming":
            score += 22
            reasons.append("当前任务明确为游戏")
        if gpu in ("intel", "amd"):
            score -= 8
            reasons.append("集显性能有限，基础项仍有收益但提升幅度较小")
        if power == "battery":
            score -= 15
    elif profile == "render-quality":
        score = 55
        if gpu in ("intel", "amd") or "nvidia" in gpu:
            score += 10
            reasons.append("检测到可用的硬件图形栈")
        if (cls.get("display_width") or 0) >= 2560:
            score += 8
            reasons.append("高分屏受益于着色器缓存与硬件解码")
        if (cls.get("display_refresh") or 0) >= 90:
            score += 6
        if intent in ("rendering", "video", "design", "visual"):
            score += 15
            reasons.append("当前任务涉及渲染/视频/设计")
        if priority == "quality":
            score += 12
    elif profile == "render-performance":
        score = 54
        if (cls.get("display_refresh") or 0) >= 120:
            score += 12
            reasons.append("高刷新率屏幕受益于关闭动画和 GL 线程")
        if gpu.startswith("hybrid-") or "nvidia" in gpu:
            score += 8
        if intent in ("gaming", "rendering", "video", "visual"):
            score += 12
        if priority == "performance":
            score += 10
        if power == "battery":
            score -= 8
    elif profile == "database":
        score = 45
        databases = snapshot.get("databases") or {}
        installed = [name for name, data in databases.items() if (data or {}).get("installed")]
        if installed:
            score += 35
            reasons.append("检测到数据库：" + "、".join(installed))
        if memory_gb >= 16:
            score += 8
            reasons.append("内存足以分配数据库缓冲池")
        if cls.get("storage_class") == "nvme":
            score += 6
        if intent in ("database", "db", "sql"):
            score += 15
            reasons.append("当前任务涉及数据库")
    return max(0, min(100, score)), reasons


def _fit(score):
    if score >= 75:
        return "high"
    if score >= 55:
        return "medium"
    return "low"


def recommend(snapshot, context=None, include_unavailable=False):
    context = context or {}
    options = []
    for profile in (*PROFILE_ORDER, *SCENARIOS):
        available, reason = profile_available(profile, snapshot)
        if not available and not include_unavailable:
            continue
        ops = operations_for(profile, snapshot, context) if available else []
        if profile in SCENARIOS:
            base = {"comfort-office": "office", "coding-smooth": "programming", "long-battery": "battery", "gaming-low-latency": "gaming", "design-accurate": "render-quality"}[profile]
            score, reasons = _score(base, snapshot, context)
            reasons.append("按电源、显示、特效、空闲行为组合组件；运行能力以计划为准")
            if not snapshot.get("desktop_native", {}).get("monitors"):
                score = max(0, score - 15)
        else:
            score, reasons = _score(profile, snapshot, context)
        if not available:
            score = 0
        meta = PROFILE_META[profile]
        options.append({
            "id": profile,
            "components": meta.get("components", []),
            "label": meta["label"],
            "summary": meta["summary"],
            "score": score,
            "fit": _fit(score),
            "available": available,
            "unavailable_reason": reason,
            "reasons": reasons,
            "tradeoffs": meta["tradeoffs"],
            "requires": meta["requires"],
            "operation_count": len([op for op in ops if op.get("kind") != "advisory"]),
            "advisory_count": len([op for op in ops if op.get("kind") == "advisory"]),
            "operations": [
                {"category": op["category"], "title": op["title"], "kind": op["kind"]}
                for op in ops
            ],
            "requires_root": any(op.get("requires_root") for op in ops),
            "requires_reboot": any(op.get("reboot_required") for op in ops),
            "requires_relogin": any(op.get("relogin_required") for op in ops),
        })
    options.sort(key=lambda item: (item["available"], item["score"]), reverse=True)
    best = options[0]["id"] if options else None
    cls = _cls(snapshot)
    session_options = []
    if cls.get("has_wayland_session"):
        session_options.append({
            "id": "wayland",
            "label": "Wayland/Treeland 会话",
            "available": True,
            "apply": False,
            "reason": "需在登录界面选择；脚本不会注销当前会话或修改登录管理器配置",
        })
    if cls.get("has_x11_session"):
        session_options.append({
            "id": "x11",
            "label": "X11 会话",
            "available": True,
            "apply": False,
            "reason": "当前会话若为 X11，可继续使用；切换同样需在登录界面完成",
        })
    return {
        "recommended": best,
        "options": options,
        "session_options": session_options,
        "notes": [
            "评分为启发式建议，不替代实际负载测试。",
            "执行前会重新读取原值；计划只包含可由脚本安全回滚的项。",
        ],
    }


def catalog():
    return {
        "scenarios": [{"id": key, **PROFILE_META[key]} for key in SCENARIOS],
        "profiles": [
            {
                "id": profile,
                **PROFILE_META[profile],
            }
            for profile in PROFILE_ORDER
        ],
        "components": [
            {
                "id": profile,
                **PROFILE_META[profile],
            }
            for profile in COMPONENT_ORDER
        ],
    }
