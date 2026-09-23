# org.deepin.dde.application-manager

应用管理器环境变量配置资源，管理启动应用时的环境变量黑名单、额外注入的环境变量和事件上报跳过列表。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `appEnvironmentsBlacklist` | 环境变量黑名单 | 启动应用时需要忽略的环境变量列表，黑名单中的环境变量不会传递给被启动的应用 | array | readwrite |
| `appExtraEnvironments` | 附加环境变量 | 启动应用时额外注入的环境变量列表 | array | readwrite |
| `skipEventAppIds` | 跳过事件上报应用 | 跳过埋点上报的应用 ID 列表，这些应用自行上报事件，应用管理器不再重复上报 | array | readonly |

## 读写示例

```bash
# 查询环境变量黑名单
dde-dconfig get -a org.deepin.dde.application-manager -r org.deepin.dde.application-manager -k appEnvironmentsBlacklist
# 设置环境变量黑名单
dde-dconfig set -a org.deepin.dde.application-manager -r org.deepin.dde.application-manager -k appEnvironmentsBlacklist -v "<value>"

# 查询附加环境变量
dde-dconfig get -a org.deepin.dde.application-manager -r org.deepin.dde.application-manager -k appExtraEnvironments
# 设置附加环境变量
dde-dconfig set -a org.deepin.dde.application-manager -r org.deepin.dde.application-manager -k appExtraEnvironments -v "<value>"

# 查询跳过事件上报应用列表
dde-dconfig get -a org.deepin.dde.application-manager -r org.deepin.dde.application-manager -k skipEventAppIds
```
