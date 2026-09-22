---
name: dde-session-ui
description: 提供 OSD 显示、通知发送关闭、黑屏、警告对话框、内存警告、欢迎界面和低电量提示的 D-Bus 接口
Categories:
  - Application
---

# dde-session-ui

dde-session-ui 是 DDE 通用 UI 组件，通过 Session 总线提供 OSD 显示、通知、黑屏、警告对话框、内存警告、欢迎界面和低电量提示能力。

## D-Bus 接口

### OSD 显示

提供屏幕显示（OSD）提示能力。

详见 [org.deepin.dde.Osd1.md](references/dbus/org.deepin.dde.Osd1.md)

### 桌面通知

提供 freedesktop 标准桌面通知发送和关闭能力。

详见 [org.freedesktop.Notifications.md](references/dbus/org.freedesktop.Notifications.md)

### DDE 通知

提供 DDE 通知发送、更新和关闭能力。

详见 [org.deepin.dde.Notification1.md](references/dbus/org.deepin.dde.Notification1.md)

### 黑屏控制

提供黑屏显示控制能力。

详见 [org.deepin.dde.BlackScreen1.md](references/dbus/org.deepin.dde.BlackScreen1.md)

### 警告对话框

提供警告对话框显示能力。

详见 [org.deepin.dde.WarningDialog1.md](references/dbus/org.deepin.dde.WarningDialog1.md)

### 内存警告对话框

提供内存警告对话框显示能力。

详见 [org.deepin.dde.MemoryWarningDialog1.md](references/dbus/org.deepin.dde.MemoryWarningDialog1.md)

### 欢迎界面

提供欢迎界面显示能力。

详见 [org.deepin.dde.Welcome1.md](references/dbus/org.deepin.dde.Welcome1.md)

### 低电量提示

提供低电量提示显示能力。

详见 [org.deepin.dde.LowPower1.md](references/dbus/org.deepin.dde.LowPower1.md)

## DConfig 配置项

### 资源: `org.deepin.login-reminder`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `LoginReminder` | 登录提醒是否启用 | bool | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.login-reminder -r org.deepin.login-reminder -k LoginReminder --get
# 设置
dde-dconfig -a org.deepin.login-reminder -r org.deepin.login-reminder -k LoginReminder -s "<value>"
```

