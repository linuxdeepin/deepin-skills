# xdg-desktop-portal-dde 命令参考

DDE 的 XDG Desktop Portal 后端实现，为沙箱应用（如 Flatpak）提供访问系统资源（文件选择、屏幕截图、屏幕共享）的 DBus 接口。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `xdg-desktop-portal-dde` |
| 安装路径 | `/usr/libexec/xdg-desktop-portal-dde` |
| DDE 角色 | 沙箱应用访问系统资源的 Portal 后端 |

## 用途

DDE 的 XDG Desktop Portal 后端实现，为沙箱应用（如 Flatpak）提供访问系统资源（文件选择、屏幕截图、屏幕共享）的 DBus 接口。它由 DBus 在沙箱应用请求系统服务时自动激活，是 DDE 沙箱应用生态的门户组件，一般不需要用户直接运行。
