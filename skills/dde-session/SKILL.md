---
name: dde-session
description: dde-session 是 DDE 桌面环境会话管理组件，负责桌面会话的启动、初始化和生命周期管理。本 skill 提供 dde-session 的 CLI 命令和 D-Bus 接口文档：CLI 覆盖会话启动（dde-session）、会话控制——关机/退出/注销（dde-session-ctl）、锁屏快速登录（dde-quick-login）；D-Bus 接口覆盖会话注销与会话 PID/路径查询（Session1，仅作用于 dde-session 自身）、全局电源操作与锁屏与抑制管理与抑制器详情查询与能力查询与会话注册与调试模式（SessionManager1、Inhibitor1）、窗口管理器查询与切换（WMSwitcher1）
Categories:
  - Settings
---

# dde-session

dde-session 是 DDE 桌面会话管理组件，负责桌面会话的启动、初始化和生命周期管理。它提供会话启动、会话控制、锁屏快速登录的 CLI 命令，并通过 Session 总线提供会话注销、电源操作、抑制管理、状态查询和窗口管理器切换能力。上述功能均为系统级会话管理能力，对整个桌面会话生效。

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

## D-Bus 接口

### 会话管理

提供会话注销、会话进程 PID 查询和会话路径查询能力。

详见 [org.deepin.dde.Session1.md](references/dbus/org.deepin.dde.Session1.md)

### 会话管理器

提供全局电源操作（重启/关机/挂起/休眠）、锁屏、抑制管理、能力查询、会话注册、会话守护进程管理和调试模式能力。

详见 [org.deepin.dde.SessionManager1.md](references/dbus/org.deepin.dde.SessionManager1.md)

### 会话抑制器

提供抑制器详情查询能力，包括应用 ID、客户端路径、抑制 flags、抑制原因和顶层窗口 XID 查询。

详见 [org.deepin.dde.Inhibitor1.md](references/dbus/org.deepin.dde.Inhibitor1.md)

### 窗口管理器切换

提供窗口管理器查询和切换能力。

详见 [org.deepin.dde.WMSwitcher1.md](references/dbus/org.deepin.dde.WMSwitcher1.md)
