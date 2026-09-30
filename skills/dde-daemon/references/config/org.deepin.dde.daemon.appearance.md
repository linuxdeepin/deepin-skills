# org.deepin.dde.daemon.appearance

外观配置资源，控制是否在不包含 Plymouth 启动画面的情况下启用缩放。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `scaleWithoutPlymouthEnabled` | 缩放排除 Plymouth | 控制是否在不包含 Plymouth 启动画面的情况下启用缩放 | bool | readwrite |

## 读写示例

```bash
# 查询缩放排除 Plymouth 开关
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.appearance -k scaleWithoutPlymouthEnabled
# 设置缩放排除 Plymouth 开关
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.appearance -k scaleWithoutPlymouthEnabled -v "<value>"
```
