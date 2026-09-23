# org.deepin.dde.AirplaneMode1 接口参考

该接口提供飞行模式开关能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.AirplaneMode1` |
| Object path | `/org/deepin/dde/AirplaneMode1` |
| Interface | `org.deepin.dde.AirplaneMode1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 飞行模式方法

#### Enable

启用或禁用飞行模式（不启用设备本身）。

- **输入参数**: `enableAirplaneMode`（bool, 类型 `b`）：是否启用飞行模式
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.AirplaneMode1 \
  --object-path /org/deepin/dde/AirplaneMode1 \
  --method org.deepin.dde.AirplaneMode1.Enable true
```

#### EnableWifi

启用或禁用 Wi-Fi 飞行模式（不启用 Wi-Fi 设备本身）。

- **输入参数**: `enableAirplaneMode`（bool, 类型 `b`）：是否启用 Wi-Fi 飞行模式
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.AirplaneMode1 \
  --object-path /org/deepin/dde/AirplaneMode1 \
  --method org.deepin.dde.AirplaneMode1.EnableWifi true
```

#### EnableBluetooth

启用或禁用蓝牙飞行模式（不启用蓝牙设备本身）。

- **输入参数**: `enableAirplaneMode`（bool, 类型 `b`）：是否启用蓝牙飞行模式
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.AirplaneMode1 \
  --object-path /org/deepin/dde/AirplaneMode1 \
  --method org.deepin.dde.AirplaneMode1.EnableBluetooth true
```

#### SetAllowCaller

设置允许的调用者。

- **输入参数**: `uniqueName`（string, 类型 `s`）：调用者唯一名称
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.AirplaneMode1 \
  --object-path /org/deepin/dde/AirplaneMode1 \
  --method org.deepin.dde.AirplaneMode1.SetAllowCaller ":1.123"
```

### 飞行模式属性

#### Enabled（属性）

飞行模式是否启用。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.AirplaneMode1 \
  --object-path /org/deepin/dde/AirplaneMode1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.AirplaneMode1 Enabled
```

设置示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.AirplaneMode1 \
  --object-path /org/deepin/dde/AirplaneMode1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.AirplaneMode1 Enabled true
```

#### WifiEnabled（属性）

Wi-Fi 飞行模式是否启用。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.AirplaneMode1 \
  --object-path /org/deepin/dde/AirplaneMode1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.AirplaneMode1 WifiEnabled
```

#### BluetoothEnabled（属性）

蓝牙飞行模式是否启用。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.AirplaneMode1 \
  --object-path /org/deepin/dde/AirplaneMode1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.AirplaneMode1 BluetoothEnabled
```

#### HasAirplaneMode（属性）

设备是否支持飞行模式。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.AirplaneMode1 \
  --object-path /org/deepin/dde/AirplaneMode1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.AirplaneMode1 HasAirplaneMode
```
