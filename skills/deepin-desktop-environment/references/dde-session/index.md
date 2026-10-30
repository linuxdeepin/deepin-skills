# dde-session

dde-session 是 DDE 桌面会话管理组件，负责桌面会话的启动、初始化和生命周期管理。它提供会话启动、会话控制、锁屏快速登录的 CLI 命令，并通过 Session 总线提供会话管理进程退出、注销请求、电源操作、抑制管理、状态查询和 X11 窗口特效选择请求能力。进程退出、当前用户会话操作和整机电源操作的作用范围分别见各接口。

普通注销使用会话管理器的 `RequestLogout`，包含会话退出准备；`Session1.Logout` 只请求退出会话管理进程。显示关机选项使用关机界面的 `Show`；会话管理器的电源请求可进入实际动作。调用方需保存抑制器 cookie，并在操作结束后显式调用 `Uninhibit`；不要假设客户端断开会自动解除抑制。

## CLI 命令

### dde-session

DDE 会话管理程序，负责 DDE 桌面会话的启动和初始化。

详见 [dde-session.md](cli/dde-session.md)

### dde-session-ctl

DDE 会话控制工具，用于执行关机、退出会话、注销这三项会话级操作。

详见 [dde-session-ctl.md](cli/dde-session-ctl.md)

### dde-quick-login

DDE 锁屏快速登录工具，用于在锁屏状态下快速重新登录。

详见 [dde-quick-login.md](cli/dde-quick-login.md)

## D-Bus 接口

### 会话管理

提供会话管理进程退出、会话进程 PID 查询和会话路径查询能力；正常注销使用会话管理器的 `RequestLogout`。

详见 [org.deepin.dde.Session1.md](dbus/org.deepin.dde.Session1.md)

### 会话管理器

提供全局电源操作（重启/关机/挂起/休眠）、锁屏、抑制管理、能力查询、会话注册、会话守护进程管理和调试模式能力。

详见 [org.deepin.dde.SessionManager1.md](dbus/org.deepin.dde.SessionManager1.md)

### 会话抑制器

提供抑制器详情查询能力，包括应用 ID、客户端路径、抑制 flags、抑制原因和顶层窗口 XID 查询。

详见 [org.deepin.dde.Inhibitor1.md](dbus/org.deepin.dde.Inhibitor1.md)

### 窗口管理器切换

提供 X11 合成能力与状态标签查询，并请求显示窗口特效选择界面；Wayland 下不执行此请求。

详见 [org.deepin.dde.WMSwitcher1.md](dbus/org.deepin.dde.WMSwitcher1.md)
