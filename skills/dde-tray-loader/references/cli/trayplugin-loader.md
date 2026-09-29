# trayplugin-loader 命令参考

DDE 托盘插件加载器，负责加载和管理系统托盘区域的插件。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-tray-loader` |
| 安装路径 | `/usr/libexec/trayplugin-loader` |
| DDE 角色 | 系统调用的辅助工具，由 dde-shell 在会话启动时自动拉起 |

## 用途

DDE 托盘插件加载器，负责加载和管理系统托盘区域的插件。它根据指定的插件路径或分组名称，将托盘插件动态加载到 DDE 面板的托盘区域中。该工具通常由 dde-shell 或面板管理进程在会话启动时自动调用，一般不需要用户直接运行。

## 用法

`/usr/libexec/trayplugin-loader (-p <plugin path(s)> | --group <group name>) [--check-group <group name>]`

> **注意**：必须指定 `-p` 或 `--group` 之一，两者互斥；均未指定或同时指定时显示帮助信息并退出。`-p` 模式和 `--group` 模式需要运行中的图形显示环境（Wayland 或 X11），无显示环境时无法启动。`--check-group` 为诊断模式，不初始化图形环境。

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `-p <plugin path(s)>` | 插件路径，单个或多个（用 `;` 分隔） | 二选一（与 `--group` 互斥） |
| `-g <group name>` | 为指定插件路径设置分组名称，用于面板中标识本进程加载的插件组。未指定时使用第一个加载插件的名称作为默认值 | 是 |
| `--group <group name>` | 加载指定分组的所有插件，由 systemd 在会话启动时自动调用 | 二选一（与 `-p` 互斥） |
| `--check-group <group name>` | 检查指定分组是否包含插件（systemd ExecCondition 诊断模式），不初始化图形环境 | 是 |

## 使用示例

```bash
# 加载单个托盘插件
/usr/libexec/trayplugin-loader -p /usr/lib/dde-tray-loader/plugins/mytray.so

# 加载多个托盘插件（用分号分隔路径）
/usr/libexec/trayplugin-loader -p /usr/lib/dde-tray-loader/plugins/tray1.so;/usr/lib/dde-tray-loader/plugins/tray2.so

# 加载插件并指定组名（用于面板分组显示）
/usr/libexec/trayplugin-loader -p /usr/lib/dde-tray-loader/plugins/mytray.so -g panel-tray

# 加载指定分组的所有插件（由 systemd 自动调用）
/usr/libexec/trayplugin-loader --group selfMaintenanceTrayPlugins

# 检查指定分组是否包含插件（systemd ExecCondition 诊断模式）
/usr/libexec/trayplugin-loader --check-group selfMaintenanceTrayPlugins

# 查看版本信息
/usr/libexec/trayplugin-loader --version
```
