# org.deepin.dde.daemon.trackpoint

小红点（Trackpoint）配置资源，管理左手模式、中键模拟、中键超时时间、小红点加速倍数、小红点速度缩放、小红点加速阈值、滚轮模拟、滚轮模拟按键、滚轮模拟超时、滚轮水平滚动配置。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `leftHanded` | 左手模式 | 控制是否为左手用户启用小红点左手模式 | bool | readwrite |
| `middleButtonEnabled` | 中键模拟 | 控制是否启用小红点中键模拟功能 | bool | readwrite |
| `middleButtonTimeout` | 中键超时时间 | 配置小红点中键模拟的超时时间（毫秒） | number | readwrite |
| `motionAcceleration` | 小红点加速倍数 | 配置小红点移动的加速倍数，-1 为系统默认值 | number | readwrite |
| `motionScaling` | 小红点速度缩放 | 配置小红点移动的速度缩放倍数，-1 为系统默认值 | number | readwrite |
| `motionThreshold` | 小红点加速阈值 | 配置激活小红点加速前指针需要移动的距离（像素），-1 为系统默认值 | number | readwrite |
| `wheelEmulation` | 滚轮模拟 | 控制是否启用小红点滚轮模拟功能，启用后按住中键移动小红点可模拟滚轮滚动 | bool | readwrite |
| `wheelEmulationButton` | 滚轮模拟按键 | 配置用于触发小红点滚轮模拟的按键 | number | readwrite |
| `wheelEmulationTimeout` | 滚轮模拟超时 | 配置小红点滚轮模拟的超时时间（毫秒） | number | readwrite |
| `wheelHorizScroll` | 滚轮水平滚动 | 控制是否启用小红点滚轮模拟的水平滚动功能 | bool | readwrite |

## 读写示例

```bash
# 查询滚轮模拟开关
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.trackpoint -k wheelEmulation
# 设置滚轮模拟开关
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.trackpoint -k wheelEmulation -v "<value>"
```
