# dde-blackwidget 命令参考

DDE 黑屏部件工具，用于在特定场景下显示全屏黑色遮罩窗口。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session-ui` |
| 安装路径 | `/usr/lib/deepin-daemon/dde-blackwidget` |
| DDE 角色 | 系统调用的辅助工具，显示状态变更时自动调用 |

## 用途

DDE 黑屏部件工具，用于在特定场景下显示全屏黑色遮罩窗口。主要在系统休眠唤醒、显示模式切换、屏幕关闭过程中使用，为用户提供平滑的视觉过渡效果，避免画面闪烁。支持通过 `nodbus` 参数禁用 DBus 通信以独立运行。该工具通常由系统在显示状态变更时自动调用。

## 用法

`dde-blackwidget [options] [nodbus]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `nodbus` | 存在时禁用 DBus |

## 使用示例

```bash
# 正常启动黑屏部件（使用 DBus 通信）
/usr/lib/deepin-daemon/dde-blackwidget

# 以无 DBus 模式启动（独立运行，不通过 DBus 控制）
/usr/lib/deepin-daemon/dde-blackwidget nodbus
```
