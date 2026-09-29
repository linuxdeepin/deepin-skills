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

## 方法、属性与信号

### 任务管理属性

#### windowSplit（属性）

是否启用窗口分屏。

- **功能**: 控制 Dock 任务栏是否启用窗口分屏功能，开启后窗口可通过 Dock 拖拽进行分屏操作
- **触发条件**: 外部程序通过 Properties.Set 修改时更新；用户在 Dock 设置界面切换分屏开关时更新
- **使用场景**: 用户通过 Dock 设置或控制中心控制窗口分屏功能的启用与禁用
- **属性值**:

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
  "org.deepin.ds.Dock.TaskManager" "windowSplit"
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock.TaskManager \
  --object-path /org/deepin/ds/Dock/TaskManager \
  --method org.freedesktop.DBus.Properties.Set \
  "org.deepin.ds.Dock.TaskManager" "windowSplit" "<true>"
```

#### allowForceQuit（属性）

是否允许强制退出。

- **功能**: 控制 Dock 任务栏是否允许用户强制退出应用窗口，开启后用户可通过右键菜单强制关闭无响应的应用
- **触发条件**: 外部程序通过 Properties.Set 修改时更新；用户在 Dock 设置界面切换强制退出开关时更新
- **使用场景**: 用户通过 Dock 设置或控制中心控制是否允许强制退出无响应的应用窗口
- **属性值**:

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
  "org.deepin.ds.Dock.TaskManager" "allowForceQuit"
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock.TaskManager \
  --object-path /org/deepin/ds/Dock/TaskManager \
  --method org.freedesktop.DBus.Properties.Set \
  "org.deepin.ds.Dock.TaskManager" "allowForceQuit" "<true>"
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
<!-- 请先通过 `busctl --user tree org.deepin.ds.Dock.TaskManager` 获取实际 Item ID 后替换 `<运行时获取的-id>` -->

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

##### isActive（属性）

- **功能**: 表示该窗口是否为当前活动窗口（拥有键盘焦点）
- **触发条件**: 窗口获得或失去焦点时值更新；外部程序通过 Properties.Set 修改时可激活对应窗口
- **使用场景**: 外部程序读取当前活动窗口状态，或通过设置此属性切换活动窗口
- **属性值**:

| 属性 | 值 |
|------|------|
| 类型 | `b`（bool） |
| 读写权限 | readwrite |

##### isDocked（属性）

- **功能**: 表示该窗口是否驻留在 Dock 任务栏中
- **触发条件**: 窗口被钉选到 Dock 或从 Dock 取消钉选时值更新；外部程序通过 Properties.Set 或 `setDocked` 方法修改时更新
- **使用场景**: 外部程序读取或修改窗口的 Dock 驻留状态，用于任务栏窗口管理
- **属性值**:

| 属性 | 值 |
|------|------|
| 类型 | `b`（bool） |
| 读写权限 | readwrite |

##### id（属性）

- **功能**: 表示该窗口的唯一标识 ID
- **触发条件**: 窗口创建时生成，窗口关闭时失效
- **使用场景**: 外部程序获取窗口 ID 用于唯一标识和引用特定窗口
- **属性值**:

| 属性 | 值 |
|------|------|
| 类型 | `s`（string） |
| 读写权限 | read |

##### name（属性）

- **功能**: 表示该窗口的显示名称
- **触发条件**: 窗口标题变化时值更新
- **使用场景**: Dock 任务栏显示窗口名称，外部程序读取窗口名称用于显示或日志
- **属性值**:

| 属性 | 值 |
|------|------|
| 类型 | `s`（string） |
| 读写权限 | read |

##### icon（属性）

- **功能**: 表示该窗口的图标名称
- **触发条件**: 窗口图标变化时值更新
- **使用场景**: Dock 任务栏显示窗口图标，外部程序读取图标名称用于显示
- **属性值**:

| 属性 | 值 |
|------|------|
| 类型 | `s`（string） |
| 读写权限 | read |

##### menus（属性）

- **功能**: 表示该窗口在 Dock 右键菜单中可用的菜单项，以 JSON 字符串形式返回
- **触发条件**: 窗口的可用菜单项变化时值更新
- **使用场景**: Dock 任务栏渲染窗口右键菜单，外部程序读取菜单项用于自定义菜单展示
- **属性值**:

| 属性 | 值 |
|------|------|
| 类型 | `s`（string） |
| 读写权限 | read |

##### setDocked（方法）

- **功能**: 设置该窗口在 Dock 中的驻留状态
- **触发条件**: 外部程序调用此方法时执行
- **使用场景**: 外部程序通过调用此方法将窗口钉选到 Dock 或从 Dock 取消钉选
- **输入参数**:
  - `docked`（bool, 类型 `b`）：是否驻留
- **返回值**: 无

##### handleClick（方法）

- **功能**: 处理用户对该窗口图标的点击操作，根据动作类型执行对应行为（如单击切换窗口、中键关闭窗口）
- **触发条件**: 用户在 Dock 任务栏点击窗口图标时触发
- **使用场景**: Dock 任务栏将用户点击事件转发给窗口管理器执行对应操作
- **输入参数**:
  - `action`（string, 类型 `s`）：点击动作标识
- **返回值**: 无

读取 Item 属性示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock.TaskManager \
  --object-path /org/deepin/ds/Dock/TaskManager/Item/<运行时获取的-id> \
  --method org.freedesktop.DBus.Properties.Get \
  "org.deepin.ds.Dock.TaskManager.Item" "name"
```

调用 Item 方法示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock.TaskManager \
  --object-path /org/deepin/ds/Dock/TaskManager/Item/<运行时获取的-id> \
  --method org.deepin.ds.Dock.TaskManager.Item.handleClick "click"
```
