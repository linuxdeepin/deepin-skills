# org.deepin.dde.Launcher1 接口参考

该接口提供启动器的显示、隐藏、切换和模式控制能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Launcher1` |
| Object path | `/org/deepin/dde/Launcher1` |
| Interface | `org.deepin.dde.Launcher1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 启动器显示控制

#### Exit

退出启动器。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1 \
  --method org.deepin.dde.Launcher1.Exit
```

#### Show

显示启动器。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1 \
  --method org.deepin.dde.Launcher1.Show
```

#### Hide

隐藏启动器。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1 \
  --method org.deepin.dde.Launcher1.Hide
```

#### Toggle

切换启动器显示状态。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1 \
  --method org.deepin.dde.Launcher1.Toggle
```

#### ShowByMode

按指定模式显示启动器。

- **输入参数**: `mode`（uint16, 类型 `q`）：显示模式
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1 \
  --method org.deepin.dde.Launcher1.ShowByMode 1
```


### 启动器属性

#### Visible（属性）

启动器是否可见。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Launcher1 Visible
```

### 启动器信号

#### Closed

启动器关闭时发出。

- **参数**: 无
- **触发条件**: 启动器被关闭时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1
```

#### Shown

启动器显示时发出。

- **参数**: 无
- **触发条件**: 启动器被显示时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1
```

#### VisibleChanged

启动器可见状态变化时发出。

- **参数**: `visible`（bool, 类型 `b`）：是否可见
- **触发条件**: 启动器可见状态变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1
```

---
