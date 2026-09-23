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

deepin-screensaver 通过 DConfig 暴露屏保轮播和当前屏保选择的配置资源。

### 自定义屏保配置

屏保轮播间隔、屏保播放模式、屏保图片路径配置。

详见 [org.deepin.customscreensaver](references/config/org.deepin.customscreensaver.md)

### 屏保选择配置

当前使用的屏保选择配置。

详见 [org.deepin.screensaver](references/config/org.deepin.screensaver.md)

## CLI 命令

### deepin-screensaver

DDE 屏幕保护程序，负责在用户空闲一段时间后启动屏幕保护动画。

详见 [deepin-screensaver.md](references/cli/deepin-screensaver.md)

