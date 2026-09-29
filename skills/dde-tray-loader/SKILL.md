---
name: dde-tray-loader
description: dde-tray-loader 是 DDE 桌面环境的托盘插件加载器组件，负责加载和管理系统托盘区域的插件。提供全局键盘布局切换与托盘图标管理的 Session D-Bus 接口，以及 dde-tray-loader 自身的托盘插件加载命令行工具（支持按插件路径或分组加载）和任务栏插件 DConfig 配置项（包含默认驻留插件列表、电源插件充电保护全局阈值与电池时间显示）
Categories:
  - Application
---

# dde-tray-loader

dde-tray-loader 是 DDE 桌面环境的托盘插件加载器组件，负责加载和管理系统托盘区域的插件。该 skill 提供以下能力：

- **全局 Session D-Bus 接口**：键盘布局切换和状态查询（Keyboard1）、托盘图标管理和通知控制（TrayManager1），对整个桌面会话生效
- **自身 CLI 工具**：`trayplugin-loader`，仅作用于 dde-tray-loader 自身的插件加载，支持通过 `-p` 指定插件路径或 `--group` 指定分组加载，由 dde-shell 在会话启动时自动拉起
- **自身 DConfig 配置项**：任务栏插件的默认驻留插件列表、电源插件充电保护全局阈值与电池时间显示，仅作用于 dde-tray-loader 自身

## CLI 命令

### trayplugin-loader

dde-tray-loader 自身的托盘插件加载器，负责加载和管理系统托盘区域的插件。支持通过 `-p` 指定插件路径或 `--group` 指定分组加载。

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
