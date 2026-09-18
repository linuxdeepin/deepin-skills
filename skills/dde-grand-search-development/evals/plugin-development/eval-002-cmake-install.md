# Eval: CMake 安装规则与 conf 生成

## 任务

请说明插件构建产物的安装位置与 `.conf` 中 `Exec` 路径的生成方式，并给出对应的 CMake 代码。

## 期望输出

回答应：
1. 安装目录为 `/usr/lib/$PLATFORM/dde-grand-search-daemon/plugins/searcher/`，x86_64 下即 `/usr/lib/x86_64-linux-gnu/dde-grand-search-daemon/plugins/searcher/`
2. 用 `${CMAKE_INSTALL_FULL_LIBDIR}` 表达平台目录，让 CMake 自动展开
3. `.conf` 从 `.conf.in` 模板用 `configure_file(... @ONLY)` 生成
4. `Exec` 的值应为 `${PLUGIN_INSTALL_DIR}/${PROJECT_NAME}` 的绝对路径
5. 可执行文件与 `.conf` 一并 `install()`
6. 说明为何不硬编码路径（多架构、`CMAKE_INSTALL_PREFIX` 可变）

## 验证要点

- [ ] 给出正确完整的安装目录
- [ ] 使用 `CMAKE_INSTALL_FULL_LIBDIR` 而非硬编码
- [ ] 使用 `configure_file` 生成 conf，且用 `@ONLY`
- [ ] `Exec` 为绝对路径且指向安装后的可执行文件
- [ ] 可执行文件与 conf 都执行了 `install()`
- [ ] 解释了避免硬编码的原因

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 路径、生成方式、安装规则全部正确，并说明了避免硬编码的理由 |
| ⚠️ **PARTIAL** | 路径正确但硬编码架构目录，或 `Exec` 指向构建目录而非安装目录 |
| ❌ **FAIL** | 安装目录错误（如 `bin/` 或插件目录名写错），或未生成 conf |

## 反模式检查

- [ ] 未硬编码 `/usr/lib/x86_64-linux-gnu`
- [ ] 未把 `Exec` 指向 `build/` 下的可执行文件
- [ ] 未遗漏 `@ONLY`（否则会误替换 `${...}` 形式的内容）
- [ ] 未把 conf 安装到与可执行文件不同的目录
