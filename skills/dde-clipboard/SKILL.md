---
name: dde-clipboard
description: dde-clipboard 是 DDE 桌面环境的剪贴板管理组件，提供剪贴板管理工具的命令行使用、剪贴板前端服务与守护进程的 Session 总线 D-Bus 接口，以及 dde-clipboard 应用自身的提示组件显示配置
Categories:
  - Application
---

# dde-clipboard

dde-clipboard 是 DDE 桌面环境的剪贴板管理组件，提供剪贴板管理工具的命令行使用、剪贴板前端服务与守护进程的 Session 总线 D-Bus 接口，以及 dde-clipboard 应用自身的提示组件显示配置。

## CLI 命令

### dde-clipboard

DDE 剪贴板工具，提供图形化的剪贴板历史管理界面。

详见 [dde-clipboard.md](references/cli/dde-clipboard.md)

### dde-clipboard-daemon

DDE 剪贴板守护进程，负责管理剪贴板历史记录和剪贴板事件监听。

详见 [dde-clipboard-daemon.md](references/cli/dde-clipboard-daemon.md)

## D-Bus 接口

### 剪贴板服务

管理 DDE 剪贴板前端服务的显示控制，提供剪贴板窗口的切换、显示和隐藏能力。该接口在 Session 总线上注册，仅对当前用户会话生效。

详见 [org.deepin.dde.Clipboard1.md](references/dbus/org.deepin.dde.Clipboard1.md)

### 剪贴板加载器

提供剪贴板守护进程的剪贴板数据接收与恢复能力。该接口在 Session 总线上注册，仅对当前用户会话生效。

详见 [org.deepin.dde.ClipboardLoader1.md](references/dbus/org.deepin.dde.ClipboardLoader1.md)

## DConfig 配置项

以下 DConfig 配置项为 dde-clipboard 应用自身的配置，用于控制提示组件的显示行为，而非系统全局配置。

### 提示组件配置

控制 dde-clipboard 应用是否显示提示组件。

详见 [org.deepin.dde.clipboard](references/config/org.deepin.dde.clipboard.md)
