# Eval: 为已有 DTK 应用接入全局搜索能力（跨 skill）

## 任务

用户有一个基于 DTK6 的笔记应用（QWidget 主窗口，已常驻运行），希望把这个应用的笔记搜索能力接入 deepin 全局搜索，让用户在全局搜索里能搜到笔记内容。要求复用应用已有的搜索逻辑，不额外常驻进程。

## 期望输出

回答应：
1. 使用 dde-grand-search-development 指导接入：编写 `.conf`，实现 `Search`/`Stop`/`Action` 三个 DBus 接口
2. 选择 `Manual` 模式（由已运行的应用自己注册 DBus 服务，daemon 只调用接口），并说明 Manual 不需要 `Exec`/`Priority`
3. 在应用启动时注册会话总线的 DBus 服务与对象，并保证应用退出时服务注销
4. 结果项 `type` 按笔记的实际形态填写（如 `text/plain` 以复用内置文本预览）
5. 使用 `$dtk-development` 加载 DTK 相关文档（如 DConfig 保存插件开关、DIconTheme 加载主题图标作为结果图标）
6. 不额外启动独立进程，符合用户「不额外常驻」的要求

## 验证要点

- [ ] 选择 `Manual` 模式，并说明该模式下 daemon 不管理进程
- [ ] 实现三个 DBus 接口，注册到会话总线
- [ ] `.conf` 字段完整（含 `Name`/`InterfaceVersion`/DBus 三要素）
- [ ] 结果项 `type` 填有效 MIME type 或语义化自定义值
- [ ] 回答中显式引用了 `$dtk-development` 或加载了 DTK 参考文档
- [ ] 未引入额外的常驻进程
- [ ] 未把接入方式描述为 `.so` 插件

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 正确选择 Manual 模式并完成三接口接入，同时按需引用 DTK 文档解决配置/图标问题 |
| ⚠️ **PARTIAL** | 接入方式正确但未引用 DTK skill，或误选 Auto 模式导致额外进程 |
| ❌ **FAIL** | 把接入实现为 `.so` 插件，或要求用户额外部署常驻进程 |

## 反模式检查

- [ ] 未在 dde-grand-search skill 中重复描述 DTK 通用知识（如 DConfig 详细用法）
- [ ] 未把插件描述为 `.so` / `Q_PLUGIN_METADATA` 方案
- [ ] 未为 Manual 模式指定 `Exec`/`Priority` 并声称生效
- [ ] 未混用托盘插件或 Shell 插件的接口
