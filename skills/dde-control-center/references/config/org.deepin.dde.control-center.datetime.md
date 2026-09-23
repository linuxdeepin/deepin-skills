# org.deepin.dde.control-center.datetime

日期时间配置资源，管理用于时间同步的自定义 NTP 服务器地址。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `customNtpServer` | 自定义 NTP 服务器 | 配置用于时间同步的自定义 NTP 服务器地址 | string | readwrite |

## 读写示例

```bash
# 查询自定义 NTP 服务器
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.datetime -k customNtpServer --get
# 设置自定义 NTP 服务器
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.datetime -k customNtpServer -s "<value>"
```
