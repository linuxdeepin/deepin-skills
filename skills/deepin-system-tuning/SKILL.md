---
name: deepin-system-tuning
description: 读取 deepin 电脑的 CPU、内存、GPU、屏幕、电源、存储、桌面会话和本地数据库，按办公、编程、性能、续航、游戏、渲染质量、低延迟渲染等目标推荐配置方案，通过可回滚计划组合显示模式、刷新率、亮度、缩放、窗口特效、DDE 电源、空闲行为、dconfig、内核和数据库设置。当用户要求整机优化、平衡性能与续航、减少桌面卡顿或调优数据库时使用；只做单次桌面查询或设置使用 deepin-desktop-environment。
---

# deepin 硬件感知系统调优

本技能把“探测硬件 → 给出若干可选方案 → 生成可审阅计划 → 执行 → 读回验证 → 回滚”拆成独立步骤。模型负责判断用户场景和选择方案，本地脚本负责固定路径、固定命令、原值快照和恢复。不要调用旧版 MCP 计划接口；不要手工用 sudo、包管理或任意 shell 命令绕过本技能。系统级操作只由脚本内部以固定 argv + `sudo -n` 执行。

## 能力边界

本技能负责硬件探测、方案推荐，以及可回滚调优计划的生成、执行、验证和恢复。只做单次桌面查询或设置（亮度、音量、电源模式、外观等）时使用 `$deepin-desktop-environment`；应用或桌面插件开发不属于本技能。

## 定位与检查

从本次加载的 `SKILL.md` 的真实路径确定技能目录，以下 `<技能目录>` 均替换为该绝对目录。所有命令必须实际执行，不能把命令文本当成结果。

```bash
python3 "<技能目录>/scripts/tune.py" doctor
python3 "<技能目录>/scripts/tune.py" inspect --summary
python3 "<技能目录>/scripts/tune.py" catalog
```

`doctor` 只读检查 Python、systemd、gsettings、sysctl、DDE 电源、power-profiles-daemon/tuned 和 root/免交互 sudo 能力。`inspect` 完整采集；`--summary` 只保留分类、CPU/内存/GPU/电源/存储摘要。两者都不修改系统。

需要完整探测字段、分类含义和真实设备限制时，读取 [references/hardware.md](references/hardware.md)。硬件信息用于缩小候选范围，不替代实际负载测试；不要从型号直接断言某个游戏、驱动或编译器一定更快。

## 控制中心与桌面设置

读取 [references/desktop.md](references/desktop.md) 后处理显示、窗口特效、输入或 dconfig 请求。先运行 `tune.py settings` 查看实际可用项；Power1 运行模式优先于旧 GSettings。分辨率与刷新率必须作为一个受支持的显示模式选择。dconfig 资源清单会区分 supported、readonly 和 inventory_only，不能把安装了 schema 当作正在使用该后端。

使用 `plan --profiles <方案> --settings '<JSON>'` 提供显式值；显式设置覆盖同一语义键的场景默认值。按屏设置放在 `outputs` 中。类型、权限、自动亮度、手动色温和合成特效约束会在计划阶段检查。dconfig 只读回配置时标为运行态未验证，不能报告完整生效。

显示模式、主屏、布局和缩放实际改变时，独立恢复进程提供 30 秒确认窗口。用户观察画面正常后执行 `tune.py confirm-display --change-id <真实ID>`；不能只根据数值读回替用户确认。超时会尝试回滚整次变更。确认前 complete=false，期间拒绝执行其他计划。生效、会话持久性、保护限制和设置示例见 desktop.md。

## 形成用户需要的方案

```bash
python3 "<技能目录>/scripts/tune.py" recommend --context '{"intent":"coding"}'
python3 "<技能目录>/scripts/tune.py" recommend --context '{"intent":"office","priority":"quiet"}'
python3 "<技能目录>/scripts/tune.py" recommend --all
```

`recommend` 返回多个选项、适合度、评分理由、代价、是否需要 root、重启或重新登录，以及每个方案的写入项摘要。默认按当前硬件、电源来源和上下文排序，并把最高分作为 `recommended`；`--all` 同时列出当前不可用方案及原因。

新增组合场景 `comfort-office`、`coding-smooth`、`long-battery`、`gaming-low-latency`、`design-accurate`，由电源、图形、显示、特效和空闲行为组件组成，`recommend` 同时给出这些组合候选及组成。新增独立组件 `display-native`、`display-high-refresh`、`display-battery`、`effects-quality`、`effects-reduced`、`idle-balanced`、`idle-battery`、`color-accurate`。详细策略见 [references/profiles.md](references/profiles.md)。

原有方案：

| ID | 目标 | 主要动作 |
| --- | --- | --- |
| `office` | 办公均衡 | 均衡电源、硬件解码、GL 线程、桌面动画、TRIM |
| `programming` | 编程开发 | inotify/句柄/映射上限、降低交换、开发环境加速；数据库需另选 `database` |
| `performance` | 性能优先 | DDE 性能模式、降低交换/缓存回收、关闭无线音频省电 |
| `render-quality` | 画质渲染 | 硬件解码、着色器缓存、保留动画；不改电源 |
| `render-performance` | 低延迟渲染 | 关闭动画、GL 线程、着色器缓存 |
| `gaming` | 游戏性能 | 性能电源、max_map_count、着色器缓存；混合显卡按应用选择独显 |
| `battery` | 续航优先 | 省电模式、Wi-Fi/音频/显示省电、降低磁盘回写 |
| `database` | 数据库调优 | 已安装 PostgreSQL/MariaDB 的保守缓冲配置 |

需要更细粒度控制时，可以只选组件：`power-performance`、`power-balanced`、`power-battery`、`graphics-quality`、`graphics-performance`、`dev-limits`、`database-auto`。例如：

```bash
python3 "<技能目录>/scripts/tune.py" plan --profiles power-balanced,graphics-quality,dev-limits
python3 "<技能目录>/scripts/tune.py" plan --profiles programming,graphics-quality
```

方案可以组合，例如 `--profiles programming,render-quality,database`。电源、图形、开发限制和数据库分别由不同方案负责，`programming` 不再自动包含数据库调优；`render-quality` 不再强制电源模式，因此可与 `programming` 组合。组合中出现同一键的不同目标时，计划会报告 `conflicts` 并拒绝执行；不能自行修改脚本里的值来强行合并。一个方案不可用时不要假装可用：SQLite 只给使用建议，不会因为装了 `sqlite3` 就推荐数据库服务调优。

评分和每个方案的具体动作见 [references/profiles.md](references/profiles.md)。用户只说“优化一下”时，先用 `recommend` 给出少量选项和代价；用户明确要求实施且授权范围覆盖所选方案后，才进入计划执行。

## 生成和执行计划

```bash
python3 "<技能目录>/scripts/tune.py" plan --profiles programming --context '{"intent":"coding"}'
python3 "<技能目录>/scripts/tune.py" plan --profiles office --user-only
```

`plan` 只读取原值并保存计划，不写系统。计划绑定当前用户、登录会话、硬件指纹和 30 分钟有效期；计划生成后原值变化、硬件变化或过期都会拒绝执行。

默认计划包含需要 root 的项。没有 root 或免交互 `sudo -n` 时，这些项会进入 `blocked`，`execute_ready=false`，但仍然可以：

- `plan --user-only`：只保留当前用户可执行项，适合先调整 DDE 电源、环境变量和桌面动画。
- `apply --allow-partial`：明确允许跳过不可执行项，只执行其余项；结果会列出 `skipped`，`complete=false`。不能在用户没有确认跳过范围时使用。

```bash
python3 "<技能目录>/scripts/tune.py" apply --plan-id "plan-真实ID"
python3 "<技能目录>/scripts/tune.py" apply --plan-id "plan-真实ID" --execute
python3 "<技能目录>/scripts/tune.py" apply --plan-id "plan-真实ID" --execute --allow-partial
python3 "<技能目录>/scripts/tune.py" apply --plan-id "plan-真实ID" --execute --allow-service-restart
```

`apply` 默认只预览，并生成将要执行的命令数组；`--execute` 才写入。执行前会重新检查所有原值，任一原值被其他程序改动就整体拒绝，而不是覆盖。每次写入前还会再次读取该操作原值，避免检查与写入之间的竞态。

原值备份在执行前完成：`plan` 把文件完整内容/权限/摘要、gsettings/桌面接口原值、dconfig 类型及默认继承状态、sysctl 运行值、服务状态和电源后端 profile 写入 `plan-…json`；`apply` 在第一次写入前把同一份 `before` 写入 `change-…json`，并在每个操作前后更新状态。即使进程中断，也可根据 `change` 记录或 `restore` 找回原值。系统文件使用 `sudo -n` 的 argv 数组调用，不启动 shell；`sudo -n` 需要密码时会失败并报告，不会弹出交互提示。

`--allow-service-restart` 只允许重启 PostgreSQL/MariaDB 以应用需要重启的参数，绝不重启系统。驱动 `modprobe` 参数只写入配置，脚本不会自动重启、注销或切换图形会话。

### 执行结果的含义

- `applied`：写入并由对应运行接口读回一致；KWin 特效仅保证当前合成器会话。
- `applied_pending_confirmation`：显示已改变，等待用户观察后限时确认。
- `applied_pending_runtime`：dconfig 配置已写，尚无消费者运行态证据。
- `unchanged`：原值已满足目标，没有写入。
- `applied_pending_restart`：配置已写入，但服务需要重启后才完全生效；没有加 `--allow-service-restart` 时会出现。
- `applied_pending_relogin`：environment.d 或 PAM limits 已写入，新登录会话才会继承；当前已运行程序不会自动改变。
- `applied_pending_reboot`：modprobe 驱动参数已写入，重启后才加载。
- `failed`：读回失败；脚本会尝试按逆序恢复已开始的写入。
- `conflict`：原值或当前值被其他程序修改，脚本保留现值，不覆盖用户操作。
- `skipped`：`--allow-partial` 或 advisory 项未执行。

`ok=true` 表示没有失败/冲突，不等于全部立即生效；必须同时看 `complete`、`pending`、`skipped` 和逐项 `status`。部分执行后 `apply.complete=false`，`verify.complete` 也应为 false，不能因为已执行部分验证通过就报告完整完成。`execute_ready=false` 表示完整计划不能执行，先处理 `blocked`/`conflicts`，或明确使用 `--user-only`/`--allow-partial`。

## 验证与恢复

```bash
python3 "<技能目录>/scripts/tune.py" verify --change-id "change-真实ID"
python3 "<技能目录>/scripts/tune.py" evaluate --plan-id "plan-真实ID"
python3 "<技能目录>/scripts/tune.py" rollback --change-id "change-真实ID"
python3 "<技能目录>/scripts/tune.py" rollback --change-id "change-真实ID" --execute
python3 "<技能目录>/scripts/tune.py" restore
python3 "<技能目录>/scripts/tune.py" restore --execute
```

`rollback` 只恢复指定变更；`restore`（别名 `reset`）会按时间从新到旧恢复本技能记录的全部活动变更，回到应用本技能之前的原值。它恢复的是“变更前状态”，不是硬编码的厂商出厂值：如果应用前就是系统默认，恢复后就是默认；如果应用前已有用户自定义，会保留那些自定义。恢复前同样预览，冲突项保留现值。

`verify` 重新读取 gsettings、文件摘要、sysctl 运行值、服务状态或电源后端配置，逐项返回 `matches`、`runtime_matches` 和 `effective`。sysctl 会验证合并文件实际加载的全部键；待登录项在检测到新登录会话（`XDG_SESSION_ID` 或内核登录会话 ID，不使用 `DISPLAY`）后才转为 `active`；待重启项在检测到新 boot ID 后读取模块参数，并按 `Y/N`、`0/1` 统一布尔值比较；数据库等服务项会读取当前服务状态，服务已停止时报告 `mismatch`，待重启项在观察到服务启动时间变化（包括用户外部重启）后转为 `active`。`matches` 表示配置一致且运行态没有明确不一致，模块参数或服务状态不一致时为 false；`effective` 会区分 `active`、`pending_restart`、`pending_reboot`、`pending_relogin`、`mismatch` 和 `skipped`，不会把“文件已写”报告成“已全部生效”。`evaluate` 读取计划保存的基线指标和当前 load/内存压力/温度等，只用于人工对比，不替代指定工作负载的基准测试。

`rollback` 默认只预览恢复命令；`--execute` 才恢复。恢复前检查当前值是否仍等于本次写入的目标；用户之后的手动修改会变成 `conflict` 并保留现值。中断留下的 `applying` 记录也可恢复；如果当前内容是既非目标也非原值的半写入内容，需显式加 `--force`，脚本会明确报告覆盖范围。驱动配置恢复后仍标记 `restored_pending_reboot`，直到检测到启动变化并确认模块参数回到原值；重复恢复在重启前保持 pending。数据库配置恢复后未重启时标记 `restored_pending_restart`。带 `reload` 的配置恢复后会执行相应重载，重载失败保持待重试；environment.d/limits 恢复后若当前进程仍继承调优值，标记 `restored_pending_relogin`，重新登录并确认不再继承后才算完成。恢复结果同时看 `ok` 和 `complete`：`ok` 只表示没有失败/冲突，`complete=false` 表示仍有待重启、待登录或待验证项（例如数据库尚未重新运行），必须继续处理，不能宣称已完全恢复。

计划、变更和原值快照保存在 `${XDG_STATE_HOME:-~/.local/state}/deepin-system-tuning/`，目录 0700，文件 0600。状态目录和托管配置文件名随本 Skill 更名而变化；旧版本记录不会自动迁移，升级前先完成恢复。可以通过本地文件工具查看 `change-*.json` 找到中断前的真实 ID；不要把状态文件当作用户授权凭据。`--execute` 只是防误写开关，用户是否真正同意由 Agent 与宿主工具权限判断，沿用已有授权，不要求重复确认同一范围。

## 安全边界

- 只操作代码白名单内的路径：`environment.d`、`/etc/sysctl.d`、`/etc/modprobe.d`、`/etc/NetworkManager/conf.d`、`/etc/security/limits.d`、已检测到的 PostgreSQL `conf.d` 和 MariaDB `conf.d`。不修改 `/etc/fstab`、GRUB 内核命令行、登录管理器、桌面主题目录或用户连接密码。
- 不解释或执行任意用户字符串。文件写入、服务控制、sysctl、电源后端和数据库重载均来自固定模板；`systemctl reload/restart` 只接受本技能允许的服务和数据库单元。
- 不自动安装软件包、不自动初始化数据库、不自动启用第三方调优守护进程。检测不到 `irqbalance`、`thermald`、`power-profiles-daemon` 时只跳过或给建议。
- 不自动重启、注销、结束应用或切换 X11/Wayland 会话；用户选择的显示和特效设置可修改当前桌面。X11/Wayland 切换只作为会话选项展示，必须在登录界面完成。
- 写入前的原值先持久化；文件按托管块修改，保留原有内容；恢复时逐项检查冲突。并发保护只覆盖本技能，不能阻止控制中心、其他调优工具或用户同时修改。

## 按需参考

| 场景 | 参考文档 |
| --- | --- |
| 完整探测字段、分类含义与设备限制 | [references/hardware.md](references/hardware.md) |
| 方案构成、评分、组合策略与显式设置 | [references/profiles.md](references/profiles.md) |
| 桌面设置、dconfig、显示模式与确认保护 | [references/desktop.md](references/desktop.md) |
| 系统文件路径、托管块、重载语义与限制 | [references/configs.md](references/configs.md) |
| 数据库调优公式、检测边界与恢复 | [references/databases.md](references/databases.md) |
| CLI 参数、状态文件与验收细节 | [references/cli.md](references/cli.md) |
