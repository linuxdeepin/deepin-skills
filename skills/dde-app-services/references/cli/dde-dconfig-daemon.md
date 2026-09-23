# dde-dconfig-daemon 命令参考

DDE 配置守护进程，是 dconfig 系统的后台服务进程。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-dconfig-daemon` |
| 安装路径 | `/usr/bin/dde-dconfig-daemon` |
| DDE 角色 | dconfig 配置系统的 DBus 后台服务 |

## 用途

DDE 配置守护进程，是 dconfig 系统的后台服务进程。它通过 DBus 提供配置读写接口，管理所有 DTK 应用的 dconfig 配置项的存储和访问。该守护进程在用户会话启动时由 DBus 自动激活，是 dconfig 配置体系的核心后端，一般不需要用户直接运行。
