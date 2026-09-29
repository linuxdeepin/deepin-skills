---
name: dde-daemon
description: dde-daemon 是 DDE 桌面环境的核心后端守护进程，负责管理系统音频、显示、电源、输入设备、语言与区域、系统信息、账户、蓝牙与飞行模式、搜索、锁屏与屏保、登录界面、GRUB 启动、会话与守护进程、剪贴板、事件日志与监控、应用商店会话、统一应用数据保护、状态通知、外观配置、默认应用设置和 X 权限修复。本 skill 按功能点组织，每个功能领域下同时包含相关的 D-Bus 接口文档、CLI 命令使用说明和 DConfig 配置项参考。
Categories:
  - Settings
---

# dde-daemon

dde-daemon 是 DDE 桌面环境的核心后端守护进程，通过 Session 和 System 总线提供系统级 D-Bus 接口，同时提供 CLI 命令和 DConfig 配置项。以下按功能点组织，每个功能领域下同时列出相关的 D-Bus 接口、CLI 命令和 DConfig 配置项的参考文档。

## 音频管理

- **D-Bus**: [Audio1](references/dbus/org.deepin.dde.Audio1.md) — 提供系统级音频设备管理能力，包括音频设备、音量、端口和音频服务器管理，影响所有应用的音频输入输出，而非仅控制单个应用的音量。
- **D-Bus**: [SoundEffect1](references/dbus/org.deepin.dde.SoundEffect1.md) — 提供系统声音效果管理能力。
- **CLI**: [soundeffect](references/cli/soundeffect.md) — 声音效果守护进程，负责管理系统事件音效的播放。
- **DConfig**: [org.deepin.dde.daemon.soundeffect](references/config/org.deepin.dde.daemon.soundeffect.md) — 音量变化音效、相机快门音效、文件复制完成音效、打印完成音效、桌面登录音效、桌面登出音效、设备添加音效、设备移除音效、错误对话框音效、严重错误对话框音效、重要错误对话框音效、音效总开关、消息通知音效、音效播放器、电源插入音效、电源拔出音效、低电量提示音效、截图开始音效、截图完成音效、系统唤醒音效、系统关机音效、清空回收站音效、应用发送到桌面音效配置。

## 显示管理

- **D-Bus**: [Display1](references/dbus/org.deepin.dde.Display1.md) — 提供显示器配置、亮度、旋转和分辨率管理能力。
- **D-Bus**: [BacklightHelper1](references/dbus/org.deepin.dde.BacklightHelper1.md) — 提供背光亮度和 DDCCI 管理能力。
- **CLI**: [backlight_helper](references/cli/backlight_helper.md) — 背光调节辅助工具，用于在权限受限的环境中设置屏幕背光亮度。
- **CLI**: [greeter-display-daemon](references/cli/greeter-display-daemon.md) — 登录界面显示守护进程，负责在 LightDM 登录阶段管理显示配置。
- **DConfig**: [org.deepin.Display](references/config/org.deepin.Display.md) — 不支持的屏幕黑名单、屏幕亮度、亮度设置方式、色温调节模式、当前自定义模式 ID、自定义显示模式、多屏显示模式、显示器映射关系、主屏幕、输出设备优先级、刷新率过滤器、屏幕旋转延时配置。

## 电源管理

- **DConfig**: [org.deepin.dde.daemon.power](references/config/org.deepin.dde.daemon.power.md) — 自动调节亮度开关、允许屏幕保护、电池模式合盖休眠、电池模式锁屏延时、电池模式黑屏延时、电池模式屏保延时、电池模式短空闲延时、电池模式休眠延时、定时关机重复日期、黑屏空闲处理间隔、黑屏程序唤醒延时、全屏抑制屏保应用列表、插电模式合盖休眠、插电模式锁屏延时、插电模式黑屏延时、插电模式屏保延时、插电模式短空闲延时、插电模式休眠延时、电源性能模式、下一次关机时间、电源键按下执行命令、功耗模式映射配置、电源模块初始化状态、电池模式自动节能、自动节能电量阈值、低电量自动节能、节能模式亮度降低比例、节能模式开关、定时关机开关、黑屏前锁定、关机倒计时、定时关机重复类型、定时关机时间、休眠前锁定、特殊 CPU 配置、CPU 支持的调频模式、基于电量百分比的策略配置。

## 输入设备管理

- **D-Bus**: [InputDevices1](references/dbus/org.deepin.dde.InputDevices1.md) — 提供键盘布局和输入设备管理能力。
- **D-Bus**: [Gesture1](references/dbus/org.deepin.dde.Gesture1.md) — 提供触摸手势管理能力。
- **DConfig**: [org.deepin.dde.daemon.inputdevices](references/config/org.deepin.dde.daemon.inputdevices.md) — 键盘启用状态、鼠标滚轮速度配置。
- **DConfig**: [org.deepin.dde.daemon.mouse](references/config/org.deepin.dde.daemon.mouse.md) — 自适应加速配置、接入鼠标时禁用触控板、双击时间间隔、拖拽阈值、左手鼠标模式、定位指针、中键模拟、鼠标加速倍数、鼠标速度缩放、鼠标加速阈值、自然滚动配置。
- **DConfig**: [org.deepin.dde.daemon.touchpad](references/config/org.deepin.dde.daemon.touchpad.md) — 自然滚动增量、打字时禁用触控板、触控板双击时间间隔、触控板拖拽阈值、边缘滚动、水平滚动、触控板按键方向、触控板加速倍数、触控板速度缩放、触控板加速阈值、自然滚动、手掌检测、手掌检测最小压力、手掌检测最小宽度、轻触点击、触控板开关、垂直滚动配置。
- **DConfig**: [org.deepin.dde.daemon.touchscreen](references/config/org.deepin.dde.daemon.touchscreen.md) — 边缘移动停止时间、长按黑名单、长按持续时间、短按持续时间配置。
- **DConfig**: [org.deepin.dde.daemon.trackpoint](references/config/org.deepin.dde.daemon.trackpoint.md) — 左手模式、中键模拟、中键超时时间、小红点加速倍数、小红点速度缩放、小红点加速阈值、滚轮模拟、滚轮模拟按键、滚轮模拟超时、滚轮水平滚动配置。
- **DConfig**: [org.deepin.dde.daemon.wacom](references/config/org.deepin.dde.daemon.wacom.md) — Wacom 光标模式、橡皮擦压感级别、橡皮擦采样窗口大小、橡皮擦压力阈值、强制比例匹配、下键操作映射、上键操作映射、Wacom 旋转设置、映射输出设备、跨屏重新映射、触控笔压感级别、触控笔采样窗口大小、触控笔压力阈值、坐标变化抑制阈值配置。

## 语言与区域设置

- **D-Bus**: [LangSelector1](references/dbus/org.deepin.dde.LangSelector1.md) — 提供系统语言选择和切换能力。
- **D-Bus**: [Timedate1](references/dbus/org.deepin.dde.Timedate1.md) — 提供时区、时间和自动同步设置能力。
- **CLI**: [langselector](references/cli/langselector.md) — 语言选择守护进程，负责管理系统的语言和区域设置。

## 系统信息

- **D-Bus**: [SystemInfo1](references/dbus/org.deepin.dde.SystemInfo1.md) — 提供系统硬件和软件信息查询能力。
- **DConfig**: [org.deepin.dde.daemon.systeminfo](references/config/org.deepin.dde.daemon.systeminfo.md) — M900 配置标识配置。

## 账户管理

- **D-Bus**: [Accounts1](references/dbus/org.deepin.dde.Accounts1.md) — 提供用户和用户组创建、删除、查询和属性管理能力。

## 蓝牙与飞行模式

- **D-Bus**: [Bluetooth1](references/dbus/org.deepin.dde.Bluetooth1.md) — 提供蓝牙适配器、设备、文件传输和配对管理能力。
- **D-Bus**: [AirplaneMode1](references/dbus/org.deepin.dde.AirplaneMode1.md) — 提供飞行模式开关能力。

## 搜索服务

- **D-Bus**: [Search1](references/dbus/org.deepin.dde.Search1.md) — 提供系统搜索和搜索字典管理能力。
- **CLI**: [search](references/cli/search.md) — DDE 文件搜索工具，是 dde-daemon 提供的文件全文搜索引擎后端。

## 锁屏与屏保

- **D-Bus**: [LockService1](references/dbus/org.deepin.dde.LockService1.md) — 提供锁屏和用户切换能力。
- **D-Bus**: [org.freedesktop.ScreenSaver](references/dbus/org.freedesktop.ScreenSaver.md) — 提供屏幕保护管理能力。
- **CLI**: [dde-lockservice](references/cli/dde-lockservice.md) — DDE 锁屏服务工具，用于触发系统锁屏。

## 登录界面管理

- **D-Bus**: [Greeter1](references/dbus/org.deepin.dde.Greeter1.md) — 提供 Greeter 主题更新能力。
- **CLI**: [dde-greeter-setter](references/cli/dde-greeter-setter.md) — 登录界面设置工具，用于在 LightDM 登录阶段配置 greeter 相关参数。

## GRUB 启动管理

- **D-Bus**: [Grub2](references/dbus/org.deepin.dde.Grub2.md) — 提供 GRUB2 引导配置管理能力。
- **CLI**: [grub2](references/cli/grub2.md) — GRUB2 相关工具，用于 GRUB 启动菜单的图形模式检测、主题设置和系统编号查询。

## 会话与守护进程管理

- **D-Bus**: [Daemon1](references/dbus/org.deepin.dde.Daemon1.md) — 提供系统级守护进程管理和调试能力。
- **D-Bus**: [SessionWatcher1](references/dbus/org.deepin.dde.SessionWatcher1.md) — 提供会话状态监控能力。
- **D-Bus**: [SwapSchedHelper1](references/dbus/org.deepin.dde.SwapSchedHelper1.md) — 提供交换分区调度辅助能力。
- **CLI**: [dde-session-daemon](references/cli/dde-session-daemon.md) — DDE 会话守护进程，是 DDE 桌面会话中运行的后台核心服务。
- **CLI**: [dde-system-daemon](references/cli/dde-system-daemon.md) — DDE 系统守护进程，是 DDE 桌面环境中运行在系统级别的核心后台服务。

## 剪贴板管理

- **D-Bus**: [ClipboardManager1](references/dbus/org.deepin.dde.ClipboardManager1.md) — 提供剪贴板目标管理能力。

## 事件日志与监控

- **D-Bus**: [EventLog1](references/dbus/org.deepin.dde.EventLog1.md) — 提供系统事件日志记录能力。
- **D-Bus**: [KeyEvent1](references/dbus/org.deepin.dde.KeyEvent1.md) — 提供按键事件监控能力。
- **D-Bus**: [XEventMonitor1](references/dbus/org.deepin.dde.XEventMonitor1.md) — 提供 X 事件区域监控能力。

## 应用商店会话

- **D-Bus**: [LastoreSessionHelper1](references/dbus/org.deepin.dde.LastoreSessionHelper1.md) — 提供应用商店会话辅助能力。

## 统一应用数据保护

- **D-Bus**: [Uadp1](references/dbus/org.deepin.dde.Uadp1.md) — 提供 UADP 服务能力。

## 状态通知

- **D-Bus**: [org.kde.StatusNotifierWatcher](references/dbus/org.kde.StatusNotifierWatcher.md) — 提供系统托盘状态通知管理能力。

## 外观配置

- **DConfig**: [org.deepin.dde.daemon.appearance](references/config/org.deepin.dde.daemon.appearance.md) — 缩放排除 Plymouth 配置。

## 默认应用设置

- **CLI**: [default-file-manager](references/cli/default-file-manager.md) — 默认文件管理器设置工具，用于查询和设置系统默认文件管理器。
- **CLI**: [default-terminal](references/cli/default-terminal.md) — 默认终端设置工具，用于查询和设置系统默认终端模拟器。

## X 权限修复

- **CLI**: [fix-xauthority-perm](references/cli/fix-xauthority-perm.md) — Xauthority 权限修复工具，用于修正 `.Xauthority` 文件的权限问题。
