# org.deepin.dde.daemon.touchpad

触摸板配置资源，管理自然滚动增量、打字时禁用触控板、触控板双击时间间隔、触控板拖拽阈值、边缘滚动、水平滚动、触控板按键方向、触控板加速倍数、触控板速度缩放、触控板加速阈值、自然滚动、手掌检测、手掌检测最小压力、手掌检测最小宽度、轻触点击、触控板开关、垂直滚动触摸板相关配置。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `deltaScroll` | 自然滚动增量 | 配置触控板自然滚动的增量值 | number | readwrite |
| `disableWhileTyping` | 打字时禁用触控板 | 控制打字时是否自动禁用触控板以防止误触 | bool | readwrite |
| `doubleClick` | 触控板双击时间间隔 | 配置触控板双击的有效时间间隔（毫秒） | number | readwrite |
| `dragThreshold` | 触控板拖拽阈值 | 配置触控板启动拖拽前需要移动的距离（像素） | number | readwrite |
| `edgeScrollEnabled` | 边缘滚动 | 控制是否启用触控板边缘滚动功能 | bool | readwrite |
| `horizScrollEnabled` | 水平滚动 | 控制是否启用触控板水平滚动功能 | bool | readwrite |
| `leftHanded` | 触控板按键方向 | 配置触控板左右键的交换设置，为左手用户提供便利 | bool | readwrite |
| `motionAcceleration` | 触控板加速倍数 | 配置触控板移动的加速倍数，-1 为系统默认值 | number | readwrite |
| `motionScaling` | 触控板速度缩放 | 配置触控板移动的速度缩放倍数，-1 为系统默认值 | number | readwrite |
| `motionThreshold` | 触控板加速阈值 | 配置激活触控板加速前指针需要移动的距离（像素），-1 为系统默认值 | number | readwrite |
| `naturalScroll` | 自然滚动 | 控制是否启用触控板自然（反向）滚动，启用后滚动方向与页面移动方向一致 | bool | readwrite |
| `palmDetect` | 手掌检测 | 控制是否启用触控板手掌检测功能，避免手掌误触 | bool | readwrite |
| `palmMinPressure` | 手掌检测最小压力 | 配置触控板手掌检测的最小压力阈值 | number | readwrite |
| `palmMinWidth` | 手掌检测最小宽度 | 配置触控板手掌检测的最小接触宽度阈值 | number | readwrite |
| `tapToClick` | 轻触点击 | 控制是否启用触控板轻触点击功能，启用后轻触触控板即可触发鼠标点击 | bool | readwrite |
| `touchpadEnabled` | 触控板开关 | 控制是否启用所有触控板设备 | bool | readwrite |
| `vertScrollEnabled` | 垂直滚动 | 控制是否启用触控板垂直滚动功能 | bool | readwrite |

## 读写示例

```bash
# 查询触控板开关
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.touchpad -k touchpadEnabled
# 设置触控板开关
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.touchpad -k touchpadEnabled -v "<value>"
```
