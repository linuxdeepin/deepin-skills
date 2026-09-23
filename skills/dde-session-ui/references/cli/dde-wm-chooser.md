# dde-wm-chooser 命令参考

DDE 窗口管理器选择工具，用于让用户选择 DDE 会话使用的窗口管理器。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session-ui` |
| 安装路径 | `/usr/bin/dde-wm-chooser` |
| DDE 角色 | 用户使用的窗口管理器选择工具 |

## 用途

DDE 窗口管理器选择工具，用于让用户选择 DDE 会话使用的窗口管理器。DDE 支持多种窗口管理器（如 kwin、deepin-wm），该工具提供图形界面让用户根据硬件性能和偏好选择合适的窗口管理器。通过 `-c` 参数可以指定配置文件路径来加载可选的窗口管理器列表。该工具通常在首次登录或用户手动切换窗口管理器时使用。

## 用法

`dde-wm-chooser [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-c, --config <ConfigPath>` | 配置文件路径 | 是 |

## 使用示例

```bash
# 使用默认配置启动窗口管理器选择界面
dde-wm-chooser

# 指定自定义配置文件启动
dde-wm-chooser -c /etc/dde/wm-chooser.conf
```

> 注意：`dde-wm-chooser` 是图形界面工具，需要图形显示环境（X11/Wayland），在无 DISPLAY 的终端中运行会失败。
