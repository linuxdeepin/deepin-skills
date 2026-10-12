# org.deepin.dde.control-center.datetime

日期时间配置资源，管理用于时间同步的自定义 NTP 服务器地址。

## 配置项

| Key | Name | Description | 类型 | 取值范围 | Permissions | Flags |
|---|---|---|---|---|---|---|
| `customNtpServer` | 自定义 NTP 服务器 | 配置用于时间同步的自定义 NTP 服务器地址 | string | 字符串（NTP 服务器地址） | readwrite | |

## 读写示例

```bash
# 查询自定义 NTP 服务器
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center.datetime -k customNtpServer
# 设置自定义 NTP 服务器
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center.datetime -k customNtpServer -v "<value>"
```
