# org.deepin.dde.control-center.sound

声音配置资源，控制是否在声音设置中显示设备管理入口。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `showDeviceManager` | 设备管理显示开关 | 控制是否在声音设置中显示设备管理入口，主要用于开启端口自动切换功能 | bool | readwrite |

## 读写示例

```bash
# 查询设备管理显示开关
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center.sound -k showDeviceManager
# 设置设备管理显示开关
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center.sound -k showDeviceManager -v "<value>"
```
