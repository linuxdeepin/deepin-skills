# dde-am 命令参考

DDE 应用管理器客户端命令行工具，用于启动应用、执行命令、列出已安装应用。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-application-manager` |
| 安装路径 | `/usr/bin/dde-am` |
| DDE 角色 | 用户和开发者均可使用的应用管理命令行工具；也被包括 dde-launchpad 在内的组件内部调用 |

## 用途

DDE 应用管理器客户端命令行工具，用于启动应用、执行命令、列出已安装应用。它是 DDE 应用管理框架的前端 CLI 接口，与 dde-application-manager 守护进程通信来管理应用的生命周期。支持通过应用 ID 或 .desktop 文件路径启动应用，也支持直接执行命令行程序。可以设置环境变量、指定工作目录和标记启动来源。典型使用场景包括：从命令行启动应用、在脚本中批量启动应用、调试应用启动流程、查看系统中已安装的应用列表。

## 用法

```
dde-am [options] <appId>              # 通过 ID 或路径启动应用
dde-am -c <program> [args...]         # 直接执行命令
dde-am --list                         # 列出所有已安装应用 ID
```

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `--list` | 列出所有已安装应用 ID | 否 |
| `--by-user` | 标记为用户启动 | 否 |
| `--autostart` | 系统自启动启动（隐藏选项） | 否 |
| `-a, --action <action>` | 指定触发的 action 标识 | 是 |
| `-e, --env <env>` | 设置环境变量，格式 `NAME=VALUE`（可多次使用） | 是 |
| `-c, --command <program>` | 直接执行命令/程序 | 是 |
| `--type <type>` | 执行类型（`shortcut`/`script`/`portablebinary`），默认 `portablebinary`，仅与 `--command` 搭配 | 是 |
| `--run-id <runId>` | 自定义 Run ID，仅与 `--command` 搭配 | 是 |
| `--workdir <dir>` | 工作目录，仅与 `--command` 搭配 | 是 |
| `--launch-type <type>` | 启动来源标识，用于事件上报（如 `dde-launchpad`、`dde-shell`） | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `appId` | 应用 ID、.desktop 文件路径或 URI；使用 `--command` 时作为命令参数（以 `-` 开头的参数前需加 `--`） |

## 使用示例

```bash
# 列出所有已安装应用 ID
# > 注意：此命令需要 D-Bus session 连接，无 D-Bus session 时会报 "Not connected to D-Bus server"。
dde-am --list

# 通过应用 ID 启动应用
dde-am org.deepin.editor

# 通过 .desktop 文件路径启动应用
dde-am /usr/share/applications/deepin-editor.desktop

# 指定 action 启动应用（如打开新窗口）
dde-am -a new-window org.deepin.editor

# 标记为用户启动
dde-am --by-user org.deepin.editor

# 直接执行命令（如执行 ls -la）
dde-am -c ls -- -la

# 执行命令并设置环境变量
dde-am -c my-program -e MY_VAR=hello -e ANOTHER_VAR=world

# 执行命令并指定工作目录
dde-am -c my-program --workdir /tmp

# 执行命令并指定执行类型为 script
dde-am -c /opt/my-script.sh --type script

# 执行命令并指定自定义 Run ID
dde-am -c my-program --run-id my-run-001

# 指定启动来源标识（用于事件统计）
dde-am --launch-type dde-launchpad org.deepin.editor

# 系统自启动场景启动应用（隐藏选项）
dde-am --autostart org.deepin.dde.dock
```

> 注意：`dde-am` 需要与 dde-application-manager 守护进程通过 D-Bus 通信，无 D-Bus session 时会报 "Not connected to D-Bus server"。
