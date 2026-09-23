# org.deepin.dde.daemon.touchscreen

触摸屏配置资源，管理边缘移动停止时间、长按黑名单、长按持续时间、短按持续时间触摸屏相关配置。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `edgemovestopDuration` | 边缘移动停止时间 | 配置触摸屏边缘移动停止的持续时间（毫秒） | number | readwrite |
| `longpressBlacklist` | 长按黑名单 | 配置禁用触摸屏长按功能的应用命令行列表 | array | readwrite |
| `longpressDuration` | 长按持续时间 | 配置触摸屏长按触发的持续时间（毫秒） | number | readwrite |
| `shortpressDuration` | 短按持续时间 | 配置触摸屏短按触发的持续时间（毫秒） | number | readwrite |

## 读写示例

```bash
# 查询长按持续时间
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.touchscreen -k longpressDuration
# 设置长按持续时间
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.touchscreen -k longpressDuration -v "<value>"
```
