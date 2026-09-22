# org.deepin.dde.ShutdownFront1 接口参考

该接口提供关机界面显示和电源操作能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ShutdownFront1` |
| Object path | `/org/deepin/dde/ShutdownFront1` |
| Interface | `org.deepin.dde.ShutdownFront1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 关机操作

#### Show

显示关机界面。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Show
```

#### Shutdown

关闭系统。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Shutdown
```

#### Restart

重启系统。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Restart
```

#### Logout

注销当前会话。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Logout
```

#### Suspend

挂起系统。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Suspend
```

#### Hibernate

休眠系统。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Hibernate
```

#### SwitchUser

切换用户。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.SwitchUser
```

#### Lock

锁屏。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Lock
```

#### UpdateAndShutdown

更新并关机。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.UpdateAndShutdown
```

#### UpdateAndReboot

更新并重启。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.UpdateAndReboot
```


### 关机属性

#### Visible（属性）

关机界面是否可见。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.ShutdownFront1 Visible
```

### 关机信号

#### ChangKey

按键变化时发出。

- **参数**: `key`（string, 类型 `s`）：按键名称
- **触发条件**: 按键变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1
```

#### Visible

可见性变化时发出。

- **参数**: `visible`（bool, 类型 `b`）：是否可见
- **触发条件**: 关机界面可见性变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1
```

