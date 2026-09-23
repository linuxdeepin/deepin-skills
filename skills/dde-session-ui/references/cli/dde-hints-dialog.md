# dde-hints-dialog 命令参考

DDE 提示对话框工具，用于显示简单的标题+内容提示对话框。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session-ui` |
| 安装路径 | `/usr/bin/dde-hints-dialog` |
| DDE 角色 | 系统调用的辅助工具，用于弹出提示对话框 |

## 用途

DDE 提示对话框工具，用于显示简单的标题+内容提示对话框。该工具不使用 QCommandLineParser，直接接收位置参数作为对话框标题和内容文本，适用于脚本或系统流程中需要弹出简短提示信息的场景。

## 用法

`dde-hints-dialog <title> <content>`

> 注：此二进制不使用 QCommandLineParser，无 `--help` 输出。参数为原始位置参数。

## 位置参数

| 参数 | 说明 |
|------|------|
| `title` | 对话框标题 |
| `content` | 对话框内容 |

## 使用示例

```bash
# 显示标题为"提示"、内容为"操作已完成"的对话框
dde-hints-dialog "提示" "操作已完成"

# 显示系统通知风格的提示
dde-hints-dialog "警告" "磁盘空间不足，请及时清理"

# 在脚本中使用（等待用户点击确认后继续）
dde-hints-dialog "确认" "确定要继续执行吗？"
```

> 注意：`dde-hints-dialog` 是图形对话框工具，需要图形显示环境（X11/Wayland），在无 DISPLAY 的终端中运行会失败。
