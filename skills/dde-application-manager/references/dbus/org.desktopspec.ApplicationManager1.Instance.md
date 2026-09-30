# org.desktopspec.ApplicationManager1.Instance 接口参考

该接口提供单个应用实例的管理能力。每个运行中的应用实例在 D-Bus 上注册一个动态对象路径，可通过 `ApplicationManager1.Application` 接口的 `Instances` 属性获取某应用所有实例的对象路径列表。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationManager1` |
| Object path | `<dynamic>` |
| Interface | `org.desktopspec.ApplicationManager1.Instance` |
| Bus | Session |

### 实例操作

#### KillAll

强制终止该实例。向该实例下所有进程发送指定信号。注意：该实例启动的所有子进程都会被终止。

- **输入参数**: `signal`（int, 类型 `i`）：要发送的信号编号（如 `9` 表示 SIGKILL，`15` 表示 SIGTERM）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.desktopspec.ApplicationManager1.Instance.KillAll 15
```

### 实例属性

#### Application（属性）

该实例所属应用的对象路径。该对象实现 `org.desktopspec.ApplicationManager1.Application` 接口。如果应用已被卸载，此路径为 `/`。

| 属性 | 值 |
|------|------|
| 类型 | `o` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Instance Application
```

#### SystemdUnitPath（属性）

该实例在 systemd 用户守护进程中的 unit 对象路径。其他桌面组件可通过此路径使用 systemd 提供的 cgroup 接口。如果该实例不受 systemd 管理，此属性为空。

| 属性 | 值 |
|------|------|
| 类型 | `o` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1.Instance SystemdUnitPath
```

#### Launcher（属性）

启动该实例的启动器标识，表示哪个组件启动了此实例。

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
  org.desktopspec.ApplicationManager1.Instance Launcher
```

#### LaunchType（属性）

该实例的启动来源名称，如 `dde-launchpad`、`dde-shell`、`autostart`。未指定时默认为 `unknown`。

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
  org.desktopspec.ApplicationManager1.Instance LaunchType
```

#### Orphaned（属性）

该实例所属的应用是否已被移除（应用被卸载后实例仍在运行时为 true）。

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
  org.desktopspec.ApplicationManager1.Instance Orphaned
```
