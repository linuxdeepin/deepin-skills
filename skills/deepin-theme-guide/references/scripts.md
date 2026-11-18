# 脚本接口、状态与验收

入口为 `scripts/theme.py`，其同目录的 `dde_backend.py` 和 `theme_state.py` 必须一起保留。支持从任意工作目录用绝对路径执行，无需 PYTHONPATH、pip 或网络服务。

## CLI

| 命令 | 行为 |
| --- | --- |
| `doctor` | 检查系统、gdbus、会话和新旧 DDE 接口，不写桌面 |
| `inspect [--monitor 名称]` | 读取能力、现值及壁纸作用范围，不写桌面 |
| `catalog [--kind all\|icon\|cursor\|background]` | 枚举 DDE 认可的资源，不用编造或扫描结果冒充可切换 ID |
| `preview --kind 类型 --id 真实ID` | 请求 DDE 缩略图并返回本地路径；DDE 可能创建缩略图缓存 |
| `plan --request /路径/请求.json` | 保存原值、目标值、壁纸摘要与 30 分钟有效计划，不改桌面 |
| `plan --request -` | 从标准输入接收同样的 JSON |
| `apply --plan-id plan-…` | 默认预览并重检前置条件，不改桌面 |
| `apply --plan-id plan-… --execute` | 执行与逐项读回；失败后尝试逆序恢复 |
| `verify --change-id change-…` | 检查当前接口读回值，不修改设置 |
| `rollback --change-id change-…` | 默认返回恢复预览 |
| `rollback --change-id change-… --execute` | 恢复本次改动，保留之后发生冲突的手动设置 |

除 `--help` 和参数错误外，输出均为 JSON；退出码 0 表示 `ok=true`，2 表示失败、blocked、验证不匹配或需要处理。不要只看进程是否运行完成，还要看 JSON 字段。

## 关键输出

- plan：`plan.id`、`plan.hash`、`plan.spec.operations`、`plan.spec.blocked`、`execute_ready`。
- 预览：`dry_run=true`；不会创建已执行的变更记录。
- 应用：`dry_run=false`、`change.id`、`change.state` 和逐项 `status`。
- 验证：`results[].matches`、`current`、`expected`。
- 恢复：`state=rolled_back` 表示可恢复项已恢复；`needs_attention` 表示至少一项仍需处理。

`unchanged` 表示原值已经满足请求，未写入。`started` 表示已先写恢复日志、随后准备或尝试调用 D-Bus；异常中断时这项需要重新读回。`applied` 表示写入后读回验证通过。`restored` 表示恢复值读回通过或当前已是原值。`conflict` 表示当前值既不是本次目标值也不是原值，脚本保留现值。

## 状态文件

状态目录为 `${XDG_STATE_HOME:-~/.local/state}/uos-theme-personalize/`，目录 0700，计划与变更文件 0600。plan 和 change ID 来自脚本，不允许任意文件路径代替 ID。

计划绑定当前用户、D-Bus 地址、显示会话和系统启动标识。重启、重新登录或不同执行环境可能导致会话校验失败，应在原会话恢复；本包没有跨会话强制恢复选项。计划哈希用于发现意外改动，不能作为抵御当前用户恶意改文件的授权机制。

可以通过本地文件工具查看 `change-*.json` 找到中断前的真实 ID；文件含操作前后值，不含 API Key。状态文件不会自动清理，以免用户试用后失去恢复点。确认不再需要恢复后，再按用户意愿清理对应文件。

`--execute` 是显式写入开关，不是用户身份验证。是否有用户授权由 Agent 与宿主的工具权限共同决定。本脚本不提供网络端口、任意命令执行、sudo、包管理或系统目录写入能力。

## 主题包入口

`theme_pack.py` 负责把生成规范变成独立包，并管理用户级安装：

```bash
theme_pack.py doctor
theme_pack.py create --spec spec.json --output ./theme-dir
theme_pack.py validate --package ./theme-dir
theme_pack.py icon-inventory --scope desktop --output ./icon-inventory.json
theme_pack.py icon-audit --package ./theme-dir --output ./icon-audit.json
theme_pack.py install --package ./theme-dir
theme_pack.py install --package ./theme-dir --execute
theme_pack.py activate --id theme-id
theme_pack.py activate --id theme-id --screensaver --execute
theme_pack.py activate --id cursor-package-id --components cursor --cursor-sync
theme_pack.py verify --id cursor-package-id --observe-seconds 20
theme_pack.py activate --id icons-package-id --components icon --launcher-overrides
theme_pack.py verify --id icons-package-id --components icon --summary
theme_pack.py rollback --change-id change-… --components icon
theme_pack.py rollback --change-id change-… --execute
theme_pack.py uninstall --id theme-id --execute
wallpaper_source.py screen
wallpaper_source.py check --path /绝对路径/wall.jpg
wallpaper_source.py fetch --url https://…/wall.jpg --output /绝对路径/wall.jpg --source-page https://…/page
wallpaper_source.py fetch --url https://…/wall.jpg --output /绝对路径/wall.jpg --source-page https://…/page --execute
```

`create` 生成图标 SVG、光标源文件、活动色、壁纸副本和图片屏保目录。有 `rsvg-convert` 即可编译 Xcursor，优先使用 xcursorgen，缺少时使用内置标准 ARGB 写入器。无光栅化工具时 `cursor.compiled=false`。`install` 不改变当前主题；`activate` 才写 DDE 外观设置。屏保激活需要 `dde-dconfig`、Deepin 自定义屏保组件和显式 `--screensaver`。

`wallpaper_source.py` 是脚本的联网入口，素材搜索使用宿主的 Web/图片搜索工具：`screen` 只读读取当前分辨率（`xrandr`、`wlr-randr`、`xdpyinfo`，可用 `--width/--height` 或 `UOS_THEME_SCREEN` 覆盖）；`check` 只读校验本地图片；`fetch` 默认只做 HEAD 预览，`--execute` 才以 HTTPS 下载并强制内容类型、64 MiB 上限和宽高 ≥ 屏幕，同时计算宽高比偏差作为提示（2% 内视为接近，不阻止），并写入 `<文件>.source.json` 来源记录（URL、作者、许可、来源页、尺寸、SHA-256）。`--license`、`--author` 可选，未知留空；许可不明不阻止下载。直接应用壁纸用 `theme.py plan/apply/verify`；创建主题包时 `create` 复制图片和侧车，把尺寸与来源写入 manifest，摘要或记录被改动时 `validate`/`install` 拒绝继续。详见 [wallpaper.md](wallpaper.md)。

主题包安装记录位于 `${XDG_STATE_HOME:-~/.local/state}/uos-theme-personalize/packages/<id>.json`，变更记录位于同目录 `<id>.active.json`，与普通 `theme.py` 计划记录分开。每次系统写入前都更新原值与执行状态，恢复成功后归档为 `change-<真实ID>.json`。恢复前检查当前值是否仍等于本次目标值；手动改动会变成 conflict，避免覆盖。激活、恢复和卸载共用本技能的写入锁。激活与已应用记录组件重叠时不再要求先回滚：新记录 `before` 保存切换前的值，旧记录立即归档为 `change-<ID>.json` 并标记 `state=superseded`、`superseded_by`，其 change ID 仍可恢复更早基线。启动器的绝对路径覆盖按 `after_hash` 校验后由新记录接管，扫描应用清单时自动忽略本技能写入的覆盖副本，因此切换主题不会让已安装包的 inventory 失效。

安装默认注册原生主题卡片并导入壁纸；desktop-status --id 检查可见性，路径、依赖及清理见 [control-center.md](control-center.md)。--no-desktop-integration 仅用于离线测试。

主题包 activate 的默认预览包含 `execute_ready`、`blocked`、`warnings`、`operations`、`screensaver`、`cursor_sync`、`scope_complete`。预览不预留系统设置，执行时重新读取并保存当时的原值。缺少组件能力会阻止激活；未编译光标会报告缺项，显式选择 `--components cursor` 时阻止执行。默认组合中的缺项通过 `scope_complete=false` 报告，不能概括成全套成功。

图标或光标激活后的 `applied_pending_runtime` 表示设置已写入，但配置一致性或按名加载不通过，返回 `ok=false` 并保留恢复记录；不得理解为没有发生修改。`verify --id` 默认复核包内图标/光标，也可用 `--components icon|cursor` 单独验证。图标分别报告 GTK3 与 Qt6 三档查找、覆盖例外和清单变化；光标报告各层、按名加载和观察窗口内的稳定性。两者均不能验证画风或屏保视觉。详见 [icons.md](icons.md)、[cursor.md](cursor.md)。

图标激活预览还包括 `icon_coverage`、`icon_design`、`design_complete`、`icon_preflight` 和 `launcher_overrides`。待完成设计与绝对路径例外都会在写入前阻止完整激活。用户明确接受缺项时可用 `--allow-partial-icons`，但仍报告 scope_complete=false。create/validate 的 ok=true 只表示包完整，需单独检查 design_complete。审计区分 runtime_verified、technical_scope_complete 与 design_complete，scope_complete 要求技术与设计都完成。范围不完整时 verify/icon-audit 返回 ok=false/退出码 2。`create/validate/install/activate/verify --summary` 省略大量资源和查找行（含待完成设计清单）；`icon-audit --output` 将完整结果写文件，终端仅摘要。

`rollback --components icon,cursor,...` 只恢复所选组件。其他组件继续激活时 state=applied，恢复完毕才归档；新包可接管已恢复的组件。启动器覆盖随 icon 同步恢复，遇到用户编辑保留冲突。

create 输出包含文件摘要；install 将完整包保存到用户资源目录并保留安装清单。激活和卸载会拒绝已被修改的资源，原始生成目录不必继续保留。内置的 `assets/aurora-blue.json` 可用于无图片的首次生成测试。

## 并发、失败与限制

脚本用状态目录文件锁阻止本技能的并发写入；无法阻止控制中心或其他应用同时修改主题。执行前检查原值，恢复前检查现值。执行期间不要切换工作区或更换主显示器；壁纸请求作用于当时的工作区，不具有跨工作区事务锁。

DDE 部分方法异步返回，脚本通过多次读回判断实际结果。超时、进程被强制结束或桌面服务退出时，不保证立即恢复；保留 change 记录并按实际结果处理。恢复也是逐项尽力完成，不是操作系统级原子事务。

接口读回验证不能替代视觉观察。缓存、第三方应用、X11/Wayland 差异都可能导致部分界面未刷新。不要为刷新图标而自动注销、重启桌面或结束应用。

## 目标机试用顺序

1. doctor → inspect → catalog，确认四项支持情况。
2. 只修改两种模式的活动色；先 plan 和默认 apply 预览，再显式执行，verify 后恢复。
3. 从 catalog 选一个与原值不同的光标或图标主题，重复验证与恢复。
4. 用一张本地壁纸验证主显示器当前工作区；有多屏需求再显式指定 monitor。
5. 最后组合四项，确认错误不会被笼统报告成“全部成功”。

## 设计预览与素材来源

`theme_pack.py design-preview --package /绝对路径/包 --output /绝对路径/包外预览.png` 生成明暗背景、实际尺寸与热点预览；可用 .svg，覆盖预览加 --force。`design-report.json` 分列生成、自绘、保留、占位素材；视觉流程、字段与依赖见 [design.md](design.md)。
