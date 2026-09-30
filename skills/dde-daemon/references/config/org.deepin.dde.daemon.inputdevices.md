# org.deepin.dde.daemon.inputdevices

输入设备配置资源，管理键盘启用状态和鼠标滚轮速度。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `keyboardEnabled` | 键盘启用状态 | 配置用户级别的键盘开关，控制键盘是否启用 | bool | readwrite |
| `wheelSpeed` | 鼠标滚轮速度 | 配置鼠标滚轮的滚动速度，范围 1-100 | number | readwrite |

## 读写示例

```bash
# 查询键盘启用状态
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.inputdevices -k keyboardEnabled
# 设置键盘启用状态
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.inputdevices -k keyboardEnabled -v "<value>"
```
