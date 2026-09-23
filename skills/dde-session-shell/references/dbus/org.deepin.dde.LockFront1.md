# org.deepin.dde.LockFront1 接口参考

该接口提供锁屏界面显示、用户列表显示、认证状态控制和电源操作能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.LockFront1` |
| Object path | `/org/deepin/dde/LockFront1` |
| Interface | `org.deepin.dde.LockFront1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 锁屏操作

#### Show

显示锁屏界面。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1 \
  --method org.deepin.dde.LockFront1.Show
```

#### ShowUserList

显示用户列表。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1 \
  --method org.deepin.dde.LockFront1.ShowUserList
```

#### ShowAuth

显示认证界面。

- **输入参数**: `active`（bool, 类型 `b`）：是否激活
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1 \
  --method org.deepin.dde.LockFront1.ShowAuth true
```

#### Suspend

挂起系统。

- **输入参数**: `enable`（bool, 类型 `b`）：是否启用
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1 \
  --method org.deepin.dde.LockFront1.Suspend true
```

#### Hibernate

休眠系统。

- **输入参数**: `enable`（bool, 类型 `b`）：是否启用
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1 \
  --method org.deepin.dde.LockFront1.Hibernate true
```


### 锁屏属性

#### Visible（属性）

锁屏界面是否可见。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.LockFront1 Visible
```

### 锁屏信号

#### ChangKey

按键变化时发出。

- **参数**: `key`（string, 类型 `s`）：按键名称
- **触发条件**: 按键变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1
```

#### Visible

可见性变化时发出。

- **参数**: `visible`（bool, 类型 `b`）：是否可见
- **触发条件**: 锁屏界面可见性变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1
```

