# com.deepin.daemon.AirplaneMode1 接口参考

该接口提供飞行模式开关能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `com.deepin.daemon.AirplaneMode` |
| Object path | `/com/deepin/daemon/AirplaneMode` |
| Interface | `com.deepin.daemon.AirplaneMode1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

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
  --dest com.deepin.daemon.AirplaneMode \
  --object-path /com/deepin/daemon/AirplaneMode \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.daemon.AirplaneMode1 Enabled
```
设置示例：

```bash
gdbus call --system \
  --dest com.deepin.daemon.AirplaneMode \
  --object-path /com/deepin/daemon/AirplaneMode \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.daemon.AirplaneMode1 Enabled true
```
