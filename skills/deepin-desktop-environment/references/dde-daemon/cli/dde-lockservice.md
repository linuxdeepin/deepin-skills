# dde-lockservice 服务说明

登录界面选中用户记录的辅助服务，不是触发锁屏的命令。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-daemon` |
| 安装路径 | `/usr/lib/deepin-daemon/dde-lockservice` |
| DDE 角色 | 登录界面选中用户名的查询、保存与变化通知 |

该进程提供 System 总线上的 `org.deepin.dde.LockService1`，供登录界面读取或保存选中的用户名。普通锁屏请求不通过启动该守护进程完成；不要把返回的用户名当作当前活动会话的身份。

接口调用方式见 [LockService1](../dbus/org.deepin.dde.LockService1.md)。
