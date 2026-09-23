# com.deepin.daemon.Power1 接口参考

该接口提供电源策略、亮度、休眠和关机管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `com.deepin.daemon.Power` |
| Object path | `/com/deepin/daemon/Power` |
| Interface | `com.deepin.daemon.Power1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 电源管理方法

#### SetScreenBlackLock

设置息屏锁定。

- **输入参数**: `value`（bool, 类型 `b`）：是否锁定
- **返回值**: 无

```bash
gdbus call --system \
  --dest com.deepin.daemon.Power \
  --object-path /com/deepin/daemon/Power \
  --method com.deepin.daemon.Power1.SetScreenBlackLock true
```

#### SetSleepLock

设置休眠锁定。

- **输入参数**: `value`（bool, 类型 `b`）：是否锁定
- **返回值**: 无

```bash
gdbus call --system \
  --dest com.deepin.daemon.Power \
  --object-path /com/deepin/daemon/Power \
  --method com.deepin.daemon.Power1.SetSleepLock true
```

#### SetSleepDelay

设置休眠延时。

- **输入参数**: `delay`（int32, 类型 `i`）：延时（秒）
- **返回值**: 无

```bash
gdbus call --system \
  --dest com.deepin.daemon.Power \
  --object-path /com/deepin/daemon/Power \
  --method com.deepin.daemon.Power1.SetSleepDelay 300
```

#### SetScreenBlackDelay

设置息屏延时。

- **输入参数**: `delay`（int32, 类型 `i`）：延时（秒）
- **返回值**: 无

```bash
gdbus call --system \
  --dest com.deepin.daemon.Power \
  --object-path /com/deepin/daemon/Power \
  --method com.deepin.daemon.Power1.SetScreenBlackDelay 300
```

#### SetLidClosedAction

设置合盖动作。

- **输入参数**: `action`（int32, 类型 `i`）：动作类型
- **返回值**: 无

```bash
gdbus call --system \
  --dest com.deepin.daemon.Power \
  --object-path /com/deepin/daemon/Power \
  --method com.deepin.daemon.Power1.SetLidClosedAction 1
```

#### SetPowerPlan

设置电源计划。

> **待核验**: `plan` 参数支持固定的电源计划选项，具体选项值待核验源码确认。

- **输入参数**: `plan`（string, 类型 `s`）：计划名称
- **返回值**: 无

```bash
gdbus call --system \
  --dest com.deepin.daemon.Power \
  --object-path /com/deepin/daemon/Power \
  --method com.deepin.daemon.Power1.SetPowerPlan "balanced"
```

#### BatteryIsPresent（属性）

是否有电池。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest com.deepin.daemon.Power \
  --object-path /com/deepin/daemon/Power \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.daemon.Power1 BatteryIsPresent
```
