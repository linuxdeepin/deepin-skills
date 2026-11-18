#!/usr/bin/env python3
"""deepin system tuning CLI: inspect, recommend, plan, apply, verify, rollback."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from tune_catalog import catalog, recommend
from tune_engine import apply_plan, create_plan, plan_view, restore_all, rollback_change, verify_change, confirm_display, validate_context
from tune_probe import Probe
from tune_state import Store, TuningError


def parser():
    result = argparse.ArgumentParser(description="deepin 硬件感知系统调优工具，默认只读或预览")
    sub = result.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="检查探测能力、权限和可用的调优后端")
    inspect = sub.add_parser("inspect", help="只读采集硬件、桌面、服务、数据库与当前配置")
    inspect.add_argument("--summary", action="store_true", help="只输出分类摘要，不输出完整明细")
    sub.add_parser("catalog", help="列出所有内置配置方案")
    sub.add_parser("settings", help="只读列出当前桌面设置能力及 dconfig 资源覆盖")
    confirm = sub.add_parser("confirm-display", help="确认显示结果正常；超时自动回滚")
    confirm.add_argument("--change-id", required=True)
    rec = sub.add_parser("recommend", help="按当前硬件和上下文给出若干可选项；不修改系统")
    rec.add_argument("--context", help="JSON 字符串或 @文件路径，例如 {\"intent\":\"coding\"}")
    rec.add_argument("--all", action="store_true", help="同时列出当前不可用的方案")
    plan = sub.add_parser("plan", help="生成计划并保存原值快照；不修改系统")
    plan.add_argument("--profiles", required=True, help="逗号分隔的方案 ID，例如 programming,render-quality")
    plan.add_argument("--context", help="JSON 字符串或 @文件路径")
    plan.add_argument("--settings", help='显式设置 JSON；例如 {"outputs":{"eDP-1":{"refresh":120}},"effects.blur":false}')
    plan.add_argument("--user-only", action="store_true", help="只保留当前用户可执行的操作，跳过需要 root 的项")
    apply_ = sub.add_parser("apply", help="默认预览；--execute 才真正写入")
    apply_.add_argument("--plan-id", required=True)
    apply_.add_argument("--execute", action="store_true", help="执行已获用户授权的计划")
    apply_.add_argument("--allow-service-restart", action="store_true",
                        help="允许重启 PostgreSQL/MariaDB 以应用需要重启的参数；不会重启系统")
    apply_.add_argument("--allow-partial", action="store_true",
                        help="明确允许跳过不可执行项，只执行其余操作")
    verify = sub.add_parser("verify", help="读回变更并与目标对比")
    verify.add_argument("--change-id", required=True)
    rollback = sub.add_parser("rollback", help="默认预览；--execute 才真正恢复单个变更")
    rollback.add_argument("--change-id", required=True)
    rollback.add_argument("--execute", action="store_true")
    rollback.add_argument("--allow-service-restart", action="store_true")
    rollback.add_argument("--force", action="store_true",
                          help="中断恢复时允许覆盖既不是本次目标也不是原值的内容；会明确报告")
    restore = sub.add_parser("restore", aliases=["reset"],
                             help="恢复本技能记录的全部变更；默认预览，--execute 才执行")
    restore.add_argument("--change-id", help="只恢复指定变更；省略表示全部活动变更")
    restore.add_argument("--execute", action="store_true")
    restore.add_argument("--allow-service-restart", action="store_true")
    restore.add_argument("--force", action="store_true",
                         help="中断恢复时允许覆盖既不是本次目标也不是原值的内容")
    evaluate = sub.add_parser("evaluate", help="读取计划/变更基线与当前指标，供人工对比；不修改系统")
    evaluate_target = evaluate.add_mutually_exclusive_group(required=True)
    evaluate_target.add_argument("--plan-id")
    evaluate_target.add_argument("--change-id")
    sub.add_parser("status", help="列出本技能保存的计划和变更记录")
    return result


def load_context(raw):
    if not raw:
        return {}
    text = raw
    if raw.startswith("@"):
        text = Path(raw[1:]).expanduser().read_text(encoding="utf-8")
    try:
        value = json.loads(text)
    except ValueError as exc:
        raise TuningError("上下文不是合法 JSON：%s" % exc) from exc
    if not isinstance(value, dict):
        raise TuningError("上下文必须是 JSON 对象")
    return value


def _summary(snapshot):
    cpu = snapshot.get("cpu") or {}
    memory = snapshot.get("memory") or {}
    gpu = snapshot.get("gpu") or {}
    power = snapshot.get("power") or {}
    desktop = snapshot.get("desktop") or {}
    return {
        "host": {
            "os": (snapshot.get("host") or {}).get("os"),
            "kernel": (snapshot.get("host") or {}).get("kernel"),
            "product": (snapshot.get("host") or {}).get("product"),
        },
        "classification": snapshot.get("classification"),
        "cpu": {
            "model": cpu.get("model"),
            "logical": cpu.get("logical"),
            "physical": cpu.get("physical"),
            "hybrid": cpu.get("hybrid"),
            "p_cores": cpu.get("p_cores"),
            "e_cores": cpu.get("e_cores"),
            "governor": cpu.get("governor"),
        },
        "memory": {
            "total_mb": memory.get("total_mb"),
            "available_mb": memory.get("available_mb"),
            "swap_total_mb": memory.get("swap_total_mb"),
            "swappiness": memory.get("swappiness"),
        },
        "gpu": {
            "cards": gpu.get("cards"),
            "renderer": (gpu.get("gl") or {}).get("renderer"),
            "mesa": (gpu.get("gl") or {}).get("mesa"),
            "vaapi": gpu.get("vaapi"),
            "vaapi_drivers": gpu.get("vaapi_drivers"),
        },
        "storage": {
            "root": (snapshot.get("storage") or {}).get("root"),
            "root_disk": (snapshot.get("storage") or {}).get("root_disk"),
            "scheduler": (snapshot.get("storage") or {}).get("scheduler"),
        },
        "power": {
            "battery_present": power.get("battery_present"),
            "ac_online": power.get("ac_online"),
            "dde": power.get("dde"),
            "effective_mode": (snapshot.get("desktop_native") or {}).get("settings", {}).get("power.mode", {}).get("value"),
            "platform_profile": power.get("platform_profile"),
        },
        "desktop": {
            "current_desktop": desktop.get("current_desktop"),
            "current_session": desktop.get("current_session"),
            "sessions": desktop.get("sessions"),
        },
        "network": {
            "wifi": (snapshot.get("network") or {}).get("wifi"),
            "manager": (snapshot.get("network") or {}).get("manager"),
        },
        "databases": snapshot.get("databases"),
        "metrics": snapshot.get("metrics"),
        "capabilities": snapshot.get("capabilities"),
        "desktop_native": {k: (snapshot.get("desktop_native") or {}).get(k) for k in ("session", "primary", "monitors", "settings", "errors")},
        "hardware_hash": snapshot.get("hardware_hash"),
    }


def dispatch(args, store):
    if args.command == "doctor":
        probe = Probe()
        snapshot = probe.collect()
        tools = snapshot.get("tools") or {}
        capabilities = snapshot.get("capabilities") or {}
        return {
            "ok": True,
            "python": sys.version.split()[0],
            "host": snapshot.get("host"),
            "classification": snapshot.get("classification"),
            "capabilities": capabilities,
            "backend": {
                "dde_power": (snapshot.get("desktop_native") or {}).get("settings", {}).get("power.mode"),
                "desktop_busctl": tools.get("busctl"),
                "powerprofilesctl": tools.get("powerprofilesctl"),
                "tuned": tools.get("tuned-adm"),
                "systemd": capabilities.get("systemd"),
                "gsettings": tools.get("gsettings"),
                "sysctl": tools.get("sysctl"),
                "sudo_noninteractive": capabilities.get("sudo_noninteractive"),
            },
            "limits": [
                "未检测到 root/免交互 sudo 时，系统级配置会标记为不可执行；不会提示输入密码。",
                "驱动 modprobe 参数只写入配置，不会自动重启。",
                "数据库参数需要显式 --allow-service-restart 才会重启服务。",
            ],
            "state_dir": str(store.root),
        }
    if args.command == "confirm-display":
        return confirm_display(store, args.change_id)
    if args.command == "settings":
        from tune_desktop import discover
        from tune_probe import run
        return {"ok": True, **discover(run)}
    if args.command == "inspect":
        snapshot = Probe().collect()
        return {"ok": True, **(snapshot if not args.summary else _summary(snapshot))}
    if args.command == "catalog":
        return {"ok": True, **catalog()}
    if args.command == "recommend":
        snapshot = Probe().collect()
        context = validate_context(load_context(args.context))
        data = recommend(snapshot, context, include_unavailable=args.all)
        return {
            "ok": True,
            "hardware": _summary(snapshot),
            "context": context,
            **data,
        }
    if args.command == "plan":
        snapshot = Probe().collect()
        context = load_context(args.context)
        if args.settings:
            if "settings" in context:
                raise TuningError("settings 只能由 --settings 或 --context 其中之一提供")
            context["settings"] = load_context(args.settings)
        profiles = [item.strip() for item in args.profiles.split(",") if item.strip()]
        plan = create_plan(store, snapshot, profiles, context, user_only=args.user_only)
        return plan_view(plan, snapshot)
    if args.command == "apply":
        snapshot = Probe().collect()
        return apply_plan(store, args.plan_id, snapshot, execute=args.execute,
                          allow_service_restart=args.allow_service_restart,
                          allow_partial=args.allow_partial)
    if args.command == "verify":
        return verify_change(store, args.change_id)
    if args.command == "rollback":
        snapshot = Probe().collect()
        return rollback_change(store, args.change_id, snapshot, execute=args.execute,
                               allow_service_restart=args.allow_service_restart,
                               force=args.force)
    if args.command in ("restore", "reset"):
        snapshot = Probe().collect()
        if args.change_id:
            return rollback_change(store, args.change_id, snapshot, execute=args.execute,
                                   allow_service_restart=args.allow_service_restart,
                                   force=args.force)
        return restore_all(store, snapshot, execute=args.execute,
                           allow_service_restart=args.allow_service_restart,
                           force=args.force)
    if args.command == "evaluate":
        item_id = args.plan_id or args.change_id
        item = store.load(item_id)
        current = Probe().collect().get("metrics")
        baseline = item.get("baseline") or (item.get("spec") or {}).get("baseline")
        deltas = {}
        if baseline and current:
            for key in ("load1", "load5", "load15", "available_mb", "swap_free_mb", "max_temp_c"):
                if isinstance(baseline.get(key), (int, float)) and isinstance(current.get(key), (int, float)):
                    deltas[key] = round(current[key] - baseline[key], 3)
            for resource in ("cpu", "memory", "io"):
                base = (baseline.get("pressure") or {}).get(resource) or {}
                now = (current.get("pressure") or {}).get(resource) or {}
                for key in ("avg10", "avg60", "avg300"):
                    if key in base and key in now:
                        deltas["pressure_%s_%s" % (resource, key)] = round(now[key] - base[key], 3)
        return {
            "ok": True,
            "id": item_id,
            "baseline": baseline,
            "current": current,
            "deltas": deltas,
            "note": "这些是系统指标，不是指定工作负载的基准；编译耗时、交互延迟等需要在同一工作负载下另行对比。",
        }
    if args.command == "status":
        items = []
        for item in store.latest():
            items.append({
                "id": item.get("id"),
                "state": item.get("state"),
                "created_at": item.get("created_at"),
                "profiles": item.get("profiles"),
            })
        return {"ok": True, "state_dir": str(store.root), "changes": items,
                "files": store.list()}
    raise TuningError("未知子命令")


def main():
    args = parser().parse_args()
    store = Store()
    try:
        result = dispatch(args, store)
    except (TuningError, OSError, ValueError) as exc:
        result = {"ok": False, "error": str(exc)}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()
    raise SystemExit(0 if result.get("ok") else 2)


if __name__ == "__main__":
    main()
