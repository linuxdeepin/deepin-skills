# org.deepin.dde.AirplaneMode1 接口参考

该接口提供飞行模式开关能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.AirplaneMode1` |
| Object path | `/org/deepin/dde/AirplaneMode1` |
| Interface | `org.deepin.dde.AirplaneMode1` |
| Bus | System |
### 飞行模式方法

#### Enable

启用或禁用飞行模式（不启用设备本身）。

- **功能**：启用或禁用飞行模式（不启用设备本身）。
- **触发条件**：当用户在控制中心或快捷面板切换飞行模式时调用。
- **使用场景**：控制中心飞行模式开关、快捷面板飞行模式切换。

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

- **功能**：启用或禁用 Wi-Fi 飞行模式（不启用 Wi-Fi 设备本身）。
- **触发条件**：当用户在控制中心或快捷面板切换 Wi-Fi 飞行模式时调用。
- **使用场景**：控制中心 Wi-Fi 飞行模式开关、快捷面板切换。
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

- **功能**：启用或禁用蓝牙飞行模式（不启用蓝牙设备本身）。
- **触发条件**：当用户在控制中心或快捷面板切换蓝牙飞行模式时调用。
- **使用场景**：控制中心蓝牙飞行模式开关、快捷面板切换。
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

- **功能**：设置允许调用飞行模式接口的调用者。
- **触发条件**：当需要授权特定调用者访问飞行模式接口时调用。
- **使用场景**：权限管理，授权特定应用控制飞行模式。
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

- **功能**：飞行模式是否已启用。
- **触发条件**：属性，当飞行模式状态变化时通过 PropertiesChanged 信号通知。
- **使用场景**：控制中心显示飞行模式当前状态、状态栏图标更新。

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

- **功能**：Wi-Fi 飞行模式是否已启用。
- **触发条件**：属性，当 Wi-Fi 飞行模式状态变化时通过 PropertiesChanged 信号通知。
- **使用场景**：控制中心显示 Wi-Fi 飞行模式当前状态。
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

- **功能**：蓝牙飞行模式是否已启用。
- **触发条件**：属性，当蓝牙飞行模式状态变化时通过 PropertiesChanged 信号通知。
- **使用场景**：控制中心显示蓝牙飞行模式当前状态。
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

- **功能**：设备是否支持飞行模式。
- **触发条件**：属性，当设备飞行模式支持状态变化时通过 PropertiesChanged 信号通知。
- **使用场景**：控制中心判断是否显示飞行模式开关。
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
