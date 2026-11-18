#!/usr/bin/env python3
"""UOS theme CLI: inspect/catalog/preview/plan/apply/verify/rollback."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dde_backend import DDE, ThemeError, environment, file_path, text_variant
from theme_state import Theme


def parser():
    result = argparse.ArgumentParser(description="UOS/Deepin 当前用户主题个性化工具，默认只读或预览")
    sub = result.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="检查依赖、登录会话和 DDE 接口")
    inspected = sub.add_parser("inspect", help="读取当前设置与能力")
    inspected.add_argument("--monitor", help="壁纸目标显示器名称；省略表示主显示器")
    catalog = sub.add_parser("catalog", help="枚举 DDE 实际可用的主题资源")
    catalog.add_argument("--kind", choices=("all", "globaltheme", "icon", "cursor", "background"), default="all")
    preview = sub.add_parser("preview", help="返回指定主题的本地缩略图路径")
    preview.add_argument("--kind", choices=("globaltheme", "icon", "cursor", "background"), required=True)
    preview.add_argument("--id", required=True, dest="resource_id")
    plan = sub.add_parser("plan", help="读取请求 JSON，生成计划与原值快照，不修改桌面")
    plan.add_argument("--request", required=True, help="本地请求 JSON 路径；- 表示从 stdin 读取")
    for name in ("apply", "rollback"):
        action = sub.add_parser(name, help="默认预览；--execute 才真正写入")
        action.add_argument("--plan-id" if name == "apply" else "--change-id", required=True)
        action.add_argument("--execute", action="store_true", help="执行已获用户授权的修改")
    verify = sub.add_parser("verify", help="读回设置并与变更记录对比")
    verify.add_argument("--change-id", required=True)
    return result


def dispatch(args):
    if args.command == "doctor":
        report = {"ok": False, "environment": environment(), "errors": []}
        try:
            backend = DDE().connect()
            report.update({"ok": True, "backend": backend.endpoint(), "capabilities": backend.capabilities()})
        except ThemeError as exc:
            report["errors"].append(str(exc))
            report["next_step"] = "在当前图形登录用户的终端运行；不要 sudo。检查 gdbus 和 UOS AI Agent 的本地执行能力。"
        return report
    if args.command == "inspect":
        return {"ok": True, "environment": environment(), **DDE().connect().inspect(args.monitor)}
    if args.command == "catalog":
        data = DDE().connect().catalog(args.kind)
        return {"ok": not data["errors"], **data}
    if args.command == "preview":
        backend = DDE().connect()
        available = backend.catalog(args.kind)["catalog"].get(args.kind, [])
        if args.resource_id not in {item["id"] for item in available}:
            raise ThemeError("资源 ID 不在 DDE 清单中")
        if not backend.method("Thumbnail", "ss", "s"):
            raise ThemeError("当前 DDE 未提供缩略图接口；可查看 catalog 返回的资源路径")
        value = backend.call(backend.interface + ".Thumbnail", text_variant(args.kind), text_variant(args.resource_id))
        path = file_path(value)
        if not path.is_file():
            raise ThemeError("缩略图路径不可读或尚未生成")
        return {"ok": True, "kind": args.kind, "id": args.resource_id, "preview_path": str(path)}
    theme = Theme()
    if args.command == "plan":
        raw = sys.stdin.read() if args.request == "-" else Path(args.request).expanduser().read_text(encoding="utf-8")
        return theme.plan(json.loads(raw))
    if args.command == "apply":
        return theme.apply(args.plan_id, args.execute)
    if args.command == "rollback":
        return theme.rollback(args.change_id, args.execute)
    if args.command == "verify":
        return theme.verify(args.change_id)
    raise ThemeError("未知子命令")


def main():
    args = parser().parse_args()
    try:
        result = dispatch(args)
    except (ThemeError, OSError, ValueError) as exc:
        result = {"ok": False, "error": str(exc)}
    except KeyboardInterrupt:
        result = {"ok": False, "error": "操作已中断。如已输出或保存 change ID，可用 rollback 检查恢复。"}
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    sys.exit(main())
