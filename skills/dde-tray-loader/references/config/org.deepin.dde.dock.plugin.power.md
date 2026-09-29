# org.deepin.dde.dock.plugin.power

任务栏电源插件配置资源，管理充电保护电量阈值和电池时间信息显示。

## 配置项

| Key | Name | Description | 类型 | Permissions | Visibility |
|---|---|---|---|---|---|
| `chargingProtectThreshold` | 充电保护电量阈值 | 全局配置，配置充电保护功能触发的电量阈值（范围 80-99），超过此值将限制充电以保护电池 | number | readwrite | public |
| `showTimeToFull` | 显示电池时间信息 | 控制是否在任务栏电源插件中显示电池使用时间/剩余充电时间 | bool | readwrite | public |

## 读写示例

```bash
# 查询充电保护阈值
dde-dconfig get -a org.deepin.dde.tray-loader -r org.deepin.dde.dock.plugin.power -k chargingProtectThreshold
```

输出示例：

```
80
```

```bash
# 设置充电保护阈值
dde-dconfig set -a org.deepin.dde.tray-loader -r org.deepin.dde.dock.plugin.power -k chargingProtectThreshold -v 85
```
