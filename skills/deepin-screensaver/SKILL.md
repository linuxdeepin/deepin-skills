---
name: deepin-screensaver
description: 提供屏保启动停止、预览、配置管理和屏保列表查询接口
Categories:
  - Settings
---

# deepin-screensaver

deepin-screensaver 是 DDE 的屏幕保护程序组件，通过 Session 总线提供屏保的启动、停止、预览、配置管理和屏保列表查询能力。

## D-Bus 接口

### 屏保控制

提供屏保的启动、停止、预览、配置管理和屏保列表查询能力。

详见 [com.deepin.ScreenSaver.md](references/dbus/com.deepin.ScreenSaver.md)

## DConfig 配置项

### 资源: `org.deepin.customscreensaver`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `intervalTime` | 屏保轮播间隔 | number | readwrite |
| `playMode` | 屏保播放模式 | number | readwrite |
| `slideshowPath` | 屏保图片路径 | string | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.screensaver -r org.deepin.customscreensaver -k intervalTime --get
# 设置
dde-dconfig -a org.deepin.screensaver -r org.deepin.customscreensaver -k intervalTime -s "<value>"
```

### 资源: `org.deepin.screensaver`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `currentScreenSaver` | 当前屏保 | string | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.screensaver -r org.deepin.screensaver -k currentScreenSaver --get
# 设置
dde-dconfig -a org.deepin.screensaver -r org.deepin.screensaver -k currentScreenSaver -s "<value>"
```

