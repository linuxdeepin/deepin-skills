---
name: xdg-desktop-portal-dde
description: DDE 的 Portal 后端，提供截图、取色、屏幕共享、壁纸、通知、文件选择、账户、访问、应用选择、后台、快捷键、抑制、密钥、请求管理及外观偏好查询。应用通过 Portal 前端调用；本 skill 的 impl 接口用于后端协作与调试，Settings 只读，Lockdown 是门户策略状态。
Categories:
  - Settings
---

# xdg-desktop-portal-dde

xdg-desktop-portal-dde 是 xdg-desktop-portal 的 DDE 后端实现。它通过 Session 总线为沙箱应用提供访问系统资源（文件选择、屏幕截图、屏幕取色、屏幕共享、壁纸设置、通知发送、用户信息查询、全局快捷键绑定、会话抑制）的 Portal D-Bus 接口，由 DBus 在沙箱应用请求系统服务时自动激活。

应用调用 `org.freedesktop.portal.Desktop` 服务的 `org.freedesktop.portal.*` 接口，由前端处理应用身份、权限与请求响应。下面的 `org.freedesktop.impl.portal.*` 是前端与 DDE 后端之间的协作接口，参数中的 `app_id`、请求 `handle` 由前端提供；后端调试示例不能代替应用调用流程。沙箱是主要使用场景，但不以应用是否沙箱化作为接口分流的唯一条件。

Settings 只提供读取和变化通知；锁定策略属性只描述门户后端的状态，不保证在系统范围禁用设备。按末尾平台表选择目标会话，不能通过重复启动后台服务修复未实现的接口。

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

查询桌面外观偏好（颜色方案、强调色）并监听变化，不提供设置方法。

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

查询和调整后端进程内的门户策略状态，不作为系统设备或应用权限的全局封禁接口。

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
