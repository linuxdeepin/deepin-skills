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

快速登录开关配置。

详见 [org.deepin.dde.daemon.accounts](references/config/org.deepin.dde.daemon.accounts.md)

## CLI 命令

### dde-lock

DDE 锁屏程序，是 DDE 桌面环境中负责屏幕锁定和用户切换的核心组件。

详见 [dde-lock.md](references/cli/dde-lock.md)

### reset-pattern-dialog

重置登录手势密码对话框，位于 `dde-session-shell/plugins/login-gesture/reset-pattern-dialog`。

详见 [reset-pattern-dialog.md](references/cli/reset-pattern-dialog.md)

### lightdm-deepin-greeter

DDE 登录界面（LightDM Greeter），是 deepin 定制的 LightDM 欢迎程序。

详见 [lightdm-deepin-greeter.md](references/cli/lightdm-deepin-greeter.md)

### greeter-display-setting

登录界面显示设置工具，用于在 LightDM 登录阶段配置显示相关参数（如分辨率、缩放）。

详见 [greeter-display-setting.md](references/cli/greeter-display-setting.md)

### lightdm-deepin-greeter-lighter

LightDM Deepin Greeter 的辅助程序，用于在登录过程中处理亮度调节初始化操作。

详见 [lightdm-deepin-greeter-lighter.md](references/cli/lightdm-deepin-greeter-lighter.md)

