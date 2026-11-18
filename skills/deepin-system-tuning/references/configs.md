# 配置路径、格式与恢复语义

## 允许写入的路径

| 类型 | 路径 | 作用域 | 生效方式 |
| --- | --- | --- | --- |
| 用户环境 | `~/.config/environment.d/90-deepin-tuning.conf` | 用户 | 新登录/新 systemd user 进程；当前应用需重启 |
| 内核参数 | `/etc/sysctl.d/90-deepin-tuning.conf` | root | 写入后执行 `sysctl -p <文件>`，立即读回 |
| 驱动参数 | `/etc/modprobe.d/90-deepin-tuning.conf` | root | 重启后由内核/模块加载 |
| Wi-Fi 省电 | `/etc/NetworkManager/conf.d/90-deepin-tuning.conf` | root | `systemctl reload NetworkManager.service` |
| 文件句柄 | `/etc/security/limits.d/90-deepin-tuning.conf` | root | 重新登录后由 PAM 应用 |
| PostgreSQL | `/etc/postgresql/<版本>/main/conf.d/90-deepin-tuning.conf` | root | reload/restart；shared_buffers 需重启 |
| MariaDB/MySQL | `/etc/mysql/mariadb.conf.d/90-deepin-tuning.cnf` 或 `/etc/mysql/conf.d/90-deepin-tuning.cnf` | root | 服务重启后生效 |

路径必须完全匹配白名单；脚本不接受调用者传入任意路径。不会修改 `/etc/fstab`、GRUB 内核命令行、登录管理器、桌面主题、网络连接密码或数据库数据目录。

## 托管块

文件修改按块进行，标记固定为：

```text
# BEGIN deepin-system-tuning
<本技能写入的行>
# END deepin-system-tuning
```

- 文件已存在时保留标记外的全部内容。
- 已有完整标记时，默认按配置键合并旧块和新块：新值覆盖同键，未在新方案中出现的旧键保留，避免重复调优丢失此前持久化参数；需要完整替换时才显式关闭合并。
- 标记不完整、重复或顺序异常时拒绝写入，不猜测修复。
- 已有文件的权限会保留；只有新建文件使用方案中的默认权限。
- 恢复时写回计划阶段保存的完整原文件内容；原文件不存在则删除本技能创建的文件。
- 如果用户在计划执行后手动改了文件，恢复会报告 `conflict` 并保留用户内容。

## 文件、权限与原子性

- 用户文件用同目录临时文件 + `os.replace`，保留原有权限，目录 0700。
- 系统文件在 root 下使用同目录临时文件；非 root 时要求 `sudo -n`，通过 `install` 写入，绝不拼接 shell 字符串。
- 目标必须是普通文件，拒绝符号链接、超过 1 MiB 的文件和含 NUL 的内容。
- 写入前先保存原值、模式、摘要和运行态；写后重新读取摘要。
- `plan` 阶段先保存一份原值；`apply` 在第一次写入前把原值写入 `change-…json`，每个操作前再读取一次并比较。进程中断后记录保持 `applying`，可用 `restore` 或 `rollback --force` 恢复。
- `plan` 保存 sysctl 的完整持久化目标；同时解析合并后的整个文件，记录 `sysctl -p` 实际会加载的全部键及运行值快照，而不只记录本次目标键。
- sysctl 恢复会先恢复文件，再按快照用 `sysctl -w` 写回全部实际加载键；原文件存在但缺少某些键时也不会留下调优后的运行值。恢复前会检查这些运行值是否仍属于本次操作，用户之后手动改成第三值会报告 `conflict`。
- 中断留下的半写入内容既不是本次目标也不是原值时，普通恢复会报 `conflict`；`--force` 只用于用户确认要恢复到记录的原值。
- 计划只保存语义值、原值和目标内容，不保存任意命令；预览阶段的命令由固定模板生成。

## 服务控制

允许的重载/重启目标：

- `NetworkManager.service`：只允许 `reload`。
- `postgresql.service`、`postgresql@<版本>-main.service`：允许 `reload`、`restart`。
- `mariadb.service`、`mysql.service`：允许 `reload`、`restart`（是否支持 reload 由 unit 决定，失败时保留配置并标记待重启）。

服务启停只来自方案模板，例如 `fstrim.timer`、`irqbalance.service`、`thermald.service`。不会启动未知服务，不会自动安装守护进程。

## 生效状态

| 状态 | 含义 | 是否算完整 |
| --- | --- | --- |
| `applied` | 写入并读回一致 | 是 |
| `unchanged` | 已经是目标值 | 是 |
| `applied_pending_restart` | 文件已写，服务需重启 | 否 |
| `applied_pending_reboot` | modprobe 已写，需重启 | 否 |
| `applied_pending_relogin` | environment/limits 已写，需重新登录 | 否 |
| `skipped` | 明确跳过（advisory 或 `--allow-partial`） | 否 |
| `failed` | 读回失败，尝试逆序恢复 | 否 |
| `conflict` | 当前值被用户/其他程序改动，保留现值 | 否 |

`ok=true` 只表示没有失败或冲突，不代表 `complete=true`。汇报时必须分别说明“写入成功”“运行态生效”“需要重启/重新登录”。

## 恢复

- gsettings：仅当当前值仍等于本次目标时写回原值；否则 conflict。
- 文件：仅当当前摘要等于本次写入摘要时恢复；否则 conflict。带 `reload` 的配置在恢复后执行对应重载，失败时标记 `restored_pending_restart` 并在再次恢复时重试。
- 环境变量/limits：恢复文件后检查当前进程实际继承值；若仍匹配本次调优值，标记 `restored_pending_relogin`，重新登录并确认不再继承后才算恢复完成。
- sysctl：恢复文件后执行 `sysctl -p`；如果原文件不存在，删除本技能文件并用 `sysctl -w` 写回原运行值。
- 服务：恢复原 enabled/active 状态，再读回。
- 数据库：恢复文件；未显式允许重启时标记 `restored_pending_restart`。显式允许重启时会先做产品/版本校验，校验或重启失败按失败处理并尝试恢复文件。`restored_pending_restart` 不会被永久跳过；再次执行 `rollback/restore` 会重新尝试重启并检查服务状态。`verify` 对数据库项始终读取当前服务状态，并在观察到服务启动时间变化（包括用户外部重启）后关闭 `pending_restart`。
- modprobe：恢复文件后仍标记 `restored_pending_reboot`；再次执行 `rollback/restore` 时，未检测到启动变化则继续保持 pending，重启后读取并比较原模块参数，确认一致才标记 `restored`。布尔参数按 `Y/N`、`0/1` 统一比较。
- 恢复是逐项尽力完成，不是跨文件原子事务。失败或冲突会保留记录并返回 `needs_attention`；待重启/待验证项返回 `rolled_back_pending` 且 `complete=false`，再次恢复会重试。


## DDE D-Bus 与 dconfig

桌面接口不通过任意文件路径写入。语义白名单固定在 tune_desktop.py，执行前检查目标接口/类型/权限。ConfigManager 读取并保存 value、类型、isDefaultValue；默认继承用 reset 恢复。global 原始配置项按系统级权限处理。接口身份、按屏模式、限时确认及运行态限制见 [desktop.md](desktop.md)。
