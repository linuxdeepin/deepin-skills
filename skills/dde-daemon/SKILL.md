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

### 资源: `org.deepin.Display`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `blacklist` | 显示器黑名单 | array | readwrite |
| `brightness` | 亮度设置 | string | readwrite |
| `brightnessSetter` | 亮度设置器 | number | readwrite |
| `colorTemperatureMode` | 色温模式 | number | readwrite |
| `currentCustomMode` | 当前自定义模式 | string | readwrite |
| `customDisplayMode` | 自定义显示模式 | number | readwrite |
| `displayMode` | 显示模式 | number | readwrite |
| `mapOutput` | 输出映射 | string | readwrite |
| `primary` | 主显示器 | string | readwrite |
| `priority` | 显示器优先级 | array | readwrite |
| `rateFilter` | 刷新率过滤 | string | readwrite |
| `rotateScreenTimeDelay` | 旋转屏幕延时 | number | readwrite |

```bash
# 查询
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.Display -k blacklist --get
# 设置
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.Display -k blacklist -s "<value>"
```

### 资源: `org.deepin.dde.daemon.appearance`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `scaleWithoutPlymouthEnabled` | 是否启用无 Plymouth 缩放 | bool | readwrite |

```bash
# 查询
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.appearance -k scaleWithoutPlymouthEnabled --get
# 设置
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.appearance -k scaleWithoutPlymouthEnabled -s "<value>"
```

### 资源: `org.deepin.dde.daemon.inputdevices`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `keyboardEnabled` | 键盘是否启用 | bool | readwrite |
| `wheelSpeed` | 滚轮速度 | number | readwrite |

```bash
# 查询
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.inputdevices -k keyboardEnabled --get
# 设置
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.inputdevices -k keyboardEnabled -s "<value>"
```

### 资源: `org.deepin.dde.daemon.mouse`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `adaptiveAccelProfile` | 自适应加速配置 | bool | readwrite |
| `disableTouchpad` | 禁用触摸板 | bool | readwrite |
| `doubleClick` | 双击间隔 | number | readwrite |
| `dragThreshold` | 拖拽阈值 | number | readwrite |
| `leftHanded` | 左手模式 | bool | readwrite |
| `locatePointer` | 定位指针 | bool | readwrite |
| `middleButtonEnabled` | 中键启用 | bool | readwrite |
| `motionAcceleration` | 移动加速度 | number | readwrite |
| `motionScaling` | 移动缩放 | number | readwrite |
| `motionThreshold` | 移动阈值 | number | readwrite |
| `naturalScroll` | 自然滚动 | bool | readwrite |

```bash
# 查询
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.mouse -k adaptiveAccelProfile --get
# 设置
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.mouse -k adaptiveAccelProfile -s "<value>"
```

### 资源: `org.deepin.dde.daemon.power`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `adjustBrightnessEnabled` | 亮度调节启用 | bool | readwrite |
| `allowScreenSaver` | 允许屏保 | bool | readwrite |
| `ambientLightAdjustBrightness` | 环境光调节亮度 | bool | readwrite |
| `batteryLidClosedSleep` | 电池模式合盖休眠 | bool | readwrite |
| `batteryLockDelay` | 电池模式锁屏延时 | number | readwrite |
| `batteryScreenBlackDelay` | 电池模式息屏延时 | number | readwrite |
| `batteryScreensaverDelay` | 电池模式屏保延时 | number | readwrite |
| `batterySleepDelay` | 电池模式休眠延时 | number | readwrite |
| `customShutdownWeekDays` | 自定义关机星期 | array | readwrite |
| `delayHandleIdleOffIntervalWhenScreenBlack` | 息屏时空闲关闭处理延时 | number | readwrite |
| `delayWakeupInterval` | 唤醒延时 | number | readwrite |
| `fullscreenWorkaroundAppList` | 全屏绕过应用列表 | array | readwrite |
| `lidClosedSleep` | 合盖休眠 | bool | readwrite |
| `linePowerLockDelay` | 电源模式锁屏延时 | number | readwrite |
| `linePowerScreenBlackDelay` | 电源模式息屏延时 | number | readwrite |
| `linePowerScreensaverDelay` | 电源模式屏保延时 | number | readwrite |
| `linePowerSleepDelay` | 电源模式休眠延时 | number | readwrite |
| `mode` | 电源模式 | string | readwrite |
| `nextShutdownTime` | 下次关机时间 | number | readwrite |
| `powerButtonPressedExec` | 电源键按下执行动作 | string | readwrite |
| `powerMappingConfig` | 电源映射配置 | string | readwrite |
| `powerModuleInitialized` | 电源模块是否初始化 | bool | readwrite |
| `powerSavingModeAuto` | 自动节能模式 | bool | readwrite |
| `powerSavingModeAutoBatteryPercent` | 自动节能电量百分比 | number | readwrite |
| `powerSavingModeAutoWhenBatteryLow` | 低电量自动节能 | bool | readwrite |
| `powerSavingModeBrightnessDropPercent` | 节能亮度降低百分比 | number | readwrite |
| `powerSavingModeEnabled` | 节能模式启用 | bool | readwrite |
| `scheduledShutdownState` | 定时关机状态 | bool | readwrite |
| `screenBlackLock` | 息屏锁定 | bool | readwrite |
| `shutdownCountdown` | 关机倒计时 | number | readwrite |
| `shutdownRepetition` | 关机重复 | number | readwrite |
| `shutdownTime` | 关机时间 | string | readwrite |
| `sleepLock` | 休眠锁定 | bool | readwrite |
| `specialCpuModeJson` | 特殊 CPU 模式配置 | string | readwrite |
| `supportCpuGovernors` | 支持的 CPU 调速器 | array | readwrite |
| `usePercentageForPolicy` | 是否使用百分比策略 | bool | readwrite |

```bash
# 查询
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k adjustBrightnessEnabled --get
# 设置
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k adjustBrightnessEnabled -s "<value>"
```

### 资源: `org.deepin.dde.daemon.soundeffect`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `audio-volume-change` | 音量变化提示音 | bool | readwrite |
| `camera-shutter` | 快门提示音 | bool | readwrite |
| `complete-copy` | 复制完成提示音 | bool | readwrite |
| `complete-print` | 打印完成提示音 | bool | readwrite |
| `desktop-login` | 桌面登录提示音 | bool | readwrite |
| `desktop-logout` | 桌面注销提示音 | bool | readwrite |
| `device-added` | 设备添加提示音 | bool | readwrite |
| `device-removed` | 设备移除提示音 | bool | readwrite |
| `dialog-error` | 对话框错误提示音 | bool | readwrite |
| `dialog-error-critical` | 严重错误提示音 | bool | readwrite |
| `dialog-error-serious` | 严重对话框错误提示音 | bool | readwrite |
| `enabled` | 声音效果启用 | bool | readwrite |
| `message` | 消息提示音 | bool | readwrite |
| `player` | 播放器选择 | number | readwrite |
| `power-plug` | 电源插入提示音 | bool | readwrite |
| `power-unplug` | 电源拔出提示音 | bool | readwrite |
| `power-unplug-battery-low` | 低电量拔出电源提示音 | bool | readwrite |
| `screen-capture` | 截屏提示音 | bool | readwrite |
| `screen-capture-complete` | 截屏完成提示音 | bool | readwrite |
| `suspend-resume` | 挂起恢复提示音 | bool | readwrite |
| `system-shutdown` | 系统关机提示音 | bool | readwrite |
| `trash-empty` | 清空回收站提示音 | bool | readwrite |
| `x-deepin-app-sent-to-desktop` | 应用发送到桌面提示音 | bool | readwrite |

```bash
# 查询
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.soundeffect -k audio-volume-change --get
# 设置
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.soundeffect -k audio-volume-change -s "<value>"
```

### 资源: `org.deepin.dde.daemon.systeminfo`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `IsM900Config` | 是否为 M900 配置 | bool | readwrite |

```bash
# 查询
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.systeminfo -k IsM900Config --get
# 设置
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.systeminfo -k IsM900Config -s "<value>"
```

### 资源: `org.deepin.dde.daemon.touchpad`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `deltaScroll` | 滚动增量 | number | readwrite |
| `disableWhileTyping` | 打字时禁用触摸板 | bool | readwrite |
| `doubleClick` | 双击间隔 | number | readwrite |
| `dragThreshold` | 拖拽阈值 | number | readwrite |
| `edgeScrollEnabled` | 边缘滚动启用 | bool | readwrite |
| `horizScrollEnabled` | 水平滚动启用 | bool | readwrite |
| `leftHanded` | 左手模式 | bool | readwrite |
| `motionAcceleration` | 移动加速度 | number | readwrite |
| `motionScaling` | 移动缩放 | number | readwrite |
| `motionThreshold` | 移动阈值 | number | readwrite |
| `naturalScroll` | 自然滚动 | bool | readwrite |
| `palmDetect` | 手掌检测 | bool | readwrite |
| `palmMinPressure` | 手掌最小压力 | number | readwrite |
| `palmMinWidth` | 手掌最小宽度 | number | readwrite |
| `tapToClick` | 点击触摸板 | bool | readwrite |
| `touchpadEnabled` | 触摸板启用 | bool | readwrite |
| `vertScrollEnabled` | 垂直滚动启用 | bool | readwrite |

```bash
# 查询
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.touchpad -k deltaScroll --get
# 设置
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.touchpad -k deltaScroll -s "<value>"
```

### 资源: `org.deepin.dde.daemon.touchscreen`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `edgemovestopDuration` | 边缘移动停止延时 | number | readwrite |
| `longpressBlacklist` | 长按黑名单 | array | readwrite |
| `longpressDuration` | 长按延时 | number | readwrite |
| `shortpressDuration` | 短按延时 | number | readwrite |

```bash
# 查询
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.touchscreen -k edgemovestopDuration --get
# 设置
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.touchscreen -k edgemovestopDuration -s "<value>"
```

### 资源: `org.deepin.dde.daemon.trackpoint`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `leftHanded` | 左手模式 | bool | readwrite |
| `middleButtonEnabled` | 中键启用 | bool | readwrite |
| `middleButtonTimeout` | 中键超时 | number | readwrite |
| `motionAcceleration` | 移动加速度 | number | readwrite |
| `motionScaling` | 移动缩放 | number | readwrite |
| `motionThreshold` | 移动阈值 | number | readwrite |
| `wheelEmulation` | 滚轮模拟 | bool | readwrite |
| `wheelEmulationButton` | 滚轮模拟按钮 | number | readwrite |
| `wheelEmulationTimeout` | 滚轮模拟超时 | number | readwrite |
| `wheelHorizScroll` | 水平滚轮 | bool | readwrite |

```bash
# 查询
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.trackpoint -k leftHanded --get
# 设置
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.trackpoint -k leftHanded -s "<value>"
```

### 资源: `org.deepin.dde.daemon.wacom`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `cursorMode` | 光标模式 | bool | readwrite |
| `eraserPressureSensitive` | 橡皮压力灵敏度 | number | readwrite |
| `eraserRawSample` | 橡皮原始采样 | number | readwrite |
| `eraserThreshold` | 橡皮阈值 | number | readwrite |
| `forceProportions` | 强制比例 | bool | readwrite |
| `keyDownAction` | 按键按下动作 | number | readwrite |
| `keyUpAction` | 按键抬起动作 | number | readwrite |
| `leftHanded` | 左手模式 | bool | readwrite |
| `mapOutput` | 映射输出 | string | readwrite |
| `mouseEnterRemap` | 鼠标进入重新映射 | bool | readwrite |
| `stylusPressureSensitive` | 触控笔压力灵敏度 | number | readwrite |
| `stylusRawSample` | 触控笔原始采样 | number | readwrite |
| `stylusThreshold` | 触控笔阈值 | number | readwrite |
| `suppress` | 抑制值 | number | readwrite |

```bash
# 查询
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.wacom -k cursorMode --get
# 设置
pkexec dde-dconfig -a org.deepin.dde.daemon -r org.deepin.dde.daemon.wacom -k cursorMode -s "<value>"
```

