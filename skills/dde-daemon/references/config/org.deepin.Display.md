# org.deepin.Display

显示器配置资源，管理不支持的屏幕黑名单、屏幕亮度、亮度设置方式、色温调节模式、当前自定义模式 ID、自定义显示模式、多屏显示模式、显示器映射关系、主屏幕、输出设备优先级、刷新率过滤器、屏幕旋转延时显示相关配置。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `blacklist` | 不支持的屏幕黑名单 | 配置需要过滤的不支持或无效的显示输出设备列表 | array | readwrite |
| `brightness` | 屏幕亮度 | 配置显示器的亮度值 | string | readwrite |
| `brightnessSetter` | 亮度设置方式 | 配置设置屏幕亮度的方式，0 为自动、1 为 gamma 校正、2 为背光调节 | number | readwrite |
| `colorTemperatureMode` | 色温调节模式 | 配置色温调节方式，0 为正常（不调节）、1 为自动、2 为手动 | number | readwrite |
| `currentCustomMode` | 当前自定义模式 ID | 在自定义显示模式下当前使用的配置 ID | string | readwrite |
| `customDisplayMode` | 自定义显示模式 | 配置自定义显示模式的类型（范围 1-2） | number | readwrite |
| `displayMode` | 多屏显示模式 | 配置多显示器显示模式，0 为自定义、1 为镜像、2 为扩展、3 为仅一个屏幕、4 为仅另一个屏幕 | number | readwrite |
| `mapOutput` | 显示器映射关系 | 配置各显示输出设备的映射关系 | string | readwrite |
| `primary` | 主屏幕 | 配置主显示输出设备名称 | string | readwrite |
| `priority` | 输出设备优先级 | 配置显示输出设备的优先级顺序，排在第一位的将作为主输出 | array | readwrite |
| `rateFilter` | 刷新率过滤器 | 配置屏幕刷新率的过滤规则（JSON 格式），用于限定可选的刷新率范围 | string | readwrite |
| `rotateScreenTimeDelay` | 屏幕旋转延时 | 配置屏幕旋转时的延时时间（范围 0-10 秒） | number | readwrite |

## 读写示例

```bash
# 查询屏幕黑名单
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.Display -k blacklist
# 设置屏幕黑名单
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.Display -k blacklist -v "<value>"
```
