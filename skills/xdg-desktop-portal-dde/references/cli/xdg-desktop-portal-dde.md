# xdg-desktop-portal-dde 命令参考

xdg-desktop-portal-dde 自身的后台服务进程，为沙箱应用（如 Flatpak）提供访问系统资源的 DBus 接口。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `xdg-desktop-portal-dde` |
| 安装路径 | `/usr/libexec/xdg-desktop-portal-dde` |
| DDE 角色 | 沙箱应用访问系统资源的 Portal 后端 |

## 用途

xdg-desktop-portal-dde 是 xdg-desktop-portal 的 DDE 后端实现，为沙箱应用提供访问系统资源（文件选择、屏幕截图、屏幕取色、壁纸设置、通知发送、用户信息查询、全局快捷键绑定、会话抑制）的 DBus 接口。它由 DBus 在沙箱应用请求系统服务时自动激活，是 DDE 沙箱应用生态的门户组件，一般不需要用户直接运行。

## 用法

`/usr/libexec/xdg-desktop-portal-dde`

> 注：该二进制不在默认 PATH 中，需使用完整路径执行。

## 命令行选项

该进程由 DBus 自动激活，不支持命令行选项参数。启动后直接注册 DBus 服务并进入事件循环。

> 注意：`xdg-desktop-portal-dde` 是 Portal 后端守护进程，由 DBus 在沙箱应用请求系统服务时自动激活，通常无需手动运行。手动运行时需要图形环境（Display）支持，否则会因无法初始化 Qt 平台插件而崩溃。
