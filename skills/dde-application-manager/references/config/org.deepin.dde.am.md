# org.deepin.dde.am

应用启动次数记录资源，记录所有应用的累计启动次数，用于应用使用频率统计。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `appsLaunchedTimes` | 应用启动次数 | 记录所有应用的累计启动次数，用于应用使用频率统计 | object | readwrite |

## 读写示例

```bash
# 查询应用启动次数
dde-dconfig get -a org.deepin.dde.application-manager -r org.deepin.dde.am -k appsLaunchedTimes
# 设置应用启动次数（object 类型，使用 JSON 对象格式）
dde-dconfig set -a org.deepin.dde.application-manager -r org.deepin.dde.am -k appsLaunchedTimes -v '{"org.deepin.editor": 5}'
```
