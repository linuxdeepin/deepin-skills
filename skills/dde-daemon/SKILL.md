---
name: dde-daemon
description: 提供音频、蓝牙、输入设备、语言选择、显示、账户、电源、键盘、定时、系统信息、网络、搜索、手势、系统托盘、剪贴板、X 事件监控、屏幕保护和图像效果的系统级 D-Bus 接口
Categories:
  - Settings
---

# dde-daemon

dde-daemon 是 DDE 后端守护进程组件，通过 Session 和 System 总线提供音频、蓝牙、输入设备、显示、账户、电源、键盘快捷键、定时、系统信息、搜索、手势、系统托盘、剪贴板、X 事件监控、屏幕保护、图像效果、GRUB2 引导和锁屏服务的系统级 D-Bus 接口。

## D-Bus 接口

### 音频管理

提供音频设备、音量、端口和音频服务器管理能力。

详见 [com.deepin.daemon.Audio1.md](references/dbus/com.deepin.daemon.Audio1.md)

### 蓝牙管理

提供蓝牙适配器、设备、文件传输和配对管理能力。

详见 [com.deepin.daemon.Bluetooth1.md](references/dbus/com.deepin.daemon.Bluetooth1.md)

### 输入设备

提供键盘布局和输入设备管理能力。

详见 [com.deepin.daemon.InputDevices1.md](references/dbus/com.deepin.daemon.InputDevices1.md)

### 语言选择

提供系统语言选择和切换能力。

详见 [com.deepin.daemon.LangSelector1.md](references/dbus/com.deepin.daemon.LangSelector1.md)

### 显示管理

提供显示器配置、亮度、旋转和分辨率管理能力。

详见 [com.deepin.daemon.Display1.md](references/dbus/com.deepin.daemon.Display1.md)

### 账户管理

提供用户和用户组创建、删除、查询和属性管理能力。

详见 [com.deepin.daemon.Accounts1.md](references/dbus/com.deepin.daemon.Accounts1.md)

### 电源管理

提供电源策略、亮度、休眠和关机管理能力。

详见 [com.deepin.daemon.Power1.md](references/dbus/com.deepin.daemon.Power1.md)

### 键盘快捷键

提供快捷键绑定、查询和管理能力。

详见 [com.deepin.daemon.Keybinding1.md](references/dbus/com.deepin.daemon.Keybinding1.md)

### 定时设置

提供时区、时间和自动同步设置能力。

详见 [com.deepin.daemon.Timedate1.md](references/dbus/com.deepin.daemon.Timedate1.md)

### 系统信息

提供系统硬件和软件信息查询能力。

详见 [com.deepin.daemon.SystemInfo1.md](references/dbus/com.deepin.daemon.SystemInfo1.md)

### 搜索服务

提供系统搜索和搜索字典管理能力。

详见 [com.deepin.daemon.Search1.md](references/dbus/com.deepin.daemon.Search1.md)

### 会话监控

提供会话状态监控能力。

详见 [com.deepin.daemon.SessionWatcher1.md](references/dbus/com.deepin.daemon.SessionWatcher1.md)

### 声音效果

提供系统声音效果管理能力。

详见 [com.deepin.daemon.SoundEffect1.md](references/dbus/com.deepin.daemon.SoundEffect1.md)

### X 事件监控

提供 X 事件区域监控能力。

详见 [com.deepin.daemon.XEventMonitor1.md](references/dbus/com.deepin.daemon.XEventMonitor1.md)

### 区域管理

提供系统区域设置管理能力。

详见 [com.deepin.daemon.Zone1.md](references/dbus/com.deepin.daemon.Zone1.md)

### 守护进程

提供系统级守护进程管理和调试能力。

详见 [com.deepin.daemon.Daemon1.md](references/dbus/com.deepin.daemon.Daemon1.md)

### 剪贴板管理

提供剪贴板目标管理能力。

详见 [com.deepin.daemon.ClipboardManager1.md](references/dbus/com.deepin.daemon.ClipboardManager1.md)

### 图像效果

提供图像效果查询和删除能力。

详见 [com.deepin.daemon.ImageEffect1.md](references/dbus/com.deepin.daemon.ImageEffect1.md)

### 屏幕保护

提供屏幕保护管理能力。

详见 [com.deepin.daemon.ScreenSaver1.md](references/dbus/com.deepin.daemon.ScreenSaver1.md)

### 系统托盘

提供系统托盘状态通知管理能力。

详见 [org.kde.StatusNotifierWatcher.md](references/dbus/org.kde.StatusNotifierWatcher.md)

### 事件日志

提供系统事件日志记录能力。

详见 [com.deepin.daemon.EventLog1.md](references/dbus/com.deepin.daemon.EventLog1.md)

### 手势管理

提供触摸手势管理能力。

详见 [com.deepin.daemon.Gesture1.md](references/dbus/com.deepin.daemon.Gesture1.md)

### 背光辅助

提供背光亮度和 DDCCI 管理能力。

详见 [com.deepin.daemon.BacklightHelper1.md](references/dbus/com.deepin.daemon.BacklightHelper1.md)

### Greeter

提供 Greeter 主题更新能力。

详见 [com.deepin.daemon.Greeter1.md](references/dbus/com.deepin.daemon.Greeter1.md)

### 锁屏服务

提供锁屏和用户切换能力。

详见 [com.deepin.daemon.LockService1.md](references/dbus/com.deepin.daemon.LockService1.md)

### GRUB2

提供 GRUB2 引导配置管理能力。

详见 [com.deepin.daemon.Grub2.md](references/dbus/com.deepin.daemon.Grub2.md)

### 飞行模式

提供飞行模式开关能力。

详见 [com.deepin.daemon.AirplaneMode1.md](references/dbus/com.deepin.daemon.AirplaneMode1.md)

### UADP

提供 UADP 服务能力。

详见 [com.deepin.daemon.Uadp1.md](references/dbus/com.deepin.daemon.Uadp1.md)

### 交换调度辅助

提供交换分区调度辅助能力。

详见 [com.deepin.daemon.SwapSchedHelper1.md](references/dbus/com.deepin.daemon.SwapSchedHelper1.md)

### 按键事件

提供按键事件监控能力。

详见 [com.deepin.daemon.KeyEvent1.md](references/dbus/com.deepin.daemon.KeyEvent1.md)

### 应用商店会话

提供应用商店会话辅助能力。

详见 [com.deepin.daemon.LastoreSessionHelper1.md](references/dbus/com.deepin.daemon.LastoreSessionHelper1.md)

## DConfig 配置项

dde-daemon 通过 DConfig 暴露显示器、外观、输入设备、鼠标、电源、音效、系统信息、触摸板、触摸屏、小红点和 Wacom 数位板等配置资源。

### 显示器配置

多屏显示模式、亮度、色温、主显示器和输出设备映射等显示相关配置。

详见 [org.deepin.Display](references/config/org.deepin.Display.md)

### 外观配置

缩放排除 Plymouth 等外观配置。

详见 [org.deepin.dde.daemon.appearance](references/config/org.deepin.dde.daemon.appearance.md)

### 输入设备配置

键盘启用状态和鼠标滚轮速度等输入设备配置。

详见 [org.deepin.dde.daemon.inputdevices](references/config/org.deepin.dde.daemon.inputdevices.md)

### 鼠标配置

鼠标加速、双击间隔、拖拽阈值、自然滚动等鼠标配置。

详见 [org.deepin.dde.daemon.mouse](references/config/org.deepin.dde.daemon.mouse.md)

### 电源管理配置

亮度调节、屏保、休眠、定时关机、节能模式等电源管理配置。

详见 [org.deepin.dde.daemon.power](references/config/org.deepin.dde.daemon.power.md)

### 音效配置

系统各种事件（音量变化、登录登出、设备插拔、截图等）的提示音开关配置。

详见 [org.deepin.dde.daemon.soundeffect](references/config/org.deepin.dde.daemon.soundeffect.md)

### 系统信息配置

M900 型号配置标识等系统信息配置。

详见 [org.deepin.dde.daemon.systeminfo](references/config/org.deepin.dde.daemon.systeminfo.md)

### 触摸板配置

触摸板的滚动、点击、拖拽、手掌检测等触摸板配置。

详见 [org.deepin.dde.daemon.touchpad](references/config/org.deepin.dde.daemon.touchpad.md)

### 触摸屏配置

触摸屏的长按、短按、边缘移动停止等触摸屏配置。

详见 [org.deepin.dde.daemon.touchscreen](references/config/org.deepin.dde.daemon.touchscreen.md)

### 小红点配置

小红点（Trackpoint）的移动加速、中键模拟、滚轮模拟等配置。

详见 [org.deepin.dde.daemon.trackpoint](references/config/org.deepin.dde.daemon.trackpoint.md)

### Wacom 数位板配置

Wacom 数位板的压感、采样、按键映射、光标模式等配置。

详见 [org.deepin.dde.daemon.wacom](references/config/org.deepin.dde.daemon.wacom.md)
