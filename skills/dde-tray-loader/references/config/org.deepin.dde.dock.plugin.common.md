# org.deepin.dde.dock.plugin.common

任务栏插件公共配置资源，管理默认驻留在任务栏上的插件列表。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `defaultDockedPlugins` | 默认驻留任务栏插件 | 配置默认驻留在任务栏上的插件列表，仅控制初始默认状态，重启后生效 | array | readonly |

## 读写示例

```bash
# 查询默认驻留插件列表
dde-dconfig get -a org.deepin.dde.tray-loader -r org.deepin.dde.dock.plugin.common -k defaultDockedPlugins
```
