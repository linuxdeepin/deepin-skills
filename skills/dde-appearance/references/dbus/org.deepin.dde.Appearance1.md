# org.deepin.dde.Appearance1 接口参考

该接口提供外观设置能力，包括字体、主题、壁纸、光标、缩放、深色模式、窗口圆角、不透明度和窗口模糊效果的读写。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Appearance1` |
| Object path | `/org/deepin/dde/Appearance1` |
| Interface | `org.deepin.dde.Appearance1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 通用设置

#### Set

设置指定类型的外观值。

- **输入参数**: `type`（string, 类型 `s`）：类型名称；`value`（string, 类型 `s`）：值
- **返回值**: 无

**`type` 支持的选项**（来源于 dde-appearance 源码 `appearancemanager.cpp` 的 `doSetByType()` 及 `commondefine.h`）:
- `gtk` — GTK 主题
- `icon` — 图标主题
- `cursor` — 光标主题
- `cursorSize` — 光标大小
- `background` — 背景
- `greeterbackground` — 登录背景
- `standardfont` — 标准字体
- `monospacefont` — 等宽字体
- `fontsize` — 字体大小
- `globaltheme` — 全局主题
- `activecolor` — 活动色
- `windowradius` — 窗口圆角
- `windowopacity` — 窗口不透明度
- `wallpaper` — 壁纸
- `dtksizemode` — DTK 缩放模式
- `qtscrollbarpolicy` — Qt 滚动条策略

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.Set "standardfont" "Sans"
```

#### Get

获取指定类型的外观值。

> **待核验**: 该方法在当前源码的 D-Bus 接口定义中未找到，待核验是否在其他版本中存在或由客户端封装。

- **输入参数**: `type`（string, 类型 `s`）：类型名称
- **返回值**: `s`（string）：当前值

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.Get "standardfont"
```

#### GetSchema

获取指定类型的默认外观值。

> **待核验**: 该方法在当前源码的 D-Bus 接口定义中未找到，待核验是否在其他版本中存在或由客户端封装。

- **输入参数**: `type`（string, 类型 `s`）：类型名称
- **返回值**: `s`（string）：默认值

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetSchema "standardfont"
```

#### List

列出指定类型的所有可用值。

- **输入参数**: `type`（string, 类型 `s`）：类型名称
- **返回值**: `as`（string 数组）：可用值列表

**`type` 支持的选项**（来源于 dde-appearance 源码 `appearancemanager.cpp` 的 `doList()`）:
- `gtk` — GTK 主题
- `icon` — 图标主题
- `cursor` — 光标主题
- `background` — 背景
- `standardfont` — 标准字体
- `monospacefont` — 等宽字体
- `globaltheme` — 全局主题

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.List "standardfont"
```


### 字体设置

#### SetFont

设置字体及大小。

- **输入参数**: `value`（string, 类型 `s`）：字体名称；`size`（double, 类型 `d`）：字体大小
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetFont "Sans" 11.0
```

#### GetFont

获取当前字体名称。

- **输入参数**: 无
- **返回值**: `s`（string）：字体名称

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetFont
```

#### GetFontSize

获取当前字体大小。

- **输入参数**: 无
- **返回值**: `d`（double）：字体大小

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetFontSize
```


### 缩放设置

#### SetScale

设置缩放比例。

- **输入参数**: `ratio`（double, 类型 `d`）：缩放比例
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetScale 1.25
```

#### GetScale

获取缩放比例。

- **输入参数**: 无
- **返回值**: `d`（double）：缩放比例

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetScale
```

#### SetGlobalScale

设置全局缩放比例。

- **输入参数**: `scale`（double, 类型 `d`）：全局缩放比例
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetGlobalScale 1.25
```

#### GetGlobalScale

获取全局缩放比例。

- **输入参数**: 无
- **返回值**: `d`（double）：全局缩放比例

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetGlobalScale
```


### 壁纸设置

#### SetWallpaper

设置壁纸。

> **待核验**: 该方法在当前 dde-appearance 源码的 D-Bus 接口定义（`appearance1.h` / `org.deepin.dde.Appearance1.xml`）中未找到。实际的壁纸设置方法为 `SetCurrentWorkspaceBackground(uri)`，不带 `type` 参数。`type` 参数支持的选项待核验。

- **输入参数**: `type`（string, 类型 `s`）：壁纸类型；`uri`（string, 类型 `s`）：壁纸 URI
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetWallpaper "picture" "file:///usr/share/wallpapers/default.jpg"
```

#### GetWallpaper

获取当前壁纸。

> **待核验**: 该方法在当前 dde-appearance 源码的 D-Bus 接口定义（`appearance1.h` / `org.deepin.dde.Appearance1.xml`）中未找到。实际的壁纸获取方法为 `GetCurrentWorkspaceBackground()`，不带 `type` 参数。`type` 参数支持的选项待核验。

- **输入参数**: `type`（string, 类型 `s`）：壁纸类型
- **返回值**: `s`（string）：壁纸 URI

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetWallpaper "picture"
```

#### SetWallpaperSlideShow

设置幻灯片壁纸。

- **输入参数**: `type`（string, 类型 `s`）：壁纸类型；`uri`（string, 类型 `s`）：壁纸 URI
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetWallpaperSlideShow "wallpaper" "/usr/share/wallpapers/"
```

#### GetWallpaperSlideShow

获取当前幻灯片壁纸。

- **输入参数**: `type`（string, 类型 `s`）：壁纸类型
- **返回值**: `s`（string）：壁纸 URI

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetWallpaperSlideShow "wallpaper"
```


### 光标与图标主题

#### SetCursor

设置光标主题。

- **输入参数**: `value`（string, 类型 `s`）：光标主题名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetCursor "bloom"
```

#### GetCursor

获取当前光标主题。

- **输入参数**: 无
- **返回值**: `s`（string）：光标主题名称

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetCursor
```

#### SetIconTheme

设置图标主题。

- **输入参数**: `value`（string, 类型 `s`）：图标主题名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetIconTheme "bloom"
```

#### GetIconTheme

获取当前图标主题。

- **输入参数**: 无
- **返回值**: `s`（string）：图标主题名称

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetIconTheme
```


### 主题与深色模式

#### SetTheme

设置 GTK 主题。

- **输入参数**: `value`（string, 类型 `s`）：主题名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetTheme "deepin"
```

#### GetTheme

获取当前 GTK 主题。

- **输入参数**: 无
- **返回值**: `s`（string）：主题名称

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetTheme
```

#### SetDarkMode

设置深色模式。

- **输入参数**: `mode`（uint32, 类型 `u`）：深色模式值
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetDarkMode 1
```


### 外观属性

#### Typeface（属性）

当前字体名称。

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
  org.deepin.dde.Appearance1 Typeface
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 Typeface "<string>"
```
#### FontSize（属性）

当前字体大小。

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
#### MonospaceFontTypeface（属性）

等宽字体名称。

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
  org.deepin.dde.Appearance1 MonospaceFontTypeface
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 MonospaceFontTypeface "<string>"
```
#### MonospaceFontSize（属性）

等宽字体大小。

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
  org.deepin.dde.Appearance1 MonospaceFontSize
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 MonospaceFontSize <11.0>
```
#### Cursor（属性）

当前光标主题。

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
  org.deepin.dde.Appearance1 Cursor
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 Cursor "<string>"
```
#### GlobalScale（属性）

全局缩放比例。

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
  org.deepin.dde.Appearance1 GlobalScale
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 GlobalScale <1.25>
```
#### Wallpaper（属性）

当前壁纸。

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
  org.deepin.dde.Appearance1 Wallpaper
```
#### WallpaperSlideShow（属性）

当前幻灯片壁纸。

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
  org.deepin.dde.Appearance1 WallpaperSlideShow
```
#### IconTheme（属性）

当前图标主题。

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
  org.deepin.dde.Appearance1 IconTheme
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 IconTheme "<string>"
```
#### GtkTheme（属性）

当前 GTK 主题。

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
  org.deepin.dde.Appearance1 GtkTheme
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 GtkTheme "<string>"
```
#### QtTheme（属性）

当前 Qt 主题。

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
  org.deepin.dde.Appearance1 QtTheme
```
#### DarkMode（属性）

深色模式状态。

| 属性 | 值 |
|------|------|
| 类型 | `u` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 DarkMode
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 DarkMode <uint32 1>
```
#### RoundRadius（属性）

窗口圆角半径。

| 属性 | 值 |
|------|------|
| 类型 | `u` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 RoundRadius
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 RoundRadius <uint32 8>
```
#### ActiveColor（属性）

活动色。

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
  org.deepin.dde.Appearance1 ActiveColor
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 ActiveColor "<string>"
```
#### WindowOpacity（属性）

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
  org.deepin.dde.Appearance1 WindowOpacity
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 WindowOpacity <1.0>
```
#### Background（属性）

背景。

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
  org.deepin.dde.Appearance1 Background
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 Background "<string>"
```
#### BlurEnabled（属性）

窗口模糊是否启用。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 BlurEnabled
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Appearance1 BlurEnabled <true>
```

### 外观变化信号

#### AppearanceChanged

外观属性变化时发出。

- **参数**: `type`（string, 类型 `s`）：属性类型；`value`（string, 类型 `s`）：新值
- **触发条件**: 外观属性被设置时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1
```

#### Refreshed

外观配置刷新完成时发出。

- **参数**: 无
- **触发条件**: 外观配置刷新完成时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1
```

---
