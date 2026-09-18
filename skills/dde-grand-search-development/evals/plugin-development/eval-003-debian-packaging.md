# Eval: Debian 打包

## 任务

请为全局搜索插件编写 Debian 打包文件，使其可以发布为独立 deb 包。

## 期望输出

回答应：
1. 提供 `debian/control`，包含 `Source`、`Build-Depends`（debhelper、cmake、Qt 开发包）、`Package`、`Architecture`、`Depends`
2. `Depends` 中包含运行依赖 `dde-grand-search`
3. 提供 `debian/rules`，使用 `dh $@ --buildsystem=cmake`
4. 提供 `debian/changelog`、`debian/compat`（或 `debhelper-compat`）、`debian/source/format`
5. 说明构建命令：`dpkg-buildpackage -uc -us -nc`
6. 说明安装后仍需重启 daemon，或说明可在 `postinst` 中处理

## 验证要点

- [ ] `control` 包含 `Build-Depends` 与 `Depends`，且依赖 `dde-grand-search`
- [ ] `rules` 使用 cmake 构建系统
- [ ] 提供了 `changelog`（格式正确，含版本、发行版、维护者、日期）
- [ ] 提供了 `compat` 或 `debhelper-compat` 声明
- [ ] 给出构建与安装命令
- [ ] 说明插件安装后需重启 daemon 才生效

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 打包文件齐全且格式正确，依赖完整，说明了生效前提 |
| ⚠️ **PARTIAL** | 文件基本齐全但缺少 `Depends: dde-grand-search`，或未说明重启 daemon |
| ❌ **FAIL** | 缺少 `debian/rules` 或 `control`，或未使用 cmake 构建系统 |

## 反模式检查

- [ ] 未遗漏 `dde-grand-search` 运行依赖
- [ ] 未把插件打包到错误的安装路径
- [ ] 未声称安装后无需重启即可生效
