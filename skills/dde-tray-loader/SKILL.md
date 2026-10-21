---
name: dde-tray-loader
description: dde-tray-loader 是 DDE 桌面环境的托盘插件加载器组件，负责加载和管理系统托盘区域的插件。提供键盘布局指示与菜单、托盘图标管理、插件加载、电源管理配置（充电保护阈值与电池时间显示）、默认驻留插件列表管理功能，提供 Dock 插件项 C++ 接口供第三方开发托盘插件
Categories:
  - Settings
  - Develop
---

# dde-tray-loader

dde-tray-loader 是 DDE 桌面环境的托盘插件加载器组件，负责加载和管理系统托盘区域的插件。该 skill 提供以下能力：

- **键盘布局指示与菜单**：通过 Session D-Bus 接口查询布局指示器状态、弹出布局选择菜单，监听布局变化与 fcitx 输入法运行状态
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

提供当前会话的键盘布局指示器状态查询与菜单显示接口。`layout` 写入只更新指示器文字；程序化修改实际键盘布局应使用键盘后端的布局设置接口。

详见 [org.deepin.dde.Keyboard1.md](references/dbus/org.deepin.dde.Keyboard1.md)

### 托盘管理

提供全局的托盘图标管理和通知控制 Session D-Bus 接口。

详见 [org.deepin.dde.TrayManager1.md](references/dbus/org.deepin.dde.TrayManager1.md)

## DConfig 配置项

DConfig 配置由对应托盘插件消费。界面显示和默认驻留列表作用于托盘自身；充电保护阈值作用于电源插件管理的电池充电行为。

### 任务栏插件通用配置

默认驻留任务栏插件列表配置。

详见 [org.deepin.dde.dock.plugin.common](references/config/org.deepin.dde.dock.plugin.common.md)

### 电源插件配置

充电保护电量阈值和电池时间信息显示配置。

详见 [org.deepin.dde.dock.plugin.power](references/config/org.deepin.dde.dock.plugin.power.md)

## 开发接口

dde-tray-loader 是 DDE Dock（任务栏）的插件加载器，以 header-only 形式提供插件接口头文件。第三方开发者通过继承接口类实现自定义 Dock 插件，编译为共享库后安装到 Dock 插件目录，由 Dock 框架在运行时通过 Qt Plugin 机制加载。

### 插件项接口

C++ 接口参考文档，涵盖 Dock 插件基础接口（V1）、V2 扩展接口和 V3 卡片 surface 扩展接口，是插件开发者需要实现的核心接口集合。

详见 [plugin-interface.md](references/interface/plugin-interface.md)
