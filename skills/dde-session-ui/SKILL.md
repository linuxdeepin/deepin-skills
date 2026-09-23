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
