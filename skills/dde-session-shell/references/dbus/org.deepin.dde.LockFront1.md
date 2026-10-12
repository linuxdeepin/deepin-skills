# org.deepin.dde.LockFront1 接口参考

该接口提供锁屏界面显示、用户列表显示、认证状态控制和电源操作能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.LockFront1` |
| Object path | `/org/deepin/dde/LockFront1` |
| Interface | `org.deepin.dde.LockFront1` |
| Bus | Session |

## 方法

### Show

显示锁屏界面。

- **功能**: 激活并显示锁屏界面，覆盖当前桌面。
- **触发条件**: 由系统会话管理、快捷键或 DBus 调用方在需要锁定屏幕时调用。
- **使用场景**: 用户离开桌面、系统空闲超时或安全策略要求锁定时，由会话管理器自动调用。

```bash
gdbus call --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1 \
  --method org.deepin.dde.LockFront1.Show
```

### ShowUserList

显示用户列表。

- **功能**: 在锁屏界面上显示系统用户列表，供用户选择登录。
- **触发条件**: 由锁屏界面在需要展示用户切换选项时调用。
- **使用场景**: 多用户环境下，用户需要切换登录账户时。

```bash
gdbus call --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1 \
  --method org.deepin.dde.LockFront1.ShowUserList
```

### ShowAuth

显示认证界面。

- **功能**: 先调用 `Show()` 显示锁屏界面，再根据 `active` 参数控制是否创建认证会话并切换到密码输入模式。
- **输入参数**: `active`（bool, 类型 `b`）：是否激活认证。`true` 表示创建认证会话并切换到密码输入模式，允许用户输入密码进行解锁；`false` 表示不创建认证会话，认证界面不切换到密码输入模式。
- **触发条件**: 由锁屏界面在用户选择账户后需要进入密码输入模式时调用。
- **使用场景**: 用户在锁屏界面选择账户后，锁屏界面调用此方法激活认证，显示密码输入框供用户输入密码进行解锁认证。

```bash
gdbus call --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1 \
  --method org.deepin.dde.LockFront1.ShowAuth true
```

### Suspend

挂起系统。

- **功能**: 触发系统挂起（待机）或从挂起中恢复，在挂起前确保锁屏界面已显示。
- **输入参数**: `enable`（bool, 类型 `b`）：`true` 表示进入挂起，设置黑屏模式并显示锁屏界面；`false` 表示从挂起中恢复，此时检查 `SleepLock` 属性：若为 `true` 则显示锁屏界面要求输入密码，若为 `false` 则隐藏锁屏界面。
- **触发条件**: 由电源管理服务在系统挂起或从挂起恢复时调用。
- **使用场景**: 系统进入待机时电源管理传入 `true` 确保锁屏界面显示；系统从待机恢复时电源管理传入 `false`，根据 `SleepLock` 配置决定是否需要解锁。

```bash
gdbus call --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1 \
  --method org.deepin.dde.LockFront1.Suspend true
```

### Hibernate

休眠系统。

- **功能**: 触发系统休眠（写入磁盘）或从休眠中恢复，始终显示锁屏界面。与 `Suspend` 不同，`Hibernate` 不检查 `SleepLock` 属性，无论 `enable` 为 `true` 还是 `false` 都会设置休眠模式并显示锁屏界面。
- **输入参数**: `enable`（bool, 类型 `b`）：`true` 表示进入休眠，设置休眠模式并显示锁屏界面；`false` 表示从休眠中恢复，同样设置休眠模式为 `false` 并显示锁屏界面（要求输入密码解锁）。
- **触发条件**: 由电源管理服务在系统休眠或从休眠恢复时调用。
- **使用场景**: 系统进入休眠时电源管理传入 `true` 确保锁屏界面显示；系统从休眠恢复时电源管理传入 `false`，锁屏界面始终显示要求输入密码解锁，不受 `SleepLock` 配置影响。

```bash
gdbus call --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1 \
  --method org.deepin.dde.LockFront1.Hibernate true
```

## 属性

### Visible

锁屏界面是否可见。

- **功能**: 表示当前锁屏界面是否处于可见状态。
- **类型**: `b`
- **触发条件**: 锁屏界面被显示或隐藏时，该属性的值随之改变。
- **读写权限**: read
- **使用场景**: 外部程序需要判断当前是否处于锁屏状态时读取此属性。

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.LockFront1 Visible
```

## 信号

### ChangKey

按键变化信号。

- **功能**: 通知订阅者锁屏界面接收到按键事件，并传递按键名称。
- **参数**: `key`（string, 类型 `s`）：按键名称
- **触发条件**: 锁屏界面接收到键盘按键事件时发出。锁屏界面独占键盘输入，按键事件通过此信号转发给 DBus 订阅者。
- **使用场景**: 外部程序（如 deepin-daemon）订阅此信号，在锁屏界面独占键盘期间接收按键事件并执行对应操作，例如处理 F1 待机键一类的特殊功能键。接收方应根据按键名称判断并执行相应行为。

```bash
gdbus monitor --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1
```

### Visible

可见性变化信号。

- **功能**: 通知订阅者锁屏界面的可见状态发生变化，并传递当前是否可见。
- **参数**: `visible`（bool, 类型 `b`）：是否可见
- **触发条件**: 锁屏界面显示或隐藏时发出。
- **使用场景**: 订阅方（如通知服务、多媒体播放器）应根据可见状态调整自身行为：锁屏界面显示时暂停媒体播放、隐藏通知弹窗，锁屏界面隐藏时恢复正常行为。

```bash
gdbus monitor --session \
  --dest org.deepin.dde.LockFront1 \
  --object-path /org/deepin/dde/LockFront1
```
