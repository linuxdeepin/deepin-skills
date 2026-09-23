---
name: dde-session-ui
description: 提供黑屏、警告对话框、欢迎界面和低电量提示的 D-Bus 接口
Categories:
  - Application
---

# dde-session-ui

dde-session-ui 是 DDE 通用 UI 组件，通过 Session 总线提供黑屏、警告对话框、欢迎界面和低电量提示能力。

## D-Bus 接口

### 黑屏控制

提供黑屏显示控制能力。

详见 [org.deepin.dde.BlackScreen1.md](references/dbus/org.deepin.dde.BlackScreen1.md)

### 警告对话框

提供警告对话框显示能力。

详见 [org.deepin.dde.WarningDialog1.md](references/dbus/org.deepin.dde.WarningDialog1.md)

### 欢迎界面

提供欢迎界面显示能力。

详见 [org.deepin.dde.Welcome1.md](references/dbus/org.deepin.dde.Welcome1.md)

### 低电量提示

提供低电量提示显示能力。

详见 [org.deepin.dde.LowPower1.md](references/dbus/org.deepin.dde.LowPower1.md)

## DConfig 配置项

dde-session-ui 通过 DConfig 暴露登录提醒配置资源。

### 登录提醒配置

登录提醒启用开关配置。

详见 [org.deepin.login-reminder](references/config/org.deepin.login-reminder.md)

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

DDE 壁纸混合工具，用于将多张壁纸图片进行混合处理，输出适合当前桌面环境使用的背景图片。

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

### dmemory-warning-dialog

内存警告对话框，在系统内存不足时弹出警告提示。

详见 [dmemory-warning-dialog.md](references/cli/dmemory-warning-dialog.md)

