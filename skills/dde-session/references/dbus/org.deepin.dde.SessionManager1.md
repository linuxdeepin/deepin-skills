# org.deepin.dde.SessionManager1 接口参考

该接口提供会话管理器的电源操作、抑制管理和状态查询能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.SessionManager1` |
| Object path | `/org/deepin/dde/SessionManager1` |
| Interface | `org.deepin.dde.SessionManager1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 电源操作

#### Logout

注销当前会话。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.Logout
```

#### Reboot

重启系统。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.Reboot
```

#### Shutdown

关闭系统。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.Shutdown
```

#### PowerOffChoose

显示电源操作选择界面。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.PowerOffChoose
```

#### ForceLogout

强制注销当前会话。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.ForceLogout
```

#### ForceReboot

强制重启系统。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.ForceReboot
```

#### ForceShutdown

强制关闭系统。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.ForceShutdown
```

#### RequestLogout

请求注销当前会话。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestLogout
```

#### RequestReboot

请求重启系统。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestReboot
```

#### RequestShutdown

请求关闭系统。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestShutdown
```

#### RequestSuspend

请求挂起系统。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestSuspend
```

#### RequestHibernate

请求休眠系统。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestHibernate
```

#### RequestLock

请求锁屏。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestLock
```

#### RequestHibernate

请求休眠。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestHibernate
```


### 能力查询

#### CanLogout

查询是否可以注销。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否可以注销

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.CanLogout
```

#### CanReboot

查询是否可以重启。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否可以重启

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.CanReboot
```

#### CanShutdown

查询是否可以关机。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否可以关机

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.CanShutdown
```

#### CanSuspend

查询是否可以挂起。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否可以挂起

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.CanSuspend
```

#### CanHibernate

查询是否可以休眠。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否可以休眠

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.CanHibernate
```


### 抑制管理

#### Inhibit

添加会话抑制。

- **输入参数**: `appId`（string, 类型 `s`）：应用 ID；`toplevelXid`（uint32, 类型 `u`）：窗口 XID；`reason`（string, 类型 `s`）：抑制原因；`flags`（uint32, 类型 `u`）：抑制标志
- **返回值**: `u`（uint32）：抑制 cookie

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.Inhibit "myapp" 0 "reason" 1
```

#### Uninhibit

移除会话抑制。

- **输入参数**: `inhibitCookie`（uint32, 类型 `u`）：抑制 cookie
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.Uninhibit 1
```

#### IsInhibited

查询是否被抑制。

- **输入参数**: `flags`（uint32, 类型 `u`）：抑制标志
- **返回值**: `b`（bool）：是否被抑制

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.IsInhibited 1
```

#### GetInhibitors

获取所有抑制器。

- **输入参数**: 无
- **返回值**: `ao`（对象路径数组）：抑制器列表

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.GetInhibitors
```


### 其他操作

#### Register

注册应用。

- **输入参数**: `id`（string, 类型 `s`）：应用 ID
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.Register "myapp"
```

#### SetLocked

设置会话锁定状态。

- **输入参数**: `value`（bool, 类型 `b`）：是否锁定
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.SetLocked true
```

#### AllowSessionDaemonRun

允许会话守护进程运行。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否允许

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.AllowSessionDaemonRun
```

#### ToggleDebug

切换调试模式。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.ToggleDebug
```


### 会话管理器属性

#### CurrentSessionPath（属性）

当前会话路径。

| 属性 | 值 |
|------|------|
| 类型 | `o` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SessionManager1 CurrentSessionPath
```
#### CurrentUid（属性）

当前用户 UID。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SessionManager1 CurrentUid
```
#### Locked（属性）

会话是否锁定。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SessionManager1 Locked
```
#### Stage（属性）

会话阶段。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SessionManager1 Stage
```

### 会话管理器信号

#### Unlock

会话解锁时发出。

- **参数**: 无
- **触发条件**: 会话解锁时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1
```

#### InhibitorAdded

抑制器添加时发出。

- **参数**: `path`（object, 类型 `o`）：抑制器路径
- **触发条件**: 添加抑制器时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1
```

#### InhibitorRemoved

抑制器移除时发出。

- **参数**: `path`（object, 类型 `o`）：抑制器路径
- **触发条件**: 移除抑制器时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1
```

