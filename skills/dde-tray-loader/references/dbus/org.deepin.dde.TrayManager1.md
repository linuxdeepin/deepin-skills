# org.deepin.dde.TrayManager1 接口参考

该接口提供托盘图标管理和通知控制能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.TrayManager1` |
| Object path | `/org/deepin/dde/TrayManager1` |
| Interface | `org.deepin.dde.TrayManager1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 托盘操作

#### EnableNotification

启用或禁用指定窗口的通知。

- **输入参数**: `win`（uint32, 类型 `u`）：窗口 ID；`enabled`（bool, 类型 `b`）：是否启用
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1 \
  --method org.deepin.dde.TrayManager1.EnableNotification 12345 true
```

#### GetName

获取指定窗口的名称。

- **输入参数**: `win`（uint32, 类型 `u`）：窗口 ID
- **返回值**: `s`（string）：窗口名称

```bash
gdbus call --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1 \
  --method org.deepin.dde.TrayManager1.GetName 12345
```

#### Manage

打开托盘管理界面。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1 \
  --method org.deepin.dde.TrayManager1.Manage
```


### 托盘属性

#### TrayIcons（属性）

当前托盘图标列表。

| 属性 | 值 |
|------|------|
| 类型 | `au` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.TrayManager1 TrayIcons
```

### 托盘信号

#### Inited

托盘初始化完成时发出。

- **参数**: 无
- **触发条件**: 托盘初始化完成时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1
```

#### Added

托盘图标添加时发出。

- **参数**: `id`（uint32, 类型 `u`）：窗口 ID
- **触发条件**: 有新窗口添加到托盘时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1
```

#### Removed

托盘图标移除时发出。

- **参数**: `id`（uint32, 类型 `u`）：窗口 ID
- **触发条件**: 托盘图标被移除时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1
```

#### Changed

托盘图标变化时发出。

- **参数**: `id`（uint32, 类型 `u`）：窗口 ID
- **触发条件**: 托盘图标属性变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1
```

---
