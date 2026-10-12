# dtkgui-dev

dtkgui 是 DTK 的 GUI 基础层，GUI 层能力涵盖 DCI 图标资源管理、图标与 SVG 渲染、文件拖拽与缩略图、调色板与主题、系统服务和窗口与平台，为 dtkwidget 和 dtkdeclarative 提供底层图形与平台支持。

## 开发包

当前版本使用 DTK6，开发包名为 `libdtk6gui-dev`。该开发包提供 DTK6 的公开头文件和以下构建入口：

- CMake 包 `Dtk6Gui` 与导出目标 `Dtk6::Gui`
- pkg-config 模块 `dtk6gui`
- qmake 模块 `dtkgui`

仍需维护 DTK5 工程时，使用兼容开发包 `libdtkgui-dev`。它提供 CMake 包 `DtkGui`、导出目标 `Dtk::Gui`、pkg-config 模块 `dtkgui` 和同名 qmake 模块。

## 集成

### CMake 配置

CMake 是当前推荐的集成方式。DTK6 工程在已有构建目标上查找 `Dtk6Gui` 并链接 `Dtk6::Gui`：

```cmake
find_package(Dtk6Gui REQUIRED)
target_link_libraries(your_target PRIVATE Dtk6::Gui)
```

`your_target` 替换为使用方工程中的目标名。`Dtk6::Gui` 会向该目标提供 dtkgui 的头文件搜索路径、链接信息、编译定义和传递依赖，不需要再使用 `include_directories()`、`link_directories()` 或逐项链接 dtkgui 所依赖的库。

仍使用 DTK5 的工程改为查找 `DtkGui` 并链接 `Dtk::Gui`：

```cmake
find_package(DtkGui REQUIRED)
target_link_libraries(your_target PRIVATE Dtk::Gui)
```

### 使用方式

构建目标链接 dtkgui 后，可以直接包含所需类型的公开转发头：

```cpp
#include <DPalette>
```

也可以包含对应的实际公开头文件，例如 `#include <dpalette.h>`。公开类型主要位于 `Dtk::Gui` 命名空间，可使用完整限定名，也可在合适的作用域使用 `DGUI_USE_NAMESPACE`。开发包还提供便捷头 `DtkGuis`，一次引入所有已安装的公开头文件。


---

## 接口分类

- [DCI 图标](dtkgui-dev/dci-icons.md) — 提供 DCI 图标资源的加载、渲染与动画播放能力，包括图标容器、单帧图像访问、图像序列播放器、内嵌调色板和整体动画播放器
- [文件拖拽、字体与缩略图](dtkgui-dev/file-drag-font-and-thumbnail.md) — 提供跨进程文件拖拽的客户端与服务端、字体安装与管理以及文件缩略图异步生成能力
- [图标与 SVG 渲染](dtkgui-dev/icon-and-svg-rendering.md) — 提供 DTK 图标加载、图标主题缓存管理、SVG 渲染和图像格式处理能力
- [调色板与主题](dtkgui-dev/palette-and-theme.md) — 提供 DTK 扩展调色板角色、应用级主题管理、原生设置读写和平台主题属性访问能力
- [系统服务](dtkgui-dev/system-services.md) — 提供系统服务调用（打开文件管理器、播放系统提示音）、屏幕区域监视和任务栏进度与计数控制能力
- [窗口与平台](dtkgui-dev/window-and-platform.md) — 提供窗口平台属性控制、窗口管理器功能查询、跨进程窗口分组和外部窗口引用能力
