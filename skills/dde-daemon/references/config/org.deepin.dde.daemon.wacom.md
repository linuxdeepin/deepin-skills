# org.deepin.dde.daemon.wacom

Wacom 数位板配置资源，管理Wacom 光标模式、橡皮擦压感级别、橡皮擦采样窗口大小、橡皮擦压力阈值、强制比例匹配、下键操作映射、上键操作映射、Wacom 旋转设置、映射输出设备、跨屏重新映射、触控笔压感级别、触控笔采样窗口大小、触控笔压力阈值、坐标变化抑制阈值配置。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `cursorMode` | Wacom 光标模式 | 控制 Wacom 数位板光标模式，true 为相对模式、false 为绝对模式 | bool | readwrite |
| `eraserPressureSensitive` | 橡皮擦压感级别 | 配置 Wacom 橡皮擦的压力曲线级别（范围 1-7） | number | readwrite |
| `eraserRawSample` | 橡皮擦采样窗口大小 | 配置 Wacom 橡皮擦原始数据点的采样窗口大小（范围 1-20） | number | readwrite |
| `eraserThreshold` | 橡皮擦压力阈值 | 配置 Wacom 橡皮擦生成按键事件所需的最小压力（范围 1-2047） | number | readwrite |
| `forceProportions` | 强制比例匹配 | 控制是否强制 Wacom 绘图表面的比例与屏幕纵横比匹配 | bool | readwrite |
| `keyDownAction` | 下键操作映射 | 配置 Wacom 下键的操作映射，0 为左键点击、1 为中键点击、2 为右键点击、3 为向上翻页、4 为向下翻页 | number | readwrite |
| `keyUpAction` | 上键操作映射 | 配置 Wacom 上键的操作映射，0 为左键点击、1 为中键点击、2 为右键点击、3 为向上翻页、4 为向下翻页 | number | readwrite |
| `leftHanded` | Wacom 旋转设置 | 配置 Wacom 设备的旋转方向，用于适应左手用户或不同摆放方向 | bool | readwrite |
| `mapOutput` | 映射输出设备 | 配置 Wacom 数位板输入区域映射到的显示输出设备 | string | readwrite |
| `mouseEnterRemap` | 跨屏重新映射 | 控制当鼠标进入新屏幕时是否自动重新映射 Wacom 输入区域 | bool | readwrite |
| `stylusPressureSensitive` | 触控笔压感级别 | 配置 Wacom 触控笔的压力曲线级别（范围 1-7） | number | readwrite |
| `stylusRawSample` | 触控笔采样窗口大小 | 配置 Wacom 触控笔原始数据点的采样窗口大小（范围 1-20） | number | readwrite |
| `stylusThreshold` | 触控笔压力阈值 | 配置 Wacom 触控笔生成按键事件所需的最小压力（范围 1-2047） | number | readwrite |
| `suppress` | 坐标变化抑制阈值 | 配置 Wacom 输入坐标变化的抑制阈值（范围 0-100），低于此阈值的微小移动将被忽略以减少噪声 | number | readwrite |

## 读写示例

```bash
# 查询 Wacom 光标模式
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.wacom -k cursorMode
# 设置 Wacom 光标模式
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.wacom -k cursorMode -v "<value>"
```
