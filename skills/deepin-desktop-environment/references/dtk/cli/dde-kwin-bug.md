# dde-kwin-bug 命令参考

DDE KWin 窗口调试工具，监测应用窗口启动时间和渲染行为。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DGui/bin/dde-kwin-bug` |
| DDE 角色 | 开发调试工具，用于监测应用窗口启动时间和渲染行为（源码目录名为 `dde-kwin-debug`，实际二进制名为 `dde-kwin-bug`） |

## 用途

DDE KWin 窗口调试工具。启动指定应用程序并监听 X11 窗口事件，监测应用窗口的创建、属性变化和渲染完成时间，从而分析窗口启动性能和渲染行为。支持自定义日志格式、禁用缓存、设置重复测试次数以及配置检查参数（检查间隔、ping 回复时间、有效计数、damage 计数）。适用于 DDE 桌面环境下窗口启动性能和渲染行为的调试分析。

## 用法

`dde-kwin-bug [options] <applications...>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `--help` | 显示帮助信息 | 否 |
| `-k` | 测试完成后自动退出对应应用程序窗口 | 否 |
| `-L` | 禁用应用程序的输出（重定向标准输出到 /dev/null） | 否 |
| `-a` | 监听所有窗口 | 否 |
| `--format <格式>` | 日志格式，支持 `%p`（进程 PID）、`%t`（启动时间，单位 ms）、`%n`（应用名称） | 是 |
| `-no-cache` | 禁用缓存（启动前清理系统缓存） | 否 |
| `--r <次数>` | 设置重复测试次数 | 是 |
| `--ci <值>` | 设置检查间隔（默认 100 ms） | 是 |
| `--cpt <值>` | 设置窗口 ping 回复时间（默认 50 ms） | 是 |
| `--cvc <值>` | 设置检查有效计数（默认 10） | 是 |
| `--cdc <值>` | 设置检查 damage 计数（默认 20） | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `applications` | 要测试的应用程序名称列表 |

## 使用示例

```bash
# 测试单个应用的窗口启动时间并自动退出
/usr/libexec/dtk6/DGui/bin/dde-kwin-bug -k --format "%p %t %n" qtcreator

# 测试多个应用并指定日志格式
/usr/libexec/dtk6/DGui/bin/dde-kwin-bug -k --format "%t %n" "app1" "app2" "app3"

# 禁用应用输出并监听所有窗口
/usr/libexec/dtk6/DGui/bin/dde-kwin-bug -L -a --format "%t %n" qtcreator

# 禁用缓存并重复测试 5 次
/usr/libexec/dtk6/DGui/bin/dde-kwin-bug -k -no-cache --r 5 --format "%t %n" qtcreator

# 设置检查参数
/usr/libexec/dtk6/DGui/bin/dde-kwin-bug -k --ci 200 --cpt 100 --cvc 20 --cdc 40 --format "%t %n" qtcreator

# 查看帮助信息
/usr/libexec/dtk6/DGui/bin/dde-kwin-bug --help
```
