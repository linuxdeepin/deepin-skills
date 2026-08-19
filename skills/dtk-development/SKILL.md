---
name: dtk-development
description: "用于 deepin/UOS v25 的 DTK（deepin Tool Kit）桌面应用及插件开发维护，同时支持 DTK5 和 DTK6。当用户需要创建 deepin/UOS 桌面应用或插件、选用 QWidget 控件或 QML 控件、实现主题与调色板、使用 DCI 图标或主题图标、管理 DConfig 配置与持久化配置、发送系统通知或应用通知、调用 D-Bus、实现单实例、处理窗口效果、平台适配，或编译调试 DTK 源码时使用。"
---

# DTK 开发指南

DTK 是深度桌面环境的核心开发框架，覆盖应用界面与交互、主题与视觉、配置、系统集成、工程构建和源码调试。按功能快速定位对应文档。

## 适用范围

- 默认目标为 deepin/UOS v25，同时支持 DTK5/Qt 5 和 DTK6/Qt 6。开始实现前先从 CMake 包名、链接库和源码分支确认 DTK/Qt 主版本，并全程使用对应版本的 API、模块名和构建配置，不要混用。
- 本 skill 负责普通 DTK 应用和 DTK 框架源码，不覆盖 DDE 组件各自的插件框架；涉及通用 DTK API 时仍可使用对应参考。

## 关键约束

- 先确定 Qt/DTK 主版本，再选择包名、target、头文件、库和安装路径；同一构建链路中不要混用 DTK5/Qt 5 与 DTK6/Qt 6。
- 修改 DTK 框架源码后，要确认应用实际加载的是构建产物，而不是只验证编译成功后继续运行系统安装库。

## 默认工作流

1. 检查目标工程的 Qt/DTK 主版本、QWidget 或 QML 技术栈、应用 ID、构建方式和现有代码约定。
2. 判断问题属于应用层还是 DTK 框架层，并从下表读取完成任务所需的最少参考文档。
3. 优先使用目标项目已有模式和 DTK 公开 API；修改 DTK 源码前先定位实际绘制、平台插件或配置链路。
4. 完成实现及必要的 CMake、资源、DConfig、翻译、桌面文件和 Debian 打包改动。
5. 构建最小相关目标并运行验证；主题和窗口问题至少覆盖亮暗主题以及当前使用的 X11/Wayland 后端。
6. 交付前检查日志、单实例恢复、图标查找、配置默认值和安装后运行结果，并报告未执行的验证。

## 快速路由

| 场景 | 参考文档 |
|------|----------|
| 了解 DTK 架构、项目关系或定位跨应用共性问题 | [references/architecture.md](references/architecture.md) |
| 创建 DTK 应用、配置 CMake、应用身份、翻译、日志和依赖 | [references/app-dev-with-dtk.md](references/app-dev-with-dtk.md) |
| 修改、编译和调试 DTK 源码 | [references/dtksrc-compile-debug.md](references/dtksrc-compile-debug.md) |
| 排查常见错误、反模式和行为异常 | [references/gotchas.md](references/gotchas.md) |
| 选择和使用 QWidget 控件 | [references/widgets/index.md](references/widgets/index.md) |
| 使用或调试 QWidget Chameleon | [references/theme/chameleon-widget.md](references/theme/chameleon-widget.md) |
| v25 选择和使用 DTK QML 控件 | [references/declarative/index.md](references/declarative/index.md) |
| v25 使用或调试 DTK QML Chameleon | [references/theme/chameleon-qml.md](references/theme/chameleon-qml.md) |
| 查看 QWidget 与 v25 DTK QML 可运行示例 | [references/examples.md](references/examples.md) |
| 处理配色、主题图标、字体和主题切换 | [references/theme/index.md](references/theme/index.md) |
| 处理窗口装饰、模糊效果和平台兼容 | [references/platform-abstraction.md](references/platform-abstraction.md) |
| 管理应用配置和 DConfig | [references/config/index.md](references/config/index.md) |
| 使用应用入口、默认日志、DBus、通知、单实例及系统服务 | [references/widgets/application.md](references/widgets/application.md)、[references/utilities/index.md](references/utilities/index.md) |

## 高频场景直达

- **自定义控件使用主题图标** → [references/theme/palette.md](references/theme/palette.md)
- **应用控件使用主题图标** → [references/theme/icontheme.md](references/theme/icontheme.md)
- **v25 QML 中显示 dci 图标** → [references/declarative/dci-icon.md](references/declarative/dci-icon.md)
- **DGuiApplicationHelper 主题/调色板** → [references/utilities/gui-helper.md](references/utilities/gui-helper.md)
- **DSysInfo 系统版本判断** → [references/utilities/sysinfo.md](references/utilities/sysinfo.md)
- **DDBusSender DBus 通信** → [references/utilities/dbus.md](references/utilities/dbus.md)
- **DWindowManagerHelper 窗口管理** → [references/utilities/window-manager.md](references/utilities/window-manager.md)
- **v25 QML D.DTK 全局对象** → [references/declarative/dtk-global.md](references/declarative/dtk-global.md)
- **DBlurEffectWidget 模糊效果** → [references/widgets/blur-effect.md](references/widgets/blur-effect.md)
- **DStyledItemDelegate 列表项** → [references/widgets/item-delegate.md](references/widgets/item-delegate.md)
- **DProgressBar 进度条** → [references/widgets/progress.md](references/widgets/progress.md)
- **DInputDialog 输入对话框** → [references/widgets/dialog.md](references/widgets/dialog.md)
- **排查主题不生效/QSS 冲突** → [references/gotchas.md](references/gotchas.md) 第 2 节
- **DConfig 配置读不到** → [references/gotchas.md](references/gotchas.md) 第 4 节
- **图标查找失败** → [references/gotchas.md](references/gotchas.md) 第 3 节

创建或维护 DTK 应用时，按任务加载上表对应的模块入口，并以模块 index 中的约束为准。遇到异常行为或不确定最佳实践时，优先查阅 [references/gotchas.md](references/gotchas.md)。

## 工程模板

创建新项目时可从 `assets/` 目录复制模板文件：

| 模板 | 路径 |
|------|------|
| CMakeLists.txt（DTK6） | [assets/cmake/CMakeLists-DTK6.txt](assets/cmake/CMakeLists-DTK6.txt) |
| CMakeLists.txt（DTK5+DTK6 兼容） | [assets/cmake/CMakeLists-DTK5-DTK6-compat.txt](assets/cmake/CMakeLists-DTK5-DTK6-compat.txt) |
| main.cpp（QWidget 应用） | [assets/src/main.cpp](assets/src/main.cpp) |
| main.cpp（日志应用） | [assets/src/main-log.cpp](assets/src/main-log.cpp) |
| .desktop 文件 | [assets/desktop/myapp.desktop](assets/desktop/myapp.desktop) |
| DConfig meta 模板 | [assets/config/org.example.settings.json](assets/config/org.example.settings.json) |
| DConfig override 模板 | [assets/config/org.example.settings-override.json](assets/config/org.example.settings-override.json) |

## Evals 测试用例

验证 skill 有效性的测试用例按功能模块分类组织，详见 [evals/README.md](evals/README.md)。
