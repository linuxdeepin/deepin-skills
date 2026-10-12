# dde-session 命令参考

DDE 会话管理程序，负责 DDE 桌面会话的启动和初始化。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session` |
| 安装路径 | `/usr/bin/dde-session` |
| DDE 角色 | 系统核心进程，由显示管理器在用户登录时自动启动 |

## 用途

DDE 会话管理程序，负责 DDE 桌面会话的启动和初始化。它在用户登录后由显示管理器启动（X11 环境下为 lightdm，Treeland 环境下为 ddm），负责拉起会话所需的各种服务和组件，包括窗口管理器、面板和控制中心后台。支持在 systemd 服务就绪后再继续启动流程。该工具是 DDE 会话的入口程序，一般不需要用户直接运行。

## 用法

`dde-session [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `--help-all` | 显示包含 Qt 通用选项的完整帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `-d, --systemd-service` | 等待 systemd 服务就绪后继续启动流程 | 否 |

## 使用示例

```bash
# 正常启动 DDE 会话（通常由显示管理器自动调用）
dde-session

# 启动并等待 systemd 服务就绪后继续
dde-session -d

# 查看版本信息
dde-session -v
```
