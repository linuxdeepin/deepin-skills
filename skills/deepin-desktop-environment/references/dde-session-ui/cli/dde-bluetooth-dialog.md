# dde-bluetooth-dialog 命令参考

DDE 蓝牙 PIN 码确认对话框，用于显示蓝牙设备配对时的 PIN 码确认界面。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session-ui` |
| 安装路径 | `/usr/lib/deepin-daemon/dde-bluetooth-dialog` |
| DDE 角色 | 蓝牙配对 PIN 码确认对话框组件 |

## 用途

DDE 蓝牙 PIN 码确认对话框，用于显示蓝牙设备配对时的 PIN 码确认界面。它接收 PIN 码、设备路径和配对时间作为必填参数，可选参数控制取消按钮的显示状态。该工具通常由蓝牙服务在设备配对时自动调用。

## 用法

`dde-bluetooth-dialog <ping-code> <device-path> <ping-time> [cancel-btn-state]`

## 位置参数

| 参数 | 说明 |
|------|------|
| `ping-code` | 蓝牙配对 PIN 码（必填） |
| `device-path` | 蓝牙设备路径（必填） |
| `ping-time` | 配对时间（必填） |
| `cancel-btn-state` | 是否显示取消按钮，取值 `true` 或 `false`（可选，默认 `true`） |

## 使用示例

```bash
# 显示蓝牙 PIN 码确认对话框（显示取消按钮）
/usr/lib/deepin-daemon/dde-bluetooth-dialog 123456 /org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX 30000 true

# 显示蓝牙 PIN 码确认对话框（不显示取消按钮）
/usr/lib/deepin-daemon/dde-bluetooth-dialog 123456 /org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX 30000 false
```

> 注意：该工具需要图形显示环境（X11/Wayland），在无 DISPLAY 的终端中运行会失败。
