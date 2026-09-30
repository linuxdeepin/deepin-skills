# org.deepin.dde.Bluetooth1 接口参考

该接口提供蓝牙适配器、设备、文件传输和配对管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Bluetooth1` |
| Object path | `/org/deepin/dde/Bluetooth1` |
| Interface | `org.deepin.dde.Bluetooth1` |
| Bus | Session |
### 蓝牙管理方法

#### CancelTransferSession

取消文件传输会话。

- **功能**：取消正在进行的蓝牙文件传输会话。
- **触发条件**：当用户取消蓝牙文件传输时调用。
- **使用场景**：蓝牙文件传输取消。
- **输入参数**: `sessionPath`（object path, 类型 `o`）：传输会话路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.CancelTransferSession "/path/to/session"
```

#### ClearUnpairedDevice

清除未配对设备。

- **功能**：清除所有未配对的蓝牙设备记录。
- **触发条件**：当用户在控制中心清理未配对设备时调用。
- **使用场景**：控制中心蓝牙设备列表清理。
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.ClearUnpairedDevice
```

#### Confirm

确认配对请求。

- **功能**：确认或拒绝蓝牙配对请求。
- **触发条件**：当蓝牙设备发起配对请求，需要用户确认时调用。
- **使用场景**：蓝牙配对确认对话框用户操作。
- **输入参数**: `device`（object path, 类型 `o`）：设备路径；`accept`（bool, 类型 `b`）：是否接受
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.Confirm "/path" true
```

#### ConnectDevice

连接设备。

- **功能**：连接指定的蓝牙设备。
- **触发条件**：当用户在控制中心点击连接蓝牙设备时调用。
- **使用场景**：控制中心蓝牙设备连接。

- **输入参数**: `device`（object path, 类型 `o`）：设备路径；`apath`（object path, 类型 `o`）：适配器路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.ConnectDevice "/path/to/device" "/path/to/adapter"
```

#### DebugInfo

获取调试信息。

- **功能**：获取蓝牙服务的调试信息。
- **触发条件**：当需要排查蓝牙问题时调用。
- **使用场景**：蓝牙问题诊断与调试。
- **输入参数**: 无
- **返回值**: `s`（string）：调试信息

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.DebugInfo
```

#### DisconnectDevice

断开设备连接。

- **功能**：断开指定蓝牙设备的连接。
- **触发条件**：当用户在控制中心点击断开蓝牙设备时调用。
- **使用场景**：控制中心蓝牙设备断开连接。

- **输入参数**: `device`（object path, 类型 `o`）：设备路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.DisconnectDevice "/path"
```

#### FeedPasskey

输入配对密钥。

- **功能**：输入蓝牙配对密钥。
- **触发条件**：当蓝牙配对过程中需要输入数字密钥时调用。
- **使用场景**：蓝牙配对密钥输入。
- **输入参数**: `device`（object path, 类型 `o`）：设备路径；`accept`（bool, 类型 `b`）：是否接受；`passkey`（uint32, 类型 `u`）：密钥
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.FeedPasskey "/path" true 123456
```

#### FeedPinCode

输入 PIN 码。

- **功能**：输入蓝牙配对 PIN 码。
- **触发条件**：当蓝牙配对过程中需要输入 PIN 码时调用。
- **使用场景**：蓝牙配对 PIN 码输入。
- **输入参数**: `device`（object path, 类型 `o`）：设备路径；`accept`（bool, 类型 `b`）：是否接受；`pinCode`（string, 类型 `s`）：PIN 码
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.FeedPinCode "/path" true "0000"
```

#### GetAdapters

获取适配器列表。

- **功能**：获取所有蓝牙适配器信息。
- **触发条件**：当需要展示蓝牙适配器列表时调用。
- **使用场景**：控制中心蓝牙适配器管理。

- **输入参数**: 无
- **返回值**: `s`（string，JSON 格式）：适配器列表（JSON 字符串）

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.GetAdapters
```

#### GetDevices

获取设备列表。

- **功能**：获取指定适配器下所有已知蓝牙设备信息。
- **触发条件**：当需要展示蓝牙设备列表时调用。
- **使用场景**：控制中心蓝牙设备列表展示。

- **输入参数**: `adapter`（object path, 类型 `o`）：适配器路径
- **返回值**: `s`（string，JSON 格式）：设备列表（JSON 字符串）

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.GetDevices "/path/to/adapter"
```

#### RemoveDevice

移除设备。

- **功能**：移除已配对的蓝牙设备。
- **触发条件**：当用户在控制中心点击删除蓝牙设备时调用。
- **使用场景**：控制中心蓝牙设备管理删除设备。

- **输入参数**: `adapter`（object path, 类型 `o`）：适配器路径；`device`（object path, 类型 `o`）：设备路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.RemoveDevice "/path/to/adapter" "/path/to/device"
```

#### RequestDiscovery

请求发现设备。

- **功能**：请求在指定适配器上开始扫描蓝牙设备。
- **触发条件**：当用户在控制中心点击搜索蓝牙设备时调用。
- **使用场景**：控制中心蓝牙设备搜索。
- **输入参数**: `adapter`（object path, 类型 `o`）：适配器路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.RequestDiscovery "/path"
```

#### SendFiles

发送文件。

- **功能**：向指定蓝牙设备发送文件，创建文件传输会话。
- **触发条件**：当用户选择通过蓝牙发送文件到已配对设备时调用。
- **使用场景**：蓝牙文件传输发送文件。
- **输入参数**: `devAddress`（string, 类型 `s`）：设备地址；`files`（string 数组, 类型 `as`）：文件列表
- **返回值**: `o`（object path）：传输会话路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Bluetooth1 \
  --object-path /org/deepin/dde/Bluetooth1 \
  --method org.deepin.dde.Bluetooth1.SendFiles "AA:BB:CC:DD:EE:FF" '["file1"]'
```
