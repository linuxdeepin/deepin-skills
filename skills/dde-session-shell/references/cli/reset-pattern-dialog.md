# reset-pattern-dialog 命令参考

重置登录手势密码对话框，用于在 DDE 手势密码登录功能中重置用户的手势密码。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session-shell` |
| 安装路径 | `/usr/lib/dde-control-center/reset-pattern-dialog` |
| DDE 角色 | 系统调用的辅助工具，手势密码重置流程中调用 |

## 用途

重置登录手势密码对话框，用于在 DDE 手势密码登录功能中重置用户的手势密码。通过读取旧密码 ID 和写入新密码 ID 来完成手势密码的重置流程，支持指定调用者用户名、全名和应用名。该工具通常在用户遗忘手势密码或需要重新设置时由系统调用。

## 用法

`/usr/lib/dde-control-center/reset-pattern-dialog [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `--old <oldPasswordId>` | 读取当前已设置的密码 | 是 |
| `--new <newPasswordId>` | 写入要设置的新密码 | 是 |
| `-u <user>` | 调用者用户名 | 是 |
| `-f <f>` | 调用者全名 | 是 |
| `-a <a>` | 调用者应用名 | 是 |

> 注：此二进制不提供 `--help` 输出。该二进制不在默认 PATH 中，需使用完整路径执行。

## 使用示例

```bash
# 重置手势密码：指定旧密码 ID 和新密码 ID
/usr/lib/dde-control-center/reset-pattern-dialog --old old-gesture-123 --new new-gesture-456

# 指定调用者信息重置手势密码
/usr/lib/dde-control-center/reset-pattern-dialog --old old-gesture-123 --new new-gesture-456 -u testuser -f "Test User" -a dde-lock
```
