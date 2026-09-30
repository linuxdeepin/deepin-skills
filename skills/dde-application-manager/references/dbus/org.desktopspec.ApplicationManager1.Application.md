# org.desktopspec.ApplicationManager1.Application 接口参考

该接口提供单个应用的启动、桌面操作和属性查询能力。每个已安装应用在 D-Bus 上注册一个动态对象路径，可通过 `ApplicationManager1` 接口的 `List` 属性获取所有应用的对象路径列表。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationManager1` |
| Object path | `<dynamic>` |
| Interface | `org.desktopspec.ApplicationManager1.Application` |
| Bus | Session |

### 应用操作

#### Launch

启动该应用。根据指定的动作标识和文件列表启动应用，支持通过 options 传递启动选项，包括用户切换（uid）、环境变量设置（env）、取消环境变量（unsetEnv）、工作目录（path）和启动来源标识（_launch_type）。

- **输入参数**:
  - `action`（string, 类型 `s`）：动作标识符，对应桌面文件中 `[Desktop Action xxx]` 的 `xxx`，空字符串表示默认动作
  - `fields`（数组, 类型 `as`）：传递给应用的文件路径或 URI 列表
  - `options`（字典, 类型 `a{sv}`）：启动选项，支持的键包括：
    - `uid`（uint）：以指定用户 ID 运行，可能需要 polkit 认证
    - `env`（数组 `as`）：传递环境变量，如 `['LANG=en_US', 'PATH=xxx:yyy']`
    - `unsetEnv`（数组 `as`）：取消设置的环境变量名列表
    - `path`（string）：设置工作目录（绝对路径）
    - `_launch_type`（string）：内部使用，启动来源标识用于事件上报（如 `dde-launchpad`、`dde-shell`），默认 `unknown`
- **返回值**: `o`（object path）：任务对象路径，可用于跟踪启动进度

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.desktopspec.ApplicationManager1.Application.Launch \
  "" "[]" "{}"
```

#### SendToDesktop

将该应用的快捷方式发送到桌面。将应用的 .desktop 文件复制到用户的桌面目录。

- **输入参数**: 无
- **返回值**: `b`（boolean）：是否成功

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.desktopspec.ApplicationManager1.Application.SendToDesktop
```

#### RemoveFromDesktop

从桌面移除该应用的快捷方式。删除用户桌面目录中该应用的 .desktop 文件。

- **输入参数**: 无
- **返回值**: `b`（boolean）：是否成功

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.desktopspec.ApplicationManager1.Application.RemoveFromDesktop
```

### 应用属性

#### ID（属性）

应用 ID（桌面文件 ID）。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application ID
```

#### Name（属性）

应用名称。键为语言代码，值为对应语言的名称。

| 属性 | 值 |
|------|------|
| 类型 | `a{ss}` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Name
```

#### GenericName（属性）

应用通用名称。键为语言代码，值为对应语言的名称。

| 属性 | 值 |
|------|------|
| 类型 | `a{ss}` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application GenericName
```

#### Categories（属性）

应用分类列表。

| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Categories
```

#### Icons（属性）

应用图标。键为动作标识符，值为图标内容。

| 属性 | 值 |
|------|------|
| 类型 | `a{ss}` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Icons
```

#### Actions（属性）

应用动作标识符列表。

| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Actions
```

#### ActionName（属性）

动作名称映射。键为动作标识符，值为语言-名称映射。

| 属性 | 值 |
|------|------|
| 类型 | `a{sa{ss}}` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application ActionName
```

#### Execs（属性）

应用执行命令。键为动作标识符，值为对应的执行命令内容。

| 属性 | 值 |
|------|------|
| 类型 | `a{ss}` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Execs
```

#### Terminal（属性）

是否在终端中运行。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Terminal
```

#### NoDisplay（属性）

是否在应用列表中隐藏该应用。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application NoDisplay
```

#### MimeTypes（属性）

该应用支持的 MIME 类型列表。

| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application MimeTypes
```

#### AutoStart（属性）

是否开机自启动。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application AutoStart
```

#### isOnDesktop（属性）

该应用的快捷方式是否已发送到桌面。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application isOnDesktop
```

#### Environ（属性）

应用实例的环境变量设置。格式为 `LANG=en_US;PATH=xxx:yyy;`，在 Launch 时传递给应用。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Environ
```

#### Instances（属性）

该应用所有运行中实例的对象路径列表。

| 属性 | 值 |
|------|------|
| 类型 | `ao` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Instances
```

#### LastLaunchedTime（属性）

最后一次启动时间（Unix 时间戳，毫秒）。值为 -1 表示发生错误。

| 属性 | 值 |
|------|------|
| 类型 | `x` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application LastLaunchedTime
```

#### LaunchedTimes（属性）

累计启动次数。值为 -1 表示发生错误。

| 属性 | 值 |
|------|------|
| 类型 | `x` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application LaunchedTimes
```

#### InstalledTime（属性）

应用安装时间（Unix 时间戳，毫秒）。值为 -1 表示发生错误。

| 属性 | 值 |
|------|------|
| 类型 | `x` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application InstalledTime
```

#### StartupWMClass（属性）

应用的 StartupWMClass 值，用于窗口管理器匹配应用窗口。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application StartupWMClass
```

#### DesktopSourcePath（属性）

桌面文件的源路径。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application DesktopSourcePath
```

#### X_Deepin_Vendor（属性）

Deepin 厂商标识。当值为 `deepin` 时，应用显示名称应使用 GenericName。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application X_Deepin_Vendor
```

#### X_Deepin_CreateBy（属性）

Deepin 创建者标识。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application X_Deepin_CreateBy
```

#### X_CreatedBy（属性）

应用创建者标识。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application X_CreatedBy
```

#### X_linglong（属性）

是否为玲珑包应用。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application X_linglong
```

#### X_Flatpak（属性）

是否为 Flatpak 应用。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application X_Flatpak
```
