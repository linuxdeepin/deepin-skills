# 控制中心、显示、窗口特效与 dconfig

入口：`tune.py settings` 返回当前会话实际可用的语义设置、原值、后端、作用域、类型/范围和 dconfig 资源清单。`inspect` 的 `desktop_native` 保留完整清单；`inspect --summary` 保留设置与输出摘要。

控制中心是用户入口；执行使用经 introspection 检查的 DDE D-Bus 接口或 ConfigManager。旧 GSettings schema 存在不能证明当前服务仍消费该配置。优先读取 Power1 运行模式；新服务不可用时才考虑 power-profiles-daemon/tuned。实际探测完成后不会仅因旧 schema 存在而写入旧电源键。旧版兼容快照保留原 GSettings 路径，不能据此保证新版 DDE 生效。

## 显式设置与场景默认

```bash
python3 "<技能目录>/scripts/tune.py" settings
python3 "<技能目录>/scripts/tune.py" plan --profiles comfort-office --user-only
python3 "<技能目录>/scripts/tune.py" plan --profiles coding-smooth --settings '{"power.mode":"balance","outputs":{"eDP-1":{"resolution":[2880,1920],"refresh":120,"brightness":0.7}},"display.auto_brightness":false,"effects.blur":false}'
```

显示器名称、分辨率、刷新率和支持项必须取自本机 `settings` 输出；上例仅示意，不能直接假定另一台机器支持。`--settings` 与 `--context` 中的 `settings` 二选一。显式设置覆盖所选方案中同一语义键的默认值；未被显式覆盖的方案冲突仍会拒绝执行。

`outputs` 是显示器名到配置对象的映射，可同时指定多个输出。每个输出支持：

| 字段 | 类型/单位 | 行为 |
| --- | --- | --- |
| `resolution` | `[宽,高]`，像素 | 与 refresh 一起匹配实际 Modes；省略时保留当前分辨率 |
| `refresh` | 数字，Hz | 仅选择该分辨率下受支持的模式；允许 0.1 Hz 内的标称误差 |
| `brightness` | 0.05–1.0 | 使用可读回、可保存的屏幕亮度接口；不以 xrandr gamma 模拟背光 |
| `scale` | 1.0–3.0 | 按屏缩放；恢复时保留原有显式/继承关系；客户端可能需重新登录 |
| `position` | `[x,y]`，有符号整数 | 调整布局，不关闭输出 |

分辨率与刷新率合并成一个 `display.mode` 操作，禁止分别选择互不兼容的值。仅修改刷新率时不会为了找到低刷而自动降低分辨率。模式写入使用 Monitor.SetMode + Display.ApplyChanges/Save；亮度使用 SetAndSaveBrightness；缩放使用 Appearance.Get/SetScreenScaleFactors。控制中心尚有未提交显示改动时，显示计划会拒绝执行。

## 显示确认与独立回滚保护

模式、布局、主屏和缩放实际改变时，脚本在写入前启动独立恢复进程并完成启动握手，保存 30 秒截止时间。成功写入后仍是 `applied_pending_confirmation`，`complete=false`。用户观察到画面正常后才执行：

```bash
python3 "<技能目录>/scripts/tune.py" confirm-display --change-id change-真实ID
```

不能仅根据模式读回一致替用户确认可见性。超时后，即使原 apply 进程已退出，恢复进程也会尝试逆序回滚整次变更。确认必须在原登录会话且截止时间之前完成；已确认则取消自动恢复。待确认期间拒绝执行其他计划。手动 `rollback` 会取消等待并立即尝试恢复。

显示恢复仍依赖当前图形服务、输出和原模式可用；进程被强制杀死、会话结束或输出断开时不能保证恢复画面。后续手动改成第三值会报告 conflict 并保留。恢复进程失败会将记录标为 `needs_attention`，不能宣称已恢复。多个输出的硬件变更不是原子事务。

## 可调设置白名单

可用性以实际服务、元数据权限和设备能力为准。未探测到的显式请求进入 blocked，不会偷偷换成不相关的 GNOME 设置。

| 语义设置 | 说明 |
| --- | --- |
| `power.mode` | `balance` / `performance` / `powersave`；读取系统 Power1.Mode，调用 SetMode |
| `power.saving` | 省电开关 |
| `power.auto_battery`、`power.auto_low_battery` | 电池供电/低电量自动省电 |
| `power.low_battery_percent` | 自动省电电量阈值，5–50 |
| `power.brightness_drop_percent` | 省电亮度衰减百分比，0–80 |
| `display.auto_brightness` | 自动亮度；开启前检查设备支持 |
| `display.color_temperature_mode` | 0 关闭、1 自动、2 手动 |
| `display.color_temperature` | 手动色温，1000–10000 K |
| `display.primary` | 主屏名称 |
| `display.auto_scale` | DDE 自动缩放策略，dconfig 配置验证 |
| `idle.ac.*`、`idle.battery.*` | screen_off / sleep / lock / screensaver 为 0–86400 秒；lid_action 为服务枚举 0–3，使用前结合设备说明确认枚举含义 |
| `idle.lock_on_sleep`、`idle.lock_on_screen_off` | 休眠/熄屏时锁屏 |
| `effects.compositing` | 仅支持可切换的 X11 合成器；不用于 Wayland |
| `effects.blur`、`effects.fade`、`effects.scale`、`effects.minimize`、`effects.slidingpopups` | 仅暴露 KWin 报告支持的特效；加载/卸载后读回，仅当前合成器会话有效 |
| `effects.blur_strength`、`effects.glass` | 活动 Treeland 的模糊强度/玻璃效果；不因为安装了 schema 就认定正在运行 Treeland |
| `effects.opacity`、`effects.window_radius` | X11 与 Treeland 分别使用本机对应 dconfig；opacity 在 X11 为 0.1–1.0，在 Treeland 为 10–100 |
| `input.mouse.natural_scroll`、`input.mouse.acceleration` | 自然滚动/加速度；X11 范围 0.1–3.0，Treeland 范围 -1–1 |
| `input.touchpad.natural_scroll`、`input.touchpad.tap_to_click`、`input.touchpad.disable_while_typing` | 自然滚动、轻触点击、打字时禁用 |
| `input.keyboard.repeat_enabled`、`input.keyboard.repeat_interval` | X11 键盘重复；间隔 10–1000 ms |
| `input.keyboard.repeat_delay`、`input.keyboard.repeat_rate` | 延迟 100–2000 ms；repeat_rate 仅活动 Treeland，1–100 次/秒 |
| `sound.effects`、`audio.mono`、`audio.noise_reduction` | 系统音效、单声道和降噪配置；只在用户明确指定时改变 |

## dconfig 发现、权限与恢复

读取 `/usr/share/dsg/configs` 中 DDE daemon、control-center、appearance、KWin、Treeland 的已安装资源，展示键、permissions、flags，以及 `supported` / `readonly` / `inventory_only` 覆盖状态。`inventory_only` 包括未适配项，也包括由 D-Bus 服务管理而未开放原始键写入的配置。这个清单用于发现和说明覆盖范围，不是任意键写入入口。

只修改 `tune_desktop.py` 中登记的语义白名单。通过 ConfigManager.acquireManagerV2 按当前 uid 获取对象，读取 value、isDefaultValue 和有效 permissions，并及时 release。元数据标为 readonly 或服务策略禁止写入时拒绝。带 global 标志的原始 dconfig 项按系统级操作处理，需要 root/免交互 sudo，`--user-only` 会移除。

原值记录包含类型和默认继承状态。原先继承默认时用 reset 恢复；原先显式设置时写回原类型的原值，避免把继承默认变成固定值。配置读回相同只证明持久化值一致，通用 dconfig 项返回 `configured_unverified` / `applied_pending_runtime`，运行态为 null，complete=false；恢复后同样报告 `restored_pending_runtime`。后续由专门消费者接口验证后才能完善为运行态确认，当前不会自行推定已生效。

不要直接编辑 `/usr/share/dsg/configs` 元数据、管理员 override、控制中心模块显隐策略或 Treeland 的“上次保存输出状态”。部分键是内部缓存或界面可用性策略。VRR/HDR、色彩配置文件和未知 Wayland 合成器的专用接口当前仅可发现/说明，尚不提供自动执行。

## 跨设置约束

- 固定亮度要求自动亮度关闭；省电亮度衰减非零时必须显式选择衰减为 0 或放弃固定亮度。
- 手动色温要求色温模式为 2；色彩准确场景选择模式 0，不宣称完成显示器校色。
- 关闭合成不能与显式启用模糊、透明或窗口动画叠加；减少特效组件保留合成器。
- 自动电池省电可能在供电或电量变化时覆盖固定电源模式，计划会说明。场景按生成计划时的电源状态选择，不安装常驻自动切换服务。
- KWin 当前会话效果、dconfig 持久化值、实际消费者运行态分别汇报，不把它们混成统一的“已生效”。

官方接口语义参考 [DConfig 文档](https://linuxdeepin.github.io/dtkcore/classDtk_1_1Core_1_1DConfig.html)。目标机 introspection 和元数据优先于远端版本。
