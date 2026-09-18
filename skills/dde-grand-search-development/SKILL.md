---
name: dde-grand-search-development
description: "用于 deepin/UOS v25 的 dde-grand-search 扩展搜索插件（Searcher Plugin）开发与维护。当用户需要以 DBus 服务接入全局搜索、实现 Search/Stop/Action 接口与结果 JSON、编写插件 .conf 与选择 Auto/Manual/Trigger 运行模式、构建打包安装，或排查插件未加载、搜索无结果时使用。 涉及 DTK 通用 API 时需配合 dtk-development 使用。"
---

# DDE 全局搜索插件开发指南

全局搜索（dde-grand-search）的扩展搜索能力以 **DBus 服务**的形式接入：插件是一个提供搜索服务的独立进程（或宿主应用的一部分），后端 `dde-grand-search-daemon` 通过 `.conf` 配置文件发现插件，调用其 `Search`/`Stop`/`Action` 三个 DBus 方法，并把返回的 JSON 结果展示在全局搜索界面中。

**这不是 `.so` 动态库插件**——不存在 IID、`Q_PLUGIN_METADATA` 或 `QPluginLoader` 加载流程。如果用户的任务描述里出现「搜索插件」「全局搜索接入」「让搜索结果出现在全局搜索里」，应优先考虑本 skill。

## 适用范围

- 默认目标为 deepin/UOS v25 的 `dde-grand-search` 及其后端 `dde-grand-search-daemon`，插件接口协议当前仅支持 **V1.0**。
- 覆盖扩展搜索插件（`plugins/searcher/`）；不覆盖预览插件（`plugins/preview/`，那是按 MIME type 匹配的 `.so` 插件）、Dock 插件、Shell 插件。
- 开始前检查目标项目是否包含 `dde-grand-search-daemon`、`docs/plugin-development-guide.md` 或 `examples/calculator-search-plugin`；若都不存在，先与用户确认目标项目与版本。

## 关键约束

以下约束全部来自 daemon 源码，违反后表现为「插件被静默忽略」或「搜索无结果」，必须优先核对：

1. **版本三处一致**：`.conf` 的 `InterfaceVersion`、DBus 接口实现、JSON 报文中的 `ver` 必须都是 `"1.0"`。结果 JSON 中 `ver` 不匹配会导致整个结果被丢弃且只留一条 warning 日志。
2. **DBus 三要素必须与实现完全一致**：`DBusService`/`DBusAddress`/`DBusInterface` 必须与插件实际注册的服务名、对象路径、接口名逐字符一致。接口名不一致时 daemon 调用会报 `no such method`，插件看似正常但永远无结果。
3. **注册到 session bus**：插件必须在会话总线注册服务与对象；daemon 也只监听会话总线。
4. **`Name` 唯一且不得与内置搜索项冲突**：冲突或重名时该 `.conf` 会被直接跳过。内置名见 [references/plugin-config.md](references/plugin-config.md#5-内置搜索项冲突)。
5. **`Mode=Auto` 必须提供 `Exec`**；`Manual`/`Trigger` 不需要（提供也无效）。`Priority` 仅在 `Auto` 下生效。
6. **`Search` 必须可中断**：`Stop` 被调用时正在执行的 `Search` 必须尽快返回。daemon 对单次搜索设 **25 秒**超时，超时按无结果处理。
7. **结果解析上限**：跨所有分组**累计最多解析 100 项**，超出部分被丢弃；`item`/`name`/`type` 任一为空的结果项被跳过；`group` 为空的分组被整体跳过。
8. **`group` 与 `name` 由插件负责国际化**：daemon 与前端只做透传（内置分组名有映射表，自定义分组名原样显示）。不要指望框架翻译。
9. **`type` 不是展示字段**：它用于匹配预览插件，需遵循 MIME type 规范；自定义值会导致落到通用预览。扩展属性（`itemLevel`/`itemTailer` 等）**只对内置搜索器生效**，第三方插件无法设置。
10. **改配置后必须重启 daemon**：`.conf` 只在 daemon 启动时读取一次。

## 关联 Skill

需要 DTK 通用知识（DConfig 配置、DIconTheme 图标、Dtk6 CMake、主题适配）或为插件开发配套的 DTK 图形界面时，使用 `$dtk-development`。若该 skill 不可用，本 skill 仍可独立执行。

## 默认工作流

1. 先确认任务类型：**新建插件**、**修改已有插件**、**接入现有应用**（Manual 模式）还是**排查故障**，并核对目标 daemon 的接口版本与插件目录。
2. 检查目标项目是否已有 `examples/` 或现存插件，复用其工程结构、conf 命名与安装规则，避免自造目录约定。
3. 按 [references/plugin-config.md](references/plugin-config.md) 选定运行模式与优先级，分配 DBus 三要素，写出 `.conf`。
4. 按 [references/plugin-protocol.md](references/plugin-protocol.md) 实现 `Search`/`Stop`/`Action`：严格构造输入解析与结果 JSON，保证可中断。
5. 按 [references/plugin-development.md](references/plugin-development.md) 配置 CMake 与打包，把可执行文件与 `.conf` 安装到 `${CMAKE_INSTALL_FULL_LIBDIR}/dde-grand-search-daemon/plugins/searcher/`。
6. 重启 daemon 并按 [references/debugging.md](references/debugging.md) 验证：先确认插件被发现，再用 `dbus-send` 单独验证接口，最后在搜索界面确认展示与点击行为。
7. 报告实际执行到的验证步骤与未验证项，不要声称已验证但未运行的内容。

## 快速路由

| 场景 | 参考文档 |
|------|----------|
| 理解整体架构、搜索与操作时序、结果流转 | [references/architecture.md](references/architecture.md) |
| 实现 Search/Stop/Action 与结果 JSON 格式 | [references/plugin-protocol.md](references/plugin-protocol.md) |
| 编写 .conf、选择运行模式与优先级、进程管理 | [references/plugin-config.md](references/plugin-config.md) |
| 完整开发流程：工程、构建、安装、打包、验证 | [references/plugin-development.md](references/plugin-development.md) |
| 日志、dbus-send、故障排查 | [references/debugging.md](references/debugging.md) |
| 常见陷阱与反模式 | [references/gotchas.md](references/gotchas.md) |

## 工程模板

创建新插件时可从 `assets/` 复制模板，避免遗漏安装路径或配置字段：

| 模板 | 路径 |
|------|------|
| CMake 构建配置（Qt5/Qt6 自动检测、conf 生成、安装规则） | [assets/cmake/CMakeLists.txt](assets/cmake/CMakeLists.txt) |
| 插件配置模板（含字段说明与 Exec 注入） | [assets/conf/plugin.conf.in](assets/conf/plugin.conf.in) |
| Trigger 模式的 D-Bus service 模板 | [assets/conf/plugin.service.in](assets/conf/plugin.service.in) |
| 插件入口（DBus 服务注册） | [assets/src/main.cpp](assets/src/main.cpp) |
| 搜索器骨架（Search/Stop/Action、中断管理与 JSON 构造） | [assets/src/searcher.h](assets/src/searcher.h)、[assets/src/searcher.cpp](assets/src/searcher.cpp) |
| DBus Adaptor（含 Introspection 元数据） | [assets/src/searchpluginadaptor.h](assets/src/searchpluginadaptor.h)、[assets/src/searchpluginadaptor.cpp](assets/src/searchpluginadaptor.cpp) |
| 接口 XML（可用于 qdbusxml2cpp 生成 Adaptor） | [assets/dbus/com.deepin.dde.grandsearch.searchplugin.xml](assets/dbus/com.deepin.dde.grandsearch.searchplugin.xml) |
| Debian 打包文件 | [assets/debian/control](assets/debian/control)、[assets/debian/rules](assets/debian/rules)、[assets/debian/changelog](assets/debian/changelog)、[assets/debian/compat](assets/debian/compat)、[assets/debian/source/format](assets/debian/source/format) |

模板已按本文档的约束验证：使用 Qt6 可编译，安装后 `.conf` 与可执行文件落在 `/usr/lib/<arch>/dde-grand-search-daemon/plugins/searcher/`，`Search`/`Stop`/`Action` 三个接口可在会话总线上正常调用并返回符合 V1.0 规范的结果。

## Evals 测试用例

验证 skill 有效性的测试用例按功能模块分类组织，详见 [evals/README.md](evals/README.md)。
