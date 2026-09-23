---
name: dde-session-shell
description: 提供锁屏界面显示控制、关机界面显示控制和电源操作接口
Categories:
  - Application
---

# dde-session-shell

dde-session-shell 是 DDE 登录锁屏组件，通过 Session 总线提供锁屏界面显示控制、关机界面显示控制和电源操作能力。

## D-Bus 接口

### 锁屏界面控制

提供锁屏界面显示、用户列表显示、认证状态控制和电源操作能力。

详见 [org.deepin.dde.LockFront1.md](references/dbus/org.deepin.dde.LockFront1.md)

### 关机界面控制

提供关机界面显示和电源操作能力。

详见 [org.deepin.dde.ShutdownFront1.md](references/dbus/org.deepin.dde.ShutdownFront1.md)

## DConfig 配置项

dde-session-shell 通过 DConfig 暴露账户快速登录配置资源。

### 账户配置

快速登录启用开关等账户配置。

详见 [org.deepin.dde.daemon.accounts](references/config/org.deepin.dde.daemon.accounts.md)
