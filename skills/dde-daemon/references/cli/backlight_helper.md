# backlight_helper 命令参考

背光调节辅助工具，用于在权限受限的环境中设置屏幕背光亮度。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-daemon` |
| 安装路径 | `/usr/lib/deepin-daemon/backlight_helper` |
| DDE 角色 | 屏幕亮度调节的权限辅助工具 |

## 用途

背光调节辅助工具，用于在权限受限的环境中设置屏幕背光亮度。它是一个 setuid 辅助程序，允许普通用户通过它来修改 `/sys/class/backlight` 下的亮度属性，不提供 flag 参数。
