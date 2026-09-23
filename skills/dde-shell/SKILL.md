---
name: dde-shell
description: 提供任务栏控制、桌面通知发送与关闭、通知能力查询、应用与系统通知配置、通知记录状态、OSD 显示和任务管理接口
Categories:
  - Application
---

# dde-shell

dde-shell 是 DDE 桌面的 Shell 组件，通过 Session 总线上的多个 D-Bus 服务提供任务栏（Dock）、通知、OSD 和任务管理能力。

## D-Bus 接口

### 任务栏控制

提供给外部控制 Dock 的服务接口，允许外部程序控制 Dock 的显示、插件重载、位置、几何区域和主屏显示属性。

详见 [org.deepin.ds.Dock](references/dbus/org.deepin.ds.Dock.md)

### 桌面通知与通知配置

提供桌面通知的发送、更新和关闭能力，可查询通知服务支持的能力与服务器信息；支持按应用读取和修改通知开关及展示配置，读取和修改系统级通知配置，查询通知记录数量，并监听通知处理状态、应用配置和系统配置的变化。

详见 [org.deepin.dde.Notification1](references/dbus/org.deepin.dde.Notification1.md)

### 桌面通知（freedesktop 标准）

实现 freedesktop.org 桌面通知规范，提供桌面通知的发送、关闭和能力查询功能。

详见 [org.freedesktop.Notifications.md](references/dbus/org.freedesktop.Notifications.md)

### OSD 显示

控制屏幕显示（On-Screen Display）提示。

详见 [org.deepin.dde.Osd1](references/dbus/org.deepin.dde.Osd1.md)

### 任务管理

管理 Dock 任务栏中运行窗口的属性和操作。

详见 [org.deepin.ds.Dock.TaskManager](references/dbus/org.deepin.ds.Dock.TaskManager.md)

## DConfig 配置项

dde-shell 通过 DConfig 暴露通知和启动器相关的配置资源。

### 通知配置

应用通知设置、通知内容行数、最大通知气泡数量、勿扰模式、勿扰结束时间、锁屏开启勿扰、最大通知数量、通知清理天数、关闭所有通知、按时间间隔开启勿扰、勿扰开始时间配置。

详见 [org.deepin.dde.shell.notification](references/config/org.deepin.dde.shell.notification.md)

### 启动器配置

启动器搜索行为配置。

详见 [org.deepin.ds.launchpad](references/config/org.deepin.ds.launchpad.md)

## CLI 命令

### dde-shell

DDE Shell 框架主程序，是 DDE 桌面环境面板（panel）和小程序（applet）的核心管理框架。

详见 [dde-shell.md](references/cli/dde-shell.md)

