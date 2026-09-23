---
name: dde-session
description: 提供会话管理、窗口管理器切换和会话状态监听的 D-Bus 接口
Categories:
  - Application
---

# dde-session

dde-session 是 DDE 会话管理组件，通过 Session 总线提供会话登录注销、电源操作、会话状态监听和窗口管理器切换能力。

## D-Bus 接口

### 会话管理

提供会话登录、注销、锁屏和电源操作能力。

详见 [org.deepin.dde.Session1.md](references/dbus/org.deepin.dde.Session1.md)

### 会话管理器

提供会话电源操作、抑制管理和状态查询能力。

详见 [org.deepin.dde.SessionManager1.md](references/dbus/org.deepin.dde.SessionManager1.md)

### 窗口管理器切换

提供窗口管理器查询和切换能力。

详见 [org.deepin.dde.WMSwitcher1.md](references/dbus/org.deepin.dde.WMSwitcher1.md)

## CLI 命令

### dde-session

DDE 会话管理程序，负责 DDE 桌面会话的启动和初始化。

详见 [dde-session.md](references/cli/dde-session.md)

### dde-session-ctl

DDE 会话控制工具，用于执行关机、退出会话、注销这三项会话级操作。

详见 [dde-session-ctl.md](references/cli/dde-session-ctl.md)

### dde-quick-login

DDE 锁屏快速登录工具，用于在锁屏状态下快速重新登录。

详见 [dde-quick-login.md](references/cli/dde-quick-login.md)

