# Eval: 从零创建插件工程

## 任务

请为一个新的全局搜索插件搭建完整的工程骨架，包括目录结构、CMake 配置、conf 模板、入口与 Adaptor。

## 期望输出

回答应：
1. 给出完整目录结构：`CMakeLists.txt`、`main.cpp`、`searcher.h/.cpp`、`searchpluginadaptor.h/.cpp`、`*.conf.in`
2. CMake 中自动检测 Qt5/Qt6 并链接 `Core`/`DBus`（必要时 `Gui`）
3. 用 `include(GNUInstallDirs)` + `${CMAKE_INSTALL_FULL_LIBDIR}` 表达安装路径
4. 用 `configure_file` 从 `.conf.in` 生成 `.conf`，注入 `Exec` 的绝对路径
5. 可执行文件与 `.conf` 安装到同一 searcher 插件目录
6. 启用 `CMAKE_AUTOMOC`

## 验证要点

- [ ] 目录结构完整，包含 conf 模板文件
- [ ] 安装路径为 `${CMAKE_INSTALL_FULL_LIBDIR}/dde-grand-search-daemon/plugins/searcher`
- [ ] 使用 `configure_file` 生成 `.conf` 而非手写架构路径
- [ ] 可执行文件与 `.conf` 安装到同一目录
- [ ] 启用 `CMAKE_AUTOMOC ON`
- [ ] 提供了 Qt5/Qt6 兼容处理
- [ ] `main()` 中注册会话总线服务与对象

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 工程结构完整、安装路径正确、conf 由模板生成，且入口注册逻辑正确 |
| ⚠️ **PARTIAL** | 结构完整但硬编码架构路径，或未安装 `.conf` |
| ❌ **FAIL** | 把插件做成 `.so`，或安装到 `bin/`，或未提供 `.conf` |

## 反模式检查

- [ ] 未把插件编译为库（`add_library` + `Q_PLUGIN_METADATA`）
- [ ] 未硬编码 `/usr/lib/x86_64-linux-gnu`
- [ ] 未把可执行文件安装到 `${CMAKE_INSTALL_BINDIR}`
- [ ] 未遗漏 `.conf` 的安装
