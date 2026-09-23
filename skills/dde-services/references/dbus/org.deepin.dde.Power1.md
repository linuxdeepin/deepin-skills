# org.deepin.dde.Power1 接口参考

该接口提供电源管理能力，包括电源状态查询、延时配置和电源操作。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Power1` |
| Object path | `/org/deepin/dde/Power1` |
| Interface | `org.deepin.dde.Power1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 电源操作

#### Reset

重置电源配置为默认值。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.Reset
```

#### SetPrepareSuspend

设置挂起准备状态。

- **输入参数**: `state`（int32, 类型 `i`）：状态
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.SetPrepareSuspend 1
```


### 电源状态属性

#### OnBattery（属性）

是否使用电池供电。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 OnBattery
```
#### UseWayland（属性）

是否使用 Wayland。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 UseWayland
```
#### LidIsPresent（属性）

是否存在翻盖。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LidIsPresent
```
#### BatteryIsPresent（属性）

电池是否存在。

| 属性 | 值 |
|------|------|
| 类型 | `map` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryIsPresent
```
#### BatteryPercentage（属性）

电池百分比。

| 属性 | 值 |
|------|------|
| 类型 | `map` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryPercentage
```
#### BatteryState（属性）

电池状态。

| 属性 | 值 |
|------|------|
| 类型 | `map` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryState
```
#### HasAmbientLightSensor（属性）

是否有环境光传感器。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 HasAmbientLightSensor
```
#### WarnLevel（属性）

电量警告级别。

| 属性 | 值 |
|------|------|
| 类型 | `u` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 WarnLevel
```
#### IsHighPerformanceSupported（属性）

是否支持高性能模式。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 IsHighPerformanceSupported
```

### 交流电源延时配置

#### LinePowerScreensaverDelay（属性）

交流电源屏保延时。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerScreensaverDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerScreensaverDelay <int32 600>
```
#### LinePowerScreenBlackDelay（属性）

交流电源息屏延时。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerScreenBlackDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerScreenBlackDelay <int32 600>
```
#### LinePowerSleepDelay（属性）

交流电源休眠延时。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerSleepDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerSleepDelay <int32 900>
```
#### LinePowerLockDelay（属性）

交流电源锁屏延时。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerLockDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerLockDelay <int32 180>
```
#### LinePowerShortIdleDelay（属性）

交流电源短空闲延时。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerShortIdleDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerShortIdleDelay <int32 300>
```

### 电池延时配置

#### BatteryScreensaverDelay（属性）

电池屏保延时。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryScreensaverDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatteryScreensaverDelay <int32 120>
```
#### BatteryScreenBlackDelay（属性）

电池息屏延时。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryScreenBlackDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatteryScreenBlackDelay <int32 120>
```
#### BatterySleepDelay（属性）

电池休眠延时。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatterySleepDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatterySleepDelay <int32 300>
```
#### BatteryLockDelay（属性）

电池锁屏延时。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryLockDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatteryLockDelay <int32 60>
```
#### BatteryShortIdleDelay（属性）

电池短空闲延时。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryShortIdleDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatteryShortIdleDelay <int32 60>
```

### 锁屏与动作配置

#### ScreenBlackLock（属性）

息屏时是否锁定。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 ScreenBlackLock
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 ScreenBlackLock <true>
```
#### SleepLock（属性）

休眠时是否锁定。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 SleepLock
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 SleepLock <true>
```
#### LinePowerLidClosedAction（属性）

交流电源翻盖关闭动作。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerLidClosedAction
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerLidClosedAction <int32 0>
```
#### BatteryLidClosedAction（属性）

电池翻盖关闭动作。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryLidClosedAction
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatteryLidClosedAction <int32 0>
```
#### LinePowerPressPowerBtnAction（属性）

交流电源按下电源键动作。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerPressPowerBtnAction
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerPressPowerBtnAction <int32 0>
```
#### BatteryPressPowerBtnAction（属性）

电池按下电源键动作。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryPressPowerBtnAction
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatteryPressPowerBtnAction <int32 0>
```

### 低电量配置

#### LowPowerNotifyEnable（属性）

低电量通知是否启用。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LowPowerNotifyEnable
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LowPowerNotifyEnable <true>
```
#### LowPowerNotifyThreshold（属性）

低电量通知阈值。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LowPowerNotifyThreshold
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LowPowerNotifyThreshold <int32 20>
```
#### LowPowerAutoSleepThreshold（属性）

低电量自动休眠阈值。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LowPowerAutoSleepThreshold
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LowPowerAutoSleepThreshold <int32 5>
```
---
