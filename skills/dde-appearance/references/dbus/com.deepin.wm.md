# com.deepin.wm 接口参考

该接口提供窗口管理器工作区背景切换、装饰主题设置、多任务状态控制和窗口显示操作能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `com.deepin.wm` |
| Object path | `/com/deepin/wm` |
| Interface | `com.deepin.wm` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 工作区背景

#### GetCurrentWorkspaceBackgrounds

获取当前工作区背景列表。

- **输入参数**: 无
- **返回值**: `as`（string 数组）：背景 URI 列表

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetCurrentWorkspaceBackgrounds
```

#### GetCurrentWorkspaceBackgroundForMonitor

获取指定显示器的当前工作区背景。

- **输入参数**: `monitorName`（string, 类型 `s`）：显示器名称
- **返回值**: `s`（string）：背景 URI

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetCurrentWorkspaceBackgroundForMonitor "eDP-1"
```

#### SetCurrentWorkspaceBackgroundForMonitor

设置指定显示器的当前工作区背景。

- **输入参数**: `monitorName`（string, 类型 `s`）：显示器名称；`uri`（string, 类型 `s`）：背景 URI
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetCurrentWorkspaceBackgroundForMonitor "eDP-1" "file:///path/to/wallpaper.jpg"
```

#### ChangeCurrentWorkspaceBackground

更改当前工作区背景。

- **输入参数**: `uri`（string, 类型 `s`）：背景 URI
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.ChangeCurrentWorkspaceBackground "file:///path/to/wallpaper.jpg"
```


### 工作区切换

#### GetCurrentWorkspace

获取当前工作区索引。

- **输入参数**: 无
- **返回值**: `i`（int32）：工作区索引

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetCurrentWorkspace
```

#### WorkspaceCount

获取工作区数量。

- **输入参数**: 无
- **返回值**: `i`（int32）：工作区数量

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.WorkspaceCount
```

#### SetCurrentWorkspace

切换到指定工作区。

- **输入参数**: `index`（int32, 类型 `i`）：工作区索引
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetCurrentWorkspace 1
```

#### PreviousWorkspace

切换到上一个工作区。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.PreviousWorkspace
```

#### NextWorkspace

切换到下一个工作区。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.NextWorkspace
```

#### SwitchToWorkspace

切换工作区方向。

- **输入参数**: `backward`（bool, 类型 `b`）：是否向后切换
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SwitchToWorkspace false
```


### 快捷键管理

#### GetAllAccels

获取所有快捷键。

- **输入参数**: 无
- **返回值**: `s`（string）：快捷键 JSON

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetAllAccels
```

#### GetAccel

获取指定 ID 的快捷键。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID
- **返回值**: `as`（string 数组）：快捷键列表

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetAccel "workspace_switch_left"
```

#### GetDefaultAccel

获取指定 ID 的默认快捷键。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID
- **返回值**: `as`（string 数组）：默认快捷键列表

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetDefaultAccel "workspace_switch_left"
```

#### SetAccel

设置快捷键。

- **输入参数**: `data`（string, 类型 `s`）：快捷键 JSON
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetAccel '{"id":"workspace_switch_left","key":["<Super>Left"]}'
```

#### RemoveAccel

移除快捷键。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.RemoveAccel "workspace_switch_left"
```


### 装饰主题

#### SetDecorationTheme

设置装饰主题。

- **输入参数**: `themeType`（string, 类型 `s`）：主题类型；`themeName`（string, 类型 `s`）：主题名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetDecorationTheme "gtk" "deepin"
```

#### SetDecorationDeepinTheme

设置 deepin 装饰主题。

- **输入参数**: `deepinThemeName`（string, 类型 `s`）：主题名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetDecorationDeepinTheme "bloom"
```


### 窗口与多任务

#### PresentWindows

展示指定窗口列表。

- **输入参数**: `xids`（uint32 数组, 类型 `au`）：窗口 ID 列表
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.PresentWindows [uint32 1, 2]
```

#### EnableZoneDetected

启用或禁用区域检测。

- **输入参数**: `enabled`（bool, 类型 `b`）：是否启用
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.EnableZoneDetected true
```

#### GetMultiTaskingStatus

获取多任务状态。

- **输入参数**: 无
- **返回值**: `b`（bool）：多任务是否启用

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetMultiTaskingStatus
```

#### SetMultiTaskingStatus

设置多任务状态。

- **输入参数**: `isActive`（bool, 类型 `b`）：是否启用
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetMultiTaskingStatus true
```

#### GetIsShowDesktop

查询是否显示桌面。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否显示桌面

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetIsShowDesktop
```

#### SetShowDesktop

设置是否显示桌面。

- **输入参数**: `isShowDesktop`（bool, 类型 `b`）：是否显示桌面
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetShowDesktop true
```


### 窗口管理器属性

#### compositingEnabled（属性）

合成器是否启用。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.wm compositingEnabled
```
设置示例：

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.wm compositingEnabled <true>
```
#### compositingPossible（属性）

合成器是否可用。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.wm compositingPossible
```
#### compositingAllowSwitch（属性）

是否允许切换合成器。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.wm compositingAllowSwitch
```
#### zoneEnabled（属性）

区域检测是否启用。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.wm zoneEnabled
```
设置示例：

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.wm zoneEnabled <true>
```
#### cursorTheme（属性）

光标主题。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.wm cursorTheme
```
设置示例：

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.wm cursorTheme "<string>"
```
#### cursorSize（属性）

光标大小。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.wm cursorSize
```
设置示例：

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.wm cursorSize <int32 24>
```

### 窗口管理器信号

#### DecorationThemeChanged

装饰主题变化时发出。

- **参数**: 无
- **触发条件**: 装饰主题被设置时发出

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### WorkspaceBackgroundChanged

工作区背景变化时发出。

- **参数**: `index`（int32, 类型 `i`）：工作区索引；`newUri`（string, 类型 `s`）：新背景 URI
- **触发条件**: 工作区背景被设置时发出

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### WorkspaceBackgroundChangedForMonitor

指定显示器工作区背景变化时发出。

- **参数**: `index`（int32, 类型 `i`）：工作区索引；`strMonitorName`（string, 类型 `s`）：显示器名称；`uri`（string, 类型 `s`）：新背景 URI
- **触发条件**: 指定显示器工作区背景被设置时发出

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### compositingEnabledChanged

合成器启用状态变化时发出。

- **参数**: `enabled`（bool, 类型 `b`）：是否启用
- **触发条件**: 合成器启用状态变化时发出

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### wmCompositingEnabledChanged

窗口管理器合成器启用状态变化时发出。

- **参数**: `enabled`（bool, 类型 `b`）：是否启用
- **触发条件**: 窗口管理器合成器启用状态变化时发出

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### workspaceCountChanged

工作区数量变化时发出。

- **参数**: `count`（int32, 类型 `i`）：新工作区数量
- **触发条件**: 工作区数量变化时发出

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### WorkspaceSwitched

工作区切换时发出。

- **参数**: `from`（int32, 类型 `i`）：原工作区索引；`to`（int32, 类型 `i`）：新工作区索引
- **触发条件**: 工作区切换时发出

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

---
