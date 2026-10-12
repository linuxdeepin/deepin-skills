---
name: dde-session-ui
description: dde-session-ui 是 DDE 通用 UI 组件集合，提供系统会话中的各类图形化交互界面。该 skill 提供黑屏显示控制、低电量警告提示、许可证内容确认、壁纸色调处理、触摸屏校准、窗口管理器选择、密码重置、系统警告提示、欢迎引导、登录提醒、会话切换、挂起确认、蓝牙配对确认功能，以及登录提醒开关配置（仅适用于 dde-session-ui 自身的登录提醒功能）
Categories:
  - Application
---

# dde-session-ui

dde-session-ui 是 DDE 通用 UI 组件集合，提供系统会话中的各类图形化交互界面。该 skill 提供黑屏显示控制、低电量警告提示、许可证内容确认、壁纸色调处理、触摸屏校准、窗口管理器选择、密码重置、系统警告提示、欢迎引导、登录提醒、会话切换、挂起确认、蓝牙配对确认功能，以及登录提醒开关配置。

## CLI 命令

### dde-blackwidget

DDE 黑屏部件工具，用于在特定场景下显示全屏黑色遮罩窗口。

详见 [dde-blackwidget.md](references/cli/dde-blackwidget.md)

### dde-hints-dialog

DDE 提示对话框工具，用于显示简单的标题+内容提示对话框。

详见 [dde-hints-dialog.md](references/cli/dde-hints-dialog.md)

### dde-license-dialog

DDE 许可证对话框工具，用于展示软件许可证内容并获取用户同意。

详见 [dde-license-dialog.md](references/cli/dde-license-dialog.md)

### dde-lowpower

DDE 低电量提示工具，当系统检测到电池电量低于阈值时弹出低电量警告窗口，提醒用户及时充电或保存工作。

详见 [dde-lowpower.md](references/cli/dde-lowpower.md)

### dde-pixmix

壁纸色调处理工具，对输入壁纸图片计算平均色调并叠加半透明着色层，生成适合桌面环境的背景图片。

详见 [dde-pixmix.md](references/cli/dde-pixmix.md)

### dde-touchscreen-dialog

DDE 触摸屏校准对话框，用于触摸屏设备的校准操作。

详见 [dde-touchscreen-dialog.md](references/cli/dde-touchscreen-dialog.md)

### dde-wm-chooser

DDE 窗口管理器选择工具，用于让用户选择 DDE 会话使用的窗口管理器。

详见 [dde-wm-chooser.md](references/cli/dde-wm-chooser.md)

### reset-password-dialog

DDE 重置密码对话框，用于在用户忘记密码时提供密码重置功能。

详见 [reset-password-dialog.md](references/cli/reset-password-dialog.md)

### dde-warning-dialog

DDE 警告对话框，用于显示系统级警告消息的图形化弹窗。

详见 [dde-warning-dialog.md](references/cli/dde-warning-dialog.md)

### dde-welcome

DDE 欢迎程序，在新用户首次登录或系统安装后显示欢迎引导界面。

详见 [dde-welcome.md](references/cli/dde-welcome.md)

### deepin-login-reminder

登录提醒工具，在用户登录时显示通知或提醒信息。

详见 [deepin-login-reminder.md](references/cli/deepin-login-reminder.md)

### dde-switchtogreeter

DDE 会话切换工具，通过 systemd/login1/lightdm DBus 切换到 greeter 登录界面或其他用户的会话。

详见 [dde-switchtogreeter.md](references/cli/dde-switchtogreeter.md)

### dde-suspend-dialog

DDE 挂起确认对话框，用于显示系统挂起或关机确认的图形化弹窗。

详见 [dde-suspend-dialog.md](references/cli/dde-suspend-dialog.md)

### dde-bluetooth-dialog

DDE 蓝牙 PIN 码确认对话框，用于显示蓝牙设备配对时的 PIN 码确认界面。

详见 [dde-bluetooth-dialog.md](references/cli/dde-bluetooth-dialog.md)

## D-Bus 接口

### 黑屏控制

提供黑屏显示控制能力。

详见 [org.deepin.dde.BlackScreen1.md](references/dbus/org.deepin.dde.BlackScreen1.md)

### 警告对话框

提供警告对话框显示能力。

详见 [org.deepin.dde.WarningDialog1.md](references/dbus/org.deepin.dde.WarningDialog1.md)

### 低电量提示

提供低电量提示显示能力。

详见 [org.deepin.dde.LowPower1.md](references/dbus/org.deepin.dde.LowPower1.md)

### 欢迎界面激活

该接口为 D-Bus 激活型服务，用于欢迎界面的进程单实例控制。

详见 [org.deepin.dde.Welcome1.md](references/dbus/org.deepin.dde.Welcome1.md)

## DConfig 配置项

dde-session-ui 通过 DConfig 暴露登录提醒配置资源，该配置仅适用于 dde-session-ui 自身的登录提醒功能。

### 登录提醒配置

登录提醒启用开关配置，控制是否显示登录提醒通知。

详见 [org.deepin.login-reminder](references/config/org.deepin.login-reminder.md)
