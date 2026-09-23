# dde-touchscreen-dialog 命令参考

DDE 触摸屏校准对话框，用于触摸屏设备的校准操作。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session-ui` |
| 安装路径 | `/usr/lib/deepin-daemon/dde-touchscreen-dialog` |
| DDE 角色 | 系统调用的辅助工具，触摸屏校准场景自动弹出 |

## 用途

DDE 触摸屏校准对话框，用于触摸屏设备的校准操作。当系统检测到新的触摸屏设备或用户需要重新校准触摸屏时，该工具弹出校准引导界面，指导用户通过点击校准点来完成触摸屏的坐标映射。通过位置参数指定触摸屏设备的 UUID。该工具通常由显示管理或设备管理模块在检测到触摸屏设备时自动调用。

## 用法

`dde-touchscreen-dialog [options] [touchscreen]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `touchscreen` | 触摸屏 UUID |

## 使用示例

```bash
# 对指定触摸屏设备（UUID）启动校准对话框
dde-touchscreen-dialog e6f1c2d3-4a5b-6c7d-8e9f-0a1b2c3d4e5f

# 不指定设备启动（系统自动选择触摸屏设备）
dde-touchscreen-dialog
```
