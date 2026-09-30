# dde-lockservice 命令参考

DDE 锁屏服务工具，用于触发系统锁屏。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-daemon` |
| 安装路径 | `/usr/lib/deepin-daemon/dde-lockservice` |
| DDE 角色 | 锁屏触发的辅助服务工具 |

## 用途

DDE 锁屏服务工具，用于触发系统锁屏。它通过 DBus 调用包括 dde-lock 在内的组件实现屏幕锁定功能，是电源管理和安全策略的辅助工具，不提供 flag 参数。
