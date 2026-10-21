# org.deepin.dde.control-center.datetime

记录控制中心中的自定义 NTP 服务器地址，默认值为空字符串。控制中心通过时间后端成功修改 NTP 服务器后保存该地址；单独写入此记录不修改系统 NTP 服务。

## 配置项

| Key | Name | Description | 类型 | 取值范围 | Permissions | Flags |
|---|---|---|---|---|---|---|
| `customNtpServer` | 自定义 NTP 服务器 | 保存控制中心使用的自定义 NTP 地址 | string | 字符串（NTP 服务器地址） | readwrite | |

## 读写示例

```bash
# 查询自定义 NTP 服务器
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center.datetime -k customNtpServer
# 更新控制中心中的自定义地址记录
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center.datetime -k customNtpServer -v "time.deepin.org"
```
