# dde-session-daemon 命令参考

DDE 会话守护进程，是 DDE 桌面会话中运行的后台核心服务。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-daemon` |
| 安装路径 | `/usr/lib/deepin-daemon/dde-session-daemon` |
| DDE 角色 | 系统核心守护进程，会话启动时自动运行 |

## 用途

DDE 会话守护进程，是 DDE 桌面会话中运行的后台核心服务。它负责管理各种功能模块的加载、启用和禁用，包括数十个功能模块（网络、蓝牙、声音、电源、账户、显示）。通过模块化的架构设计，可以灵活地启用或禁用特定功能模块。支持日志级别控制、强制启动已禁用模块、列出模块及其依赖关系。该守护进程在用户登录后由会话管理自动启动，是 DDE 桌面环境正常运行的基础服务。使用 Go flag 风格参数。

## 用法

`dde-session-daemon [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-v` / `-verbose` | 详细输出（`--loglevel debug` 的简写） | 否 |
| `-l` / `-loglevel <string>` | 日志级别：`error`/`warn`/`info`/`debug`/`no`（默认 `info`） | 是 |
| `-f` / `-force` | 强制启动已禁用的模块 | 否 |
| `-i` / `-ignore` | 忽略缺失模块（默认 true） | 否 |
| `-list <string>` | 列出所有模块或指定模块的依赖（参数：`all` 或模块名） | 是 |
| `-enable <string>` | 启用模块及其依赖（逗号分隔） | 是 |
| `-disable <string>` | 禁用模块（逗号分隔） | 是 |

## 使用示例

```bash
# 正常启动会话守护进程（默认日志级别 info）
dde-session-daemon

# 以 debug 日志级别启动（输出详细调试信息）
dde-session-daemon -l debug

# 使用简写方式启用详细输出
dde-session-daemon -v

# 列出所有已注册的模块
dde-session-daemon -list all

# 列出指定模块的依赖关系
dde-session-daemon -list network

# 启用指定模块及其依赖
dde-session-daemon -enable network,bluetooth

# 禁用指定模块
dde-session-daemon -disable bluetooth

# 强制启动已禁用的模块
dde-session-daemon -f

# 忽略缺失模块启动（默认行为，显式指定）
dde-session-daemon -i
```
