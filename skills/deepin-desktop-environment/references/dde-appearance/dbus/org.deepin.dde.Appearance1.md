# org.deepin.dde.Appearance1 接口参考

该接口提供外观设置能力，包括字体、主题、壁纸、光标、缩放、窗口圆角、不透明度的读写。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Appearance1` |
| Object path | `/org/deepin/dde/Appearance1` |
| Interface | `org.deepin.dde.Appearance1` |
| Bus | Session |

## 方法（Methods）

### 通用设置

#### Set

设置指定类型的外观值。

- **输入参数**:
  - `ty`（string, 类型 `s`）：类型名称
  - `value`（string, 类型 `s`）：值
- **返回值**: 无
- **触发条件**: 用户通过控制中心外观设置页面修改某项外观属性时调用
- **使用场景**: 需要程序化设置某个外观属性时使用，例如设置字体、主题、壁纸、光标、缩放、窗口圆角、不透明度。

**`ty` 支持的选项**:
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

#### List

列出指定类型的所有可用值。

- **输入参数**: `ty`（string, 类型 `s`）：类型名称
- **返回值**: `s`（string）：JSON 格式的可用值列表
- **触发条件**: 需要获取可用外观选项列表时调用
- **使用场景**: 需要获取可用的外观选项列表用于 UI 展示或选择时使用。

**`ty` 支持的选项**:
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

#### Delete

删除指定类型的指定项。

- **输入参数**:
  - `ty`（string, 类型 `s`）：类型名称
  - `name`（string, 类型 `s`）：项名称
- **返回值**: 无
- **触发条件**: 用户删除自定义外观项时调用
- **使用场景**: 需要删除用户自定义的外观项时使用，例如删除自定义壁纸、自定义字体。

**`ty` 支持的选项**:
- `gtk` — GTK 主题
- `icon` — 图标主题
- `cursor` — 光标主题
- `background` — 背景

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.Delete "background" "file:///usr/share/wallpapers/custom.jpg"
```

#### Show

按名称筛选并返回指定类型的项详情。

- **输入参数**:
  - `ty`（string, 类型 `s`）：类型名称
  - `names`（string 数组, 类型 `as`）：要筛选的名称列表
- **返回值**: `s`（string）：JSON 格式的筛选结果
- **触发条件**: 需要获取指定外观项详细信息时调用
- **使用场景**: 需要获取指定外观项的详细信息时使用，例如获取某个图标主题或字体详情。

**`ty` 支持的选项**: `gtk`、`icon`、`cursor`、`background`、`globaltheme`、`standardfont`、`monospacefont`

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.Show "icon" "['bloom']"
```

#### Thumbnail

获取指定类型指定项的缩略图路径。

- **输入参数**:
  - `ty`（string, 类型 `s`）：类型名称
  - `name`（string, 类型 `s`）：项名称
- **返回值**: `s`（string）：缩略图文件路径
- **触发条件**: 需要获取外观项缩略图用于 UI 展示时调用
- **使用场景**: 需要获取图标、光标、全局主题的缩略图用于 UI 展示时使用。

**`ty` 支持的选项**: `icon`、`cursor`、`globaltheme`

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
- **触发条件**: 用户点击恢复默认设置时调用
- **使用场景**: 需要将所有外观设置恢复为系统默认值时使用，例如用户点击「恢复默认设置」按钮。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.Reset
```

### 字体与活动色

#### SetActiveColors

设置活动色。

- **输入参数**: `activeColors`（string, 类型 `s`）：活动色值
- **返回值**: 无
- **触发条件**: 用户在控制中心选择新的活动色时调用
- **使用场景**: 需要设置系统活动色（强调色）时使用，例如用户在控制中心选择新的活动色。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetActiveColors "#007AFF"
```

#### GetActiveColors

获取当前活动色。

- **输入参数**: 无
- **返回值**: `s`（string）：活动色值
- **触发条件**: 需要读取当前系统活动色时调用
- **使用场景**: 需要读取当前系统活动色用于显示或其他组件同步时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetActiveColors
```

### 缩放设置

#### SetScaleFactor

设置缩放比例。

- **输入参数**: `scale`（double, 类型 `d`）：缩放比例
- **返回值**: 无
- **触发条件**: 用户在控制中心调整全局缩放比例时调用
- **使用场景**: 需要设置全局缩放比例时使用，例如用户在控制中心调整缩放比例。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetScaleFactor 1.25
```

#### GetScaleFactor

获取全局缩放比例。

- **输入参数**: 无
- **返回值**: `scaleFactor`（double, 类型 `d`）：当前全局缩放比例
- **触发条件**: 需要读取当前全局缩放比例时调用
- **使用场景**: 需要读取当前缩放比例用于显示或同步时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetScaleFactor
```

#### SetScreenScaleFactors

设置各屏幕的缩放比例。

- **输入参数**: `scaleFactor`（字典 `a{sd}`）：屏幕名到缩放比例的映射
- **返回值**: 无
- **触发条件**: 用户为不同显示器设置不同缩放比例时调用
- **使用场景**: 需要为不同显示器设置不同缩放比例时使用，例如多显示器环境下为高 DPI 屏幕设置更大缩放。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetScreenScaleFactors "{'eDP-1': 1.25}"
```

#### GetScreenScaleFactors

获取各屏幕的缩放比例。

- **输入参数**: 无
- **返回值**: `a{sd}`（字典）：屏幕名到缩放比例的映射
- **触发条件**: 需要读取各屏幕缩放比例时调用
- **使用场景**: 需要读取各屏幕的缩放比例用于显示或同步时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetScreenScaleFactors
```

### 壁纸与背景设置

以下工作区背景方法（SetCurrentWorkspaceBackground、GetCurrentWorkspaceBackground、SetCurrentWorkspaceBackgroundForMonitor、GetCurrentWorkspaceBackgroundForMonitor、SetWorkspaceBackgroundForMonitor、GetWorkspaceBackgroundForMonitor）为 `org.deepin.dde.Appearance1` 对 `com.deepin.wm` 同名方法的代理转发。调用方可通过 `org.deepin.dde.Appearance1` 接口统一访问外观相关能力，无需直接调用 `com.deepin.wm`。新代码推荐使用 `org.deepin.dde.Appearance1` 接口。

#### SetCurrentWorkspaceBackground

设置当前工作区背景。

- **输入参数**: `uri`（string, 类型 `s`）：背景 URI
- **返回值**: 无
- **触发条件**: 用户设置当前工作区壁纸时调用
- **使用场景**: 需要设置当前工作区的壁纸时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetCurrentWorkspaceBackground "file:///usr/share/wallpapers/default.jpg"
```

#### GetCurrentWorkspaceBackground

获取当前工作区背景。

- **输入参数**: 无
- **返回值**: `s`（string）：背景 URI
- **触发条件**: 需要读取当前工作区壁纸 URI 时调用
- **使用场景**: 需要读取当前工作区的壁纸 URI 用于显示时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetCurrentWorkspaceBackground
```

#### SetCurrentWorkspaceBackgroundForMonitor

设置指定显示器的当前工作区背景。

- **输入参数**:
  - `uri`（string, 类型 `s`）：背景 URI
  - `strMonitorName`（string, 类型 `s`）：显示器名称
- **返回值**: 无
- **触发条件**: 用户为指定显示器设置当前工作区壁纸时调用
- **使用场景**: 需要为指定显示器设置当前工作区壁纸时使用，例如多显示器环境下为不同屏幕设置不同壁纸。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetCurrentWorkspaceBackgroundForMonitor \
  "file:///usr/share/wallpapers/default.jpg" "eDP-1"
```

#### GetCurrentWorkspaceBackgroundForMonitor

获取指定显示器的当前工作区背景。

- **输入参数**: `strMonitorName`（string, 类型 `s`）：显示器名称
- **返回值**: `s`（string）：背景 URI
- **触发条件**: 需要读取指定显示器的当前工作区壁纸时调用
- **使用场景**: 需要读取指定显示器的当前工作区壁纸 URI 时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetCurrentWorkspaceBackgroundForMonitor "eDP-1"
```

#### SetWorkspaceBackgroundForMonitor

设置指定工作区和显示器的背景。

- **输入参数**:
  - `index`（int32, 类型 `i`）：工作区索引
  - `strMonitorName`（string, 类型 `s`）：显示器名称
  - `uri`（string, 类型 `s`）：背景 URI
- **返回值**: 无
- **触发条件**: 用户为指定工作区和显示器设置壁纸时调用
- **使用场景**: 需要为指定工作区和显示器设置壁纸时使用，例如为第 2 个工作区的副屏设置专属壁纸。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetWorkspaceBackgroundForMonitor \
  0 "eDP-1" "file:///usr/share/wallpapers/default.jpg"
```

#### GetWorkspaceBackgroundForMonitor

获取指定工作区和显示器的背景。

- **输入参数**:
  - `index`（int32, 类型 `i`）：工作区索引
  - `strMonitorName`（string, 类型 `s`）：显示器名称
- **返回值**: `s`（string）：背景 URI
- **触发条件**: 需要读取指定工作区和显示器的壁纸时调用
- **使用场景**: 需要读取指定工作区和显示器的壁纸 URI 时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetWorkspaceBackgroundForMonitor 0 "eDP-1"
```

#### SetMonitorBackground

设置指定显示器的背景图片文件。

- **输入参数**:
  - `monitorName`（string, 类型 `s`）：显示器名称
  - `imageGile`（string, 类型 `s`）：图片文件路径
- **返回值**: 无
- **触发条件**: 用户为指定显示器设置背景图片时调用
- **使用场景**: 需要为指定显示器设置背景图片文件时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetMonitorBackground "eDP-1" "/usr/share/wallpapers/default.jpg"
```

#### SetWallpaperSlideShow

设置壁纸幻灯片播放。

- **输入参数**:
  - `monitorName`（string, 类型 `s`）：显示器名称
  - `slideShow`（string, 类型 `s`）：幻灯片配置（JSON 格式）
- **返回值**: 无
- **触发条件**: 用户配置壁纸幻灯片轮播时调用
- **使用场景**: 需要配置壁纸幻灯片轮播时使用，例如设置壁纸自动切换间隔。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.SetWallpaperSlideShow "eDP-1" '{"interval": 300}'
```

#### GetWallpaperSlideShow

获取壁纸幻灯片播放配置。

- **输入参数**: `monitorName`（string, 类型 `s`）：显示器名称
- **返回值**: `s`（string）：幻灯片配置（JSON 格式）
- **触发条件**: 需要读取壁纸幻灯片轮播配置时调用
- **使用场景**: 需要读取壁纸幻灯片轮播配置用于显示时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.deepin.dde.Appearance1.GetWallpaperSlideShow "eDP-1"
```

## 属性（Properties）

#### FontSize

当前字体大小。

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | readwrite |
- **使用场景**: 需要读取或设置当前字体大小时使用。

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

#### Opacity

窗口不透明度。

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | readwrite |
- **使用场景**: 需要读取或设置窗口不透明度时使用。

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

#### WindowRadius

窗口圆角半径。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |
- **使用场景**: 需要读取或设置窗口圆角半径时使用。

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

#### Background

当前背景。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |
- **使用场景**: 需要读取当前背景 URI 用于显示时使用。

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 Background
```

#### GlobalTheme

当前全局主题。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |
- **使用场景**: 需要读取当前全局主题名称时使用。

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 GlobalTheme
```

#### GtkTheme

当前 GTK 主题。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |
- **使用场景**: 需要读取当前 GTK 主题名称时使用。

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 GtkTheme
```

#### IconTheme

当前图标主题。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |
- **使用场景**: 需要读取当前图标主题名称时使用。

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 IconTheme
```

#### CursorTheme

当前光标主题。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |
- **使用场景**: 需要读取当前光标主题名称时使用。

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 CursorTheme
```

#### CursorSize

光标大小。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |
- **使用场景**: 需要读取或设置光标大小时使用。

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

#### MonospaceFont

当前等宽字体。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |
- **使用场景**: 需要读取当前等宽字体名称时使用。

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 MonospaceFont
```

#### StandardFont

当前标准字体。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |
- **使用场景**: 需要读取当前标准字体名称时使用。

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 StandardFont
```

#### QtActiveColor

Qt 活动色。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |
- **使用场景**: 需要读取或设置 Qt 活动色时使用。

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
  org.deepin.dde.Appearance1 QtActiveColor "<'#007AFF'>"
```

#### WallpaperSlideShow

壁纸幻灯片播放配置。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |
- **使用场景**: 需要读取或设置壁纸幻灯片轮播配置时使用。

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
  org.deepin.dde.Appearance1 WallpaperSlideShow "<'{\"interval\": 300}'>"
```

#### WallpaperURls

壁纸 URI 列表。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |
- **使用场景**: 需要读取壁纸 URI 列表用于显示时使用。

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Appearance1 WallpaperURls
```

#### DTKSizeMode

DTK 缩放模式。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |
- **使用场景**: 需要读取或设置 DTK 缩放模式时使用。

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

#### QtScrollBarPolicy

Qt 滚动条策略。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |
- **使用场景**: 需要读取或设置 Qt 滚动条显示策略时使用。

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

## 信号（Signals）

#### Changed

外观属性变化时发出。

- **参数**:
  - `ty`（string, 类型 `s`）：属性类型
  - `value`（string, 类型 `s`）：新值
- **触发条件**: 外观属性被设置时发出
- **使用场景**: 需要监听外观属性变化以同步更新 UI 或其他组件状态时使用。

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1
```

#### Refreshed

外观配置刷新完成时发出。

- **参数**: `type`（string, 类型 `s`）：刷新类型
- **触发条件**: 外观配置刷新完成时发出
- **使用场景**: 需要在外观配置刷新完成后执行后续操作时使用。

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1
```

---
