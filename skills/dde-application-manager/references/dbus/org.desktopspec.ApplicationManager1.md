# org.desktopspec.ApplicationManager1 接口参考

该接口提供应用列表查询、应用识别、用户应用增删和命令执行能力。这是应用管理器的核心入口接口，通过 Session 总线暴露应用管理功能。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationManager1` |
| Object path | `/org/desktopspec/ApplicationManager1` |
| Interface | `org.desktopspec.ApplicationManager1` |
| Bus | Session |

### 应用管理操作

#### ReloadApplications

重新加载应用列表，更新桌面文件缓存。当桌面文件发生变化（如安装或卸载应用）后调用此方法刷新应用管理器的内部缓存。仅支持 `$XDG_DATA_DIRS` 中的目录路径。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.desktopspec.ApplicationManager1.ReloadApplications
```

#### Identify

通过进程文件描述符（pidfd）识别应用。给定一个 pidfd，返回该进程对应的应用 ID、应用实例对象路径和实例属性信息。调用方需先通过 `pidfd_open(2)` 系统调用获取 pidfd。

- **输入参数**: `pidfd`（handle, 类型 `h`）：进程文件描述符
- **返回值**: `(s, o, a{sa{sv}})`（元组）：应用 ID、实例对象路径、实例属性映射

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.desktopspec.ApplicationManager1.Identify 0
```

> **注意**：上述 `gdbus call` 示例无法直接执行。`Identify` 方法需要 pidfd（`h` 类型），而 `gdbus call` 命令行不支持传递文件描述符（`h` 类型）参数，传入整数 `0` 无法作为 pidfd 生效。命令行场景推荐使用 `app-identifier` 工具调用该方法（已在本 skill 的 CLI 参考中说明）。

#### addUserApplication

添加用户应用。根据桌面文件内容和应用名称注册一个新的用户应用。

- **输入参数**:
  - `desktop_file`（字典, 类型 `a{sv}`）：桌面文件内容，遵循 [Desktop Entry Spec](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html)
  - `name`（string, 类型 `s`）：应用名称
- **返回值**: `s`（string）：应用 ID

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.desktopspec.ApplicationManager1.addUserApplication \
  "{}" "myapp"
```

#### deleteUserApplication

删除用户应用。根据应用 ID 删除已注册的用户应用。

- **输入参数**: `app_id`（string, 类型 `s`）：应用 ID
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.desktopspec.ApplicationManager1.deleteUserApplication "myapp"
```

#### executeCommand

执行非系统应用命令。创建一个 systemd 服务来运行指定命令，并进行正确的 cgroup 管理。systemd unit 名称格式为 `app-DDE-tmp.{type}.{runId}@{random}.service`。

- **输入参数**:
  - `program`（string, 类型 `s`）：可执行文件的完整路径
  - `arguments`（数组, 类型 `as`）：命令行参数列表
  - `type`（string, 类型 `s`）：执行类型，取值为 `shortcut`、`script`、`portablebinary`
  - `runId`（string, 类型 `s`）：用于标识的自定义 Run ID（可选，默认为转义后的程序路径）
  - `envVars`（字典, 类型 `a{ss}`）：自定义环境变量
  - `workdir`（string, 类型 `s`）：工作目录
- **返回值**: `o`（object path）：实例对象路径（当前为空，保留供未来使用）

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.desktopspec.ApplicationManager1.executeCommand \
  "/usr/bin/ls" "[]" "portablebinary" "" "{}" "/tmp"
```

### 应用列表属性

#### List（属性）

所有已安装应用的对象路径列表。

| 属性 | 值 |
|------|------|
| 类型 | `ao` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1 List
```
