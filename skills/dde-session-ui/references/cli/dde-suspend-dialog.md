# dde-suspend-dialog 命令参考

DDE 挂起确认对话框，用于显示系统挂起或关机确认的图形化弹窗。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session-ui` |
| 安装路径 | `/usr/lib/deepin-daemon/dde-suspend-dialog` |
| DDE 角色 | 系统调用的挂起/关机确认对话框组件 |

## 用途

DDE 挂起确认对话框，用于显示系统挂起或关机确认的图形化弹窗。它通过 `setSingleInstance()` 实现进程单实例控制，不需要命令行参数。该工具通常由系统电源管理组件在挂起或关机前自动调用，为用户提供确认操作。

## 用法

`dde-suspend-dialog`

## 使用示例

```bash
# 启动挂起确认对话框
/usr/lib/deepin-daemon/dde-suspend-dialog
```
