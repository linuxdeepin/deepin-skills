# Eval: 插件未被加载的排查

## 任务

用户安装插件并重启了 daemon，但全局搜索里看不到任何插件结果。daemon 日志中没有 `Added plugin` 这一行。请给出排查步骤。

## 期望输出

回答应：
1. 首先确认 `.conf` 的文件名后缀与目录是否正确（`/usr/lib/$PLATFORM/dde-grand-search-daemon/plugins/searcher/`）
2. 检查 INI 根节点是否为 `[Grand Search]`
3. 检查必填字段 `Name`/`InterfaceVersion`/`DBusService`/`DBusAddress`/`DBusInterface` 是否齐全
4. 检查 `Name` 是否与内置搜索项冲突或与其他插件重名
5. 检查 `InterfaceVersion` 是否为 `1.0`
6. 检查插件目录与文件权限是否可读
7. 建议开启 `QT_LOGGING_RULES="logDaemon.debug=true"` 观察具体跳过原因

## 验证要点

- [ ] 检查了配置文件路径与 `.conf` 后缀
- [ ] 检查了 INI 根节点 `[Grand Search]`
- [ ] 检查了全部必填字段
- [ ] 检查了 `Name` 与内置搜索项冲突 / 重名
- [ ] 检查了 `InterfaceVersion` 为 `1.0`
- [ ] 建议开启 daemon 调试日志查看具体原因
- [ ] 未把问题归因于「daemon 需要重新编译」等错误方向

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 覆盖路径、根节点、必填字段、名称冲突、版本、权限等主要成因，并建议开日志定位 |
| ⚠️ **PARTIAL** | 覆盖部分成因但遗漏根节点或名称冲突这类高概率项 |
| ❌ **FAIL** | 建议修改 daemon 源码，或直接跳到插件代码层面排查 |

## 反模式检查

- [ ] 未建议修改 `dde-grand-search-daemon` 源码来「支持」插件
- [ ] 未忽略「配置未被解析」这一层，直接排查 DBus
- [ ] 未声称需要重新编译插件才能生效（配置问题与编译无关）
