# com.deepin.wm 接口参考

该接口提供窗口管理器工作区背景切换、装饰主题设置、多任务状态控制和窗口显示操作能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `com.deepin.wm` |
| Object path | `/com/deepin/wm` |
| Interface | `com.deepin.wm` |
| Bus | Session |

### 窗口操作

#### SwitchApplication

切换应用程序窗口。

- **输入参数**: `backward`（bool, 类型 `b`）：是否向后切换
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SwitchApplication false
```

#### TileActiveWindow

将当前活动窗口平铺到指定方向。

- **输入参数**: `side`（uint, 类型 `u`）：平铺方向（0=左, 1=右）
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.TileActiveWindow 0
```

#### BeginToMoveActiveWindow

开始移动当前活动窗口。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.BeginToMoveActiveWindow
```

#### ToggleActiveWindowMaximize

切换当前活动窗口的最大化状态。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.ToggleActiveWindowMaximize
```

#### MinimizeActiveWindow

最小化当前活动窗口。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.MinimizeActiveWindow
```

#### MaximizeActiveWindow

最大化当前活动窗口。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.MaximizeActiveWindow
```

#### UnMaximizeActiveWindow

取消最大化当前活动窗口。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.UnMaximizeActiveWindow
```

#### ShowWorkspace

显示工作区概览。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.ShowWorkspace
```

#### ShowWindow

显示窗口概览。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.ShowWindow
```

#### ShowAllWindow

显示所有窗口概览。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.ShowAllWindow
```

#### PerformAction

执行指定类型的操作。

- **输入参数**: `type`（int32, 类型 `i`）：操作类型
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.PerformAction 1
```

#### PreviewWindow

预览指定窗口。

- **输入参数**: `xid`（uint, 类型 `u`）：窗口 XID
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.PreviewWindow 41943040
```

#### CancelPreviewWindow

取消窗口预览。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.CancelPreviewWindow
```

#### PresentWindows

展示指定的多个窗口。

- **输入参数**: `xids`（uint 数组, 类型 `au`）：窗口 XID 列表
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.PresentWindows "[41943040,41943041]"
```

### 工作区背景

#### GetCurrentWorkspaceBackground

获取当前工作区背景。

- **输入参数**: 无
- **返回值**: `result`（string, 类型 `s`）：背景 URI

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetCurrentWorkspaceBackground
```

#### SetCurrentWorkspaceBackground

设置当前工作区背景。

- **输入参数**: `uri`（string, 类型 `s`）：背景 URI
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetCurrentWorkspaceBackground "file:///path/to/wallpaper.jpg"
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

#### GetWorkspaceBackground

获取指定工作区索引的背景。

- **输入参数**: `index`（int32, 类型 `i`）：工作区索引
- **返回值**: `result`（string, 类型 `s`）：背景 URI

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetWorkspaceBackground 0
```

#### SetWorkspaceBackground

设置指定工作区索引的背景。

- **输入参数**: `index`（int32, 类型 `i`）：工作区索引；`uri`（string, 类型 `s`）：背景 URI
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetWorkspaceBackground 0 "file:///path/to/wallpaper.jpg"
```

#### SetTransientBackground

设置临时背景。

- **输入参数**: `uri`（string, 类型 `s`）：背景 URI
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetTransientBackground "file:///path/to/wallpaper.jpg"
```

#### GetCurrentWorkspaceBackgroundForMonitor

获取指定显示器的当前工作区背景。

- **输入参数**: `strMonitorName`（string, 类型 `s`）：显示器名称
- **返回值**: `result`（string, 类型 `s`）：背景 URI

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetCurrentWorkspaceBackgroundForMonitor "eDP-1"
```

#### SetCurrentWorkspaceBackgroundForMonitor

设置指定显示器的当前工作区背景。

- **输入参数**: `uri`（string, 类型 `s`）：背景 URI；`strMonitorName`（string, 类型 `s`）：显示器名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetCurrentWorkspaceBackgroundForMonitor "file:///path/to/wallpaper.jpg" "eDP-1"
```

#### GetWorkspaceBackgroundForMonitor

获取指定工作区和显示器的背景。

- **输入参数**: `index`（int32, 类型 `i`）：工作区索引；`strMonitorName`（string, 类型 `s`）：显示器名称
- **返回值**: `result`（string, 类型 `s`）：背景 URI

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetWorkspaceBackgroundForMonitor 0 "eDP-1"
```

#### SetWorkspaceBackgroundForMonitor

设置指定工作区和显示器的背景。

- **输入参数**: `index`（int32, 类型 `i`）：工作区索引；`strMonitorName`（string, 类型 `s`）：显示器名称；`uri`（string, 类型 `s`）：背景 URI
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetWorkspaceBackgroundForMonitor 0 "eDP-1" "file:///path/to/wallpaper.jpg"
```

#### SetTransientBackgroundForMonitor

设置指定显示器的临时背景。

- **输入参数**: `uri`（string, 类型 `s`）：背景 URI；`strMonitorName`（string, 类型 `s`）：显示器名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetTransientBackgroundForMonitor "file:///path/to/wallpaper.jpg" "eDP-1"
```

### 工作区切换

#### GetCurrentWorkspace

获取当前工作区索引。

- **输入参数**: 无
- **返回值**: `index`（int32, 类型 `i`）：工作区索引

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetCurrentWorkspace
```

#### WorkspaceCount

获取工作区数量。

- **输入参数**: 无
- **返回值**: `count`（int32, 类型 `i`）：工作区数量

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

按方向切换工作区。

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
- **返回值**: `data`（string, 类型 `s`）：快捷键 JSON

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetAllAccels
```

#### GetAccel

获取指定 ID 的快捷键。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID
- **返回值**: `data`（string 数组, 类型 `as`）：快捷键列表

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetAccel "workspace_switch_left"
```

#### GetDefaultAccel

获取指定 ID 的默认快捷键。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID
- **返回值**: `data`（string 数组, 类型 `as`）：默认快捷键列表

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetDefaultAccel "workspace_switch_left"
```

#### SetAccel

设置快捷键。

- **输入参数**: `data`（string, 类型 `s`）：快捷键 JSON
- **返回值**: `result`（bool, 类型 `b`）：是否成功

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
  --method com.deepin.wm.SetDecorationTheme "deepin" "default"
```

#### SetDecorationDeepinTheme

设置 Deepin 装饰主题。

- **输入参数**: `deepinThemeName`（string, 类型 `s`）：Deepin 主题名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetDecorationDeepinTheme "default"
```

### 多任务与桌面

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
- **返回值**: `isActive`（bool, 类型 `b`）：是否激活

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.GetMultiTaskingStatus
```

#### SetMultiTaskingStatus

设置多任务状态。

- **输入参数**: `isActive`（bool, 类型 `b`）：是否激活
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm \
  --method com.deepin.wm.SetMultiTaskingStatus true
```

#### GetIsShowDesktop

获取是否显示桌面状态。

- **输入参数**: 无
- **返回值**: `isShowDesktop`（bool, 类型 `b`）：是否显示桌面

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

### 属性

#### compositingEnabled

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

#### compositingPossible

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

#### compositingAllowSwitch

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

#### zoneEnabled

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

#### cursorTheme

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

#### cursorSize

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

### 信号

#### DecorationThemeChanged

装饰主题变化时发出。

- **参数**: 无

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### WorkspaceBackgroundChanged

工作区背景变化时发出。

- **参数**: `index`（int32, 类型 `i`）：工作区索引；`newUri`（string, 类型 `s`）：新背景 URI

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### WorkspaceBackgroundChangedForMonitor

指定显示器工作区背景变化时发出。

- **参数**: `index`（int32, 类型 `i`）：工作区索引；`strMonitorName`（string, 类型 `s`）：显示器名称；`uri`（string, 类型 `s`）：新背景 URI

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### compositingEnabledChanged

合成器启用状态变化时发出。

- **参数**: `enabled`（bool, 类型 `b`）：是否启用

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### wmCompositingEnabledChanged

窗口管理器合成器启用状态变化时发出。

- **参数**: `enabled`（bool, 类型 `b`）：是否启用

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### workspaceCountChanged

工作区数量变化时发出。

- **参数**: `count`（int32, 类型 `i`）：新工作区数量

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### BeginToMoveActiveWindowChanged

开始移动活动窗口状态变化时发出。

- **参数**: 无

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### SwitchApplicationChanged

切换应用程序状态变化时发出。

- **参数**: `backward`（bool, 类型 `b`）：是否向后切换

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### TileActiveWindowChanged

平铺活动窗口状态变化时发出。

- **参数**: `side`（int32, 类型 `i`）：平铺方向

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### ToggleActiveWindowMaximizeChanged

切换活动窗口最大化状态变化时发出。

- **参数**: 无

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### MaximizeActiveWindowChanged

最大化活动窗口状态变化时发出。

- **参数**: 无

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### UnMaximizeActiveWindowChanged

取消最大化活动窗口状态变化时发出。

- **参数**: 无

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### ShowAllWindowChanged

显示所有窗口状态变化时发出。

- **参数**: 无

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### ShowWindowChanged

显示窗口状态变化时发出。

- **参数**: 无

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### ShowWorkspaceChanged

显示工作区状态变化时发出。

- **参数**: 无

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### ResumeCompositorChanged

恢复合成器时发出。

- **参数**: `reason`（int32, 类型 `i`）：恢复原因

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### SuspendCompositorChanged

暂停合成器时发出。

- **参数**: `reason`（int32, 类型 `i`）：暂停原因

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

#### WorkspaceSwitched

工作区切换时发出。

- **参数**: `from`（int32, 类型 `i`）：原工作区索引；`to`（int32, 类型 `i`）：新工作区索引

```bash
gdbus monitor --session \
  --dest com.deepin.wm \
  --object-path /com/deepin/wm
```

---
