# dde-session-shell

dde-session-shell 是 DDE 登录锁屏组件，提供锁屏程序、登录界面、关机界面的 CLI 命令工具，通过 Session 总线提供锁屏界面显示控制、关机界面显示控制和电源操作能力，并通过 DConfig 暴露快速登录开关配置。

`ShutdownFront1.Show` 只显示电源选项界面；`Shutdown`、`Restart`、`Suspend`、`Hibernate` 可发起实际动作，不能保证每次显示确认界面。锁屏前端控制认证界面，会话管理器负责会话请求；登录阶段显示工具与当前用户桌面显示配置分开。

## CLI 命令

### dde-lock

DDE 锁屏程序，是 DDE 桌面环境中负责屏幕锁定和用户切换的核心组件。

详见 [dde-lock.md](cli/dde-lock.md)

### reset-pattern-dialog

重置登录手势密码对话框，用于在 DDE 手势密码登录功能中重置用户的手势密码。

详见 [reset-pattern-dialog.md](cli/reset-pattern-dialog.md)

### lightdm-deepin-greeter

DDE 登录界面（LightDM Greeter），是 deepin 定制的 LightDM 欢迎程序。

详见 [lightdm-deepin-greeter.md](cli/lightdm-deepin-greeter.md)

### greeter-display-setting

登录界面显示设置工具，用于在 LightDM 登录阶段配置显示相关参数（如分辨率、缩放）。

详见 [greeter-display-setting.md](cli/greeter-display-setting.md)

## D-Bus 接口

### 锁屏界面控制

提供锁屏界面显示、用户列表显示、认证状态控制和电源操作能力。

详见 [org.deepin.dde.LockFront1.md](dbus/org.deepin.dde.LockFront1.md)

### 关机界面控制

提供关机界面显示和电源操作能力。

详见 [org.deepin.dde.ShutdownFront1.md](dbus/org.deepin.dde.ShutdownFront1.md)

## DConfig 配置项

dde-session-shell 相关的 DConfig 配置项为快速登录开关。该配置来自 dde-daemon 仓库，注册在 appId `org.deepin.dde.lightdm-deepin-greeter` 下，由 lightdm-deepin-greeter 读取应用。

### 快速登录开关

控制是否启用快速登录功能，开启时开机后自动登录并进入锁屏状态。该配置属于 dde-daemon 发布的全局账户配置资源，非 dde-session-shell 自身发布的 schema。

详见 [org.deepin.dde.daemon.accounts](config/org.deepin.dde.daemon.accounts.md)
