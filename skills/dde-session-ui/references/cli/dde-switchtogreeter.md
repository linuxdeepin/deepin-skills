# dde-switchtogreeter 命令参考

DDE 会话切换工具，通过 systemd/login1/lightdm DBus 切换到 greeter 登录界面或其他用户的会话。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session-ui` |
| 安装路径 | `/usr/bin/dde-switchtogreeter` |
| DDE 角色 | 系统会话切换辅助工具 |

## 用途

DDE 会话切换工具，通过 systemd/login1/lightdm DBus 切换到 greeter 登录界面或其他用户的会话。不带参数时切换到 greeter 登录界面；带用户名参数时切换到指定用户的会话。该工具通过 system bus 与 `org.freedesktop.login1.Manager` 和 `org.freedesktop.DisplayManager` 通信，查找当前用户的 seat 和 session 信息，执行会话切换操作。

## 用法

`dde-switchtogreeter [options] [username]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `username` | 要切换到的目标用户名（可选）。省略时切换到 greeter 登录界面 |

## 使用示例

```bash
# 切换到 greeter 登录界面
dde-switchtogreeter

# 切换到指定用户的会话
dde-switchtogreeter anotheruser
```

> 注意：该工具需要通过 system bus 访问 `org.freedesktop.login1` 和 `org.freedesktop.DisplayManager`，需要相应的系统权限。
