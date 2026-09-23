# org.deepin.dde.control-center

控制中心窗口尺寸配置资源，管理控制中心窗口的高度和宽度。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `height` | 控制中心高度 | 配置控制中心窗口的高度（像素） | number | readwrite |
| `width` | 控制中心宽度 | 配置控制中心窗口的宽度（像素） | number | readwrite |

## 读写示例

```bash
# 查询窗口高度
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k height
# 设置窗口高度
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k height -v "<value>"
```
