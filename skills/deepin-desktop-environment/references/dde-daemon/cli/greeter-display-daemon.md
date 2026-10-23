# greeter-display-daemon 命令参考

登录界面显示守护进程，负责在 LightDM 登录阶段管理显示配置。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-daemon` |
| 安装路径 | `/usr/lib/deepin-daemon/greeter-display-daemon` |
| DDE 角色 | 登录阶段的显示配置守护进程 |

## 用途

登录界面显示守护进程，负责在 LightDM 登录阶段管理显示配置。它在 greeter 运行期间提供显示设置的 DBus 接口，配合 greeter 完成显示初始化，不提供 flag 参数。
