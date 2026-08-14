---
name: dtk-development
description: "用于 deepin/UOS v20（仅 1070）和 v25 的 DTK（deepin Tool Kit）桌面应用开发维护，覆盖 v20 的 Qt 5/DTK5 QWidget 环境以及 v25 的 DTK5/DTK6 QWidget/QML 环境。当用户需要创建或修改 DTK 应用，选择控件，实现主题、调色板、DCI 图标、DConfig、D-Bus、通知、单实例、窗口效果、平台适配，处理跨版本 API 差异，或编译调试 DTK 源码时使用。"
---

# DTK 开发指南

DTK 是深度桌面环境的核心开发框架，覆盖应用界面与交互、主题与视觉、配置、系统集成、工程构建和源码调试。按功能快速定位对应文档。

## 适用范围

- 支持 deepin/UOS v20 和 v25；本文中的 v20 统一指 1070，不再支持其他 v20 版本。任务已明确系统版本时使用指定版本；未明确时按 `DSysInfo::majorVersion()`/`minorVersion()` 的实现读取当前系统。
- v20 以 Qt 5.11、DTK5 和 QWidget 为基线；DTK 在 v20 不提供 `dtkdeclarative` 或 DTK QML 控件，QML 任务直接使用 Qt Quick/Qt Quick Controls 2。
- v25 同时支持 DTK5/Qt 5 和 DTK6/Qt 6，并提供 dtkdeclarative。系统版本确定后仍须独立检查目标工程实际使用的 Qt/DTK 主版本和构建系统。
- 本 skill 负责普通 DTK 应用和 DTK 框架源码，不覆盖 DDE 组件各自的插件框架；涉及通用 DTK API 时仍可使用对应参考。

## 系统版本判定

1. 优先采用任务中明确给出的 v20 或 v25 目标。交叉开发时目标系统可以和当前宿主系统不同。
2. 任务未给出目标版本时，读取 `/etc/os-version` 的 `[Version]` 节：`MajorVersion=20` 选择 v20，`MajorVersion=25` 选择 v25；同时记录 `MinorVersion` 用于报告环境。
3. 上述字段正是 `DSysInfo::majorVersion()` 和 `DSysInfo::minorVersion()` 的数据源。`/etc/os-release` 的 `VERSION_ID` 属于 `DSysInfo::productVersion()` 数据源，不替代该判断。
4. 文件缺失、字段为空或主版本不是 20/25 时，先向用户确认目标版本，不静默回退。

## GUI 技术栈判定

GUI 任务在读取控件或风格文档前，先根据目标工程现有依赖、应用入口和当前改动所在的 UI 边界判定技术栈：

- 使用 `QApplication`、`QWidget` 或 dtkwidget 控件的任务按 QWidget 处理，读取 [widgets/index.md](references/widgets/index.md)；涉及 Chameleon 插件、控件绘制或风格调试时再读取 [theme/chameleon-widget.md](references/theme/chameleon-widget.md)。
- v25 中使用 `QQmlApplicationEngine`、Qt Quick 或 `org.deepin.dtk` 的任务按 QML 处理，读取 [declarative/index.md](references/declarative/index.md)；涉及 Qt Quick Controls 2 Chameleon 时再读取 [theme/chameleon-qml.md](references/theme/chameleon-qml.md)。
- v20 QML 只使用 Qt Quick/Qt Quick Controls 2，不读取 `references/declarative/` 或 DTK QML Chameleon 文档；按目标环境实际发布的 Qt QML 模块实现。
- QWidget 与 QML 混合工程按当前改动所在边界选择文档；需要比较两套风格或定位跨栈视觉差异时，按目标系统能力分别读取 QWidget 与 QML 专篇。技术栈尚未确定时先检查工程入口和依赖，不通过额外总览文档分流。
- 非 GUI 任务不加载 QWidget、dtkdeclarative 或 Chameleon 文档。

## 关键约束

- 先确定目标系统版本，再确定 Qt/DTK 主版本和构建系统；同一构建链路中不要混用 v20/v25 专有 API，也不要混用 DTK5/Qt 5 与 DTK6/Qt 6。
- 使用任何 DTK 接口、类、控件、重载、枚举、宏或辅助工具前，先检查目标构建环境实际发布并由编译器使用的公共头文件；以目标 sysroot/SDK、开发包或安装暂存目录中的公共转发头和声明为准，不根据系统版本标签、其他环境的头文件、源码目录或文档示例臆测可用性。只使用公共声明，不依赖私有头文件或源码中的未发布接口。
- 同时检查目标环境导出的 CMake package/target、pkg-config 和可执行工具；daemon 与协议能力通过 DBus introspection 或服务公开接口确认。不要在各模块文档中维护单个接口或控件的 v20/v25 可用性清单。
- 同一源码可分别面向 v20 和 v25 构建，不要求同一二进制跨系统运行。头文件、
  符号和依赖差异在构建配置、适配层或最小 API 调用点进行编译期隔离；两边均可
  编译但行为取决于环境时，才使用 `DSysInfo`、DBus introspection、服务 unit、
  显示后端或资源存在性进行运行时判断。
- v20 只面向 1070 实际发布的公共能力，不增加其他 v20 版本兼容分支。
- v20 QML 只使用 Qt 提供的模块与控件，不导入 `org.deepin.dtk`，不使用 D.DTK、DciIcon、ColorSelector 或 Chameleon DTK QML 风格。
- 修改 DTK 框架源码后，要确认应用实际加载的是构建产物，而不是只验证编译成功后继续运行系统安装库。

## 默认工作流

1. 按“系统版本判定”确定 v20/v25，并记录 `MinorVersion`。
2. 检查目标工程的 Qt/DTK 主版本、应用 ID、构建方式和现有代码约定；GUI 任务按“GUI 技术栈判定”确定 QWidget、QML 或当前混合边界。
3. 从目标构建环境的公共头文件与导出构建元数据确认所需能力，判断问题属于应用层还是 DTK 框架层。
4. 从下表读取完成任务所需的最少参考文档；不要同时加载无关的 QWidget 与 QML 控件/风格档案。
5. 使用对应档案的公开 API；v25 再区分 DTK5/DTK6。
6. 完成实现及必要的 CMake/qmake、资源、配置、翻译、桌面文件和 Debian 打包改动。
7. 构建最小相关目标并运行验证；主题和窗口问题至少覆盖亮暗主题以及目标环境使用的 X11/Wayland 后端。
8. 交付前检查日志、单实例恢复、图标查找、配置默认值和安装后运行结果，并报告未执行的验证。

## 文档路由

| 场景 | 参考文档 |
|------|----------|
| 了解 DTK 架构、项目关系或定位跨应用共性问题 | [architecture.md](references/architecture.md) |
| 创建 DTK 应用、配置 CMake、应用身份、翻译、日志和依赖 | [app-dev-with-dtk.md](references/app-dev-with-dtk.md) |
| 修改、编译和调试 DTK 源码 | [dtksrc-compile-debug.md](references/dtksrc-compile-debug.md) |
| 选择和使用 QWidget 控件 | [widgets/index.md](references/widgets/index.md) |
| 使用或调试 QWidget Chameleon | [theme/chameleon-widget.md](references/theme/chameleon-widget.md) |
| v25 选择和使用 DTK QML 控件 | [declarative/index.md](references/declarative/index.md) |
| v25 使用或调试 DTK QML Chameleon | [theme/chameleon-qml.md](references/theme/chameleon-qml.md) |
| 查看 QWidget 与 v25 DTK QML 可运行示例 | [examples.md](references/examples.md) |
| 处理配色、主题图标、字体和主题切换 | [theme/index.md](references/theme/index.md) |
| 处理窗口装饰、模糊效果和平台兼容 | [platform-abstraction.md](references/platform-abstraction.md) |
| 管理应用配置和 DConfig | [config/index.md](references/config/index.md) |
| 使用应用入口、默认日志、DBus、通知、单实例及系统服务 | [widgets/application.md](references/widgets/application.md)、[utilities/index.md](references/utilities/index.md) |

## 高频场景直达

- **自定义控件使用主题图标** → [theme/palette.md](references/theme/palette.md)
- **应用控件使用主题图标** → [theme/icontheme.md](references/theme/icontheme.md)
- **v25 QML 中显示 dci 图标** → [declarative/dci-icon.md](references/declarative/dci-icon.md)
- **DGuiApplicationHelper 主题/调色板** → [utilities/gui-helper.md](references/utilities/gui-helper.md)
- **DSysInfo 系统版本判断** → [utilities/sysinfo.md](references/utilities/sysinfo.md)
- **DDBusSender DBus 通信** → [utilities/dbus.md](references/utilities/dbus.md)
- **DWindowManagerHelper 窗口管理** → [utilities/window-manager.md](references/utilities/window-manager.md)
- **v25 QML D.DTK 全局对象** → [declarative/dtk-global.md](references/declarative/dtk-global.md)
- **DBlurEffectWidget 模糊效果** → [widgets/blur-effect.md](references/widgets/blur-effect.md)
- **DStyledItemDelegate 列表项** → [widgets/item-delegate.md](references/widgets/item-delegate.md)
- **DProgressBar 进度条** → [widgets/progress.md](references/widgets/progress.md)
- **DInputDialog 输入对话框** → [widgets/dialog.md](references/widgets/dialog.md)

创建或维护 DTK 应用时，按任务加载上表对应的模块入口，并以模块 index 中的约束为准。

## Evals 测试用例

验证 skill 有效性的测试用例按功能模块分类组织。详见 [evals/README.md](evals/README.md)。
