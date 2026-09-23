# org.deepin.dde.shell.notification

通知配置资源，管理应用通知设置、通知内容行数、最大通知气泡数量、勿扰模式、勿扰结束时间、锁屏开启勿扰、最大通知数量、通知清理天数、关闭所有通知、按时间间隔开启勿扰、勿扰开始时间通知相关配置。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `appsInfo` | 应用通知设置 | 配置各应用的通知相关设置信息 | object | readwrite |
| `bubbleContentRowCount` | 通知内容行数 | 配置通知气泡中显示的内容行数，值应大于 0 | number | readwrite |
| `bubbleCount` | 最大通知气泡数量 | 配置同时显示的最大通知气泡数量，值应大于 0 | number | readwrite |
| `dndMode` | 勿扰模式 | 控制系统通知的勿扰模式开关 | bool | readwrite |
| `endTime` | 勿扰结束时间 | 配置勿扰模式的结束时间 | string | readwrite |
| `lockScreenOpenDndMode` | 锁屏开启勿扰 | 控制锁屏时是否自动开启勿扰模式 | bool | readwrite |
| `maxCount` | 最大通知数量 | 配置通知中心保存的最大通知数量 | number | readwrite |
| `notificationCleanupDays` | 通知清理天数 | 配置通知自动清理的天数，超过此天数的通知将被自动删除 | number | readwrite |
| `notificationClosed` | 关闭所有通知 | 控制是否关闭所有通知 | bool | readwrite |
| `openByTimeInterval` | 按时间间隔开启勿扰 | 控制是否按设定的时间间隔开启勿扰模式 | bool | readwrite |
| `startTime` | 勿扰开始时间 | 配置勿扰模式的开始时间 | string | readwrite |

## 读写示例

```bash
# 查询勿扰模式开关
dde-dconfig get -a org.deepin.dde.shell -r org.deepin.dde.shell.notification -k dndMode
# 设置勿扰模式开关
dde-dconfig set -a org.deepin.dde.shell -r org.deepin.dde.shell.notification -k dndMode -v "<value>"
```
