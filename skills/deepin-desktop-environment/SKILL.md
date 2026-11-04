---
name: deepin-desktop-environment
description: 查询、使用和配置 deepin/UOS 的 DDE 桌面与系统设置。按用户意图查询和调整 DDE 全局主题与 Qt/DTK 应用外观、GTK 主题、图标主题、深色模式、壁纸与轮播、字体名称与大小、光标、缩放和窗口效果；查询登录会话路径与进程 PID、会话锁定状态、当前工作区、窗口管理器、X 设置属性与缩放、已注册应用数量与显示名称、系统版本和内存容量；查询电池是否存在、电池状态与当前供电方式，管理音量、音频设备与事件音效、亮度、多显示器与分辨率、电源模式、合盖休眠、空闲锁屏和定时关机；查询键盘布局列表、布局指示器、输入法运行状态与 NumLock 状态，调整键盘布局、鼠标、触控板、数位板、快捷键和手势；控制蓝牙配对与飞行模式，探查 polkit 认证代理成员，查询用户组、校验用户名，管理账户、人脸认证、密码策略和登录设置；使用启动器、任务栏、托盘、通知与勿扰模式，查询剪贴板前端与守护进程状态，管理剪贴板历史，通过应用管理器打开或启动应用并管理默认关联；配置桌面语言、区域格式、时区与时间；管理锁屏、屏保、会话抑制、注销与关机，使用触屏校准和会话提示界面；打开控制中心、查询设置模块、搜索设置并跳转指定页面；通过公开 DConfig 资源发现、查询、修改和恢复配置，核对用户、权限与作用范围；查询和调整 GRUB 启动配置；查询桌面门户外观偏好、用户信息与后台运行能力，发送和撤回门户通知，探测全局快捷键能力及 D-Bus 服务、对象树和接口。只读查询、布尔判断和列表计数同样适用。用户无需知道组件名称，可通过相关公开 D-Bus、CLI 和 DConfig 控制面完成操作并验证结果。
Categories:
  - Settings
---

# deepin-desktop-environment

根据用户意图操作 DDE 的公开控制面。先从下表选取并读取参考页，再执行查询或修改；具体参数、类型、方法、权限及示例以该页为准，需要更多能力时再读对应组件的 `index.md`。只读、只输出布尔值或整数、不创建文件均不妨碍读取本 Skill 和所需参考页；最终回复仍遵守用户要求的格式。本页只维护跨组件意图和能力边界，不绑定当前会话实现；组件接口细节由各自的 `references/` 目录维护。

## 状态来源约束

- 查询 DDE 当前状态时，以本 Skill 列出的 daemon D-Bus 属性、方法或公开 CLI 的返回值为准。
- `gsettings`、`xset`、`loginctl`、`xprop` 和 `.desktop` 文件计数可能滞后于 daemon，或反映的是不同层次的状态，不能替代 DDE 控制面的权威结果。
- 只读查询同样先按意图表读取对应属性或方法；不要因为任务简单或命令更常见就改用旁路工具。用户明确指定其他工具或数据来源时遵守其要求，并区分该来源与 DDE 状态的语义。
- 汇总与巡检先逐项确定“字段 → 接口/属性 → 语义”，分别读取，标注来源；原样输出请求只返回对应原值。当前值读属性，可用集合读列表，统计只计数解析后的集合，不沿用历史测试常量。
- 以下查询与探测规则适用于本 Skill 的所有 D-Bus 接口：先从对应参考页确认 Bus、服务名、对象路径和接口名，不从名称相互推导。查询状态使用文档定义的可读属性或查询方法，并按返回类型解析；不能仅凭方法名称判断是否只读。
- 用户要求服务或能力探测、接口缺失或签名不符时，按需使用 `busctl --user tree <service>` 和 `busctl --user introspect <service> <path>`；System 总线改用 `--system`。只确认服务是否运行时先通过总线的 `NameHasOwner` 查询，避免向目标服务发送可能自动激活它的请求。探测不调用设置、显示、启动或创建会话的方法。
- 区分服务未运行、不可激活、对象/接口缺失与权限错误；父对象可用不代表子接口存在，也不能将探测失败当作 false、零或空集合。

## 意图与参考资料

以下路径均相对本 Skill 根目录。一次任务涉及多个组件时，只读取所需部分。

| 用户意图 | 优先读取 | 补充与分流 |
| --- | --- | --- |
| DDE 全局主题与 Qt/DTK 应用外观、GTK 主题、图标主题 | [Appearance1](references/dde-appearance/dbus/org.deepin.dde.Appearance1.md) | `GlobalTheme` 是 DDE 全局主题，`GtkTheme` 只表示 GTK 主题；Qt 活动色与滚动条策略分别用 `QtActiveColor`、`QtScrollBarPolicy` |
| 深色模式、壁纸、字体名称与大小、光标、缩放、圆角、背景 URI | [Appearance1](references/dde-appearance/dbus/org.deepin.dde.Appearance1.md) | 读取 `StandardFont`、`FontSize`、`Background` 等属性；工作区与窗口操作读 [appearance 索引](references/dde-appearance/index.md)；轮播、缓存读 [services 索引](references/dde-services/index.md)；`gsettings` 结果可能滞后，不作权威来源 |
| 音量、音频设备、事件音效 | [Audio1](references/dde-daemon/dbus/org.deepin.dde.Audio1.md)、[SoundEffect1](references/dde-daemon/dbus/org.deepin.dde.SoundEffect1.md) | 底层声音主题播放读 [api 索引](references/dde-api/index.md) |
| 亮度、分辨率、多显示器、旋转 | [Display1](references/dde-daemon/dbus/org.deepin.dde.Display1.md) | 背光辅助见 [daemon 索引](references/dde-daemon/index.md)，环境亮度见 [services 索引](references/dde-services/index.md) |
| 合盖、休眠、自动锁屏、电源延时、定时关机 | [电源策略](references/dde-daemon/config/org.deepin.dde.daemon.power.md) | 会话策略与动作读 [Session Power1](references/dde-services/dbus/org.deepin.dde.Power1.Session.md)；按实际会话及服务可用性选用 |
| 是否装有电池、电池状态、充电信息、节能与性能模式、CPU 调频 | [System Power1](references/dde-services/dbus/org.deepin.dde.Power1.System.md) | 电池是否存在读 `HasBattery`，是否使用电池供电读 `OnBattery`；位于 System 总线，不能将服务缺失当成没有电池 |
| 键盘布局、鼠标、触控板、数位板、手势 | [daemon 索引](references/dde-daemon/index.md)中的输入设备及配置 | 手势能力按 [services 索引](references/dde-services/index.md) 的对应接口确认；布局指示菜单读 [tray 索引](references/dde-tray-loader/index.md) |
| 键盘布局指示器与输入法运行状态 | [Keyboard1](references/dde-tray-loader/dbus/org.deepin.dde.Keyboard1.md) | 分别读取 `layout` 与 `fcitxRunning`；指示器可为空，实际输入布局读 InputDevices1，进程搜索不能代替接口状态 |
| 键盘布局列表与数量 | [InputDevices1](references/dde-daemon/dbus/org.deepin.dde.InputDevices1.md) | `AllLayoutList` 是全集，`UserLayoutList` 是已添加列表，`LayoutList` 是筛选后的候选字典；各集合的条目数分别表示对应范围的布局数量 |
| NumLock 数字锁定是否开启 | [Keybinding1.GetNumLockState](references/dde-services/dbus/org.deepin.dde.Keybinding1.md) | 先核对部署版本的返回类型和状态枚举，再转换为布尔值；不调用设置方法来探测状态 |
| 快捷键查询、修改、冲突检查 | [Keybinding1](references/dde-services/dbus/org.deepin.dde.Keybinding1.md) | 调用前用 `gdbus introspect` 核对当前可用的服务、方法集与签名 |
| 蓝牙配对、关闭蓝牙、飞行模式 | [Bluetooth1](references/dde-daemon/dbus/org.deepin.dde.Bluetooth1.md)、[AirplaneMode1](references/dde-daemon/dbus/org.deepin.dde.AirplaneMode1.md) | 底层蓝牙阻止状态读 [api 索引](references/dde-api/index.md) |
| 账户、用户组数量、用户名是否可用、登录界面 | [Accounts1](references/dde-daemon/dbus/org.deepin.dde.Accounts1.md) | `GetGroups` 解析后计数；`IsUsernameValid` 取布尔返回项；登录和快速登录见 [session-shell 索引](references/dde-session-shell/index.md) |
| 人脸认证、密码策略、图形授权 | [人脸管理](references/deepin-face/index.md)、[密码策略](references/deepin-pw-check/index.md)、[授权说明](references/dde-polkit-agent/index.md) | 按目标用户、设备和方法核对权限 |
| 锁屏界面、屏保、空闲抑制 | [session-shell 索引](references/dde-session-shell/index.md)、[屏保索引](references/deepin-screensaver/index.md) | 空闲计时与抑制读 [ScreenSaver](references/dde-daemon/dbus/org.freedesktop.ScreenSaver.md)；抑制不解除锁屏 |
| 会话锁定状态（只读） | [SessionManager1.Locked](references/dde-session/dbus/org.deepin.dde.SessionManager1.md) | `LockFront1.Visible` 只表示锁屏界面可见性，`loginctl` 的 `LockedHint` 也不可替代 `Locked` |
| 当前桌面会话进程 PID | dde-session 项目 `org.deepin.dde.Session1.GetSessionPid` | logind Leader 与进程搜索不是同一语义 |
| 会话路径 | [Session1.GetSessionPath](references/dde-session/dbus/org.deepin.dde.Session1.md)、[SessionManager1.CurrentSessionPath](references/dde-session/dbus/org.deepin.dde.SessionManager1.md) | 返回 login1 会话对象路径；不要用 `loginctl` 的 `session-N.scope` 名称代替 |
| 窗口管理器兼容标签、合成状态 | [WMSwitcher1.CurrentWM](references/dde-session/dbus/org.deepin.dde.WMSwitcher1.md) | `CurrentWM` 是方法，返回合成状态兼容标签，不是实际窗口管理器可执行文件名 |
| X 设置属性清单、缩放与双击间隔 | [XSettings1.ListProps](references/dde-services/dbus/org.deepin.dde.XSettings1.md) | `ListProps` 解析后计数；缩放读 `GetScaleFactor`；双击间隔先发现 `Net/DoubleClickTime` 再读写并回读 |
| 已注册应用数量、应用 ID 与默认显示名称 | [ApplicationManager1.List](references/dde-application-manager/dbus/org.desktopspec.ApplicationManager1.md) | `List` 是 `ao` 属性；`.desktop` 文件数不等于应用管理器注册的应用数 |
| 注销、重启、关机、挂起、会话抑制 | [session 索引](references/dde-session/index.md) | 普通注销用会话管理器 RequestLogout；退出管理进程与完整注销不同；显示关机界面不等于执行关机 |
| 通知中心支持的能力名称 | [Notification1.GetCapabilities](references/dde-shell/dbus/org.deepin.dde.Notification1.md) | 读取本次返回的能力数组；方法、信号名称不是通知能力列表 |
| 启动器、任务栏、通知、勿扰、OSD | [启动器索引](references/dde-launchpad/index.md)、[shell 索引](references/dde-shell/index.md) | 充电保护、托盘驻留配置见 [tray 索引](references/dde-tray-loader/index.md) |
| 剪贴板前端与守护进程是否可用、对象树与接口名、窗口和历史恢复 | [clipboard 索引](references/dde-clipboard/index.md) | 只读探测分别读取前端与守护进程的对象树和接口；不调用显示、切换或恢复方法；后端拥有者与保存协议见 [daemon 索引](references/dde-daemon/index.md) |
| 打开或启动应用、默认应用关联、应用实例 | [application-manager 索引](references/dde-application-manager/index.md) | 通过应用管理器定位应用并启动；默认终端/文件管理器工具只启动已配置程序，不修改关联 |
| 刷新应用列表后按应用 ID 启动 | [ApplicationManager1](references/dde-application-manager/dbus/org.desktopspec.ApplicationManager1.md)、[Application](references/dde-application-manager/dbus/org.desktopspec.ApplicationManager1.Application.md) | `ReloadApplications` 后从 `List` 定位目标 ID 并调用该对象的 `Launch`；不直接执行应用程序替代管理器启动 |
| 桌面语言、区域格式、时区、时间 | [daemon 索引](references/dde-daemon/index.md)、[DTK 用户配置](references/dtk/index.md) | 系统默认 locale 读 [api 索引](references/dde-api/index.md)，与当前用户语言分开 |
| 系统版本、发行版、处理器、内存容量 | [SystemInfo1（Session）](references/dde-daemon/dbus/org.deepin.dde.SystemInfo1.md) | 同名服务在 Session 与 System 总线属性集不同；版本与发行版走 Session，DMI 与显卡驱动走 System |
| 打开控制中心、跳转设置页、设置入口显隐 | [control-center 索引](references/dde-control-center/index.md) | 隐藏模块或设备管理入口不改变后端功能开关 |
| 公开 DConfig 资源发现、配置项枚举与计数、读取、修改和恢复 | [dde-dconfig](references/dde-app-services/cli/dde-dconfig.md)、[ConfigManager.Manager](references/dde-app-services/dbus/org.desktopspec.ConfigManager.Manager.md) | 配置资源说明提供资源与 key 的含义；通用枚举由 CLI 或管理器 `keyList` 提供，权限与作用范围见 [app-services 索引](references/dde-app-services/index.md) |
| 会话提示、触屏校准、配对确认界面 | [session-ui 索引](references/dde-session-ui/index.md) | 显示界面和执行系统动作分开处理 |
| GRUB 启动项、引导主题 | [Grub2](references/dde-daemon/dbus/org.deepin.dde.Grub2.md)、[api 索引](references/dde-api/index.md) | 属于高影响系统配置，修改前核对恢复条件 |
| 桌面门户外观设置、用户信息、后台运行、通知及全局快捷键能力 | [Portal 前端查询与边界](references/xdg-desktop-portal-dde/index.md) | 按任务读取前端接口资料并核对实际部署；后端 impl 协议不能代替前端调用与授权 |

## 操作工作流

1. **只读探测。** 确认系统版本、当前用户、图形会话类型（X11、Wayland/Treeland）、目标组件版本及服务是否存在。读取目标当前值与必要的能力信息；按参考页确认 Bus、服务名、对象路径、方法和参数。查询当前系统提供的功能时必须实际探测，不能仅依据文档总结。参考资料不代表所有部署版本都提供该能力，不能仅凭 Wayland 就认定使用 Treeland。
2. **核对变更与授权。** 明确目标值、目标用户、影响范围及用户已有授权。普通可逆设置已有明确授权时直接执行；目标不清或授权不足时先澄清。账户删除、密码策略、认证数据删除、GRUB、飞行模式/蓝牙断连、强制终止应用及注销/关机等高影响动作，要具体说明数据、网络连接或会话中断影响；已有授权须覆盖该影响，否则先取得确认。只读查询不因使用 System 总线而统一提权，受限写操作走服务端授权与图形认证流程。
3. **记录恢复条件。** 对可恢复设置记录原值、目标值、资源、key、用户及恢复方法；只改所需项。DConfig 同时检查类型、公开可见性、权限、是否默认值及共享标志；恢复默认值与恢复原值不同，不能用整组 reset 代替单项恢复。敏感信息不记录到日志或回复，不保存密码、密钥及生物特征数据；账户删除等不可逆操作不能承诺回滚。
4. **执行并验证。** 使用参考页中的公开 CLI 或 D-Bus 操作，一次处理明确目标；DConfig 默认使用当前用户身份的 `dde-dconfig`。回读实际值，必要时检查界面或状态；重登后生效的设置明确说明生效条件。会话抑制按接口要求保留并释放 cookie，不混用不同抑制协议。
5. **处理失败并报告。** 服务不存在、版本不支持或权限不足时，说明探测结果；有文档支持才切换替代入口。不要重复启动后台守护进程、伪造方法或绕过授权。失败后先核对当前状态，在适合且已获授权时恢复原值；报告实际修改、验证结果、待生效条件及恢复方式，不把命令提交成功当成设置生效。
