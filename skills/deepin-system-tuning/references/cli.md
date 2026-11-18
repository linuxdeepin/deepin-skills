# CLI、状态与验收

入口为 `scripts/tune.py`。同目录的 `tune_probe.py`、`tune_catalog.py`、`tune_engine.py`、`tune_state.py`、`tune_desktop.py`、`tune_policies.py`、`tune_guard.py` 必须一起保留。脚本使用 Python 3.9+ 标准库，桌面后端另需支持 JSON 输出的 busctl 和对应 DDE 服务，可从任意工作目录用绝对路径执行，不需要 `PYTHONPATH`、pip、网络或 MCP 服务。

除 argparse 的帮助/参数错误外，输出均为 JSON；退出码 0 表示 `ok=true`，2 表示失败、冲突、blocked 或需要处理。不要只看进程退出码，始终检查 JSON 字段。

## 命令

| 命令 | 行为 |
| --- | --- |
| `doctor` | 只读检查 Python、systemd、gsettings、DDE 电源、电源后端、sysctl、sudo 能力 |
| `inspect [--summary]` | 只读采集完整/摘要硬件、桌面、服务、数据库和当前设置 |
| `catalog` | 列出内置方案元数据 |
| `recommend [--context JSON] [--all]` | 按硬件和上下文返回候选方案、评分、代价；不写系统 |
| `plan --profiles ID[,ID] [--context JSON] [--user-only]` | 保存原值快照和 30 分钟计划；ID 可包含整套方案或独立组件 |
| `apply --plan-id plan-…` | 默认预览，返回命令数组；不写系统 |
| `apply --plan-id plan-… --execute` | 执行完整计划；原值变化或权限丢失时拒绝 |
| `apply … --execute --allow-partial` | 明确允许跳过 blocked 项，只执行可执行项 |
| `apply … --execute --allow-service-restart` | 允许重启 PostgreSQL/MariaDB；不重启系统 |
| `verify --change-id change-…` | 重新读取并逐项比较，不修改 |
| `rollback --change-id change-…` | 单个变更恢复预览 |
| `rollback --change-id change-… --execute` | 单个变更逆序恢复，保留冲突 |
| `rollback … --execute --force` | 中断的半写入恢复；显式覆盖既非目标也非原值的内容 |
| `restore` / `reset` | 全部活动变更恢复预览，从新到旧 |
| `restore --execute` | 恢复全部活动变更到应用本技能前的原值 |
| `restore --execute --force` | 全部恢复，并显式覆盖中断造成的半写入内容 |
| `restore --change-id change-… [--execute]` | 只恢复指定变更 |
| `evaluate --plan-id plan-…` / `--change-id change-…` | 读取计划或变更基线与当前指标，输出 load/内存/温度等差值；只读 |
| `status` | 列出最近变更和状态文件 |

`--context` 支持 JSON 字符串或 `@/绝对路径/context.json`。允许字段：`intent`、`power_source`、`priority`、`allow_service_restart`、`active_app`、`notes`、`settings`。其他字段会被拒绝，避免把任意内容带进计划。

示例：

```bash
python3 tune.py inspect --summary
python3 tune.py recommend --context '{"intent":"coding","priority":"balanced"}'
python3 tune.py plan --profiles programming,render-quality --context '{"intent":"coding"}'
python3 tune.py plan --profiles office --user-only
python3 tune.py apply --plan-id plan-… --execute --allow-partial
python3 tune.py verify --change-id change-…
python3 tune.py rollback --change-id change-… --execute
python3 tune.py restore
python3 tune.py restore --execute
python3 tune.py evaluate --plan-id plan-…
```

## 关键输出

- `recommend`：`recommended`、`options[]`（`score`、`fit`、`reasons`、`tradeoffs`、`operation_count`、`requires_root`、`requires_reboot`、`requires_relogin`）、`session_options`。
- `plan`：`plan_id`、`execute_ready`、`partial_ready`、`blocked`、`conflicts`、`warnings`、`operations[].commands`。
- `apply`：`dry_run`、`change_id`、`state`、`complete`、`pending`、`skipped`、`results[].status`。`complete=false` 表示仍有非 advisory 跳过项或待生效项。
- `rollback`：`ok` 只表示没有失败/冲突；`complete=false` 表示仍有待重启/待验证项，不能当成全部恢复。
- `verify`：`results[].matches`、`runtime_matches`、`effective`、`current`、`expected`、`detail`。`complete` 与 `apply.complete` 一致：只有所有实际写入项都 `effective=active` 且没有非 advisory 跳过项时才为 true；部分执行后验证通过但 `complete=false`。
- `evaluate`：`baseline`、`current`、`deltas`；仅提供系统指标对比，不替代指定工作负载测试。
- `rollback`：`state=rolled_back` 或 `rolled_back_pending` / `needs_attention`；`ok` 表示没有失败/冲突，`complete` 表示没有待重启/待验证项；`pending` 列出仍待处理的影响。

## 状态文件

`${XDG_STATE_HOME:-~/.local/state}/deepin-system-tuning/`：

- 目录 0700，计划和变更文件 0600。
- `plan-<16hex>.json`：语义操作、原值、目标内容、计划哈希和会话/硬件绑定。
- `change-<16hex>.json`：变更状态、逐项前后值、执行结果和恢复结果。
- `.lock`：本技能的写入锁，不阻止控制中心或其他工具。

计划绑定当前用户、登录会话 ID（`XDG_SESSION_ID` 或内核登录会话 ID）、启动 ID、硬件指纹和 30 分钟有效期。重启、重新登录、不同用户、硬件变化或过期都会拒绝执行；应重新生成计划。不要通过手工编辑状态文件绕过检查。

变更记录不自动清理，以免用户失去恢复点。确认不再需要恢复后，按用户意愿清理对应文件。

## 常见状态

| 现象 | 含义 | 处理 |
| --- | --- | --- |
| `execute_ready=false` | 有冲突或 blocked | 看 `blocked`/`conflicts`；移除冲突方案，或用 `--user-only` |
| `blocked: 需要 root 或免交互 sudo` | 当前环境无法写系统路径 | 以 root 运行、配置 `sudo -n`、或用 `--user-only` |
| `state=conflict` | 计划生成后原值变化 | 重新 `plan`，不要强制覆盖 |
| `state=applied_pending` | 写入成功但有待生效项 | 看 `pending`，按要求重启/重新登录；重复应用不会把待登录项误报成 complete |
| `state=rolled_back_pending` | 文件已恢复，但重启、重载或重新登录尚未确认 | `ok=true, complete=false`；驱动项在重启并确认模块参数前持续 pending；数据库项可再次 `rollback/restore --execute --allow-service-restart` 重试；environment/limits 项需重新登录后再次恢复确认 |
| `state=needs_attention` | 自动恢复或手动恢复有项目失败/冲突 | 查看 `rollback`/`results`，逐项处理 |
| `计划已过期` | 超过 30 分钟 | 重新 `plan` |
| `硬件指纹已变化` | 换了机器/硬件 | 重新探测并生成计划 |

## 验收流程

1. `doctor` → `inspect --summary` → `recommend`，确认硬件分类和候选。
2. 只选择用户确认的方案；先 `plan`，再默认 `apply` 预览，检查命令和 blocked。
3. 用户授权范围内执行；无需 root 时优先 `--user-only`。
4. `verify`，区分配置一致、运行态一致、待重启/待登录。
5. 不满意时 `rollback` 预览后执行；冲突项保留现值并报告。

## 边界

本技能不提供网络访问、包管理、任意命令、sudo 提权、重启/注销或内核命令行编辑。它不能验证桌面画质、游戏帧率、数据库 SQL 性能和长期稳定性；这些必须由用户在实际负载下观察。配置文件写对不等于体验已经变好，报告时要明确验证范围。


## 桌面扩展

- `settings`：只读列出桌面设置能力、输出 Modes、dconfig 资源覆盖。
- `plan --profiles <ID> --settings '<JSON>'`：显式语义设置；可用 `@文件`，覆盖场景的同键默认值。
- `confirm-display --change-id <ID>`：在 30 秒内确认画面正常，取消独立超时恢复；必须有用户视觉反馈且在原登录会话执行。
- `applied_pending_confirmation` / `pending_confirmation`：显示待确认，complete=false。
- `applied_pending_runtime` / `configured_unverified`：dconfig 配置已验证，消费者运行态未知，complete=false。
- `restored_pending_runtime`：dconfig 原值和默认继承已恢复，消费者运行态未知。

settings 字段、参数示例、资源白名单与显示保护限制见 [desktop.md](desktop.md)。
