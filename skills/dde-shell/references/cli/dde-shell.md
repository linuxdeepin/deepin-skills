# dde-shell 命令参考

DDE Shell 框架主程序，是 DDE 桌面环境面板（panel）和小程序（applet）的核心管理框架。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-shell` |
| 安装路径 | `/usr/bin/dde-shell` |
| DDE 角色 | DDE 桌面环境核心进程，会话启动时自动拉起；开发调试时可手动运行 |

## 用途

DDE Shell 框架主程序，是 DDE 桌面环境面板（panel）和小程序（applet）的核心管理框架。它负责加载和运行各种面板（如任务栏 dock、启动器面板）及其上的小程序组件，管理面板的生命周期、布局和交互。dde-shell 支持通过参数指定加载哪些面板、按类别筛选面板、禁用特定小程序、注册 DBus 服务名、进入测试模式。它是 DDE 桌面环境的核心进程之一，通常在会话启动时自动运行，也可以在开发调试时手动启动以测试特定面板或小程序。

## 用法

`dde-shell [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `-p <panel>` | 指定 panel 集合 | 是 |
| `-C <category>` | 按 category 指定根 panel 集合 | 是 |
| `-t, --test` | 应用测试模式 | 否 |
| `-d <disable-applet>` | 禁用指定 applet | 是 |
| `--list` | 列出所有 applet | 否 |
| `--sceneview` | 在场景中查看 applet（仅在无 Window 时生效） | 否 |
| `--serviceName <serviceName>` | 注册 DBus 服务名（默认：`org.deepin.dde.shell`） | 是 |

## 使用示例

```bash
# 以指定插件（panel）启动 dde-shell，如加载 dock 面板
dde-shell -p dock

# 指定多个 panel 启动
dde-shell -p dock,launcher

# 按 category 指定根 panel 集合
dde-shell -C main-panel

# 列出所有可用的 applet
dde-shell --list

# 启动时禁用指定 applet（如禁用音量控制小程序）
dde-shell -d volume

# 以测试模式启动（用于开发调试）
dde-shell -t

# 注册自定义 DBus 服务名
dde-shell --serviceName org.deepin.dde.shell.test

# 查看版本信息
dde-shell -v
```

> 注意：`dde-shell` 是 DDE 桌面环境核心图形进程，需要图形显示环境（X11/Wayland），在无 DISPLAY 的终端中运行会失败。
