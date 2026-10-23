# dde-daemon

dde-daemon 提供桌面后端的 CLI、D-Bus 和 DConfig 能力，以下按接口类型索引。同名电源、快捷键与手势接口在 Treeland 会话可由 dde-services 提供，调用前确认实际 Bus 与服务归属。

当前用户语言与系统默认 locale 分开管理；事件音效策略与底层声音播放器协作。剪贴板后端保存与前端历史管理不同；空闲抑制与屏保本体、锁屏认证不同。默认终端和文件管理器工具只启动已配置的应用。

账户删除、引导配置与会话状态变更的影响见对应参考页；只读查询不因使用 System 总线而统一提权。

## CLI 命令

### 音频管理

- [soundeffect](cli/soundeffect.md) — 声音效果守护进程，负责管理系统事件音效的播放。

### 显示管理

- [backlight_helper](cli/backlight_helper.md) — 背光调节辅助工具，用于在权限受限的环境中设置屏幕背光亮度。
- [greeter-display-daemon](cli/greeter-display-daemon.md) — 登录界面显示守护进程，负责在 LightDM 登录阶段管理显示配置。

### 语言与区域设置

- [langselector](cli/langselector.md) — 语言选择守护进程，负责管理当前用户桌面语言及可用语言列表。

### 搜索服务

- [search](cli/search.md) — 接收应用提供的候选字符串集合并提供拼音与模糊搜索，不扫描文件正文。

### 登录用户选择

- [dde-lockservice](cli/dde-lockservice.md) — 为登录界面保存选中的用户名，不直接触发锁屏。

### 登录界面管理

- [dde-greeter-setter](cli/dde-greeter-setter.md) — 登录界面设置工具，用于在 LightDM 登录阶段配置 greeter 相关参数。

### GRUB 启动管理

- [grub2](cli/grub2.md) — GRUB2 相关工具，用于 GRUB 启动菜单的图形模式检测、主题设置和系统编号查询。

### 会话与守护进程管理

- [dde-session-daemon](cli/dde-session-daemon.md) — DDE 会话守护进程，是 DDE 桌面会话中运行的后台核心服务。
- [dde-system-daemon](cli/dde-system-daemon.md) — DDE 系统守护进程，是 DDE 桌面环境中运行在系统级别的核心后台服务。

### 默认应用启动

- [default-file-manager](cli/default-file-manager.md) — 启动当前用户配置的默认文件管理器，不修改默认关联。
- [default-terminal](cli/default-terminal.md) — 启动当前用户配置的默认终端，不修改默认关联。

### X 权限修复

- [fix-xauthority-perm](cli/fix-xauthority-perm.md) — Xauthority 权限修复工具，用于修正 `.Xauthority` 文件的权限问题。

## D-Bus 接口

### 音频管理

- [Audio1](dbus/org.deepin.dde.Audio1.md) — 提供系统级音频设备管理能力，包括音频设备、音量、端口和音频服务器管理，影响所有应用的音频输入输出，而非仅控制单个应用的音量。
- [SoundEffect1](dbus/org.deepin.dde.SoundEffect1.md) — 管理当前用户事件音效开关，与底层声音主题播放器协作。

### 显示管理

- [Display1](dbus/org.deepin.dde.Display1.md) — 提供显示器配置、亮度、旋转和分辨率管理能力。
- [BacklightHelper1](dbus/org.deepin.dde.BacklightHelper1.md) — 提供背光亮度和 DDCCI 管理能力。

### 输入设备管理

- [InputDevices1](dbus/org.deepin.dde.InputDevices1.md) — 提供键盘布局和输入设备管理能力。
- [Gesture1](dbus/org.deepin.dde.Gesture1.md) — 提供触摸手势管理能力。

### 语言与区域设置

- [LangSelector1](dbus/org.deepin.dde.LangSelector1.md) — 管理当前用户桌面语言，重新登录后生效。
- [Timedate1](dbus/org.deepin.dde.Timedate1.md) — 提供时区、时间和自动同步设置能力。

### 系统信息

- [SystemInfo1](dbus/org.deepin.dde.SystemInfo1.md) — 提供系统硬件和软件信息查询能力。

### 账户管理

- [Accounts1](dbus/org.deepin.dde.Accounts1.md) — 提供用户和用户组创建、删除、查询和属性管理能力。

### 蓝牙与飞行模式

- [Bluetooth1](dbus/org.deepin.dde.Bluetooth1.md) — 提供蓝牙适配器、设备、文件传输和配对管理能力。
- [AirplaneMode1](dbus/org.deepin.dde.AirplaneMode1.md) — 提供飞行模式开关能力。

### 搜索服务

- [Search1](dbus/org.deepin.dde.Search1.md) — 创建并检索调用方提供的候选字符串集合，返回匹配条目。

### 登录用户选择与空闲抑制

- [LockService1](dbus/org.deepin.dde.LockService1.md) — 查询和保存登录界面选中的用户名，不直接切换会话。
- [org.freedesktop.ScreenSaver](dbus/org.freedesktop.ScreenSaver.md) — 提供会话空闲计时、绑定调用连接的空闲抑制和活动模拟；不控制屏保动画或解除锁屏。

### 登录界面管理

- [Greeter1](dbus/org.deepin.dde.Greeter1.md) — 提供 Greeter 主题更新能力。

### GRUB 启动管理

- [Grub2](dbus/org.deepin.dde.Grub2.md) — 提供 GRUB2 引导配置管理能力。

### 会话与守护进程管理

- [SessionWatcher1](dbus/org.deepin.dde.SessionWatcher1.md) — 提供会话状态监控能力。
- [SwapSchedHelper1](dbus/org.deepin.dde.SwapSchedHelper1.md) — 提供交换分区调度辅助能力。

### 剪贴板管理

- [ClipboardManager1](dbus/org.deepin.dde.ClipboardManager1.md) — 提供剪贴板目标管理能力。

### 事件日志与监控

- [EventLog1](dbus/org.deepin.dde.EventLog1.md) — 提供系统事件日志记录能力。
- [KeyEvent1](dbus/org.deepin.dde.KeyEvent1.md) — 提供按键事件监控能力。
- [XEventMonitor1](dbus/org.deepin.dde.XEventMonitor1.md) — 提供 X 事件区域监控能力。

### 应用商店会话

- [LastoreSessionHelper1](dbus/org.deepin.dde.LastoreSessionHelper1.md) — 提供应用商店会话辅助能力。

### 统一应用数据保护

- [Uadp1](dbus/org.deepin.dde.Uadp1.md) — 提供 UADP 服务能力。

### 状态通知

- [org.kde.StatusNotifierWatcher](dbus/org.kde.StatusNotifierWatcher.md) — 提供系统托盘状态通知管理能力。

## DConfig 配置项

### 音频管理

- [org.deepin.dde.daemon.soundeffect](config/org.deepin.dde.daemon.soundeffect.md) — 当前用户事件音效开关与播放策略。

### 显示管理

- [org.deepin.Display](config/org.deepin.Display.md) — 显示器布局、亮度、色温与模式配置。

### 电源管理

- [org.deepin.dde.daemon.power](config/org.deepin.dde.daemon.power.md) — 电源延时、自动锁屏、休眠、低电量动作与定时关机策略。

### 输入设备管理

- [org.deepin.dde.daemon.inputdevices](config/org.deepin.dde.daemon.inputdevices.md) — 键盘启用状态、鼠标滚轮速度配置。
- [org.deepin.dde.daemon.mouse](config/org.deepin.dde.daemon.mouse.md) — 鼠标加速、速度、按键与滚动配置。
- [org.deepin.dde.daemon.touchpad](config/org.deepin.dde.daemon.touchpad.md) — 触控板按键、手势、滚动、速度和误触防护配置。
- [org.deepin.dde.daemon.touchscreen](config/org.deepin.dde.daemon.touchscreen.md) — 边缘移动停止时间、长按黑名单、长按持续时间、短按持续时间配置。
- [org.deepin.dde.daemon.trackpoint](config/org.deepin.dde.daemon.trackpoint.md) — 指点杆速度、加速、按键映射与滚动配置。
- [org.deepin.dde.daemon.wacom](config/org.deepin.dde.daemon.wacom.md) — 数位板按键、压感、旋转与屏幕映射配置。

### 系统信息

- [org.deepin.dde.daemon.systeminfo](config/org.deepin.dde.daemon.systeminfo.md) — M900 配置标识配置。

### 外观配置

- [org.deepin.dde.daemon.appearance](config/org.deepin.dde.daemon.appearance.md) — 缩放排除 Plymouth 配置。
