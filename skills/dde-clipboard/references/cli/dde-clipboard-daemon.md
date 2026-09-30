# dde-clipboard-daemon 命令参考

DDE 剪贴板守护进程，负责管理剪贴板历史记录和剪贴板事件监听。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-clipboard` |
| 安装路径 | `/usr/bin/dde-clipboard-daemon` |
| DDE 角色 | 剪贴板管理系统的后台守护进程 |

## 用途

DDE 剪贴板守护进程，负责管理剪贴板历史记录和剪贴板事件监听。它在用户会话中后台运行，通过 D-Bus 为剪贴板管理器提供数据存储和检索支持。该守护进程在会话启动时自动运行，一般不需要用户直接运行。

## 用法

`dde-clipboard-daemon`

该守护进程不接受命令行参数。

## 使用示例

```bash
# 手动启动剪贴板守护进程（通常由会话管理自动启动）
dde-clipboard-daemon
```

> 注意：`dde-clipboard-daemon` 是后台守护进程，需要 D-Bus Session 总线环境，在无 Session 总线的终端中运行会注册失败并退出。正常运行时由 DDE 会话管理自动启动。
