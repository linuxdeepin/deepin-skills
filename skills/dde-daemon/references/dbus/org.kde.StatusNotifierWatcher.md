# org.kde.StatusNotifierWatcher 接口参考

该接口提供系统托盘状态通知管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.kde.StatusNotifierWatcher` |
| Object path | `/org/kde/StatusNotifierWatcher` |
| Interface | `org.kde.StatusNotifierWatcher` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 托盘监控属性

#### RegisteredStatusNotifierItems（属性）

已注册的状态通知项列表。

| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.kde.StatusNotifierWatcher \
  --object-path /org/kde/StatusNotifierWatcher \
  --method org.freedesktop.DBus.Properties.Get \
  org.kde.StatusNotifierWatcher RegisteredStatusNotifierItems
```
#### IsStatusNotifierHostRegistered（属性）

是否有状态通知宿主注册。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.kde.StatusNotifierWatcher \
  --object-path /org/kde/StatusNotifierWatcher \
  --method org.freedesktop.DBus.Properties.Get \
  org.kde.StatusNotifierWatcher IsStatusNotifierHostRegistered
```

### 托盘监控信号

#### StatusNotifierItemRegistered

状态通知项注册时发出。

- **参数**: `itemId`（string, 类型 `s`）：项 ID
- **触发条件**: 状态通知项注册时发出

```bash
gdbus monitor --session \
  --dest org.kde.StatusNotifierWatcher \
  --object-path /org/kde/StatusNotifierWatcher
```

#### StatusNotifierItemUnregistered

状态通知项注销时发出。

- **参数**: `itemId`（string, 类型 `s`）：项 ID
- **触发条件**: 状态通知项注销时发出

```bash
gdbus monitor --session \
  --dest org.kde.StatusNotifierWatcher \
  --object-path /org/kde/StatusNotifierWatcher
```

