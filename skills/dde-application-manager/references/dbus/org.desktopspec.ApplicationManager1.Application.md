# org.desktopspec.ApplicationManager1.Application 接口参考

该接口提供单个应用的启动、桌面操作和属性查询能力。动态对象路径由 ApplicationManager1.List 返回。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationManager1` |
| Object path | `<dynamic>` |
| Interface | `org.desktopspec.ApplicationManager1.Application` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 应用操作

#### Launch

启动应用。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.desktopspec.ApplicationManager1.Application.Launch
```

#### SendToDesktop

发送到桌面。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.desktopspec.ApplicationManager1.Application.SendToDesktop
```

#### RemoveFromDesktop

从桌面移除。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.desktopspec.ApplicationManager1.Application.RemoveFromDesktop
```


### 应用属性

#### ID（属性）

应用 ID。

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

应用名称。

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
  org.desktopspec.ApplicationManager1.Application Name
```
#### DisplayName（属性）

应用显示名称。

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
  org.desktopspec.ApplicationManager1.Application DisplayName
```
#### GenericName（属性）

应用通用名称。

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
  org.desktopspec.ApplicationManager1.Application GenericName
```
#### Categories（属性）

应用分类。

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

应用图标。

| 属性 | 值 |
|------|------|
| 类型 | `a{sv}` |
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

应用动作列表。

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

当前动作名称。

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
  org.desktopspec.ApplicationManager1.Application ActionName
```
设置示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Set \
  org.desktopspec.ApplicationManager1.Application ActionName "<action_name>"
```
#### Execs（属性）

应用执行命令。

| 属性 | 值 |
|------|------|
| 类型 | `a{sv}` |
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
