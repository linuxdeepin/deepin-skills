# Eval: Trigger 模式配置

## 任务

用户希望插件不要常驻后台，只在用户搜索时按需启动。请给出完整的配置方案。

## 期望输出

回答应：
1. 推荐 `Mode=Trigger`（从 5.1.1 版本开始支持）
2. 给出 `.conf` 内容，说明 Trigger 模式**不需要** `Exec` 和 `Priority`
3. 说明还需在 `/usr/share/dbus-1/services/` 安装 `.service` 文件，声明服务名与可执行文件映射
4. 给出 `.service` 文件内容（`[D-BUS Service]` + `Name` + `Exec`）
5. 说明 daemon 通过向 `org.freedesktop.DBus.Peer.Ping` 发消息来激活服务
6. 说明 `.service` 中的 `Name` 必须与 `.conf` 的 `DBusService` 一致

## 验证要点

- [ ] 推荐 `Mode=Trigger`
- [ ] 说明 Trigger 不需要 `Exec`/`Priority`
- [ ] 给出 `.service` 文件内容，包含 `[D-BUS Service]`、`Name`、`Exec`
- [ ] 给出 `.service` 的正确安装路径 `/usr/share/dbus-1/services/`
- [ ] 说明激活机制为 DBus Ping / DBus 自启动
- [ ] 说明 `.service` 的 `Name` 与 `.conf` 的 `DBusService` 必须一致

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 给出 conf 与 service 两处配置，路径与一致性要求均正确 |
| ⚠️ **PARTIAL** | 选择了 Trigger 模式但遗漏 `.service` 文件或安装路径 |
| ❌ **FAIL** | 用 Auto+Low 冒充「按需启动」并声称进程不会常驻，或遗漏 Trigger 的关键前提 |

## 反模式检查

- [ ] 未在 Trigger 模式下要求填写 `Exec`
- [ ] 未遗漏 `.service` 文件的安装
- [ ] 未把 `.service` 安装到 `plugins/searcher/` 目录
