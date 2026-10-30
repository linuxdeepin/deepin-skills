# org.deepin.dde.daemon.power DConfig 配置参考

电源管理的统一 DConfig 参考。资源为 `org.deepin.dde.daemon.power`，appId 为 `org.deepin.dde.daemon`；dde-daemon 与 dde-services 的相关任务均使用本页，不分别维护单位或枚举副本。

## 单位、版本与作用范围

- 屏保、黑屏、睡眠、锁屏和短空闲的 Delay 值使用**秒**。十分钟应写 `600`，不能写 `10`。`delayWakeupInterval` 和 `delayHandleIdleOffIntervalWhenScreenBlack` 使用毫秒；`shutdownCountdown` 使用秒。
- `shutdownRepetition`：`0` 单次、`1` 每天、`2` 工作日、`3` 自定义。周末使用自定义日期，不存在独立“周末”枚举；`shutdownTime` 使用 `HH:MM`。
- 配置按具体 key 的 flags、权限及目标用户生效；flags 含 global 的项为共享值，不能将整个资源视为当前用户私有配置。
- 写入前读取部署版本的元数据、当前值和服务能力。元数据只给出枚举范围时，不依据数值大小猜含义；版本与本页不匹配且不能核实时停止写入。不要通过写入初始化标记或硬件能力缓存来模拟配置成功。

### 核对依据

本页记录的单位及枚举已核对：dde-services `1.0.47.0` 安装的 DConfig 元数据（资源文件名同上）；dde-control-center 源码修订 `5987b369e` 中 `src/plugin-power/operation/powerworker.cpp` 的 `converToDataMap`（分钟乘 60、小时乘 3600），以及 `src/plugin-power/qml/GeneralPage.qml` 的重复类型列表（Once、Every day、Working days、Custom Time）。这些核对结论已包含在本页，使用时不依赖源码目录。

安装版本可能改变配置项、权限或实现；以部署版本核验结果为准。

## CPU 调频与性能模式

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `supportCpuGovernors` | CPU 支持的 Governor 模式列表 | 服务维护的 CPU Governor 能力列表；仅查询，不通过改写列表宣称支持新模式 | array | readwrite |
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
| `shutdownRepetition` | 重复类型 | 定时关机的重复类型：0=单次、1=每天、2=工作日、3=自定义 | int32 | readwrite |
| `customShutdownWeekDays` | 自定义关机重复日期 | 自定义关机重复日期，星期序号数组（1=周一，7=周日）；元素类型须按部署版本元数据与消费接口核对 | array | readwrite |
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
| `fullscreenWorkaroundAppList` | 全屏工作模式应用列表 | 全屏工作模式应用列表，列表中的应用在全屏时抑制屏保 | array | readwrite |

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

## 运行状态（仅查询）

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `powerModuleInitialized` | 电源模块是否初始化 | 由服务维护的初始化标记，不作为用户设置修改 | boolean | 部署元数据可能允许写入，本 Skill 仅查询 |

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

## 数值示例

以下示例仅在用户明确要求对应设置，并已核对元数据、供电模式和当前值后执行：

```bash
# 插电与电池供电时均十分钟自动锁屏：每项均为 600 秒
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k linePowerLockDelay -v 600
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k batteryLockDelay -v 600
# 每天重复：枚举为 1；此操作不自动代表已授权开启定时关机
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.power -k shutdownRepetition -v 1
```

逐项回读验证，并记录原值及是否默认值。恢复原覆盖值时写回原值；原本为默认值时仅 reset 对应 key，不重置整个资源。
