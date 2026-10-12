# dtkwidget-dev

dtkwidget 是 DTK 的 C++ 控件库，全链路界面控件涵盖按钮、容器与布局、对话框、输入控件、列表视图、样式与主题、窗口与标题栏，统一遵循 DTK 视觉与交互规范。

## 开发包

当前版本使用 DTK6，开发包名为 `libdtk6widget-dev`。该开发包提供 DTK6 的公开头文件和以下构建入口：

- CMake 包 `Dtk6Widget` 与导出目标 `Dtk6::Widget`
- pkg-config 模块 `dtk6widget`
- qmake 模块 `DtkWidget`

仍需维护 DTK5 工程时，使用兼容开发包 `libdtkwidget-dev`。它提供 CMake 包 `DtkWidget`、导出目标 `Dtk::Widget`、pkg-config 模块 `dtkwidget` 和同名 qmake 模块。

## 集成

### CMake 配置

CMake 是当前推荐的集成方式。DTK6 工程在已有构建目标上查找 `Dtk6Widget` 并链接 `Dtk6::Widget`：

```cmake
find_package(Dtk6Widget REQUIRED)
target_link_libraries(your_target PRIVATE Dtk6::Widget)
```

`your_target` 替换为使用方工程中的目标名。`Dtk6::Widget` 会向该目标提供 dtkwidget 的头文件搜索路径、链接信息、编译定义和传递依赖，不需要再使用 `include_directories()`、`link_directories()` 或逐项链接 dtkwidget 所依赖的库。

仍使用 DTK5 的工程改为查找 `DtkWidget` 并链接 `Dtk::Widget`：

```cmake
find_package(DtkWidget REQUIRED)
target_link_libraries(your_target PRIVATE Dtk::Widget)
```

### 使用方式

构建目标链接 dtkwidget 后，可以直接包含所需类型的公开转发头：

```cpp
#include <DLineEdit>
```

也可以包含对应的实际公开头文件，例如 `#include <dlineedit.h>`。公开类型主要位于 `Dtk::Widget` 命名空间，可使用完整限定名，也可在合适的作用域使用 `DWIDGET_USE_NAMESPACE`。开发包还提供便捷头 `DtkWidgets`，一次引入所有已安装的公开头文件。


---

## 接口分类

- [按钮](dtkwidget-dev/buttons.md) — 提供图标按钮、语义化按钮（建议/警告）、开关切换按钮、命令链接按钮、浮动操作按钮、方向箭头按钮六种按钮类型及按钮组容器，覆盖常见交互触发场景
- [容器与布局](dtkwidget-dev/containers-and-layout.md) — 提供框架、分隔线、分组背景三类结构化容器，以及抽屉、展开组两类可折叠内容区域和锚点布局、标签页栏两类布局工具，帮助组织界面层级和空间分配
- [对话框](dtkwidget-dev/dialogs.md) — 提供模态与非模态对话框基类框架，并内置关于、文件选择、文本输入、许可证展示和功能特性介绍五类常用专用对话框
- [浮层与提示](dtkwidget-dev/overlays-and-tooltips.md) — 提供浮动在主界面之上的临时消息和提示控件，支持消息停留、自动消失和吐司式通知，适用于不阻塞用户操作的轻量反馈场景
- [输入控件](dtkwidget-dev/input-controls.md) — 为文本、数值和选择类输入提供 DTK 风格的编辑控件，支持单行与多行文本、密码、搜索、IP 地址、文件路径、快捷键、面包屑导航以及数值滑动和组合选择场景
- [列表与视图](dtkwidget-dev/list-and-views.md) — 提供列表展示和项渲染能力，支持标准项和自定义样式化项代理，适用于设置面板、文件浏览两类结构化数据展示场景
- [打印预览](dtkwidget-dev/print-preview.md) — 提供打印预览对话框及关联的页面设置能力，支持在预览界面中调整打印参数并实时查看效果
- [设置界面](dtkwidget-dev/settings-ui.md) — 提供从配置模型自动生成设置界面的框架，通过设置对话框和控件工厂将配置项映射为复选框、下拉框两类界面控件
- [样式与主题](dtkwidget-dev/style-and-theme.md) — 管理 DTK 样式引擎、调色板、主题切换、尺寸模式、字号规格和水印效果，并为无障碍检查提供开发辅助工具
- [工具与辅助](dtkwidget-dev/tools-and-helpers.md) — 提供标签显示、图片查看、文件图标获取三类辅助控件和控件操作工具函数，补充核心控件库未覆盖的通用界面需求
- [视觉效果与进度](dtkwidget-dev/visual-effects-and-progress.md) — 为控件和窗口添加高斯模糊、圆角裁剪、投影阴影三类视觉增强效果，并提供弹跳动画、水波进度、加载指示器和进度条四类动态反馈控件
- [窗口与标题栏](dtkwidget-dev/window-and-titlebar.md) — 提供 DTK 风格的主窗口框架和自定义标题栏，集成窗口装饰和交互能力，包括窗口圆角、阴影、拖拽、最大化/最小化/关闭按钮
