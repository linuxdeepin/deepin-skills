# org.deepin.dde.ShutdownFront1 接口参考

该接口提供关机界面显示和电源操作能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ShutdownFront1` |
| Object path | `/org/deepin/dde/ShutdownFront1` |
| Interface | `org.deepin.dde.ShutdownFront1` |
| Bus | Session |

## 兼容接口

在早期 Qt5 版本（v20）中，该接口使用旧版服务名 `com.deepin.dde.shutdownFront`（对象路径 `/com/deepin/dde/shutdownFront`）。当前 Qt6 版本已切换至 `org.deepin.dde.ShutdownFront1`，旧版服务名不再注册，仅供历史应用参考。

## 方法

### Show

显示关机界面。

- **功能**: 激活并显示关机界面，展示关机、重启、注销、锁屏、切换用户、挂起、休眠操作选项。
- **触发条件**: 由系统快捷键、会话管理或 DBus 调用方在需要显示关机界面时调用。
- **使用场景**: 用户按下电源键或通过系统菜单选择关机时触发。

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Show
```

### Shutdown

关闭系统。

- **功能**: 执行系统关机操作。若当前无法显示关机界面（如界面已锁定），则直接发出 `RequireShutdown(false)` 信号表示跳过界面直接关机；否则显示关机界面并发出 `RequireShutdown(true)` 信号。
- **触发条件**: 用户在关机界面选择关机时调用，或由系统在无法显示界面时直接调用执行关机。
- **使用场景**: 用户确认关机操作后触发关机流程。消费方收到 `RequireShutdown` 信号后，根据参数值决定是否需要显示关机确认界面。

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Shutdown
```

### Restart

重启系统。

- **功能**: 执行系统重启操作。若当前无法显示关机界面，则直接发出 `RequireRestart(false)` 信号表示跳过界面直接重启；否则显示关机界面并发出 `RequireRestart(true)` 信号。
- **触发条件**: 用户在关机界面选择重启时调用，或由系统在无法显示界面时直接调用执行重启。
- **使用场景**: 用户确认重启操作后触发重启流程。消费方收到 `RequireRestart` 信号后，根据参数值决定是否需要显示重启确认界面。

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Restart
```

### Logout

注销当前会话。

- **功能**: 注销当前登录用户的会话，返回登录界面。
- **触发条件**: 用户在关机界面选择注销时调用。
- **使用场景**: 用户需要退出当前会话但不关机时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Logout
```

### Suspend

挂起系统。

- **功能**: 执行系统挂起（待机）操作。若当前无法显示关机界面，则设置电源动作为待机；否则显示关机界面，检查 `SleepLock` 配置后发出 `RequireSuspend(true)` 信号。
- **触发条件**: 用户在关机界面选择挂起时调用。
- **使用场景**: 用户需要将系统进入待机状态以节省功耗时使用。消费方收到 `RequireSuspend` 信号后执行挂起操作。

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Suspend
```

### Hibernate

休眠系统。

- **功能**: 执行系统休眠（写入磁盘）操作。若当前无法显示关机界面，则设置电源动作为休眠；否则显示关机界面，检查 `SleepLock` 配置后发出 `RequireHibernate(true)` 信号。
- **触发条件**: 用户在关机界面选择休眠时调用。
- **使用场景**: 用户需要将系统状态保存到磁盘后关机，下次开机恢复状态时使用。消费方收到 `RequireHibernate` 信号后执行休眠操作。

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Hibernate
```

### SwitchUser

切换用户。

- **功能**: 切换到另一个用户账户，不注销当前用户会话。
- **触发条件**: 用户在关机界面选择切换用户时调用。
- **使用场景**: 多用户环境下，用户需要切换到另一个账户而不退出当前会话时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.SwitchUser
```

### Lock

锁屏。

- **功能**: 锁定当前屏幕，显示锁屏界面。
- **触发条件**: 用户在关机界面选择锁屏时调用。
- **使用场景**: 用户需要临时锁定屏幕以保护隐私时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.Lock
```

### UpdateAndShutdown

更新并关机。

- **功能**: 设置更新电源模式为「更新并关机」（`UPM_UpdateAndShutdown`），将当前模式切换为关机模式并显示关机界面。该 DBus 方法本身不直接触发系统更新，实际的更新流程在用户确认后由 `updateworker` 调用 lastore 服务的 `PrepareFullScreenUpgrade(true)` 方法启动全屏更新，更新完成后系统自动关机。
- **触发条件**: 系统检测到有待安装的系统更新包时，由系统更新服务或关机界面调用此方法进入「更新并关机」模式。
- **使用场景**: 系统有更新包待安装时，用户选择在关机前执行系统更新。该接口设置更新模式并显示关机界面，用户确认后触发全屏更新流程，更新完成后系统自动关机。

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.UpdateAndShutdown
```

### UpdateAndReboot

更新并重启。

- **功能**: 设置更新电源模式为「更新并重启」（`UPM_UpdateAndReboot`），将当前模式切换为重启模式并显示关机界面。该 DBus 方法本身不直接触发系统更新，实际的更新流程在用户确认后由 `updateworker` 调用 lastore 服务的 `PrepareFullScreenUpgrade(false)` 方法启动全屏更新，更新完成后系统自动重启。
- **触发条件**: 系统检测到有待安装的系统更新包时，由系统更新服务或关机界面调用此方法进入「更新并重启」模式。
- **使用场景**: 系统有更新包待安装时，用户选择在重启前执行系统更新。该接口设置更新模式并显示关机界面，用户确认后触发全屏更新流程，更新完成后系统自动重启。

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.deepin.dde.ShutdownFront1.UpdateAndReboot
```

## 属性

### Visible

关机界面是否可见。

- **功能**: 表示当前关机界面是否处于可见状态。
- **类型**: `b`
- **触发条件**: 关机界面被显示或隐藏时，该属性的值随之改变。
- **读写权限**: read
- **使用场景**: 外部程序需要判断当前关机界面是否处于显示状态时读取此属性。

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.ShutdownFront1 Visible
```

## 信号

### ChangKey

按键变化信号。

- **功能**: 通知订阅者关机界面接收到按键事件，并传递按键名称。
- **参数**: `key`（string, 类型 `s`）：按键名称
- **触发条件**: 关机界面接收到键盘按键事件时发出。关机界面独占键盘输入，按键事件通过此信号转发给 DBus 订阅者。
- **使用场景**: 外部程序（如 deepin-daemon）订阅此信号，在关机界面独占键盘期间接收按键事件并执行对应操作，例如处理特殊功能键。接收方应根据按键名称判断并执行相应行为。

```bash
gdbus monitor --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1
```

### Visible

可见性变化信号。

- **功能**: 通知订阅者关机界面的可见状态发生变化，并传递当前是否可见。
- **参数**: `visible`（bool, 类型 `b`）：是否可见
- **触发条件**: 关机界面显示或隐藏时发出。
- **使用场景**: 订阅方（如通知服务、多媒体播放器）应根据可见状态调整自身行为：关机界面显示时暂停媒体播放、隐藏通知弹窗，关机界面隐藏时恢复正常行为。

```bash
gdbus monitor --session \
  --dest org.deepin.dde.ShutdownFront1 \
  --object-path /org/deepin/dde/ShutdownFront1
```
