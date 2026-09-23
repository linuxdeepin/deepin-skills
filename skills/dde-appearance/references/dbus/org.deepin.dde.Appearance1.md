# org.deepin.dde.Appearance1 接口参考

该接口提供外观设置能力，包括主题、字体、壁纸、光标、缩放、窗口圆角、不透明度、活动色的读写和查询。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Appearance1` |
| Object path | `/org/deepin/dde/Appearance1` |
| Interface | `org.deepin.dde.Appearance1` |
| Bus | Session |


### 通用设置

#### Set

设置指定类型的外观值。

- **输入参数**: `ty`（string, 类型 `s`）：类型名称；`value`（string, 类型 `s`）：值
- **返回值**: 无

`ty` 支持的选项：`gtk`（GTK 主题）、`icon`（图标主题）、`cursor`（光标主题）、`cursorSize`（光标大小）、`background`（背景）、`greeterbackground`（登录背景）、`standardfont`（标准字体）、`monospacefont`（等宽字体）、`fontsize`（字体大小）、`globaltheme`（全局主题）、`activecolor`（活动色）、`windowradius`（窗口圆角）、`windowopacity`（窗口不透明度）、`wallpaper`（壁纸）、`dtksizemode`（DTK 缩放模式）、`qtscrollbarpolicy`（Qt 滚动条策略）

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.Set "standardfont" "Sans"
```

#### List

列出指定类型的所有可用值。

- **输入参数**: `ty`（string, 类型 `s`）：类型名称
- **返回值**: `list`（string, 类型 `s`）：可用值 JSON 列表

`ty` 支持的选项：`gtk`、`icon`、`cursor`、`background`、`standardfont`、`monospacefont`、`globaltheme`

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.List "icon"
```

#### Delete

删除指定类型和名称的主题项。

- **输入参数**: `ty`（string, 类型 `s`）：类型名称；`name`（string, 类型 `s`）：主题项名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.Delete "icon" "MyIconTheme"
```

#### Show

显示指定类型和名称列表的主题详情。

- **输入参数**: `ty`（string, 类型 `s`）：类型名称；`names`（string 数组, 类型 `as`）：主题项名称列表
- **返回值**: `detail`（string, 类型 `s`）：主题详情 JSON

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.Show "icon" "['bloom']"
```

#### Thumbnail

获取指定类型和名称的主题缩略图路径。

- **输入参数**: `ty`（string, 类型 `s`）：类型名称；`name`（string, 类型 `s`）：主题项名称
- **返回值**: `file`（string, 类型 `s`）：缩略图文件路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.Thumbnail "icon" "bloom"
```

#### Reset

重置所有外观设置为默认值。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.Reset
```


### 缩放设置

#### GetScaleFactor

获取全局缩放比例。

- **输入参数**: 无
- **返回值**: `scaleFactor`（double, 类型 `d`）：缩放比例

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetScaleFactor
```

#### SetScaleFactor

设置全局缩放比例。

- **输入参数**: `scale`（double, 类型 `d`）：缩放比例
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetScaleFactor 1.25
```

#### GetScreenScaleFactors

获取各显示器的缩放比例。

- **输入参数**: 无
- **返回值**: `scaleFactor`（字典, 类型 `a{sd}`）：显示器名称到缩放比例的映射

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetScreenScaleFactors
```

#### SetScreenScaleFactors

设置各显示器的缩放比例。

- **输入参数**: `scaleFactor`（字典, 类型 `a{sd}`）：显示器名称到缩放比例的映射
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetScreenScaleFactors "{'eDP-1': <1.25>}"
```


### 壁纸与背景

#### SetMonitorBackground

设置指定显示器的背景。

- **输入参数**: `monitorName`（string, 类型 `s`）：显示器名称；`imageGile`（string, 类型 `s`）：图片路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetMonitorBackground "eDP-1" "/usr/share/wallpapers/deepin/desktop.jpg"
```

#### GetWallpaperSlideShow

获取指定显示器的壁纸轮播配置。

- **输入参数**: `monitorName`（string, 类型 `s`）：显示器名称
- **返回值**: `slideShow`（string, 类型 `s`）：轮播配置（间隔时间，单位秒）

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetWallpaperSlideShow "eDP-1"
```

#### SetWallpaperSlideShow

设置指定显示器的壁纸轮播配置。

- **输入参数**: `monitorName`（string, 类型 `s`）：显示器名称；`slideShow`（string, 类型 `s`）：轮播配置（间隔时间，单位秒）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetWallpaperSlideShow "eDP-1" "300"
```


### 工作区背景

#### SetCurrentWorkspaceBackground

设置当前工作区背景。

- **输入参数**: `uri`（string, 类型 `s`）：背景 URI
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetCurrentWorkspaceBackground "file:///usr/share/wallpapers/deepin/desktop.jpg"
```

#### GetCurrentWorkspaceBackground

获取当前工作区背景。

- **输入参数**: 无
- **返回值**: `uri`（string, 类型 `s`）：背景 URI

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetCurrentWorkspaceBackground
```

#### SetCurrentWorkspaceBackgroundForMonitor

设置指定显示器的当前工作区背景。

- **输入参数**: `uri`（string, 类型 `s`）：背景 URI；`strMonitorName`（string, 类型 `s`）：显示器名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetCurrentWorkspaceBackgroundForMonitor "file:///usr/share/wallpapers/deepin/desktop.jpg" "eDP-1"
```

#### GetCurrentWorkspaceBackgroundForMonitor

获取指定显示器的当前工作区背景。

- **输入参数**: `strMonitorName`（string, 类型 `s`）：显示器名称
- **返回值**: `uri`（string, 类型 `s`）：背景 URI

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetCurrentWorkspaceBackgroundForMonitor "eDP-1"
```

#### SetWorkspaceBackgroundForMonitor

设置指定工作区和显示器的背景。

- **输入参数**: `index`（int32, 类型 `i`）：工作区索引；`strMonitorName`（string, 类型 `s`）：显示器名称；`uri`（string, 类型 `s`）：背景 URI
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetWorkspaceBackgroundForMonitor 1 "eDP-1" "file:///usr/share/wallpapers/deepin/desktop.jpg"
```

#### GetWorkspaceBackgroundForMonitor

获取指定工作区和显示器的背景。

- **输入参数**: `index`（int32, 类型 `i`）：工作区索引；`strMonitorName`（string, 类型 `s`）：显示器名称
- **返回值**: `uri`（string, 类型 `s`）：背景 URI

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetWorkspaceBackgroundForMonitor 1 "eDP-1"
```


### 活动色

#### SetActiveColors

设置活动色。

- **输入参数**: `activeColors`（string, 类型 `s`）：活动色 JSON
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetActiveColors "#2CA7F8"
```

#### GetActiveColors

获取活动色。

- **输入参数**: 无
- **返回值**: `activeColors`（string, 类型 `s`）：活动色 JSON

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetActiveColors
```


### 外观属性

#### FontSize（属性）

字体大小。

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 FontSize
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 FontSize <11.0>
```

#### Opacity（属性）

窗口不透明度。

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 Opacity
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 Opacity <1.0>
```

#### WindowRadius（属性）

窗口圆角半径。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 WindowRadius
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 WindowRadius <int32 8>
```

#### Background（属性）

当前背景 URI。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 Background
```

#### GlobalTheme（属性）

当前全局主题。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 GlobalTheme
```

#### GtkTheme（属性）

当前 GTK 主题。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 GtkTheme
```

#### IconTheme（属性）

当前图标主题。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 IconTheme
```

#### CursorTheme（属性）

当前光标主题。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 CursorTheme
```

#### MonospaceFont（属性）

当前等宽字体。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 MonospaceFont
```

#### QtActiveColor（属性）

Qt 活动色。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 QtActiveColor
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 QtActiveColor "<'#2CA7F8'>"
```

#### StandardFont（属性）

当前标准字体。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 StandardFont
```

#### WallpaperSlideShow（属性）

壁纸轮播配置。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 WallpaperSlideShow
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 WallpaperSlideShow "<'300'>"
```

#### DTKSizeMode（属性）

DTK 缩放模式。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 DTKSizeMode
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 DTKSizeMode <int32 1>
```

#### QtScrollBarPolicy（属性）

Qt 滚动条策略。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 QtScrollBarPolicy
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 QtScrollBarPolicy <int32 0>
```

#### CursorSize（属性）

光标大小。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 CursorSize
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 CursorSize <int32 24>
```

#### WallpaperURls（属性）

壁纸 URL 列表。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 WallpaperURls
```


### 外观变化信号

#### Changed

外观属性变化时发出。

- **参数**: `ty`（string, 类型 `s`）：属性类型；`value`（string, 类型 `s`）：新值
- **触发条件**: 外观属性被设置时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1
```

#### Refreshed

外观配置刷新完成时发出。

- **参数**: `type`（string, 类型 `s`）：刷新的类型
- **触发条件**: 外观配置刷新完成时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1
```

---
