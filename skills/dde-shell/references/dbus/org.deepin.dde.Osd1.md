# org.deepin.dde.Osd1 接口参考

该接口提供 OSD（On-Screen Display）提示的显示能力，支持通过 OSD 类型标识触发对应的屏幕提示显示。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Osd1` |
| Object path | `/` |
| Interface | `org.deepin.dde.Osd1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

## 方法、属性与信号

### OSD 显示

#### ShowOSD

显示 OSD 提示。

- **输入参数**:
  - `text`（string, 类型 `s`）：OSD 类型标识
- **返回值**: 无

**支持的选项**（来源于 dde-shell 源码 `panels/notification/osd/` 下各 applet 的 `match()` / `types` / `osdTypeModel`）:

音频：
- `AudioUp` — 音量增大
- `AudioDown` — 音量减小
- `AudioMute` — 静音
- `AudioUpAsh` — 音量增大（置灰）
- `AudioDownAsh` — 音量减小（置灰）
- `AudioMuteAsh` — 静音（置灰）

亮度：
- `BrightnessUp` — 亮度增大
- `BrightnessDown` — 亮度减小
- `BrightnessUpAsh` — 亮度增大（置灰）
- `BrightnessDownAsh` — 亮度减小（置灰）

开关与状态：
- `WLANOn` — WLAN 开启
- `WLANOff` — WLAN 关闭
- `CapsLockOn` — 大写锁定开启
- `CapsLockOff` — 大写锁定关闭
- `NumLockOn` — 数字键盘开启
- `NumLockOff` — 数字键盘关闭
- `TouchpadOn` — 触摸板开启
- `TouchpadOff` — 触摸板关闭
- `TouchpadToggle` — 触摸板切换
- `FnToggle` — Fn 键切换
- `AirplaneModeOn` — 飞行模式开启
- `AirplaneModeOff` — 飞行模式关闭
- `AudioMicMuteOn` — 麦克风静音
- `AudioMicMuteOff` — 麦克风取消静音
- `CameraOn` — 摄像头开启
- `CameraOff` — 摄像头关闭

电源模式：
- `balance` — 平衡模式
- `powersave` — 省电模式
- `performance` — 高性能模式

窗口特效：
- `SwitchWM3D` — 窗口特效已启用
- `SwitchWM2D` — 窗口特效已关闭
- `SwitchWMError` — 窗口特效启用失败
- `SwitchWM` — 切换窗口特效

显示与布局：
- `SwitchMonitors` — 切换显示器
- `DirectSwitchLayout` — 直接切换布局
- `SwitchLayout` — 切换键盘布局

```bash
gdbus call --session \
  --dest org.deepin.dde.Osd1 \
  --object-path / \
  --method org.deepin.dde.Osd1.ShowOSD "SwitchWM3D"
```

---
