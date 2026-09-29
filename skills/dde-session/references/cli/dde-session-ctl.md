# dde-session-ctl 命令参考

DDE 会话控制工具，用于执行关机、退出会话、注销这三项会话级操作。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session` |
| 安装路径 | `/usr/libexec/dde-session-ctl` |
| DDE 角色 | 用户和系统脚本均可使用的会话控制工具 |

## 用途

DDE 会话控制工具，用于执行关机、退出会话、注销这三项会话级操作。它是一个轻量级的命令行工具，用户或系统脚本可以通过它触发会话退出流程。与图形化的关机/注销界面不同，该工具直接通过命令行发起操作，适用于无图形界面环境下的会话管理或自动化脚本场景。

## 用法

`/usr/libexec/dde-session-ctl [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `--help-all` | 显示包含 Qt 通用选项的完整帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `-s, --shutdown` | 关闭 DDE（关机） | 否 |
| `-S, --session-exit` | 会话退出任务 | 否 |
| `-l, --logout` | 注销会话 | 否 |

## 使用示例

```bash
# 关闭 DDE（关机）
/usr/libexec/dde-session-ctl -s

# 退出当前 DDE 会话
/usr/libexec/dde-session-ctl -S

# 注销当前用户会话
/usr/libexec/dde-session-ctl -l

# 查看版本信息
/usr/libexec/dde-session-ctl -v
```
