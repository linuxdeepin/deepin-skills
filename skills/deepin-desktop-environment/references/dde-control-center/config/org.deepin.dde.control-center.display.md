# org.deepin.dde.control-center.display

控制中心亮度调节范围的最小比例，默认值为 `0.1`（10%）。使用 `0.0`～`1.0` 的比例值；修改此配置不直接设置当前显示器亮度，控制中心初始化显示页面时读取该值。

## 配置项

| Key | Name | Description | 类型 | 取值范围 | Permissions | Flags |
|---|---|---|---|---|---|---|
| `minBrightnessValue` | 亮度最小值 | 配置控制中心显示设置中亮度调节的最小值 | float | 0.0 ~ 1.0（亮度比例） | readwrite | |

## 读写示例

```bash
# 查询亮度最小值
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center.display -k minBrightnessValue
# 设置亮度最小值
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center.display -k minBrightnessValue -v 0.1
```
