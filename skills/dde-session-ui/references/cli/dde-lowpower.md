# dde-lowpower 命令参考

DDE 低电量提示工具，当系统检测到电池电量低于阈值时弹出低电量警告窗口，提醒用户及时充电或保存工作。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session-ui` |
| 安装路径 | `/usr/lib/deepin-daemon/dde-lowpower` |
| DDE 角色 | 系统调用的辅助工具，电源管理在低电量时自动弹出 |

## 用途

DDE 低电量提示工具，当系统检测到电池电量低于阈值时弹出低电量警告窗口，提醒用户及时充电或保存工作。支持提升窗口（`--raise`）使其置顶显示，以及退出所有正在运行的 dde-lowpower 实例（`--quit`）。该工具通常由电源管理守护进程在电池电量低时自动调用。

## 用法

`dde-lowpower [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `--raise` | 提升主窗口 | 否 |
| `--quit` | 退出所有 dde-lowpower 实例 | 否 |

## 使用示例

```bash
# 正常启动低电量提示窗口
/usr/lib/deepin-daemon/dde-lowpower

# 提升窗口到最前显示（强制置顶）
/usr/lib/deepin-daemon/dde-lowpower --raise

# 退出所有正在运行的 dde-lowpower 实例
/usr/lib/deepin-daemon/dde-lowpower --quit
```
