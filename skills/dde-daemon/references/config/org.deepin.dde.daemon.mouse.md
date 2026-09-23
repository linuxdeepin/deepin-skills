# org.deepin.dde.daemon.mouse

鼠标配置资源，管理自适应加速配置、接入鼠标时禁用触控板、双击时间间隔、拖拽阈值、左手鼠标模式、定位指针、中键模拟、鼠标加速倍数、鼠标速度缩放、鼠标加速阈值、自然滚动鼠标行为设置。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `adaptiveAccelProfile` | 自适应加速配置 | 控制是否使用自适应鼠标加速配置文件 | bool | readwrite |
| `disableTouchpad` | 接入鼠标时禁用触控板 | 控制当检测到外接鼠标时是否自动禁用触控板 | bool | readwrite |
| `doubleClick` | 双击时间间隔 | 配置鼠标双击的有效时间间隔（毫秒），在此时间内的两次单击被视为双击 | number | readwrite |
| `dragThreshold` | 拖拽阈值 | 配置启动拖拽操作前鼠标需要移动的距离（像素） | number | readwrite |
| `leftHanded` | 左手鼠标模式 | 控制是否为左手用户交换鼠标左右键功能 | bool | readwrite |
| `locatePointer` | 定位指针 | 控制按下并释放 Ctrl 键时是否高亮显示鼠标指针当前位置 | bool | readwrite |
| `middleButtonEnabled` | 中键模拟 | 控制是否启用通过同时点击鼠标左右键来模拟中键的功能 | bool | readwrite |
| `motionAcceleration` | 鼠标加速倍数 | 配置鼠标移动的加速倍数，-1 为系统默认值 | number | readwrite |
| `motionScaling` | 鼠标速度缩放 | 配置鼠标移动的速度缩放倍数，-1 为系统默认值 | number | readwrite |
| `motionThreshold` | 鼠标加速阈值 | 配置激活鼠标加速前指针需要移动的距离（像素），-1 为系统默认值 | number | readwrite |
| `naturalScroll` | 自然滚动 | 控制是否启用鼠标自然（反向）滚动，启用后滚动方向与页面移动方向一致 | bool | readwrite |

## 读写示例

```bash
# 查询自适应加速配置
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.mouse -k adaptiveAccelProfile
# 设置自适应加速配置
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.mouse -k adaptiveAccelProfile -v "<value>"
```
