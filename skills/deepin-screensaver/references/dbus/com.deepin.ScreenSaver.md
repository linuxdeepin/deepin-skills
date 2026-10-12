# com.deepin.ScreenSaver 接口参考

该接口在 **Session 总线**上注册，对象路径为 `/com/deepin/ScreenSaver`，提供屏幕保护程序的启动、停止、预览、配置管理和屏保列表查询能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `com.deepin.ScreenSaver` |
| Object path | `/com/deepin/ScreenSaver` |
| Interface | `com.deepin.ScreenSaver` |
| Bus | Session |

### 屏保启动与停止

#### Start

启动屏保。

- **功能**: 启动屏幕保护程序。
- **触发条件**: 用户手动调用，或空闲超时后由系统自动触发。
- **使用场景**: 需要立即启动屏幕保护时使用。
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.Start
```

#### Stop

停止屏保。

- **功能**: 停止正在运行的屏幕保护程序。
- **触发条件**: 用户手动调用，或检测到用户输入活动时触发。
- **使用场景**: 需要停止正在运行的屏幕保护时使用。
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.Stop
```

### 预览与配置

#### Preview

预览指定屏保。

- **功能**: 以预览模式启动指定屏保，用于展示屏保效果。
- **触发条件**: 用户在屏保设置界面选择预览某个屏保时调用。
- **使用场景**: 在屏保配置界面预览屏保效果时使用。
- **输入参数**: `name`（string, 类型 `s`）：屏保名称；`staysOn`（int32, 类型 `i`）：是否保持显示（0 = 底层显示，1 = 顶层显示）
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.Preview "deepin-custom-screensaver" 1
```

#### GetScreenSaverCover

获取指定屏保的封面图片路径。

- **功能**: 返回指定屏保的封面缩略图路径。
- **触发条件**: 渲染屏保配置界面的屏保列表时调用。
- **使用场景**: 在屏保列表中展示每个屏保的封面缩略图时使用。
- **输入参数**: `name`（string, 类型 `s`）：屏保名称
- **返回值**: `s`（string）：封面图片路径

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.GetScreenSaverCover "deepin-custom-screensaver"
```

#### StartCustomConfig

启动指定屏保的自定义配置。

- **功能**: 打开指定屏保的自定义配置对话框。
- **触发条件**: 用户点击屏保配置界面的配置按钮时调用。
- **使用场景**: 需要配置特定屏保的自定义参数时使用。
- **输入参数**: `name`（string, 类型 `s`）：屏保名称
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.StartCustomConfig "deepin-custom-screensaver"
```

#### ConfigurableItems

获取可配置的屏保项列表。

- **功能**: 返回所有支持自定义配置的屏保名称列表。
- **触发条件**: 初始化屏保配置界面时调用。
- **使用场景**: 加载屏保配置界面前获取可配置的屏保列表时使用。
- **输入参数**: 无
- **返回值**: `as`（string 数组）：可配置屏保名称列表

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.ConfigurableItems
```

#### IsConfigurable

查询指定屏保是否可配置。

- **功能**: 判断指定屏保是否支持自定义配置。
- **触发条件**: 渲染屏保配置界面、判断是否显示配置按钮时调用。
- **使用场景**: 判断某个屏保是否支持自定义配置时使用。
- **输入参数**: `name`（string, 类型 `s`）：屏保名称
- **返回值**: `b`（bool）：是否可配置

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.IsConfigurable "deepin-custom-screensaver"
```

#### RefreshScreenSaverList

刷新屏保列表。

- **功能**: 重新扫描并更新屏保列表。
- **触发条件**: 屏保应用安装或卸载后调用。
- **使用场景**: 安装或卸载屏保应用后需要更新屏保列表时使用。
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.RefreshScreenSaverList
```

### 屏保属性

#### isRunning（属性）

屏保是否正在运行。

- **功能**: 标识屏幕保护程序当前是否处于运行状态。
- **触发条件**: 屏保启动时变为 `true`，停止时变为 `false`。
- **使用场景**: 判断当前屏保运行状态时使用。
- **信号关联**（已废弃/不推荐使用）: 屏保启动（调用 `Start` 或 `Preview` 方法）或停止（调用 `Stop` 方法）时触发 `isRunningChanged` 信号。该信号未在 D-Bus 内省 XML 中声明，属性变化通过 `org.freedesktop.DBus.Properties.PropertiesChanged` 信号通知。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver isRunning
```

#### currentScreenSaver（属性）

当前使用的屏保名称。

- **功能**: 获取或设置当前正在使用的屏保名称。
- **触发条件**: 用户切换屏保时属性值更新。
- **使用场景**: 获取或设置当前使用的屏保时使用。
- **信号关联**（已废弃/不推荐使用）: 设置该属性后会触发 `currentScreenSaverChanged` 信号。该信号未在 D-Bus 内省 XML 中声明，属性变化通过 `org.freedesktop.DBus.Properties.PropertiesChanged` 信号通知。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver currentScreenSaver
```

设置示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.ScreenSaver currentScreenSaver "<string>"
```

#### allScreenSaver（属性）

所有可用屏保列表。

- **功能**: 返回系统中所有已安装的屏保名称列表。
- **触发条件**: 安装或卸载屏保应用后属性值更新。
- **使用场景**: 获取系统中所有可用屏保列表时使用。
- **信号关联**（已废弃/不推荐使用）: 调用 `RefreshScreenSaverList` 方法刷新屏保列表后触发 `allScreenSaverChanged` 信号。该信号未在 D-Bus 内省 XML 中声明，属性变化通过 `org.freedesktop.DBus.Properties.PropertiesChanged` 信号通知。

| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver allScreenSaver
```

#### batteryScreenSaverTimeout（属性）

电池模式下屏保超时时间。

- **功能**: 获取或设置电池供电时屏保启动的空闲超时时间（单位：秒）。
- **触发条件**: 用户在电源设置中修改时更新。
- **使用场景**: 获取或设置电池模式下的屏保启动延迟时间时使用。
- **信号关联**（已废弃/不推荐使用）: 设置该属性后会触发 `batteryScreenSaverTimeoutChanged` 信号。该信号未在 D-Bus 内省 XML 中声明，属性变化通过 `org.freedesktop.DBus.Properties.PropertiesChanged` 信号通知。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver batteryScreenSaverTimeout
```

设置示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.ScreenSaver batteryScreenSaverTimeout "<int32 60>"
```

#### linePowerScreenSaverTimeout（属性）

交流电源模式下屏保超时时间。

- **功能**: 获取或设置交流电源供电时屏保启动的空闲超时时间（单位：秒）。
- **触发条件**: 用户在电源设置中修改时更新。
- **使用场景**: 获取或设置交流电源模式下的屏保启动延迟时间时使用。
- **信号关联**（已废弃/不推荐使用）: 设置该属性后会触发 `linePowerScreenSaverTimeoutChanged` 信号。该信号未在 D-Bus 内省 XML 中声明，属性变化通过 `org.freedesktop.DBus.Properties.PropertiesChanged` 信号通知。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver linePowerScreenSaverTimeout
```

设置示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.ScreenSaver linePowerScreenSaverTimeout "<int32 300>"
```

#### lockScreenAtAwake（属性）

唤醒时是否锁定屏幕。

- **功能**: 控制从屏保唤醒后是否自动锁定屏幕。
- **触发条件**: 用户在锁屏设置中修改时更新。
- **使用场景**: 控制从屏保唤醒后是否自动锁定屏幕时使用。
- **信号关联**（已废弃/不推荐使用）: 设置该属性后会触发 `lockScreenAtAwakeChanged` 信号。该信号未在 D-Bus 内省 XML 中声明，属性变化通过 `org.freedesktop.DBus.Properties.PropertiesChanged` 信号通知。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver lockScreenAtAwake
```

设置示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.ScreenSaver lockScreenAtAwake "<true>"
```

#### lockScreenDelay（属性）

锁定屏幕延迟时间。

- **功能**: 从屏幕保护启动开始到一定时间段内唤醒不锁定屏幕，超过该时间段后唤醒才锁定屏幕（单位：秒）。
- **触发条件**: 用户在锁屏设置中修改时更新。
- **使用场景**: 控制屏保启动后到锁定屏幕的延迟时间时使用。
- **信号关联**（已废弃/不推荐使用）: 设置该属性后会触发 `lockScreenDelayChanged` 信号。该信号未在 D-Bus 内省 XML 中声明，属性变化通过 `org.freedesktop.DBus.Properties.PropertiesChanged` 信号通知。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver lockScreenDelay
```

设置示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.ScreenSaver lockScreenDelay "<int32 5>"
```

## 信号

> **注意**：以下信号均为已废弃/不推荐使用的信号。这些信号未在 D-Bus 内省 XML（`com.deepin.ScreenSaver.xml`）中声明，但在 C++ 源码中仍通过 `Q_PROPERTY ... NOTIFY` 定义并发射。属性变化实际通过标准 `org.freedesktop.DBus.Properties.PropertiesChanged` 信号通知，建议监听该标准信号而非以下废弃信号。

### allScreenSaverChanged(QStringList)

> 已废弃/不推荐使用

屏保列表发生变化时触发。

- **功能**: 通知屏保列表已发生变化。
- **触发条件**: 调用 `RefreshScreenSaverList` 方法重新扫描屏保模块目录并更新屏保列表后触发，参数为更新后的屏保名称列表。
- **使用场景**: 监听屏保列表变化以更新屏保选择界面时使用。
- **关联属性**: `allScreenSaver`（只读）

### batteryScreenSaverTimeoutChanged(int)

> 已废弃/不推荐使用

电池模式下屏保超时时间发生变化时触发。

- **功能**: 通知电池模式下屏保超时时间已发生变化。
- **触发条件**: 当电源管理服务（`com.deepin.daemon.Power` 或 `org.deepin.dde.Power1`）的 `BatteryScreensaverDelay` 属性发生变化时触发，参数为新的超时时间值。
- **使用场景**: 需要在电池模式下同步显示或响应屏保超时时间变化时使用。
- **关联属性**: `batteryScreenSaverTimeout`（读写）

### linePowerScreenSaverTimeoutChanged(int)

> 已废弃/不推荐使用

交流电源模式下屏保超时时间发生变化时触发。

- **功能**: 通知交流电源模式下屏保超时时间已发生变化。
- **触发条件**: 当电源管理服务（`com.deepin.daemon.Power` 或 `org.deepin.dde.Power1`）的 `LinePowerScreensaverDelay` 属性发生变化时触发，参数为新的超时时间值。
- **使用场景**: 需要在交流电源模式下同步显示或响应屏保超时时间变化时使用。
- **关联属性**: `linePowerScreenSaverTimeout`（读写）

### currentScreenSaverChanged(QString)

> 已废弃/不推荐使用

当前使用的屏保发生变化时触发。

- **功能**: 通知当前使用的屏保已切换。
- **触发条件**: 调用 `setCurrentScreenSaver` 设置当前屏保名称且值实际发生变化时触发，参数为新的屏保名称。
- **使用场景**: 监听当前屏保切换以更新界面显示或执行相关逻辑时使用。
- **关联属性**: `currentScreenSaver`（读写）

### isRunningChanged(bool)

> 已废弃/不推荐使用

屏保运行状态发生变化时触发。

- **功能**: 通知屏保运行状态的变化。
- **触发条件**: 屏保启动（调用 `Start` 或 `Preview` 方法）时以 `true` 触发，屏保停止（调用 `Stop` 方法）时以 `false` 触发。
- **使用场景**: 需要根据屏保启停状态执行相应操作（如暂停媒体播放）时使用。
- **关联属性**: `isRunning`（只读）

### lockScreenAtAwakeChanged(bool)

> 已废弃/不推荐使用

唤醒时是否锁定屏幕的设置发生变化时触发。

- **功能**: 通知唤醒时是否锁定屏幕的设置已发生变化。
- **触发条件**: 调用 `setLockScreenAtAwake` 设置该属性且值实际发生变化时触发，参数为新的布尔值。
- **使用场景**: 监听唤醒锁定设置变化以同步界面显示时使用。
- **关联属性**: `lockScreenAtAwake`（读写）

### lockScreenDelayChanged(int)

> 已废弃/不推荐使用

锁定屏幕延迟时间发生变化时触发。

- **功能**: 通知锁定屏幕的延迟时间已发生变化。
- **触发条件**: 调用 `setLockScreenDelay` 设置该属性且值实际发生变化时触发，参数为新的延迟时间值（单位：秒）。
- **使用场景**: 监听锁定延迟时间变化以同步界面显示时使用。
- **关联属性**: `lockScreenDelay`（读写）

## 接口关系

deepin-screensaver 仅注册一个 D-Bus 服务 `com.deepin.ScreenSaver`（对象路径 `/com/deepin/ScreenSaver`），无旧版别名或废弃接口。

系统中另存在 `org.freedesktop.ScreenSaver` 标准 FreeDesktop 屏保接口，由 `treeland-screensaver` 提供（对象路径 `/org/freedesktop/ScreenSaver`），提供 `Inhibit` 和 `UnInhibit` 标准屏保抑制功能。该接口属于 `treeland-screensaver` 组件，与 deepin-screensaver 的 `com.deepin.ScreenSaver` 是独立的不同实现，非兼容别名。
