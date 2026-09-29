# dde-dconfig-daemon 命令参考

DDE 配置守护进程，是 DConfig 系统的后台服务进程。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-dconfig-daemon` |
| 安装路径 | `/usr/bin/dde-dconfig-daemon` |
| DDE 角色 | DConfig 配置系统的 DBus 后台服务 |

## 用途

DDE 配置守护进程，是 DConfig 系统的后台服务进程。它通过 DBus 提供配置读写接口，管理所有 DTK 应用的 DConfig 配置项的存储和访问。该守护进程为 system 级 systemd 服务，由 systemd 启动，同时支持 DBus 激活，是 DConfig 配置体系的核心后端，一般不需要用户直接运行。

## 用法

`dde-dconfig-daemon [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-t <time>` | 延迟释放时间 | 是 |
| `-p <prefix>` | 工作目录前缀 | 是 |
| `-e <exit>` | 资源释放后退出 | 否 |

