---
name: deepin-screensaver
description: deepin-screensaver 是 DDE 的屏幕保护程序组件，提供屏保启动停止、预览、配置管理和屏保列表查询的 D-Bus 接口，屏保启动与配置对话框的 CLI 命令，以及 deepin-screensaver 自身的屏保轮播和屏保选择的 DConfig 配置
Categories:
  - Application
---

# deepin-screensaver

deepin-screensaver 是 DDE 的屏幕保护程序组件，负责在用户空闲一段时间后启动屏幕保护动画。该 skill 提供全局的屏保控制 D-Bus 接口与 CLI 命令，以及仅作用于 deepin-screensaver 自身的 DConfig 配置。

## CLI 命令

### deepin-screensaver

DDE 屏幕保护程序，负责在用户空闲一段时间后启动屏幕保护动画。支持通过 D-Bus 注册服务供系统调用、直接启动屏保、以及打开特定屏保应用的配置对话框。

详见 [deepin-screensaver.md](references/cli/deepin-screensaver.md)

## D-Bus 接口

### 屏保控制

提供全局的屏保启动、停止、预览、配置管理和屏保列表查询能力。

详见 [com.deepin.ScreenSaver.md](references/dbus/com.deepin.ScreenSaver.md)

## DConfig 配置项

以下 DConfig 配置仅作用于 deepin-screensaver 自身应用（App ID: `org.deepin.screensaver`）。

### 自定义屏保配置

屏保轮播间隔、屏保播放模式、屏保图片路径配置。

详见 [org.deepin.customscreensaver](references/config/org.deepin.customscreensaver.md)

### 屏保选择配置

当前使用的屏保选择配置。

详见 [org.deepin.screensaver](references/config/org.deepin.screensaver.md)
