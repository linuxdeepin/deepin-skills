---
name: dde-shell
description: dde-shell 是 DDE 桌面环境的 Shell 组件，提供任务栏（Dock）、通知、OSD 和任务管理桌面面板能力。本 skill 提供 dde-shell 的 D-Bus 接口（任务栏控制、桌面通知与通知配置、通知中心显示控制、OSD 显示、任务管理）、面板框架启动调试的 CLI 命令、以及 DConfig 配置项（dde-shell 自身通知行为配置）的参考文档。其中通知行为配置仅作用于 dde-shell 自身，OSD 显示为全局系统级屏幕提示控制。
Categories:
  - Application
  - Settings
---

# dde-shell

dde-shell 是 DDE 桌面的 Shell 组件，通过 Session 总线上的多个 D-Bus 服务提供任务栏（Dock）、通知、OSD 和任务管理能力。

## CLI 命令

### dde-shell

DDE Shell 框架主程序，是 DDE 桌面环境面板（panel）和小程序（applet）的核心管理框架。

详见 [dde-shell.md](references/cli/dde-shell.md)

## D-Bus 接口

### 任务栏控制

提供给外部控制 Dock 的服务接口，允许外部程序控制 Dock 的显示、插件重载、位置、几何区域和主屏显示属性。

详见 [org.deepin.ds.Dock](references/dbus/org.deepin.ds.Dock.md)

### 桌面通知与通知配置

提供桌面通知的发送、更新和关闭能力，可查询通知服务支持的能力与服务器信息；支持按应用读取和修改通知开关及展示配置，读取和修改系统级通知配置，查询通知记录数量，并监听通知处理状态、应用配置和系统配置的变化。

详见 [org.deepin.dde.Notification1](references/dbus/org.deepin.dde.Notification1.md)

### 通知中心

提供通知中心面板的显示控制能力，支持切换、显示和隐藏通知中心。

详见 [org.deepin.dde.shell.notification.center](references/dbus/org.deepin.dde.shell.notification.center.md)

### OSD 显示

控制屏幕显示（On-Screen Display）提示。

详见 [org.deepin.dde.Osd1](references/dbus/org.deepin.dde.Osd1.md)

### 任务管理

管理 Dock 任务栏中运行窗口的属性和操作。

详见 [org.deepin.ds.Dock.TaskManager](references/dbus/org.deepin.ds.Dock.TaskManager.md)

## DConfig 配置项

dde-shell 通过 DConfig 暴露自身通知行为相关的配置资源。

### 通知配置

应用通知设置、通知内容行数、最大通知气泡数量、勿扰模式、勿扰结束时间、锁屏开启勿扰、最大通知数量、通知清理天数、关闭所有通知、按时间间隔开启勿扰、勿扰开始时间配置。

详见 [org.deepin.dde.shell.notification](references/config/org.deepin.dde.shell.notification.md)
