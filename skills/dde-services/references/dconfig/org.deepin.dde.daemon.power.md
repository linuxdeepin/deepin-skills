# org.deepin.dde.daemon.power DConfig 配置参考

该文件文档化电源管理的 DConfig 配置项，包括 CPU 调频、节能模式、定时关机、屏幕延时、电源按键动作配置。

## CPU 调频与性能模式

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `supportCpuGovernors` | CPU 支持的 Governor 模式列表 | CPU 支持的 Governor 模式，包括 performance、powersave、userspace、ondemand、conservative、schedutil | array\<string\> | readwrite |
| `specialCpuModeJson` | 特殊处理的 CPU 配置 | 需要进行特殊处理的 CPU 配置，以 JSON 字符串形式存储，按机型名称映射各功耗模式是否可用 | string | readwrite |
| `mode` | 性能模式 | 当前性能模式，可选值：balance（平衡）、performance（高性能）、powersave（节能） | string | readwrite |
| `powerMappingConfig` | 电源性能模式映射配置 | 四种功耗模式（平衡、低电量、高性能、节能）对应的 DSPC 配置映射，以 JSON 字符串形式存储 | string | readwrite |

## 节能模式

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `powerSavingModeAuto` | 使用电池自动开启节能模式 | 使用电池时是否自动开启节能模式 | boolean | readwrite |
| `powerSavingModeEnabled` | 是否开启节能模式 | 是否开启节能模式 | boolean | readwrite |
| `powerSavingModeAutoWhenBatteryLow` | 低电量时自动开启节能模式 | 低电量时是否自动开启节能模式 | boolean | readwrite |
| `powerSavingModeAutoBatteryPercent` | 自动开启节能模式阈值 | 自动开启节能模式的电池电量百分比阈值 | int32 | readwrite |
| `powerSavingModeBrightnessDropPercent` | 节能模式亮度降低百分比 | 节能模式下亮度降低的百分比 | int32 | readwrite |

## 定时关机

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `scheduledShutdownState` | 定时关机开关 | 定时关机功能开关 | boolean | readwrite |
| `shutdownTime` | 关机时间 | 定时关机的触发时间，格式为 HH:MM | string | readwrite |
| `shutdownRepetition` | 重复类型 | 定时关机的重复类型：0=每天、1=工作日、2=周末、3=自定义 | int32 | readwrite |
| `customShutdownWeekDays` | 自定义关机重复日期 | 自定义关机重复日期，数组形式存储星期几（1-7） | array\<string\> | readwrite |
| `shutdownCountdown` | 关机倒计时 | 关机倒计时时长，单位秒 | int32 | readwrite |
| `delayWakeupInterval` | 延时关闭 DDE 黑屏程序时间间隔 | 延时关闭 DDE 黑屏程序的时间间隔，单位毫秒 | int32 | readwrite |
| `nextShutdownTime` | 下一次关机时间 | 下一次关机时间，以 Unix 时间戳形式存储 | int32 | readwrite |

## 屏幕延时配置

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `linePowerScreensaverDelay` | 插电时屏保超时时间 | 插电时显示屏保的超时时间，单位秒 | int32 | readwrite |
| `batteryScreensaverDelay` | 电池时屏保超时时间 | 使用电池时显示屏保的超时时间，单位秒 | int32 | readwrite |
| `linePowerScreenBlackDelay` | 插电时屏幕黑屏延时 | 插电时屏幕黑屏延时，单位秒 | int32 | readwrite |
| `batteryScreenBlackDelay` | 电池时屏幕黑屏延时 | 使用电池时屏幕黑屏延时，单位秒 | int32 | readwrite |
| `linePowerSleepDelay` | 插电时休眠延时 | 插电时休眠延时，单位秒 | int32 | readwrite |
| `batterySleepDelay` | 电池时休眠延时 | 使用电池时休眠延时，单位秒 | int32 | readwrite |
| `linePowerLockDelay` | 插电时锁屏延时 | 插电时锁屏延时，单位秒 | int32 | readwrite |
| `batteryLockDelay` | 电池时锁屏延时 | 使用电池时锁屏延时，单位秒 | int32 | readwrite |
| `linePowerShortIdleDelay` | 插电时短 idle 延时 | 插电时短 idle 延时，单位秒 | int32 | readwrite |
| `batteryShortIdleDelay` | 电池时短 idle 延时 | 使用电池时短 idle 延时，单位秒 | int32 | readwrite |

## 屏幕与亮度控制

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `allowScreenSaver` | 允许屏幕保护 | 是否允许屏幕保护程序运行 | boolean | readwrite |
| `adjustBrightnessEnabled` | 启用自动调节亮度 | 是否启用自动调节亮度功能 | boolean | readwrite |
| `ambientLightAdjustBrightness` | 通过环境光自动调节亮度 | 是否通过环境光传感器自动调节屏幕背光亮度 | boolean | readwrite |
| `screenBlackLock` | 关闭屏幕前锁定 | 关闭屏幕前是否锁定会话 | boolean | readwrite |
| `sleepLock` | 睡眠前锁定 | 系统休眠前是否锁定会话 | boolean | readwrite |
| `delayHandleIdleOffIntervalWhenScreenBlack` | 延时调用 HandleIdleOff 时间间隔 | 屏幕黑屏后延时调用 HandleIdleOff 的时间间隔，单位毫秒 | int32 | readwrite |
| `fullscreenWorkaroundAppList` | 全屏工作模式应用列表 | 全屏工作模式应用列表，列表中的应用在全屏时抑制屏保 | array\<string\> | readwrite |

## 翻盖与电源键动作

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `lidClosedSleep` | 插电时合盖休眠 | 插电时合上翻盖是否休眠 | boolean | readwrite |
| `batteryLidClosedSleep` | 电池时合盖休眠 | 使用电池时合上翻盖是否休眠 | boolean | readwrite |
| `powerButtonPressedExec` | 电源键按下执行的命令 | 电源键按下时执行的命令 | string | readwrite |

## 低电量策略

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `usePercentageForPolicy` | 使用基于电池百分比的策略 | 是否使用基于电池百分比的低电量策略，比剩余时间估算更可靠 | boolean | readwrite |

## 其他

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `powerModuleInitialized` | 电源模块是否初始化 | 电源模块是否已完成初始化 | boolean | readwrite |

## 读写示例

```bash
# 查询当前性能模式
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k mode
# 设置当前性能模式
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k mode -v "performance"

# 查询是否开启节能模式
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k powerSavingModeEnabled
# 设置开启节能模式
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k powerSavingModeEnabled -v "true"

# 查询定时关机开关
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k scheduledShutdownState
# 设置定时关机时间
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k shutdownTime -v "19:00"

# 查询插电时屏幕黑屏延时
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k linePowerScreenBlackDelay
```
