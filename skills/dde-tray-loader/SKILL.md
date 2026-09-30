---
name: dde-tray-loader
description: dde-tray-loader 是 DDE 桌面环境的托盘插件加载器组件，负责加载和管理系统托盘区域的插件。提供键盘布局切换、托盘图标管理、插件加载、电源管理配置（充电保护阈值与电池时间显示）、默认驻留插件列表管理功能
Categories:
  - Settings
---

# dde-tray-loader

dde-tray-loader 是 DDE 桌面环境的托盘插件加载器组件，负责加载和管理系统托盘区域的插件。该 skill 提供以下能力：

- **键盘布局切换**：通过 Session D-Bus 接口查询和切换当前键盘布局，监听布局变化与 fcitx 输入法运行状态
- **托盘图标管理**：通过 Session D-Bus 接口管理 X11 系统托盘选择权、查询托盘图标列表、监听图标增删与变化
- **插件加载**：通过 `trayplugin-loader` 命令行工具按插件路径加载托盘插件，由 dde-shell 在会话启动时自动拉起
- **电源管理配置**：通过 DConfig 配置充电保护电量阈值和电池时间信息显示
- **默认驻留插件管理**：通过 DConfig 配置默认驻留在任务栏上的插件列表

## CLI 命令

### trayplugin-loader

dde-tray-loader 的托盘插件加载器，通过 `-p` 指定插件路径加载托盘插件。

详见 [trayplugin-loader.md](references/cli/trayplugin-loader.md)

## D-Bus 接口

### 键盘布局

提供全局的键盘布局切换和状态查询 Session D-Bus 接口。

详见 [org.deepin.dde.Keyboard1.md](references/dbus/org.deepin.dde.Keyboard1.md)

### 托盘管理

提供全局的托盘图标管理和通知控制 Session D-Bus 接口。

详见 [org.deepin.dde.TrayManager1.md](references/dbus/org.deepin.dde.TrayManager1.md)

## DConfig 配置项

dde-tray-loader 自身插件的 DConfig 配置资源，仅作用于 dde-tray-loader 自身。

### 任务栏插件通用配置

默认驻留任务栏插件列表配置。

详见 [org.deepin.dde.dock.plugin.common](references/config/org.deepin.dde.dock.plugin.common.md)

### 电源插件配置

充电保护电量阈值和电池时间信息显示配置。

详见 [org.deepin.dde.dock.plugin.power](references/config/org.deepin.dde.dock.plugin.power.md)
