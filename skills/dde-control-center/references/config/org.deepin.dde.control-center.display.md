# org.deepin.dde.control-center.display

显示配置资源，管理控制中心显示设置中亮度调节的最小值。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `minBrightnessValue` | 亮度最小值 | 配置控制中心显示设置中亮度调节的最小值 | number | readwrite |

## 读写示例

```bash
# 查询亮度最小值
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center.display -k minBrightnessValue
# 设置亮度最小值
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center.display -k minBrightnessValue -v "<value>"
```
