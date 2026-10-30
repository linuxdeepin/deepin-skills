# org.deepin.dde.control-center

控制中心窗口尺寸配置资源，管理控制中心窗口尺寸与模块显隐配置。

## 配置项

| Key | Name | Description | 类型 | 取值范围 | Permissions | Flags |
|---|---|---|---|---|---|---|
| `width` | 控制中心宽度 | 配置控制中心窗口的宽度（像素） | int | 正整数（像素） | readwrite | |
| `height` | 控制中心高度 | 配置控制中心窗口的高度（像素） | int | 正整数（像素） | readwrite | |
| `sidebarWidth` | 侧边栏宽度 | 配置控制中心窗口的侧边栏宽度（像素） | int | 整数（像素），-1 表示使用默认值 | readwrite | true |
| `hideModule` | 隐藏模块列表 | 配置控制中心中需要隐藏的模块列表 | array | 字符串数组（模块 ID 列表） | readwrite | |
| `disableModule` | 禁用模块列表 | 配置控制中心中需要禁用的模块列表 | array | 字符串数组（模块 ID 列表） | readwrite | |

## 读写示例

```bash
# 查询窗口宽度
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k width
# 设置窗口宽度
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k width -v "<value>"

# 查询窗口高度
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k height
# 设置窗口高度
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k height -v "<value>"

# 查询侧边栏宽度
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k sidebarWidth
# 设置侧边栏宽度
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k sidebarWidth -v "<value>"

# 查询隐藏模块列表
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k hideModule
# 设置隐藏模块列表
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k hideModule -v "<value>"

# 查询禁用模块列表
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k disableModule
# 设置禁用模块列表
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k disableModule -v "<value>"
```
