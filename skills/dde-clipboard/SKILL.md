---
name: dde-clipboard
description: 提供剪贴板前端服务和剪贴板守护进程的 D-Bus 接口
Categories:
  - Application
---

# dde-clipboard

dde-clipboard 是 DDE 剪贴板组件，通过 Session 总线提供剪贴板前端服务和剪贴板守护进程的 D-Bus 接口。

## D-Bus 接口

### 剪贴板服务

管理 DDE 剪贴板历史服务，提供剪贴板历史记录管理能力，而非直接操作系统剪贴板。

详见 [org.deepin.dde.Clipboard1.md](references/dbus/org.deepin.dde.Clipboard1.md)

### 剪贴板加载器

提供剪贴板守护进程的加载能力。

详见 [org.deepin.dde.ClipboardLoader1.md](references/dbus/org.deepin.dde.ClipboardLoader1.md)

## CLI 命令

### dde-clipboard

DDE 剪贴板工具，提供图形化的剪贴板历史管理界面。

详见 [dde-clipboard.md](references/cli/dde-clipboard.md)

### dde-clipboard-daemon

DDE 剪贴板守护进程，负责管理剪贴板历史记录和剪贴板事件监听。

详见 [dde-clipboard-daemon.md](references/cli/dde-clipboard-daemon.md)

