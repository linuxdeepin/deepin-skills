# sound-theme-player 命令参考

声音主题播放守护进程，提供 DBus 接口供其他程序播放系统声音。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-api` |
| 安装路径 | `/usr/lib/deepin-api/sound-theme-player` |
| DDE 角色 | 系统调用的声音播放守护进程，由会话管理自动启动 |

## 用途

声音主题播放守护进程，提供 DBus 接口供其他程序播放系统声音。它基于 freedesktop.org 声音主题规范，管理 DDE 系统事件音效（如登录音、通知音、错误提示音）。通过 DBus 接口，其他组件可以请求播放指定主题下的特定声音事件。支持自动退出模式（默认开启），即在空闲一段时间后自动退出以节省资源。该工具通常由 DDE 会话自动启动。使用 Go flag 风格参数。

## 用法

`sound-theme-player [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-auto-quit <bool>` | 自动退出（默认 true） | 是 |

## 使用示例

```bash
# 默认启动（自动退出开启，空闲后自动退出）
sound-theme-player

# 启动并禁用自动退出（保持常驻，适用于持续需要播放声音的场景）
sound-theme-player -auto-quit false

# 显式启用自动退出
sound-theme-player -auto-quit true
```
