# app-identifier 命令参考

应用身份识别工具，用于识别指定进程以何种身份（应用 ID）运行。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-application-manager` |
| 安装路径 | `/usr/bin/app-identifier` |
| DDE 角色 | 系统调用的辅助工具，用于应用身份识别和安全审计 |

## 用途

应用身份识别工具，用于识别指定进程以何种身份（应用 ID）运行。它通过查询 dde-application-manager 的应用管理信息，将进程 PID 映射到对应的应用标识。该工具主要用于 DDE 的应用权限管理和安全审计场景，例如判断某个进程属于哪个应用、是否以沙箱方式运行。通常由系统安全组件或调试工具调用。

## 用法

`app-identifier [options] [pid1,pid2,pid3 ...]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `PIDs` | 待识别的进程 PID（逗号分隔） |

## 使用示例

```bash
# 识别单个进程的应用身份
app-identifier 1234

# 识别多个进程的应用身份（逗号分隔 PID）
app-identifier 1234,5678,9012

# 查看版本信息
app-identifier -v
```

> 注意：`app-identifier` 需要与 dde-application-manager 守护进程通过 D-Bus 通信，无 D-Bus session 时会报 "Not connected to D-Bus server"。
