# org.deepin.dde.clipboard

剪贴板应用提示组件显示配置资源，控制 dde-clipboard 应用是否显示提示组件。

## 配置项

| Key | Name | Description | 类型 | 取值范围 | Permissions |
|---|---|---|---|---|---|
| `showTipsWidget` | 提示组件显示开关 | 控制 dde-clipboard 应用是否显示提示组件 | bool | `true` / `false` | readwrite |

## 读写示例

```bash
# 查询提示组件显示开关
dde-dconfig get -a org.deepin.dde.clipboard -r org.deepin.dde.clipboard -k showTipsWidget
# 设置提示组件显示开关
dde-dconfig set -a org.deepin.dde.clipboard -r org.deepin.dde.clipboard -k showTipsWidget -v "<value>"
```
