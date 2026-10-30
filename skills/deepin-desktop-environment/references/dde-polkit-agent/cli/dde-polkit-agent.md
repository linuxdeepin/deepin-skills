# dde-polkit-agent 命令参考

DDE 的 PolicyKit 认证代理守护进程，负责在用户执行需要特权的操作时弹出图形认证对话框，收集用户密码或指纹认证信息，是 DDE 权限管理的前端组件。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-polkit-agent` |
| 安装路径 | `/usr/lib/polkit-1-dde/dde-polkit-agent` |
| DDE 角色 | PolicyKit 图形化认证代理 |

## 启动方式

`dde-polkit-agent` 由 systemd 用户服务 `dde-polkit-agent.service` 在用户会话初始化时自动启动，无需手动运行。该服务在 `dde-session-initialized.target` 之前启动，依赖于 `dde-session-core.target`。

服务单元文件位于 `/usr/lib/systemd/user/dde-polkit-agent.service`，`ExecStart` 指向 `/usr/lib/polkit-1-dde/dde-polkit-agent`。
