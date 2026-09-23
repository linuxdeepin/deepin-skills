# deepin-screensaver 命令参考

DDE 屏幕保护程序，负责在用户空闲一段时间后启动屏幕保护动画。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `deepin-screensaver` |
| 安装路径 | `/usr/bin/deepin-screensaver` |
| DDE 角色 | 系统调用的辅助工具，空闲超时后自动启动 |

## 用途

DDE 屏幕保护程序，负责在用户空闲一段时间后启动屏幕保护动画。它支持通过 DBus 注册服务供系统调用、直接启动屏保、以及打开特定屏保应用的配置对话框。支持多个屏保应用，通过位置参数指定使用的屏保名称。该工具通常由 DDE 会话管理在检测到用户空闲时自动调用，也可以手动运行用于测试和配置屏保。

## 用法

`deepin-screensaver [options] [screensaer-name]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `-d, --dbus` | 注册 DBus 服务 | 否 |
| `-s, --start` | 启动屏幕保护 | 否 |
| `-c, --config <screensaer-name>` | 启动屏保的配置对话框 | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `screensaer-name` | 使用的屏保应用名 |

## 使用示例

```bash
# 以 DBus 服务模式启动（通常由会话管理自动调用）
deepin-screensaver -d

# 立即启动屏幕保护
deepin-screensaver -s

# 启动指定屏保应用
deepin-screensaver -s my-screensaver

# 打开指定屏保应用的配置对话框
deepin-screensaver -c my-screensaver

# 查看版本信息
deepin-screensaver -v
```

> 注意：`deepin-screensaver` 是图形化屏幕保护程序，需要图形显示环境（X11/Wayland），在无 DISPLAY 的终端中运行会失败。
