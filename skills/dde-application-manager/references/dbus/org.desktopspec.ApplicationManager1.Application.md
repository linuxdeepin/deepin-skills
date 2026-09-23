# org.desktopspec.ApplicationManager1.Application 接口参考

该接口提供单个应用的启动、桌面操作和属性查询能力。动态对象路径由 ApplicationManager1.List 属性返回。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationManager1` |
| Object path | `<dynamic>` |
| Interface | `org.desktopspec.ApplicationManager1.Application` |
| Bus | Session |

### 应用操作

#### Launch

启动应用。

- **输入参数**: `action`（string, 类型 `s`）：动作标识，空字符串表示默认启动；`fields`（string 数组, 类型 `as`）：文件路径或 URI 列表；`options`（字典, 类型 `a{sv}`）：额外选项（如 `uid`、`env`、`path` 等）
- **返回值**: `job`（object path, 类型 `o`）：任务对象路径

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.desktopspec.ApplicationManager1.Application.Launch \
  "" "[]" "{}"
```

#### SendToDesktop

发送应用快捷方式到桌面。

- **输入参数**: 无
- **返回值**: `success`（bool, 类型 `b`）：是否成功

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.desktopspec.ApplicationManager1.Application.SendToDesktop
```

#### RemoveFromDesktop

从桌面移除应用快捷方式。

- **输入参数**: 无
- **返回值**: `success`（bool, 类型 `b`）：是否成功

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.desktopspec.ApplicationManager1.Application.RemoveFromDesktop
```

### 属性

#### ID

应用桌面文件 ID。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application ID
```

#### Name

应用名称（多语言映射）。

| 属性 | 值 |
|------|------|
| 类型 | `a{ss}` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Name
```

#### GenericName

应用通用名称（多语言映射）。

| 属性 | 值 |
|------|------|
| 类型 | `a{ss}` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application GenericName
```

#### Icons

应用图标映射。

| 属性 | 值 |
|------|------|
| 类型 | `a{ss}` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Icons
```

#### Categories

应用分类列表。

| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Categories
```

#### Actions

应用动作标识列表。

| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Actions
```

#### ActionName

动作名称映射（动作标识到多语言名称）。

| 属性 | 值 |
|------|------|
| 类型 | `a{sa{ss}}` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application ActionName
```

#### Execs

应用执行命令映射。

| 属性 | 值 |
|------|------|
| 类型 | `a{ss}` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Execs
```

#### Terminal

是否在终端中运行。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Terminal
```

#### MimeTypes

应用关联的 MIME 类型列表。

| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application MimeTypes
```

设置示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Set \
  org.desktopspec.ApplicationManager1.Application MimeTypes <["text/plain"]>
```

#### AutoStart

是否自动启动。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application AutoStart
```

设置示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Set \
  org.desktopspec.ApplicationManager1.Application AutoStart <true>
```

#### Instances

应用所有实例的对象路径列表。

| 属性 | 值 |
|------|------|
| 类型 | `ao` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Instances
```

#### NoDisplay

是否在应用列表中隐藏。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application NoDisplay
```

#### Environ

应用实例的环境变量。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application Environ
```

设置示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Set \
  org.desktopspec.ApplicationManager1.Application Environ "<string>"
```

#### LaunchedTimes

应用累计启动次数，-1 表示出错。

| 属性 | 值 |
|------|------|
| 类型 | `x` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application LaunchedTimes
```

#### isOnDesktop

应用是否已发送到桌面。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/org_deepin_editor \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Application isOnDesktop
```

---
