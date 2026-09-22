# org.deepin.ds.Dock.TaskManager 接口参考

该接口提供 Dock 任务栏中运行窗口的动态管理能力，包括窗口分屏开关、强制退出控制，以及运行时动态 Item 对象的发现和操作（窗口激活、驻留和点击处理）。

> **说明**: TaskManager 的 Item 路径由运行时窗口列表决定，路径格式为 `/org/deepin/ds/Dock/TaskManager/Item/{id}`。以下仅提供通用发现和调用示例，不枚举运行时 Item。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.ds.Dock.TaskManager` |
| Object path | `/org/deepin/ds/Dock/TaskManager` |
| Interface | `org.deepin.ds.Dock.TaskManager` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

## 方法、属性与信号

### 任务管理属性

#### windowSplit（属性）

是否启用窗口分屏。

| 属性 | 值 |
|------|------|
| 类型 | `b`（bool） |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock.TaskManager \
  --object-path /org/deepin/ds/Dock/TaskManager \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.ds.Dock.TaskManager windowSplit
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock.TaskManager \
  --object-path /org/deepin/ds/Dock/TaskManager \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.ds.Dock.TaskManager windowSplit "<true>"
```

#### allowForceQuit（属性）

是否允许强制退出。

| 属性 | 值 |
|------|------|
| 类型 | `b`（bool） |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock.TaskManager \
  --object-path /org/deepin/ds/Dock/TaskManager \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.ds.Dock.TaskManager allowForceQuit
```

### 动态 Item 发现与操作

TaskManager 的 Item 为运行时动态注册对象，路径取决于当前打开的窗口列表。使用前需先获取实际对象路径。

#### 步骤一：获取对象树

```bash
busctl --user tree org.deepin.ds.Dock.TaskManager
```

#### 步骤二：内省任意 Item 路径

```bash
gdbus introspect --session \
  --dest org.deepin.ds.Dock.TaskManager \
  --object-path /org/deepin/ds/Dock/TaskManager/Item/<运行时获取的-id>
```

#### 步骤三：调用 Item 接口（通用格式）

Item 接口 `org.deepin.ds.Dock.TaskManager.Item` 提供以下成员：

| 成员 | 类型 | 读写 | 说明 |
|------|------|------|------|
| `isActive` | `b` | readwrite | 是否为活动窗口 |
| `isDocked` | `b` | readwrite | 是否驻留 Dock |
| `id` | `s` | read | 窗口 ID |
| `name` | `s` | read | 窗口名称 |
| `icon` | `s` | read | 图标名称 |
| `menus` | `s` | read | 菜单 JSON |
| `setDocked` | 方法 | — | 设置驻留状态，参数 `docked`(b) |
| `handleClick` | 方法 | — | 处理点击，参数 `action`(s) |

读取 Item 属性示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock.TaskManager \
  --object-path /org/deepin/ds/Dock/TaskManager/Item/<运行时获取的-id> \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.ds.Dock.TaskManager.Item name
```

调用 Item 方法示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock.TaskManager \
  --object-path /org/deepin/ds/Dock/TaskManager/Item/<运行时获取的-id> \
  --method org.deepin.ds.Dock.TaskManager.Item.handleClick "click"
```
