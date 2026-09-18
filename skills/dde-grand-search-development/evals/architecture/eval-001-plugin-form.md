# Eval: 识别全局搜索插件的接入形态

## 任务

用户说：「我想给 deepin 全局搜索加一个搜索能力，让我自己的数据也能在全局搜索里出现。我准备写一个 .so 插件，用 Q_PLUGIN_METADATA 注册，IID 该怎么定？」

请判断用户的方案是否正确，并给出正确的接入方式。

## 期望输出

回答应：
1. 明确指出全局搜索扩展插件**不是** `.so` 插件，不存在 IID / `Q_PLUGIN_METADATA` / `QPluginLoader` 加载流程
2. 说明正确形态：插件是一个提供 DBus 服务的进程，通过 `.conf` 配置文件被 daemon 发现
3. 说明 `.conf` 的安装路径为 `/usr/lib/$PLATFORM/dde-grand-search-daemon/plugins/searcher/`
4. 说明 daemon 通过 `Search`/`Stop`/`Action` 三个 DBus 方法与插件通信
5. 说明需要重启 `dde-grand-search-daemon` 才能加载

## 验证要点

- [ ] 明确否定了 `.so` + IID 的方案，而不是顺着用户的错误前提继续设计
- [ ] 指出接入方式是 `.conf` 配置文件 + 独立 DBus 服务
- [ ] 给出正确的插件目录路径（含 `$PLATFORM` / `x86_64-linux-gnu`）
- [ ] 提到 `Search`/`Stop`/`Action` 三个接口
- [ ] 提到重启 daemon 使配置生效
- [ ] 未虚构 IID 常量或 `Q_PLUGIN_METADATA` 字段

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 明确指出方案错误并给出正确的 `.conf` + DBus 服务接入方式，关键路径与接口正确 |
| ⚠️ **PARTIAL** | 指出不是 `.so` 插件，但未给出完整接入方式或路径错误 |
| ❌ **FAIL** | 顺着错误前提编造 IID，或把插件设计成 `.so`/`QPluginLoader` 方案 |

## 反模式检查

- [ ] 未虚构 IID 或 `Q_PLUGIN_METADATA` 元数据字段
- [ ] 未混用托盘插件（`PluginsItemInterfaceV2`）或 Shell 插件（`DApplet`）的接口
- [ ] 未把插件描述成需要实现 `pluginName()`/`init()` 等托盘接口
