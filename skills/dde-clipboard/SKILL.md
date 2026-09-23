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

