# reset-password-dialog 命令参考

DDE 重置密码对话框，用于在用户忘记密码时提供密码重置功能。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session-ui` |
| 安装路径 | `/usr/lib/dde-control-center/reset-password-dialog` |
| DDE 角色 | 用户使用的密码重置工具，登录界面中触发 |

## 用途

DDE 重置密码对话框，用于在用户忘记密码时提供密码重置功能。它通过 PAM 认证机制验证用户身份后允许设置新密码。支持指定用户名和应用名参数，通常在登录界面（如 lightdm-deepin-greeter）中由用户点击"忘记密码"触发。该工具也可以在系统恢复或运维场景中手动调用。

## 用法

`reset-password-dialog [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-u, --username <username>` | 用户名 | 是 |
| `-a, --appname <applicationName>` | 应用名 | 是 |
| `--fd <filedescriptor>` | 文件描述符 | 是 |

## 使用示例

```bash
# 为指定用户弹出重置密码对话框
/usr/lib/dde-control-center/reset-password-dialog -u testuser

# 指定用户名和应用名
/usr/lib/dde-control-center/reset-password-dialog -u testuser -a lightdm-deepin-greeter

# 使用文件描述符进行通信
/usr/lib/dde-control-center/reset-password-dialog -u testuser -a lightdm-deepin-greeter --fd 3
```
