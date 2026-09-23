# org.deepin.dde.daemon.power

电源管理配置资源，控制自动调节亮度开关、允许屏幕保护、环境光自动调节亮度、电池模式合盖休眠、电池模式锁屏延时、电池模式黑屏延时、电池模式屏保延时、电池模式休眠延时、定时关机重复日期、黑屏空闲处理间隔、黑屏程序唤醒延时、全屏抑制屏保应用列表、插电模式合盖休眠、插电模式锁屏延时、插电模式黑屏延时、插电模式屏保延时、插电模式休眠延时、电源性能模式、下一次关机时间、电源键按下执行命令、功耗模式映射配置、电源模块初始化状态、电池模式自动节能、自动节能电量阈值、低电量自动节能、节能模式亮度降低比例、节能模式开关、定时关机开关、黑屏前锁定、关机倒计时、定时关机重复类型、定时关机时间、休眠前锁定、特殊 CPU 配置、CPU 支持的调频模式、基于电量百分比的策略电源相关配置。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `adjustBrightnessEnabled` | 自动调节亮度开关 | 控制是否启用自动调节屏幕亮度功能 | bool | readwrite |
| `allowScreenSaver` | 允许屏幕保护 | 控制是否允许启动屏幕保护程序 | bool | readwrite |
| `ambientLightAdjustBrightness` | 环境光自动调节亮度 | 控制是否根据环境光强度自动调节屏幕背光亮度 | bool | readwrite |
| `batteryLidClosedSleep` | 电池模式合盖休眠 | 控制使用电池供电时合上笔记本盖子是否进入休眠 | bool | readwrite |
| `batteryLockDelay` | 电池模式锁屏延时 | 配置使用电池供电时自动锁屏的延时时间（分钟） | number | readwrite |
| `batteryScreenBlackDelay` | 电池模式黑屏延时 | 配置使用电池供电时自动关闭屏幕的延时时间（分钟） | number | readwrite |
| `batteryScreensaverDelay` | 电池模式屏保延时 | 配置使用电池供电时启动屏保的延时时间（分钟） | number | readwrite |
| `batterySleepDelay` | 电池模式休眠延时 | 配置使用电池供电时进入休眠的延时时间（分钟） | number | readwrite |
| `customShutdownWeekDays` | 定时关机重复日期 | 配置定时关机在一周中重复执行的日期 | array | readwrite |
| `delayHandleIdleOffIntervalWhenScreenBlack` | 黑屏空闲处理间隔 | 配置屏幕黑屏后延时调用空闲处理的时间间隔（毫秒） | number | readwrite |
| `delayWakeupInterval` | 黑屏程序唤醒延时 | 配置延时关闭 DDE 黑屏程序的时间间隔 | number | readwrite |
| `fullscreenWorkaroundAppList` | 全屏抑制屏保应用列表 | 配置当列表中的应用处于全屏状态时抑制屏保启动 | array | readwrite |
| `lidClosedSleep` | 插电模式合盖休眠 | 控制使用外接电源时合上笔记本盖子是否进入休眠 | bool | readwrite |
| `linePowerLockDelay` | 插电模式锁屏延时 | 配置使用外接电源时自动锁屏的延时时间（分钟） | number | readwrite |
| `linePowerScreenBlackDelay` | 插电模式黑屏延时 | 配置使用外接电源时自动关闭屏幕的延时时间（分钟） | number | readwrite |
| `linePowerScreensaverDelay` | 插电模式屏保延时 | 配置使用外接电源时启动屏保的延时时间（分钟） | number | readwrite |
| `linePowerSleepDelay` | 插电模式休眠延时 | 配置使用外接电源时进入休眠的延时时间（分钟） | number | readwrite |
| `mode` | 电源性能模式 | 配置当前电源性能模式（平衡模式、高性能模式、节能模式） | string | readwrite |
| `nextShutdownTime` | 下一次关机时间 | 记录定时关机的下一次执行时间 | number | readwrite |
| `powerButtonPressedExec` | 电源键按下执行命令 | 配置按下电源键时执行的命令 | string | readwrite |
| `powerMappingConfig` | 功耗模式映射配置 | 配置四种功耗模式（平衡、高性能、节能、自定义）对应的具体参数 | string | readwrite |
| `powerModuleInitialized` | 电源模块初始化状态 | 标记电源管理模块是否已完成初始化 | bool | readwrite |
| `powerSavingModeAuto` | 电池模式自动节能 | 控制使用电池供电时是否自动开启节能模式 | bool | readwrite |
| `powerSavingModeAutoBatteryPercent` | 自动节能电量阈值 | 配置电池电量低于此百分比时自动开启节能模式 | number | readwrite |
| `powerSavingModeAutoWhenBatteryLow` | 低电量自动节能 | 控制电池电量过低时是否自动开启节能模式 | bool | readwrite |
| `powerSavingModeBrightnessDropPercent` | 节能模式亮度降低比例 | 配置开启节能模式时屏幕亮度降低的百分比 | number | readwrite |
| `powerSavingModeEnabled` | 节能模式开关 | 控制是否开启节能模式 | bool | readwrite |
| `scheduledShutdownState` | 定时关机开关 | 控制定时关机功能的启用状态 | bool | readwrite |
| `screenBlackLock` | 黑屏前锁定 | 控制关闭屏幕前是否先锁定屏幕 | bool | readwrite |
| `shutdownCountdown` | 关机倒计时 | 配置定时关机的倒计时时间 | number | readwrite |
| `shutdownRepetition` | 定时关机重复类型 | 配置定时关机的重复类型（0-3），包括每天、每周、每月 | number | readwrite |
| `shutdownTime` | 定时关机时间 | 配置定时关机的执行时间 | string | readwrite |
| `sleepLock` | 休眠前锁定 | 控制进入休眠前是否先锁定屏幕 | bool | readwrite |
| `specialCpuModeJson` | 特殊 CPU 配置 | 配置需要进行特殊处理的 CPU 型号及其对应的功耗模式参数（JSON 格式） | string | readwrite |
| `supportCpuGovernors` | CPU 支持的调频模式 | 记录当前 CPU 支持的调频 Governor 模式列表 | array | readwrite |
| `usePercentageForPolicy` | 基于电量百分比的策略 | 控制是否使用基于电池百分比的电源策略，比剩余时间估算更可靠，可规避固件问题 | bool | readwrite |

## 读写示例

```bash
# 查询节能模式开关
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k powerSavingModeEnabled
# 设置节能模式开关
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k powerSavingModeEnabled -v "<value>"
```

## 覆盖说明

- 该资源存在 Override 覆盖：`allowAdjustAmdGPU` 被 `org.deepin.dde.daemon/org.deepin.dde.daemon.power/4000-org.deepin.dde.daemon.power.override.json` 覆盖
