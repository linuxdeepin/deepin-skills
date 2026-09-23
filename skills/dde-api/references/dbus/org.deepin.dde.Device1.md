# org.deepin.dde.Device1 接口参考

该接口提供蓝牙设备阻止状态查询和解锁能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Device1` |
| Object path | `/org/deepin/dde/Device1` |
| Interface | `org.deepin.dde.Device1` |
| Bus | System |


### 设备管理方法

#### HasBluetoothDeviceBlocked

查询是否有蓝牙设备被阻止。

- **输入参数**: 无
- **返回值**: `has`（bool, 类型 `b`）：是否有设备被阻止

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Device1 \
  --object-path /org/deepin/dde/Device1 \
  --method org.deepin.dde.Device1.HasBluetoothDeviceBlocked
```

#### UnblockBluetoothDevices

解除所有蓝牙设备的阻止。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Device1 \
  --object-path /org/deepin/dde/Device1 \
  --method org.deepin.dde.Device1.UnblockBluetoothDevices
```

---
