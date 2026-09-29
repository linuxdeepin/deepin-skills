# org.deepin.dde.SessionManager1 接口参考

该接口在 **Session 总线**上注册，提供会话管理器的电源操作、抑制管理和状态查询能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.SessionManager1` |
| Object path | `/org/deepin/dde/SessionManager1` |
| Interface | `org.deepin.dde.SessionManager1` |
| Bus | Session |

### 电源操作

#### RequestLogout

请求注销当前会话。

- **功能**: 注销当前桌面会话，终止当前用户的会话进程并返回登录界面。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 需要通过程序化方式注销当前用户会话时使用，例如脚本自动化注销、第三方应用提供注销按钮。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestLogout
```

#### RequestReboot

请求重启系统。

- **功能**: 请求系统重启，执行重启前的准备工作（如播放关机音效、停止特定服务）后触发系统重启。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 用户或脚本需要通过命令行方式重启系统时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestReboot
```

#### RequestShutdown

请求关闭系统。

- **功能**: 请求关闭系统，执行关机前的准备工作（如播放关机音效、停止特定服务）后触发系统关机。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 用户或脚本需要通过命令行方式关闭系统时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestShutdown
```

#### RequestSuspend

请求挂起系统。

- **功能**: 请求系统进入挂起（待机）状态，降低系统功耗。如果 `/etc/deepin/no_suspend` 文件存在则不执行挂起，仅关闭显示器。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 电源管理按钮、快捷键触发系统挂起/休眠。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestSuspend
```

#### RequestHibernate

请求休眠系统。

- **功能**: 请求系统进入休眠状态，将内存内容写入磁盘后关闭电源。同时设置 DPMS 模式关闭显示器。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 电源管理按钮、快捷键触发系统挂起/休眠。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestHibernate
```

#### RequestLock

请求锁屏。

- **功能**: 请求锁定屏幕。在 Wayland 环境下通过 logind 锁定；在 X11 环境下调用锁屏服务显示锁屏界面。
- **触发条件**: 由调用方主动调用触发；锁定成功后会发出 `LockedChanged` 信号。
- **使用场景**: 外部程序需要触发锁屏时调用，如快捷键锁屏、离开超时自动锁屏。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.RequestLock
```

### 能力查询

#### CanLogout

查询是否可以注销。

- **功能**: 返回当前系统是否允许注销操作。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 在提供注销功能前检查当前是否允许注销，用于控制 UI 中注销按钮的可用状态。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.CanLogout
```

#### CanReboot

查询是否可以重启。

- **功能**: 返回当前系统是否允许重启操作。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 在提供重启功能前检查当前是否允许重启，用于控制 UI 中重启按钮的可用状态。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.CanReboot
```

#### CanShutdown

查询是否可以关机。

- **功能**: 返回当前系统是否允许关机操作。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 在提供关机功能前检查当前是否允许关机，用于控制 UI 中关机按钮的可用状态。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.CanShutdown
```

#### CanSuspend

查询系统是否支持待机。

- **功能**: 返回当前系统是否支持挂起（待机）操作。虚拟机环境或特定配置下可能不支持。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 在提供待机功能前检查当前系统是否支持待机，用于控制 UI 中待机按钮的显示和可用状态。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.CanSuspend
```

#### CanHibernate

查询系统是否支持休眠。

- **功能**: 返回当前系统是否支持休眠操作。虚拟机环境或特定配置下可能不支持。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 在提供休眠功能前检查当前系统是否支持休眠，用于控制 UI 中休眠按钮的显示和可用状态。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.CanHibernate
```

### 抑制管理

#### Inhibit

注册会话抑制器，阻止系统执行指定的会话操作。flags 参数为位掩码，取值：1=阻止注销、2=阻止用户切换、4=阻止挂起/休眠、8=阻止会话闲置。

- **功能**: 创建一个抑制器对象，阻止系统执行由 `flags` 指定的操作。`flags` 支持的取值：`1` 注销、`2` 用户切换、`4` 会话或系统休眠、`8` 会话闲置。多个操作可通过按位或组合（如 `5` = `1|4` 表示同时阻止注销和休眠）。注册成功后返回抑制器 cookie，用于后续移除。
- **触发条件**: 由调用方主动调用触发；注册成功后会发出 `InhibitorAdded` 信号。
- **使用场景**: 应用程序需要阻止系统在执行关键操作期间进入待机、注销或关机状态时使用，例如刻录光盘、执行系统更新、播放视频时阻止屏幕休眠。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.Inhibit "myapp" 0 "reason" 1
```

#### Uninhibit

移除会话抑制。

- **功能**: 根据 cookie 移除之前注册的抑制器，恢复系统对相应操作的正常响应。
- **触发条件**: 由调用方主动调用触发；移除成功后会发出 `InhibitorRemoved` 信号。
- **使用场景**: 应用程序在完成关键操作后移除抑制器，恢复系统的正常电源管理行为。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.Uninhibit 1
```

#### IsInhibited

查询是否被抑制。

- **功能**: 查询指定的 `flags` 对应的操作是否被当前已注册的抑制器阻止。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 在执行电源操作前检查该操作是否被抑制，用于决定是否继续执行或提示用户。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.IsInhibited 1
```

#### GetInhibitors

获取所有抑制器。

- **功能**: 返回当前所有已注册的抑制器对象的 D-Bus 路径列表。返回的每个路径上注册了 `org.deepin.dde.Inhibitor1` 接口，可通过该接口查询抑制器的应用 ID、客户端路径、抑制 flags、抑制原因和顶层窗口 XID。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 需要枚举当前所有活跃的抑制器以展示抑制状态或进行批量管理时使用。获取路径后可通过 [org.deepin.dde.Inhibitor1](org.deepin.dde.Inhibitor1.md) 接口查询各抑制器的详细信息。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.GetInhibitors
```

### 其他操作

#### Register

注册应用，使其参与会话生命周期管理。

- **功能**: 注册应用 ID 到会话管理器，使其参与会话生命周期管理。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 应用程序注册参与会话生命周期管理，以便会话退出时收到通知。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.Register "myapp"
```

#### SetLocked

设置会话锁定状态。

- **功能**: 设置会话的锁定状态。仅允许锁屏进程（`dde-lock`）调用，其他调用方会被拒绝。
- **触发条件**: 由锁屏进程在锁定或解锁时调用触发；设置成功后会发出 `LockedChanged` 信号。
- **使用场景**: 锁屏程序设置会话锁定状态。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.SetLocked true
```

#### AllowSessionDaemonRun

允许会话守护进程运行。

- **功能**: 检查并允许会话守护进程继续运行，当前实现始终返回 `true`。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 查询当前是否允许会话守护进程运行。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.deepin.dde.SessionManager1.AllowSessionDaemonRun
```

#### ToggleDebug

切换调试模式。

- **功能**: 在运行时开启 debug 日志输出，无需重启服务即可获取详细的调试日志。开启后所有 Qt 日志分类的 debug 级别消息都会输出。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 开发调试时切换调试日志模式。

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

- **功能**: 返回当前会话的 D-Bus 对象路径。
- **触发条件**: 会话启动时设置，会话切换时更新。
- **使用场景**: 需要获取当前会话的对象路径以进行后续 D-Bus 操作时使用。

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

- **功能**: 返回当前登录用户的 UID 字符串。
- **触发条件**: 用户登录时设置，用户切换时更新。
- **使用场景**: 需要获取当前会话用户 UID 以进行用户相关操作或权限判断时使用。

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

- **功能**: 返回当前会话是否处于锁定状态。
- **触发条件**: 锁屏进程调用 `SetLocked` 方法时更新。
- **使用场景**: 需要检查当前会话是否被锁定以决定是否显示特定 UI 或执行特定逻辑时使用。

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SessionManager1 Locked
```

### 会话管理器信号

#### LockedChanged

会话锁定状态变化时发出。

- **功能**: 通知会话锁定状态已发生变化，调用方可据此感知锁定或解锁事件。
- **参数**: `locked`（bool, 类型 `b`）：是否锁定
- **触发条件**: 锁屏进程调用 `SetLocked` 方法改变锁定状态时发出。
- **使用场景**: 需要在会话锁定或解锁时执行特定逻辑的应用监听此信号，例如暂停播放、隐藏通知。

```bash
gdbus monitor --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1
```

#### Unlock

会话解锁时发出。

- **功能**: 通知会话已从锁定状态切换到解锁状态。
- **参数**: 无
- **触发条件**: 会话从锁定状态切换到解锁状态时发出。
- **使用场景**: 需要在会话解锁时恢复操作的应用监听此信号，例如恢复播放、显示通知。

```bash
gdbus monitor --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1
```

#### InhibitorAdded

抑制器添加时发出。

- **功能**: 通知有新的抑制器被注册到会话管理器中。
- **参数**: `path`（object, 类型 `o`）：新添加的抑制器对象路径
- **触发条件**: 调用 `Inhibit` 方法成功注册抑制器后发出。
- **使用场景**: 需要实时感知抑制器变化的应用监听此信号，例如在状态栏显示当前抑制状态。

```bash
gdbus monitor --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1
```

#### InhibitorRemoved

抑制器移除时发出。

- **功能**: 通知有抑制器从会话管理器中移除。
- **参数**: `path`（object, 类型 `o`）：被移除的抑制器对象路径
- **触发条件**: 调用 `Uninhibit` 方法成功移除抑制器后发出。
- **使用场景**: 需要实时感知抑制器变化的应用监听此信号，例如在状态栏更新当前抑制状态。

```bash
gdbus monitor --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/SessionManager1
```

### 已废弃接口

以下方法和属性已废弃，不应在新代码中使用，建议使用对应的 `Request*` 方法替代：

| 废弃方法/属性 | 替代方法 | 说明 |
|---------------|----------|------|
| `Logout` | `RequestLogout` | 注销当前会话，废弃后为空实现 |
| `Reboot` | `RequestReboot` | 重启系统，废弃后为空实现 |
| `Shutdown` | `RequestShutdown` | 关闭系统，废弃后为空实现 |
| `PowerOffChoose` | 无直接替代 | 显示电源操作选择界面，废弃后为空实现 |
| `Stage`（属性） | 无直接替代 | 会话阶段，已废弃，不再使用 |
