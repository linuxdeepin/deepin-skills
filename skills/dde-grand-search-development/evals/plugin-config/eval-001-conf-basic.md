# Eval: 编写插件配置文件

## 任务

为一个全局搜索插件编写 `.conf` 配置文件。插件信息：名称 `com.example.NoteSearch`，DBus 服务名 `com.example.NoteSearch`，对象路径 `/com/example/NoteSearch`，接口名 `com.example.NoteSearch.SearchPlugin`，希望由 daemon 管理进程，搜索时才启动但启动后常驻。

## 期望输出

回答应：
1. 使用 INI 格式，根节点为 `[Grand Search]`
2. 填写全部必填字段：`Name`、`InterfaceVersion`、`DBusService`、`DBusAddress`、`DBusInterface`
3. `Mode` 填 `Auto`，`Priority` 填 `1`（Middle：搜索时启动并守护）
4. 提供 `Exec` 字段（Auto 模式必须）
5. 说明安装路径为 `/usr/lib/$PLATFORM/dde-grand-search-daemon/plugins/searcher/`
6. 说明修改后需重启 `dde-grand-search-daemon`

## 验证要点

- [ ] 根节点为 `[Grand Search]`
- [ ] `InterfaceVersion=1.0`
- [ ] `Mode=Auto` 且 `Priority=1`
- [ ] 提供了 `Exec` 字段
- [ ] DBus 三要素与用户给出的信息一致
- [ ] 给出了正确的插件目录路径
- [ ] 提到重启 daemon

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 配置完整合法，模式与优先级选择符合需求，路径与生效方式正确 |
| ⚠️ **PARTIAL** | 配置基本正确但 `Priority` 选错，或遗漏路径/重启说明 |
| ❌ **FAIL** | 根节点错误，或遗漏必填字段，或 Auto 模式未提供 `Exec` |

## 反模式检查

- [ ] 未把根节点写成 `[Plugin]`、`[GrandSearch]` 等其他形式
- [ ] 未遗漏 `InterfaceVersion` 或填写非 `1.0` 的值
- [ ] 未把插件描述成 `.so` 或需要声明 IID
- [ ] 未在 `Name` 中使用内置搜索项名称
