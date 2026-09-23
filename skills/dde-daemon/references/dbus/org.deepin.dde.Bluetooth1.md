# org.deepin.dde.Bluetooth1 接口参考

该接口提供蓝牙适配器、设备、文件传输和配对管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Bluetooth` |
| Object path | `/com/deepin/daemon/Bluetooth` |
| Interface | `org.deepin.dde.Bluetooth1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 蓝牙管理方法

#### CancelTransferSession

取消文件传输会话。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.CancelTransferSession
```

#### ClearUnpairedDevice

清除未配对设备。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.ClearUnpairedDevice
```

#### Confirm

确认配对请求。

- **输入参数**: `device`（object, 类型 `o`）：设备路径；`accept`（bool, 类型 `b`）：是否接受
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.Confirm "/path" true
```

#### ConnectDevice

连接设备。

- **输入参数**: `device`（object, 类型 `o`）：设备路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.ConnectDevice "/path"
```

#### DebugInfo

获取调试信息。

- **输入参数**: 无
- **返回值**: `s`（string）：调试信息

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.DebugInfo
```

#### DisconnectDevice

断开设备连接。

- **输入参数**: `device`（object, 类型 `o`）：设备路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.DisconnectDevice "/path"
```

#### FeedPasskey

输入配对密钥。

- **输入参数**: `device`（object, 类型 `o`）：设备路径；`passkey`（uint32, 类型 `u`）：密钥
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.FeedPasskey "/path" 123456
```

#### FeedPinCode

输入 PIN 码。

- **输入参数**: `device`（object, 类型 `o`）：设备路径；`pinCode`（string, 类型 `s`）：PIN 码
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.FeedPinCode "/path" "0000"
```

#### GetAdapters

获取适配器列表。

- **输入参数**: 无
- **返回值**: `ao`（对象路径数组）：适配器列表

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.GetAdapters
```

#### GetDevices

获取设备列表。

- **输入参数**: `adapter`（object, 类型 `o`）：适配器路径
- **返回值**: `ao`（对象路径数组）：设备列表

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.GetDevices "/path"
```

#### RemoveDevice

移除设备。

- **输入参数**: `device`（object, 类型 `o`）：设备路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.RemoveDevice "/path"
```

#### RequestDiscovery

请求发现设备。

- **输入参数**: `adapter`（object, 类型 `o`）：适配器路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.RequestDiscovery "/path"
```

#### SendFiles

发送文件。

- **输入参数**: `device`（object, 类型 `o`）：设备路径；`files`（string 数组, 类型 `as`）：文件列表
- **返回值**: `o`（object path）：传输会话路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth \
  --object-path /com/deepin/daemon/Bluetooth \
  --method org.deepin.dde.Bluetooth1.SendFiles "/path" ["file1"]
```

