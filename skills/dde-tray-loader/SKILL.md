---
name: dde-tray-loader
description: 提供键盘布局切换、布局列表查询和托盘插件管理的 D-Bus 接口
Categories:
  - Application
---

# dde-tray-loader

dde-tray-loader 是 DDE 托盘加载器组件，通过 Session 总线提供键盘布局切换和托盘插件管理能力。

## D-Bus 接口

### 键盘布局

提供键盘布局切换和状态查询能力。

详见 [org.deepin.dde.Keyboard1.md](references/dbus/org.deepin.dde.Keyboard1.md)

### 托盘管理

提供托盘图标管理和通知控制能力。

详见 [org.deepin.dde.TrayManager1.md](references/dbus/org.deepin.dde.TrayManager1.md)

## DConfig 配置项

dde-tray-loader 通过 DConfig 暴露任务栏插件默认驻留和电源插件配置资源。

### 任务栏插件通用配置

默认驻留任务栏插件列表配置。

详见 [org.deepin.dde.dock.plugin.common](references/config/org.deepin.dde.dock.plugin.common.md)

### 电源插件配置

充电保护电量阈值、显示电池时间信息配置。

详见 [org.deepin.dde.dock.plugin.power](references/config/org.deepin.dde.dock.plugin.power.md)

## CLI 命令

### trayplugin-loader

DDE 托盘插件加载器，负责加载和管理系统托盘区域的插件。

详见 [trayplugin-loader.md](references/cli/trayplugin-loader.md)

