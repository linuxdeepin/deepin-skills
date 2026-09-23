# org.deepin.dde.daemon.systeminfo

系统信息配置资源，标记当前系统是否为 M900 型号配置。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `IsM900Config` | M900 配置标识 | 标记当前系统是否为 M900 型号配置 | bool | readwrite |

## 读写示例

```bash
# 查询 M900 配置标识
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.systeminfo -k IsM900Config
# 设置 M900 配置标识
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.systeminfo -k IsM900Config -v "<value>"
```
