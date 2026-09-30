---
name: xdg-desktop-portal-dde
description: xdg-desktop-portal-dde 是 xdg-desktop-portal 的 DDE 后端实现，为沙箱应用提供访问系统资源的 Portal D-Bus 接口。本 skill 提供通过 Session 总线为沙箱应用提供截图、屏幕取色、屏幕共享、壁纸设置、通知发送与移除（仅作用于 portal 通道）、文件选择、账户查询、访问对话框、应用选择、后台运行管理、全局快捷键绑定、会话抑制、密钥检索、锁定模式设置、请求生命周期管理的 Portal D-Bus 接口，读写桌面环境全局设置（颜色方案、强调色）的 Settings 接口，以及 xdg-desktop-portal-dde 自身的后台服务命令行工具
Categories:
  - Settings
---

# xdg-desktop-portal-dde

xdg-desktop-portal-dde 是 xdg-desktop-portal 的 DDE 后端实现。它通过 Session 总线为沙箱应用提供访问系统资源（文件选择、屏幕截图、屏幕取色、屏幕共享、壁纸设置、通知发送、用户信息查询、全局快捷键绑定、会话抑制）的 Portal D-Bus 接口，由 DBus 在沙箱应用请求系统服务时自动激活。

## CLI 命令

### xdg-desktop-portal-dde

xdg-desktop-portal-dde 自身的后台服务进程，为沙箱应用（如 Flatpak）提供访问系统资源的 DBus 接口。由 DBus 在沙箱应用请求系统服务时自动激活，一般不需要用户直接运行。

详见 [xdg-desktop-portal-dde.md](references/cli/xdg-desktop-portal-dde.md)


## D-Bus 接口

以下 D-Bus 接口均通过 Session 总线注册。服务名为 `org.freedesktop.impl.portal.desktop.dde`，对象路径为 `/org/freedesktop/portal/desktop`。

### 截图

提供屏幕截图和屏幕取色能力。

详见 [org.freedesktop.impl.portal.Screenshot.md](references/dbus/org.freedesktop.impl.portal.Screenshot.md)

### 屏幕共享

提供屏幕共享会话创建、源选择和共享启动能力。仅在 Wayland 环境下可用。

详见 [org.freedesktop.impl.portal.ScreenCast.md](references/dbus/org.freedesktop.impl.portal.ScreenCast.md)

### 设置

读写桌面环境全局设置（颜色方案、强调色）。

详见 [org.freedesktop.impl.portal.Settings.md](references/dbus/org.freedesktop.impl.portal.Settings.md)

### 壁纸

提供壁纸设置能力。

详见 [org.freedesktop.impl.portal.Wallpaper.md](references/dbus/org.freedesktop.impl.portal.Wallpaper.md)

### 通知

仅作用于 portal 通道的通知发送与移除。

详见 [org.freedesktop.impl.portal.Notification.md](references/dbus/org.freedesktop.impl.portal.Notification.md)

### 文件选择

提供文件打开和保存对话框能力。

详见 [org.freedesktop.impl.portal.FileChooser.md](references/dbus/org.freedesktop.impl.portal.FileChooser.md)

### 账户

提供用户信息查询能力。

详见 [org.freedesktop.impl.portal.Account.md](references/dbus/org.freedesktop.impl.portal.Account.md)

### 访问

提供访问对话框能力。

详见 [org.freedesktop.impl.portal.Access.md](references/dbus/org.freedesktop.impl.portal.Access.md)

### 应用选择

提供应用选择对话框能力。

详见 [org.freedesktop.impl.portal.AppChooser.md](references/dbus/org.freedesktop.impl.portal.AppChooser.md)

### 后台管理

提供后台运行请求和通知能力。

详见 [org.freedesktop.impl.portal.Background.md](references/dbus/org.freedesktop.impl.portal.Background.md)

### 全局快捷键

提供全局快捷键会话创建和绑定能力。

详见 [org.freedesktop.impl.portal.GlobalShortcuts.md](references/dbus/org.freedesktop.impl.portal.GlobalShortcuts.md)

### Inhibit

提供会话抑制能力。

详见 [org.freedesktop.impl.portal.Inhibit.md](references/dbus/org.freedesktop.impl.portal.Inhibit.md)

### 密钥

提供密钥检索能力。

详见 [org.freedesktop.impl.portal.Secret.md](references/dbus/org.freedesktop.impl.portal.Secret.md)

### 锁定

提供锁定模式设置能力。

详见 [org.freedesktop.impl.portal.Lockdown.md](references/dbus/org.freedesktop.impl.portal.Lockdown.md)

### 请求

提供标准 portal 请求关闭能力。

详见 [org.freedesktop.impl.portal.Request.md](references/dbus/org.freedesktop.impl.portal.Request.md)

## 平台可用性

各 D-Bus 接口的平台可用性如下：

| 接口 | 平台可用性 |
|------|------------|
| ScreenCast | 仅 Wayland |
| Wallpaper | 仅 Wayland |
| Background | 仅 X11（需 `XDG_CURRENT_DESKTOP=DDE` 或 `DEEPIN`） |
| Settings | 仅 X11（需 `XDG_CURRENT_DESKTOP=DDE` 或 `DEEPIN`） |
| Inhibit | 仅 X11（需 `XDG_CURRENT_DESKTOP=DDE` 或 `DEEPIN`） |
| Account | 仅 X11（需 `XDG_CURRENT_DESKTOP=DDE` 或 `DEEPIN`） |
| GlobalShortcuts | 仅 X11（需 `XDG_CURRENT_DESKTOP=DDE` 或 `DEEPIN`） |
| Lockdown | 仅 X11（需 `XDG_CURRENT_DESKTOP=DDE` 或 `DEEPIN`） |
| Secret | 仅 X11（需 `XDG_CURRENT_DESKTOP=DDE` 或 `DEEPIN`） |
| FileChooser | 双平台（Wayland 和 X11） |
| Screenshot | 双平台（Wayland 和 X11） |
| Notification | 仅 X11 |
| Access | 仅 X11 |
| AppChooser | 仅 X11 |
| Request | 双平台（Wayland 和 X11） |
