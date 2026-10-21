---
name: dde-session-shell
description: dde-session-shell 是 DDE 桌面环境的登录锁屏组件，负责系统锁屏、用户登录认证、关机重启界面显示。该 skill 提供锁屏程序启动、登录界面显示设置、登录欢迎界面运行、手势密码重置的 CLI 命令，锁屏界面显示控制、关机界面显示控制、电源操作的 D-Bus 接口，以及快速登录开关的 DConfig 配置项，提供登录插件接口、托盘插件接口和辅助登录 C 接口开发接口
Categories:
  - Application
  - Develop
---

# dde-session-shell

dde-session-shell 是 DDE 登录锁屏组件，提供锁屏程序、登录界面、关机界面的 CLI 命令工具，通过 Session 总线提供锁屏界面显示控制、关机界面显示控制和电源操作能力，并通过 DConfig 暴露快速登录开关配置。

`ShutdownFront1.Show` 只显示电源选项界面；`Shutdown`、`Restart`、`Suspend`、`Hibernate` 可发起实际动作，不能保证每次显示确认界面。锁屏前端控制认证界面，会话管理器负责会话请求；登录阶段显示工具与当前用户桌面显示配置分开。

## CLI 命令

### dde-lock

DDE 锁屏程序，是 DDE 桌面环境中负责屏幕锁定和用户切换的核心组件。

详见 [dde-lock.md](references/cli/dde-lock.md)

### reset-pattern-dialog

重置登录手势密码对话框，用于在 DDE 手势密码登录功能中重置用户的手势密码。

详见 [reset-pattern-dialog.md](references/cli/reset-pattern-dialog.md)

### lightdm-deepin-greeter

DDE 登录界面（LightDM Greeter），是 deepin 定制的 LightDM 欢迎程序。

详见 [lightdm-deepin-greeter.md](references/cli/lightdm-deepin-greeter.md)

### greeter-display-setting

登录界面显示设置工具，用于在 LightDM 登录阶段配置显示相关参数（如分辨率、缩放）。

详见 [greeter-display-setting.md](references/cli/greeter-display-setting.md)

## D-Bus 接口

### 锁屏界面控制

提供锁屏界面显示、用户列表显示、认证状态控制和电源操作能力。

详见 [org.deepin.dde.LockFront1.md](references/dbus/org.deepin.dde.LockFront1.md)

### 关机界面控制

提供关机界面显示和电源操作能力。

详见 [org.deepin.dde.ShutdownFront1.md](references/dbus/org.deepin.dde.ShutdownFront1.md)

## DConfig 配置项

dde-session-shell 相关的 DConfig 配置项为快速登录开关。该配置来自 dde-daemon 仓库，注册在 appId `org.deepin.dde.lightdm-deepin-greeter` 下，由 lightdm-deepin-greeter 读取应用。

### 快速登录开关

控制是否启用快速登录功能，开启时开机后自动登录并进入锁屏状态。该配置属于 dde-daemon 发布的全局账户配置资源，非 dde-session-shell 自身发布的 schema。

详见 [org.deepin.dde.daemon.accounts](references/config/org.deepin.dde.daemon.accounts.md)

## 开发接口

dde-session-shell 是 DDE 登录锁屏壳，提供登录界面（lightdm-deepin-greeter）和锁屏界面（dde-lock）。支持登录插件、托盘插件和辅助登录插件扩展，允许第三方通过继承接口实现自定义登录认证界面和托盘功能。

### 插件接口（C++）

C++ 插件接口参考文档，包括模块基础接口、V2 登录模块接口、认证回调数据结构和托盘模块接口，用于开发登录认证插件和托盘插件。

详见 [plugin-interface.md](references/interface/plugin-interface.md)

### 辅助登录接口（C）

C 语言辅助认证接口参考文档，用于通过 C 函数与认证服务交互，发送账号密码进行认证。

详见 [assist-login-interface.md](references/interface/assist-login-interface.md)
