# dde-control-center 命令参考

DDE 控制中心主程序，是 DDE 桌面环境中用于系统设置管理的核心图形应用。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-control-center` |
| 安装路径 | `/usr/bin/dde-control-center` |
| 实际二进制 | `/usr/libexec/deepin/dde-control-center` |
| DDE 角色 | 用户直接使用的系统设置 GUI 工具；同时被包括 dde-shell 在内的组件通过 DBus 调用以打开特定设置页 |

`/usr/bin/dde-control-center` 是一个 bash 脚本包装器，实际二进制位于 `/usr/libexec/deepin/dde-control-center`。该包装器通过加载器（loader）启动实际二进制，以满足安全执行要求。由于实际二进制通过加载器启动，`--help`、`--help-all`、`-v`（`--version`）选项无法产生终端输出，因此不提供相关示例。

## 用途

DDE 控制中心主程序，是 DDE 桌面环境中用于系统设置管理的核心图形应用。它集成了数十个设置模块（显示、声音、网络、个性化、账户、电源、键盘鼠标、日期时间、更新），为用户提供统一的系统配置入口。在 DDE 中，它既是用户直接通过桌面快捷方式启动的 GUI 应用，也支持命令行参数来指定打开特定模块、以 DBus 模式运行或进行启动耗时调试。控制中心还支持插件机制，允许从指定目录加载第三方设置插件。

## 用法

`/usr/bin/dde-control-center [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-s, --show` | 显示控制中心（默认隐藏） | 否 |
| `-t, --toggle` | 切换控制中心可见性 | 否 |
| `-d, --dbus` | 以 DBus 模式启动 | 否 |
| `-m <module>` | 指定要显示的模块 ID | 是 |
| `-p <page>` | 指定模块页面 | 是 |
| `-z, --time` | 显示控制中心启动耗时 | 否 |
| `-l, --logging-module <loggingModule>` | 仅输出指定模块的日志 | 是 |
| `--spec <plugindir>` | 从指定目录加载插件 | 是 |

## 使用示例

```bash
# 显示控制中心主界面
/usr/bin/dde-control-center -s

# 切换控制中心可见性（若已显示则隐藏，反之亦然）
/usr/bin/dde-control-center -t

# 直接打开"显示"设置模块
/usr/bin/dde-control-center -m display

# 打开"网络"模块的特定页面
/usr/bin/dde-control-center -m network -p 1

# 以 DBus 模式启动（供其他程序通过 DBus 调用控制中心）
/usr/bin/dde-control-center -d

# 显示启动耗时（用于性能调试）
/usr/bin/dde-control-center -s -z

# 仅输出 network 模块的日志（用于调试特定模块）
/usr/bin/dde-control-center -s -l network

# 从自定义目录加载插件
/usr/bin/dde-control-center --spec /opt/my-plugins/
```

> 注意：
> - `dde-control-center` 是图形应用，GUI 启动类操作（`-s`、`-t`、`-m`、`-d` 这些）需要图形显示环境（X11/Wayland），在无 DISPLAY 的终端中运行会报 Qt platform plugin 错误。
