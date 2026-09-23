# org.deepin.dde.application-manager

应用管理器环境变量配置资源，管理启动应用时的环境变量黑名单和额外注入的环境变量。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `appEnvironmentsBlacklist` | 环境变量黑名单 | 配置启动应用时需要忽略的环境变量黑名单列表，黑名单中的环境变量不会传递给被启动的应用 | array | readwrite |
| `appExtraEnvironments` | 附加环境变量 | 配置启动应用时额外注入的环境变量列表 | array | readwrite |

## 读写示例

```bash
# 查询环境变量黑名单
dde-dconfig get -a org.deepin.dde.application-manager -r org.deepin.dde.application-manager -k appEnvironmentsBlacklist
# 设置环境变量黑名单
dde-dconfig set -a org.deepin.dde.application-manager -r org.deepin.dde.application-manager -k appEnvironmentsBlacklist -v "<value>"
```
