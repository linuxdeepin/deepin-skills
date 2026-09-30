# org.deepin.dde.Power1 接口参考

该接口提供电源管理能力，包括电源状态查询、延时配置和电源操作。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Power1` |
| Object path | `/org/deepin/dde/Power1` |
| Interface | `org.deepin.dde.Power1` |
| Bus | Session |

### 电源操作

#### Reset

重置电源配置为默认值。

- **功能**：将所有电源管理配置恢复为系统默认值
- **触发条件**：用户在控制中心点击「恢复默认」电源设置时调用
- **输入参数**：无
- **返回值**：无
- **使用场景**：用户在控制中心点击「恢复默认」电源设置时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.Reset
```

#### SetPrepareSuspend

设置挂起准备状态。

- **功能**：通知电源管理服务系统即将进入挂起状态，以便服务执行挂起前的准备工作
- **触发条件**：系统在执行挂起操作前由电源管理模块调用
- **输入参数**：`state`（int32, 类型 `i`）：挂起准备状态，取值如下：1 = PS_Unknown（未知）、2 = PS_LidOpen（翻盖打开）、3 = PS_LidClose（翻盖关闭）、4 = PS_Finish（完成）、5 = PS_Resume（恢复）、6 = PS_Prepare（准备）、7 = PS_ButtonClick（按下电源键）
- **返回值**：无
- **使用场景**：系统在执行挂起操作前由电源管理模块调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.SetPrepareSuspend 1
```

#### TurnOffScreen

关闭屏幕。

- **功能**：立即关闭屏幕显示，屏幕进入黑屏状态
- **触发条件**：用户手动触发息屏操作，或系统根据电源策略自动关闭屏幕时调用
- **输入参数**：无
- **返回值**：无
- **使用场景**：电源管理模块根据延时配置自动息屏，或用户通过快捷键手动息屏时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.TurnOffScreen
```

#### TurnOnScreen

打开屏幕。

- **功能**：唤醒屏幕显示，从黑屏状态恢复显示
- **触发条件**：用户移动鼠标、按下键盘或打开翻盖时触发屏幕唤醒
- **输入参数**：无
- **返回值**：无
- **使用场景**：用户从息屏状态唤醒设备时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.TurnOnScreen
```

### 电源状态属性

#### OnBattery（属性）

是否使用电池供电。

- **功能**：指示当前设备是否处于电池供电状态（未接入交流电源）
- **触发条件**：电源接入状态发生变化时更新
- **使用场景**：UI 根据供电状态显示不同的电源配置选项

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 OnBattery
```

#### UseWayland（属性）

是否使用 Wayland。

- **功能**：指示当前会话是否使用 Wayland 显示协议
- **触发条件**：会话启动时确定，运行期间保持不变
- **使用场景**：电源管理模块根据显示协议类型选择不同的电源行为

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 UseWayland
```

#### LidIsPresent（属性）

是否存在翻盖。

- **功能**：指示当前设备是否具备翻盖（笔记本电脑盖子）硬件
- **触发条件**：硬件探测完成时确定，设备未变更时保持不变
- **使用场景**：UI 根据设备类型决定是否显示翻盖关闭动作设置项

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LidIsPresent
```

#### BatteryIsPresent（属性）

电池是否存在。

- **功能**：以映射形式返回各电池槽位的存在状态
- **触发条件**：电池热插拔时更新
- **使用场景**：UI 判断设备是否有电池以决定是否显示电池相关设置

| 属性 | 值 |
|------|------|
| 类型 | `map` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryIsPresent
```

#### BatteryPercentage（属性）

电池百分比。

- **功能**：以映射形式返回各电池的剩余电量百分比
- **触发条件**：电池电量变化时更新
- **使用场景**：UI 显示电池电量百分比

| 属性 | 值 |
|------|------|
| 类型 | `map` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryPercentage
```

#### BatteryState（属性）

电池状态。

- **功能**：以映射形式返回各电池的当前状态（充电、放电、已充满）
- **触发条件**：电池充放电状态变化时更新
- **使用场景**：UI 显示电池充电状态图标和提示信息

| 属性 | 值 |
|------|------|
| 类型 | `map` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryState
```

#### HasAmbientLightSensor（属性）

是否有环境光传感器。

- **功能**：指示当前设备是否具备环境光传感器硬件
- **触发条件**：硬件探测完成时确定，设备未变更时保持不变
- **使用场景**：UI 根据设备是否支持自动亮度来显示或隐藏相关设置项

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 HasAmbientLightSensor
```

#### WarnLevel（属性）

电量警告级别。

- **功能**：返回当前电池电量的警告级别，用于触发低电量通知或自动休眠
- **触发条件**：电池电量变化达到警告级别阈值时更新
- **使用场景**：系统根据警告级别执行低电量通知或自动休眠操作

| 属性 | 值 |
|------|------|
| 类型 | `u` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 WarnLevel
```

#### IsHighPerformanceSupported（属性）

是否支持高性能模式。

- **功能**：指示当前设备是否支持高性能电源模式
- **触发条件**：硬件探测完成时确定，设备未变更时保持不变
- **使用场景**：UI 根据设备是否支持高性能模式来显示或隐藏该模式选项

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 IsHighPerformanceSupported
```

### 交流电源延时配置

#### LinePowerScreensaverDelay（属性）

交流电源屏保延时。

- **功能**：设置交流电源下激活屏保的空闲等待时间（秒）
- **触发条件**：用户在控制中心修改插电时屏保延时设置时更新
- **使用场景**：用户在控制中心设置交流电源下的屏保延时时间

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerScreensaverDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerScreensaverDelay <int32 600>
```

#### LinePowerScreenBlackDelay（属性）

交流电源息屏延时。

- **功能**：设置交流电源下关闭屏幕的空闲等待时间（秒）
- **触发条件**：用户在控制中心修改插电时息屏延时设置时更新
- **使用场景**：用户在控制中心设置交流电源下的息屏延时时间

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerScreenBlackDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerScreenBlackDelay <int32 600>
```

#### LinePowerSleepDelay（属性）

交流电源休眠延时。

- **功能**：设置交流电源下进入休眠的空闲等待时间（秒）
- **触发条件**：用户在控制中心修改插电时休眠延时设置时更新
- **使用场景**：用户在控制中心设置交流电源下的休眠延时时间

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerSleepDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerSleepDelay <int32 900>
```

#### LinePowerLockDelay（属性）

交流电源锁屏延时。

- **功能**：设置交流电源下自动锁屏的空闲等待时间（秒）
- **触发条件**：用户在控制中心修改插电时锁屏延时设置时更新
- **使用场景**：用户在控制中心设置交流电源下的锁屏延时时间

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerLockDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerLockDelay <int32 180>
```

#### LinePowerShortIdleDelay（属性）

交流电源短空闲延时。

- **功能**：设置交流电源下进入短空闲状态的空闲等待时间（秒），用于触发低功耗降频
- **触发条件**：用户在控制中心修改插电时短 idle 延时设置时更新
- **使用场景**：系统电源管理模块根据此值在短空闲时执行降频操作

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerShortIdleDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerShortIdleDelay <int32 300>
```

### 电池延时配置

#### BatteryScreensaverDelay（属性）

电池屏保延时。

- **功能**：设置电池供电下激活屏保的空闲等待时间（秒）
- **触发条件**：用户在控制中心修改电池时屏保延时设置时更新
- **使用场景**：用户在控制中心设置电池供电下的屏保延时时间

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryScreensaverDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatteryScreensaverDelay <int32 120>
```

#### BatteryScreenBlackDelay（属性）

电池息屏延时。

- **功能**：设置电池供电下关闭屏幕的空闲等待时间（秒）
- **触发条件**：用户在控制中心修改电池时息屏延时设置时更新
- **使用场景**：用户在控制中心设置电池供电下的息屏延时时间

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryScreenBlackDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatteryScreenBlackDelay <int32 120>
```

#### BatterySleepDelay（属性）

电池休眠延时。

- **功能**：设置电池供电下进入休眠的空闲等待时间（秒）
- **触发条件**：用户在控制中心修改电池时休眠延时设置时更新
- **使用场景**：用户在控制中心设置电池供电下的休眠延时时间

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatterySleepDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatterySleepDelay <int32 300>
```

#### BatteryLockDelay（属性）

电池锁屏延时。

- **功能**：设置电池供电下自动锁屏的空闲等待时间（秒）
- **触发条件**：用户在控制中心修改电池时锁屏延时设置时更新
- **使用场景**：用户在控制中心设置电池供电下的锁屏延时时间

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryLockDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatteryLockDelay <int32 60>
```

#### BatteryShortIdleDelay（属性）

电池短空闲延时。

- **功能**：设置电池供电下进入短空闲状态的空闲等待时间（秒），用于触发低功耗降频
- **触发条件**：用户在控制中心修改电池时短 idle 延时设置时更新
- **使用场景**：系统电源管理模块根据此值在短空闲时执行降频操作

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryShortIdleDelay
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatteryShortIdleDelay <int32 60>
```

### 锁屏与动作配置

#### ScreenBlackLock（属性）

息屏时是否锁定。

- **功能**：设置息屏时是否同时锁定屏幕
- **触发条件**：用户在控制中心修改息屏前锁定设置时更新
- **使用场景**：用户在控制中心设置息屏时是否自动锁屏

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 ScreenBlackLock
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 ScreenBlackLock <true>
```

#### SleepLock（属性）

休眠时是否锁定。

- **功能**：设置系统从休眠唤醒时是否需要锁定屏幕
- **触发条件**：用户在控制中心修改休眠前锁定设置时更新
- **使用场景**：用户在控制中心设置休眠唤醒后是否自动锁屏

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 SleepLock
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 SleepLock <true>
```

#### LinePowerLidClosedAction（属性）

交流电源翻盖关闭动作。

- **功能**：设置交流电源下合上翻盖时执行的动作（如无操作、息屏、休眠）
- **触发条件**：用户在控制中心修改插电时合盖动作设置时更新
- **使用场景**：用户在控制中心设置交流电源下合上翻盖时的系统行为

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerLidClosedAction
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerLidClosedAction <int32 0>
```

#### BatteryLidClosedAction（属性）

电池翻盖关闭动作。

- **功能**：设置电池供电下合上翻盖时执行的动作（如无操作、息屏、休眠）
- **触发条件**：用户在控制中心修改电池时合盖动作设置时更新
- **使用场景**：用户在控制中心设置电池供电下合上翻盖时的系统行为

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryLidClosedAction
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatteryLidClosedAction <int32 0>
```

#### LinePowerPressPowerBtnAction（属性）

交流电源按下电源键动作。

- **功能**：设置交流电源下按下电源键时执行的动作（如无操作、息屏、休眠、关机）
- **触发条件**：用户在控制中心修改插电时电源键动作设置时更新
- **使用场景**：用户在控制中心设置交流电源下按下电源键时的系统行为

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LinePowerPressPowerBtnAction
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LinePowerPressPowerBtnAction <int32 0>
```

#### BatteryPressPowerBtnAction（属性）

电池按下电源键动作。

- **功能**：设置电池供电下按下电源键时执行的动作（如无操作、息屏、休眠、关机）
- **触发条件**：用户在控制中心修改电池时电源键动作设置时更新
- **使用场景**：用户在控制中心设置电池供电下按下电源键时的系统行为

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryPressPowerBtnAction
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 BatteryPressPowerBtnAction <int32 0>
```


#### LowPowerAction（属性）

低电量时系统动作。

- **功能**：设置电池电量达到动作阈值时系统执行的动作（0=挂起、1=休眠）
- **触发条件**：用户在控制中心修改低电量系统动作设置时更新
- **使用场景**：用户在控制中心设置低电量时系统自动挂起或休眠

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LowPowerAction
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LowPowerAction <int32 1>
```

#### ScheduledShutdownState（属性）

定时关机开关。

- **功能**：开启或关闭定时关机功能
- **触发条件**：用户在控制中心开启或关闭定时关机时更新
- **使用场景**：用户在控制中心设置是否启用定时关机功能

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 ScheduledShutdownState
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 ScheduledShutdownState <true>
```

#### ShutdownTime（属性）

定时关机时间。

- **功能**：设置定时关机的触发时间，格式为 HH:MM
- **触发条件**：用户在控制中心修改定时关机时间时更新
- **使用场景**：用户在控制中心设置每天或指定日期的关机时间

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 ShutdownTime
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 ShutdownTime "19:00"
```

#### ShutdownRepetition（属性）

定时关机重复类型。

- **功能**：设置定时关机的重复类型：0=每天、1=工作日、2=周末、3=自定义
- **触发条件**：用户在控制中心修改定时关机重复类型时更新
- **使用场景**：用户在控制中心选择定时关机的重复周期

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 ShutdownRepetition
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 ShutdownRepetition <int32 1>
```

#### CustomShutdownWeekDays（属性）

自定义关机重复日期。

- **功能**：设置自定义定时关机的星期几，以字节数组形式存储星期几（1-7）
- **触发条件**：用户在控制中心修改自定义关机日期时更新
- **使用场景**：当 ShutdownRepetition 设为自定义类型时，用户选择每周哪几天执行定时关机

| 属性 | 值 |
|------|------|
| 类型 | `ay` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 CustomShutdownWeekDays
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 CustomShutdownWeekDays [b'1', b'3', b'5']
```

### 低电量配置

#### LowPowerNotifyEnable（属性）

低电量通知是否启用。

- **功能**：设置是否在电池电量低于阈值时发送低电量通知
- **触发条件**：用户在控制中心开启或关闭低电量通知时更新
- **使用场景**：用户在控制中心开启或关闭低电量通知功能

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LowPowerNotifyEnable
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LowPowerNotifyEnable <true>
```

#### LowPowerNotifyThreshold（属性）

低电量通知阈值。

- **功能**：设置触发低电量通知的电池电量百分比阈值
- **触发条件**：用户在控制中心修改低电量通知阈值时更新
- **使用场景**：用户在控制中心设置低电量通知触发的电量百分比

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LowPowerNotifyThreshold
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LowPowerNotifyThreshold <int32 20>
```

#### LowPowerAutoSleepThreshold（属性）

低电量自动休眠阈值。

- **功能**：设置触发自动休眠的电池电量百分比阈值
- **触发条件**：用户在控制中心修改低电量自动休眠阈值时更新
- **使用场景**：用户在控制中心设置自动休眠触发的电量百分比

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LowPowerAutoSleepThreshold
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 LowPowerAutoSleepThreshold <int32 5>
```

### 电源信号

#### onBatteryChanged

供电状态变化时发出。

- **功能**：通知订阅者设备的供电状态（电池供电或交流电源）发生了变化
- **触发条件**：设备接入或断开交流电源时发出
- **使用场景**：UI 根据供电状态切换不同的电源配置面板时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### lidIsPresentChanged

翻盖存在状态变化时发出。

- **功能**：通知订阅者设备是否具备翻盖硬件的状态发生了变化
- **触发条件**：设备硬件变更导致翻盖存在状态变化时发出
- **使用场景**：UI 根据设备是否具备翻盖决定是否显示合盖动作设置项时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryIsPresentChanged

电池存在状态变化时发出。

- **功能**：通知订阅者电池槽位的存在状态发生了变化
- **触发条件**：电池热插拔导致电池存在状态变化时发出
- **使用场景**：UI 判断设备是否有电池以决定是否显示电池相关设置时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryPercentageChanged

电池百分比变化时发出。

- **功能**：通知订阅者电池剩余电量百分比发生了变化
- **触发条件**：电池电量增减导致百分比变化时发出
- **使用场景**：UI 实时显示电池电量百分比时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryStateChanged

电池状态变化时发出。

- **功能**：通知订阅者电池的充放电状态发生了变化（充电、放电、已充满）
- **触发条件**：电池开始充电或停止充电或完全充满时发出
- **使用场景**：UI 显示电池充电状态图标和提示信息时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryTimeToEmptyChanged

预计剩余使用时间变化时发出。

- **功能**：通知订阅者电池预计剩余使用时间发生了变化
- **触发条件**：电池放电速率变化导致预计剩余使用时间更新时发出
- **使用场景**：UI 显示电池剩余使用时间时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### hasAmbientLightSensorChanged

环境光传感器存在状态变化时发出。

- **功能**：通知订阅者设备是否具备环境光传感器的状态发生了变化
- **触发条件**：环境光传感器硬件接入或断开时发出
- **使用场景**：UI 根据设备是否支持自动亮度来显示或隐藏相关设置项时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### warnLevelChanged

警告级别变化时发出。

- **功能**：通知订阅者电池低电量警告级别发生了变化
- **触发条件**：电池电量或剩余时间跨越警告级别阈值时发出
- **使用场景**：UI 根据警告级别显示不同级别的低电量提醒时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### isHighPerformanceSupportedChanged

高性能模式支持状态变化时发出。

- **功能**：通知订阅者设备是否支持高性能模式的状态发生了变化
- **触发条件**：设备硬件能力变更导致高性能模式支持状态变化时发出
- **使用场景**：UI 根据是否支持高性能模式决定是否显示高性能模式选项时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### linePowerScreensaverDelayChanged

插电时屏保延时变化时发出。

- **功能**：通知订阅者插电时屏保延时配置发生了变化
- **触发条件**：用户在控制中心修改插电时屏保延时时发出
- **使用场景**：UI 实时同步屏保延时配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### linePowerScreenBlackDelayChanged

插电时息屏延时变化时发出。

- **功能**：通知订阅者插电时息屏延时配置发生了变化
- **触发条件**：用户在控制中心修改插电时息屏延时时发出
- **使用场景**：UI 实时同步息屏延时配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### linePowerSleepDelayChanged

插电时休眠延时变化时发出。

- **功能**：通知订阅者插电时休眠延时配置发生了变化
- **触发条件**：用户在控制中心修改插电时休眠延时时发出
- **使用场景**：UI 实时同步休眠延时配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### linePowerShortIdleDelayChanged

插电时短 idle 延时变化时发出。

- **功能**：通知订阅者插电时短 idle 延时配置发生了变化
- **触发条件**：用户在控制中心修改插电时短 idle 延时时发出
- **使用场景**：UI 实时同步短 idle 延时配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### linePowerLockDelayChanged

插电时锁屏延时变化时发出。

- **功能**：通知订阅者插电时锁屏延时配置发生了变化
- **触发条件**：用户在控制中心修改插电时锁屏延时时发出
- **使用场景**：UI 实时同步锁屏延时配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryScreensaverDelayChanged

电池时屏保延时变化时发出。

- **功能**：通知订阅者电池时屏保延时配置发生了变化
- **触发条件**：用户在控制中心修改电池时屏保延时时发出
- **使用场景**：UI 实时同步屏保延时配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryScreenBlackDelayChanged

电池时息屏延时变化时发出。

- **功能**：通知订阅者电池时息屏延时配置发生了变化
- **触发条件**：用户在控制中心修改电池时息屏延时时发出
- **使用场景**：UI 实时同步息屏延时配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batterySleepDelayChanged

电池时休眠延时变化时发出。

- **功能**：通知订阅者电池时休眠延时配置发生了变化
- **触发条件**：用户在控制中心修改电池时休眠延时时发出
- **使用场景**：UI 实时同步休眠延时配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryShortIdleDelayChanged

电池时短 idle 延时变化时发出。

- **功能**：通知订阅者电池时短 idle 延时配置发生了变化
- **触发条件**：用户在控制中心修改电池时短 idle 延时时发出
- **使用场景**：UI 实时同步短 idle 延时配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryLockDelayChanged

电池时锁屏延时变化时发出。

- **功能**：通知订阅者电池时锁屏延时配置发生了变化
- **触发条件**：用户在控制中心修改电池时锁屏延时时发出
- **使用场景**：UI 实时同步锁屏延时配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### screenBlackLockChanged

息屏前锁定配置变化时发出。

- **功能**：通知订阅者息屏前是否锁定会话的配置发生了变化
- **触发条件**：用户在控制中心修改息屏前锁定设置时发出
- **使用场景**：UI 实时同步息屏前锁定配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### sleepLockChanged

休眠前锁定配置变化时发出。

- **功能**：通知订阅者休眠前是否锁定会话的配置发生了变化
- **触发条件**：用户在控制中心修改休眠前锁定设置时发出
- **使用场景**：UI 实时同步休眠前锁定配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### linePowerLidClosedActionChanged

插电时合盖动作变化时发出。

- **功能**：通知订阅者插电时合盖执行动作的配置发生了变化
- **触发条件**：用户在控制中心修改插电时合盖动作设置时发出
- **使用场景**：UI 实时同步合盖动作配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryLidClosedActionChanged

电池时合盖动作变化时发出。

- **功能**：通知订阅者电池时合盖执行动作的配置发生了变化
- **触发条件**：用户在控制中心修改电池时合盖动作设置时发出
- **使用场景**：UI 实时同步合盖动作配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### linePowerPressPowerBtnActionChanged

插电时电源键动作变化时发出。

- **功能**：通知订阅者插电时按下电源键执行动作的配置发生了变化
- **触发条件**：用户在控制中心修改插电时电源键动作设置时发出
- **使用场景**：UI 实时同步电源键动作配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryPressPowerBtnActionChanged

电池时电源键动作变化时发出。

- **功能**：通知订阅者电池时按下电源键执行动作的配置发生了变化
- **触发条件**：用户在控制中心修改电池时电源键动作设置时发出
- **使用场景**：UI 实时同步电源键动作配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### lowPowerNotifyEnableChanged

低电量通知开关变化时发出。

- **功能**：通知订阅者低电量通知功能的启用状态发生了变化
- **触发条件**：用户在控制中心开启或关闭低电量通知时发出
- **使用场景**：UI 实时同步低电量通知开关变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### lowPowerNotifyThresholdChanged

低电量通知阈值变化时发出。

- **功能**：通知订阅者低电量通知的电池电量百分比阈值发生了变化
- **触发条件**：用户在控制中心修改低电量通知阈值时发出
- **使用场景**：UI 实时同步低电量通知阈值变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### lowPowerAutoSleepThresholdChanged

低电量自动休眠阈值变化时发出。

- **功能**：通知订阅者低电量自动休眠的电池电量百分比阈值发生了变化
- **触发条件**：用户在控制中心修改低电量自动休眠阈值时发出
- **使用场景**：UI 实时同步低电量自动休眠阈值变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### lowPowerActionChanged

低电量系统动作变化时发出。

- **功能**：通知订阅者低电量时系统执行的动作（挂起或休眠）发生了变化
- **触发条件**：用户在控制中心修改低电量系统动作设置时发出
- **使用场景**：UI 实时同步低电量系统动作配置变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### scheduledShutdownStateChanged

定时关机开关变化时发出。

- **功能**：通知订阅者定时关机功能的开关状态发生了变化
- **触发条件**：用户在控制中心开启或关闭定时关机时发出
- **使用场景**：UI 实时同步定时关机开关变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### shutdownTimeChanged

定时关机时间变化时发出。

- **功能**：通知订阅者定时关机的触发时间发生了变化
- **触发条件**：用户在控制中心修改定时关机时间时发出
- **使用场景**：UI 实时同步定时关机时间变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### shutdownRepetitionChanged

定时关机重复类型变化时发出。

- **功能**：通知订阅者定时关机的重复类型发生了变化
- **触发条件**：用户在控制中心修改定时关机重复类型时发出
- **使用场景**：UI 实时同步定时关机重复类型变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### customShutdownWeekDaysChanged

自定义关机日期变化时发出。

- **功能**：通知订阅者自定义定时关机的星期几配置发生了变化
- **触发条件**：用户在控制中心修改自定义关机日期时发出
- **使用场景**：UI 实时同步自定义关机日期变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```


---

## 低电量告警配置接口（org.deepin.dde.Power1.WarnLevelConfig）

该接口为 `org.deepin.dde.Power1` 对象上的附加适配器接口，提供低电量告警策略配置能力，包括基于时间或百分比的告警阈值设置。

### 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Power1` |
| Object path | `/org/deepin/dde/Power1` |
| Interface | `org.deepin.dde.Power1.WarnLevelConfig` |
| Bus | Session |

### 方法

#### Reset

重置低电量告警配置为默认值。

- **功能**：将所有低电量告警配置恢复为系统默认值
- **触发条件**：用户在控制中心点击「恢复默认」电源设置时调用
- **输入参数**：无
- **返回值**：无
- **使用场景**：用户在控制中心重置电源设置时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.WarnLevelConfig.Reset
```

### 属性

#### UsePercentageForPolicy（属性）

是否使用百分比策略。

- **功能**：指示低电量告警是否基于电池百分比而非剩余时间触发
- **触发条件**：用户在控制中心切换告警策略模式时更新
- **使用场景**：系统根据该值决定使用百分比还是时间来判定告警级别

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.WarnLevelConfig UsePercentageForPolicy
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1.WarnLevelConfig UsePercentageForPolicy <true>
```

#### LowTime（属性）

低电量告警时间阈值。

- **功能**：设置剩余时间低于该值（秒）时进入低电量告警级别
- **触发条件**：用户在控制中心修改低电量时间阈值时更新
- **使用场景**：基于时间的告警策略下，判定是否进入低电量告警

| 属性 | 值 |
|------|------|
| 类型 | `x` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.WarnLevelConfig LowTime
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1.WarnLevelConfig LowTime <int64 1200>
```

#### DangerTime（属性）

危险电量告警时间阈值。

- **功能**：设置剩余时间低于该值（秒）时进入危险电量告警级别
- **触发条件**：用户在控制中心修改危险电量时间阈值时更新
- **使用场景**：基于时间的告警策略下，判定是否进入危险电量告警

| 属性 | 值 |
|------|------|
| 类型 | `x` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.WarnLevelConfig DangerTime
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1.WarnLevelConfig DangerTime <int64 600>
```

#### CriticalTime（属性）

临界电量告警时间阈值。

- **功能**：设置剩余时间低于该值（秒）时进入临界电量告警级别
- **触发条件**：用户在控制中心修改临界电量时间阈值时更新
- **使用场景**：基于时间的告警策略下，判定是否进入临界电量告警

| 属性 | 值 |
|------|------|
| 类型 | `x` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.WarnLevelConfig CriticalTime
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1.WarnLevelConfig CriticalTime <int64 300>
```

#### ActionTime（属性）

执行动作时间阈值。

- **功能**：设置剩余时间低于该值（秒）时执行低电量动作（如自动休眠）
- **触发条件**：用户在控制中心修改动作执行时间阈值时更新
- **使用场景**：基于时间的告警策略下，判定是否触发低电量动作

| 属性 | 值 |
|------|------|
| 类型 | `x` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.WarnLevelConfig ActionTime
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1.WarnLevelConfig ActionTime <int64 120>
```

#### LowPowerNotifyThreshold（属性）

低电量通知百分比阈值。

- **功能**：设置电池百分比低于该值时发送低电量通知
- **触发条件**：用户在控制中心修改低电量通知阈值时更新
- **使用场景**：基于百分比的告警策略下，判定是否发送低电量通知

| 属性 | 值 |
|------|------|
| 类型 | `x` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.WarnLevelConfig LowPowerNotifyThreshold
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1.WarnLevelConfig LowPowerNotifyThreshold <int64 20>
```

#### ActionPercentage（属性）

执行动作百分比阈值。

- **功能**：设置电池百分比低于该值时执行低电量动作（如自动休眠）
- **触发条件**：用户在控制中心修改动作执行百分比阈值时更新
- **使用场景**：基于百分比的告警策略下，判定是否触发低电量动作

| 属性 | 值 |
|------|------|
| 类型 | `x` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.WarnLevelConfig ActionPercentage
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1.WarnLevelConfig ActionPercentage <int64 5>
```

### 信号

#### usePercentageForPolicyChanged

告警策略模式变化时发出。

- **功能**：通知订阅者告警策略模式（百分比/时间）发生了变化
- **触发条件**：用户切换告警策略模式时发出
- **使用场景**：UI 实时同步告警策略模式变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### lowTimeChanged

低电量时间阈值变化时发出。

- **功能**：通知订阅者低电量时间阈值发生了变化
- **触发条件**：用户修改低电量时间阈值时发出
- **使用场景**：UI 实时同步低电量时间阈值变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### dangerTimeChanged

危险电量时间阈值变化时发出。

- **功能**：通知订阅者危险电量时间阈值发生了变化
- **触发条件**：用户修改危险电量时间阈值时发出
- **使用场景**：UI 实时同步危险电量时间阈值变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### criticalTimeChanged

临界电量时间阈值变化时发出。

- **功能**：通知订阅者临界电量时间阈值发生了变化
- **触发条件**：用户修改临界电量时间阈值时发出
- **使用场景**：UI 实时同步临界电量时间阈值变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### actionTimeChanged

动作执行时间阈值变化时发出。

- **功能**：通知订阅者动作执行时间阈值发生了变化
- **触发条件**：用户修改动作执行时间阈值时发出
- **使用场景**：UI 实时同步动作执行时间阈值变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### lowPowerNotifyThresholdChanged

低电量通知百分比阈值变化时发出。

- **功能**：通知订阅者低电量通知百分比阈值发生了变化
- **触发条件**：用户修改低电量通知百分比阈值时发出
- **使用场景**：UI 实时同步低电量通知百分比阈值变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### actionPercentageChanged

动作执行百分比阈值变化时发出。

- **功能**：通知订阅者动作执行百分比阈值发生了变化
- **触发条件**：用户修改动作执行百分比阈值时发出
- **使用场景**：UI 实时同步动作执行百分比阈值变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```


---

## System 总线电源管理接口（org.deepin.dde.Power1）

该接口在 System 总线上提供系统级电源管理能力，包括电池状态查询、节能模式配置、电源模式切换和 CPU 调频控制。与 Session 总线上的 `org.deepin.dde.Power1` 接口名相同但注册在不同总线上，提供面向系统级的电源管理功能。

### 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Power1` |
| Object path | `/org/deepin/dde/Power1` |
| Interface | `org.deepin.dde.Power1` |
| Bus | System |

### 方法

#### GetBatteries

获取所有已注册的电池设备对象路径。

- **功能**：返回当前系统中所有电池设备的 D-Bus 对象路径列表
- **触发条件**：需要枚举系统电池设备时调用
- **输入参数**：无
- **返回值**：`ao`（对象路径数组）：电池设备对象路径列表
- **使用场景**：获取电池设备列表后逐个查询详细电池信息

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.GetBatteries
```

#### Refresh

刷新电源状态。

- **功能**：重新读取并更新所有电源状态信息
- **触发条件**：需要强制刷新电源状态时调用
- **输入参数**：无
- **返回值**：无
- **使用场景**：电源状态可能不同步时手动刷新

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.Refresh
```

#### RefreshBatteries

刷新电池设备状态。

- **功能**：重新读取并更新所有电池设备的状态信息
- **触发条件**：需要强制刷新电池状态时调用
- **输入参数**：无
- **返回值**：无
- **使用场景**：电池状态可能不同步时手动刷新

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.RefreshBatteries
```

#### RefreshMains

刷新交流电源状态。

- **功能**：重新读取并更新交流电源连接状态
- **触发条件**：需要强制刷新交流电源状态时调用
- **输入参数**：无
- **返回值**：无
- **使用场景**：交流电源状态可能不同步时手动刷新

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.RefreshMains
```

#### SetCpuGovernor

设置 CPU 调频策略。

- **功能**：设置 CPU 的调频策略（governor）
- **触发条件**：电源模式切换或用户手动设置时调用
- **输入参数**：`gov`（string, 类型 `s`）：调频策略名称，如 `performance`、`powersave`、`schedutil`
- **返回值**：无
- **使用场景**：切换电源模式时设置对应的 CPU 调频策略

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.SetCpuGovernor "performance"
```

#### SetCpuBoost

设置 CPU 加速开关。

- **功能**：开启或关闭 CPU 加速（turbo boost）
- **触发条件**：电源模式切换或用户手动设置时调用
- **输入参数**：`on`（boolean, 类型 `b`）：是否开启 CPU 加速
- **返回值**：无
- **使用场景**：高性能模式开启 CPU 加速，节能模式关闭 CPU 加速

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.SetCpuBoost true
```

#### LockCpuFreq

锁定 CPU 频率。

- **功能**：在指定时间内锁定 CPU 调频策略，防止自动切换
- **触发条件**：需要临时固定 CPU 频率时调用
- **输入参数**：`gov`（string, 类型 `s`）：调频策略名称；`lockTime`（int32, 类型 `i`）：锁定时长（秒）
- **返回值**：无
- **使用场景**：特定场景下需要固定 CPU 频率避免频繁切换

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.LockCpuFreq "performance" 60
```

#### SetMode

设置电源模式。

- **功能**：切换系统电源模式（平衡、高性能、节能）
- **触发条件**：用户在控制中心切换电源模式时调用
- **输入参数**：`mode`（string, 类型 `s`）：电源模式名称，取值为 `balance`（平衡）、`performance`（高性能）、`powersave`（节能）
- **返回值**：无
- **使用场景**：用户在控制中心选择不同的电源模式

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.SetMode "balance"
```

#### SetTlpMode

设置 TLP 模式。

- **功能**：设置 TLP（Thin and Light Power）模式
- **触发条件**：电源模式切换时内部调用
- **输入参数**：`mode`（string, 类型 `s`）：TLP 模式名称
- **返回值**：无
- **使用场景**：电源模式切换时同步设置 TLP 模式

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.SetTlpMode "balance"
```

#### SetAllowCaller

添加允许调用者。

- **功能**：将指定 D-Bus 唯一名添加到允许调用列表，用于权限控制
- **触发条件**：需要授权特定进程调用系统电源管理接口时调用
- **输入参数**：`uniqueName`（string, 类型 `s`）：D-Bus 唯一名
- **返回值**：无
- **使用场景**：授权特定进程执行电源操作

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.SetAllowCaller ":1.123"
```

#### SetShortIdleState

设置短空闲状态。

- **功能**：设置系统短空闲状态开关
- **触发条件**：系统空闲状态变化时调用
- **输入参数**：`state`（boolean, 类型 `b`）：是否进入短空闲状态
- **返回值**：无
- **使用场景**：系统根据空闲状态切换短空闲模式

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.SetShortIdleState true
```

#### SetIdleState

设置空闲状态。

- **功能**：设置系统空闲状态开关
- **触发条件**：系统空闲状态变化时调用
- **输入参数**：`state`（boolean, 类型 `b`）：是否进入空闲状态
- **返回值**：无
- **使用场景**：系统根据空闲状态切换空闲模式

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.SetIdleState true
```

#### SetScreenState

设置屏幕状态。

- **功能**：设置屏幕开闭状态
- **触发条件**：屏幕开关时调用
- **输入参数**：`state`（boolean, 类型 `b`）：屏幕是否开启
- **返回值**：无
- **使用场景**：系统根据电源策略控制屏幕开关

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.deepin.dde.Power1.SetScreenState true
```

### 属性

#### OnBattery（属性）

是否使用电池供电。

- **功能**：指示当前系统是否由电池供电（非交流电源）
- **触发条件**：交流电源连接/断开时更新
- **使用场景**：UI 显示电源连接状态

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 OnBattery
```

#### HasBattery（属性）

是否有电池。

- **功能**：指示系统是否安装了电池设备
- **触发条件**：电池设备插拔时更新
- **使用场景**：UI 根据是否有电池显示或隐藏电池相关设置

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 HasBattery
```

#### HasLidSwitch（属性）

是否有翻盖开关。

- **功能**：指示系统是否具备翻盖开关硬件
- **触发条件**：硬件探测完成时确定
- **使用场景**：UI 根据是否有翻盖开关显示或隐藏翻盖相关设置

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 HasLidSwitch
```

#### LidClosed（属性）

翻盖是否关闭。

- **功能**：指示当前翻盖是否处于关闭状态
- **触发条件**：翻盖开合时更新
- **使用场景**：系统根据翻盖状态执行翻盖动作策略

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 LidClosed
```

#### BatteryPercentage（属性）

电池剩余电量百分比。

- **功能**：返回当前电池的剩余电量百分比
- **触发条件**：电池电量变化时更新
- **使用场景**：UI 显示电池电量百分比

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryPercentage
```

#### BatteryStatus（属性）

电池状态。

- **功能**：返回当前电池的充放电状态
- **触发条件**：电池充放电状态变化时更新
- **使用场景**：UI 显示电池充电状态

| 属性 | 值 |
|------|------|
| 类型 | `u` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryStatus
```

#### BatteryTimeToEmpty（属性）

电池剩余使用时间。

- **功能**：返回当前电池预计剩余使用时间（秒）
- **触发条件**：电池放电时随电量变化更新
- **使用场景**：UI 显示电池剩余使用时间

| 属性 | 值 |
|------|------|
| 类型 | `t` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryTimeToEmpty
```

#### BatteryTimeToFull（属性）

电池充满时间。

- **功能**：返回当前电池预计充满所需时间（秒）
- **触发条件**：电池充电时随电量变化更新
- **使用场景**：UI 显示电池充满剩余时间

| 属性 | 值 |
|------|------|
| 类型 | `t` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryTimeToFull
```

#### BatteryCapacity（属性）

电池容量。

- **功能**：返回电池当前容量与设计容量的比值（百分比）
- **触发条件**：电池容量变化时更新
- **使用场景**：UI 显示电池健康度信息

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 BatteryCapacity
```

#### PowerSavingModeEnabled（属性）

节能模式开关。

- **功能**：指示节能模式是否已开启
- **触发条件**：用户或系统切换节能模式时更新
- **使用场景**：UI 显示节能模式开关状态

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 PowerSavingModeEnabled
```

设置示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 PowerSavingModeEnabled <true>
```

#### PowerSavingModeAuto（属性）

节能模式自动开关。

- **功能**：指示是否启用节能模式自动切换
- **触发条件**：用户在控制中心修改节能模式自动开关时更新
- **使用场景**：系统根据该值决定是否自动切换节能模式

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 PowerSavingModeAuto
```

设置示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 PowerSavingModeAuto <true>
```

#### PowerSavingModeAutoWhenBatteryLow（属性）

低电量自动节能。

- **功能**：指示是否在低电量时自动开启节能模式
- **触发条件**：用户在控制中心修改低电量自动节能开关时更新
- **使用场景**：系统根据该值在低电量时自动切换节能模式

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 PowerSavingModeAutoWhenBatteryLow
```

设置示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 PowerSavingModeAutoWhenBatteryLow <true>
```

#### PowerSavingModeBrightnessDropPercent（属性）

节能模式亮度降幅。

- **功能**：设置节能模式下屏幕亮度的降低百分比
- **触发条件**：用户在控制中心修改节能模式亮度降幅时更新
- **使用场景**：节能模式开启时按该值降低屏幕亮度

| 属性 | 值 |
|------|------|
| 类型 | `u` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 PowerSavingModeBrightnessDropPercent
```

设置示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 PowerSavingModeBrightnessDropPercent <uint32 30>
```

#### PowerSavingModeAutoBatteryPercent（属性）

自动节能电量阈值。

- **功能**：设置自动开启节能模式的电池电量百分比阈值
- **触发条件**：用户在控制中心修改自动节能电量阈值时更新
- **使用场景**：电池电量低于该值时自动开启节能模式

| 属性 | 值 |
|------|------|
| 类型 | `u` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 PowerSavingModeAutoBatteryPercent
```

设置示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 PowerSavingModeAutoBatteryPercent <uint32 20>
```

#### PowerSavingModeBrightnessData（属性）

节能模式亮度数据。

- **功能**：存储节能模式下的亮度配置数据
- **触发条件**：节能模式亮度配置变化时更新
- **使用场景**：系统恢复节能模式亮度配置时读取

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 PowerSavingModeBrightnessData
```

设置示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 PowerSavingModeBrightnessData "<brightness_data>"
```

#### ShortIdleState（属性）

短空闲状态。

- **功能**：指示系统是否处于短空闲状态
- **触发条件**：系统短空闲状态变化时更新
- **使用场景**：系统根据短空闲状态执行相应策略

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 ShortIdleState
```

#### TlpMode（属性）

TLP 模式。

- **功能**：返回当前 TLP（Thin and Light Power）模式
- **触发条件**：TLP 模式切换时更新
- **使用场景**：UI 显示当前 TLP 模式

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 TlpMode
```

#### Mode（属性）

电源模式。

- **功能**：返回当前电源模式（平衡、高性能、节能）
- **触发条件**：电源模式切换时更新
- **使用场景**：UI 显示当前电源模式

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 Mode
```

#### IsHighPerformanceSupported（属性）

是否支持高性能模式。

- **功能**：指示当前设备是否支持高性能电源模式
- **触发条件**：硬件探测完成时确定
- **使用场景**：UI 根据设备是否支持高性能模式显示或隐藏该选项

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 IsHighPerformanceSupported
```

#### IsBalanceSupported（属性）

是否支持平衡模式。

- **功能**：指示当前设备是否支持平衡电源模式
- **触发条件**：硬件探测完成时确定
- **使用场景**：UI 根据设备是否支持平衡模式显示或隐藏该选项

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 IsBalanceSupported
```

#### IsPowerSaveSupported（属性）

是否支持节能模式。

- **功能**：指示当前设备是否支持节能电源模式
- **触发条件**：硬件探测完成时确定
- **使用场景**：UI 根据设备是否支持节能模式显示或隐藏该选项

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 IsPowerSaveSupported
```

#### SupportSwitchPowerMode（属性）

是否支持切换电源模式。

- **功能**：指示是否允许切换电源模式
- **触发条件**：系统配置变化时更新
- **使用场景**：UI 根据该值决定是否显示电源模式切换选项

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 SupportSwitchPowerMode
```

设置示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Power1 SupportSwitchPowerMode <true>
```

#### CpuGovernor（属性）

CPU 调频策略。

- **功能**：返回当前 CPU 调频策略名称
- **触发条件**：调频策略切换时更新
- **使用场景**：UI 显示当前 CPU 调频策略

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 CpuGovernor
```

#### CpuBoost（属性）

CPU 加速开关状态。

- **功能**：指示 CPU 加速（turbo boost）是否已开启
- **触发条件**：CPU 加速开关变化时更新
- **使用场景**：UI 显示 CPU 加速状态

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1 CpuBoost
```

### 信号

#### onBatteryChanged

电池供电状态变化时发出。

- **功能**：通知订阅者电池供电状态发生了变化
- **触发条件**：交流电源连接/断开时发出
- **使用场景**：UI 实时同步电源连接状态变更时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### hasBatteryChanged

电池设备存在状态变化时发出。

- **功能**：通知订阅者系统是否有电池设备的状态发生了变化
- **触发条件**：电池设备插拔时发出
- **使用场景**：UI 实时同步电池设备存在状态变更时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### hasLidSwitchChanged

翻盖开关存在状态变化时发出。

- **功能**：通知订阅者系统是否有翻盖开关的状态发生了变化
- **触发条件**：硬件配置变化时发出
- **使用场景**：UI 实时同步翻盖开关存在状态变更时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### lidClosedChanged

翻盖开合状态变化时发出。

- **功能**：通知订阅者翻盖开合状态发生了变化
- **触发条件**：翻盖开合时发出
- **使用场景**：系统实时响应翻盖开合状态变更时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### LidClosed

翻盖关闭事件。

- **功能**：通知订阅者翻盖已关闭
- **触发条件**：翻盖合上时发出
- **使用场景**：系统执行翻盖关闭动作策略时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### LidOpened

翻盖打开事件。

- **功能**：通知订阅者翻盖已打开
- **触发条件**：翻盖打开时发出
- **使用场景**：系统执行翻盖打开动作策略时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### BatteryDisplayUpdate

电池显示更新事件。

- **功能**：通知订阅者电池显示信息已更新
- **触发条件**：电池信息刷新完成时发出
- **使用场景**：UI 实时刷新电池显示信息时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### BatteryAdded

电池添加事件。

- **功能**：通知订阅者有新电池设备添加
- **触发条件**：电池设备注册时发出
- **使用场景**：UI 实时响应电池设备添加时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### BatteryRemoved

电池移除事件。

- **功能**：通知订阅者有电池设备被移除
- **触发条件**：电池设备注销时发出
- **使用场景**：UI 实时响应电池设备移除时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryPercentageChanged

电池百分比变化时发出。

- **功能**：通知订阅者电池剩余电量百分比发生了变化
- **触发条件**：电池电量变化时发出
- **使用场景**：UI 实时同步电池电量显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryStatusChanged

电池状态变化时发出。

- **功能**：通知订阅者电池充放电状态发生了变化
- **触发条件**：电池充放电状态切换时发出
- **使用场景**：UI 实时同步电池充电状态显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryTimeToEmptyChanged

电池剩余使用时间变化时发出。

- **功能**：通知订阅者电池剩余使用时间发生了变化
- **触发条件**：电池放电时随电量变化发出
- **使用场景**：UI 实时同步电池剩余使用时间显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryTimeToFullChanged

电池充满时间变化时发出。

- **功能**：通知订阅者电池充满所需时间发生了变化
- **触发条件**：电池充电时随电量变化发出
- **使用场景**：UI 实时同步电池充满时间显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### batteryCapacityChanged

电池容量变化时发出。

- **功能**：通知订阅者电池容量发生了变化
- **触发条件**：电池容量变化时发出
- **使用场景**：UI 实时同步电池健康度显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### powerSavingModeEnabledChanged

节能模式开关变化时发出。

- **功能**：通知订阅者节能模式开关状态发生了变化
- **触发条件**：节能模式开启/关闭时发出
- **使用场景**：UI 实时同步节能模式开关状态时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### powerSavingModeAutoChanged

节能模式自动开关变化时发出。

- **功能**：通知订阅者节能模式自动切换开关发生了变化
- **触发条件**：用户修改节能模式自动开关时发出
- **使用场景**：UI 实时同步节能模式自动开关状态时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### powerSavingModeAutoWhenBatteryLowChanged

低电量自动节能开关变化时发出。

- **功能**：通知订阅者低电量自动节能开关发生了变化
- **触发条件**：用户修改低电量自动节能开关时发出
- **使用场景**：UI 实时同步低电量自动节能开关状态时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### powerSavingModeBrightnessDropPercentChanged

节能模式亮度降幅变化时发出。

- **功能**：通知订阅者节能模式亮度降幅百分比发生了变化
- **触发条件**：用户修改节能模式亮度降幅时发出
- **使用场景**：UI 实时同步节能模式亮度降幅配置时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### powerSavingModeAutoBatteryPercentChanged

自动节能电量阈值变化时发出。

- **功能**：通知订阅者自动开启节能模式的电量阈值发生了变化
- **触发条件**：用户修改自动节能电量阈值时发出
- **使用场景**：UI 实时同步自动节能电量阈值配置时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### powerSavingModeBrightnessDataChanged

节能模式亮度数据变化时发出。

- **功能**：通知订阅者节能模式亮度配置数据发生了变化
- **触发条件**：节能模式亮度配置变化时发出
- **使用场景**：系统实时同步节能模式亮度配置时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### shortIdleStateChanged

短空闲状态变化时发出。

- **功能**：通知订阅者系统短空闲状态发生了变化
- **触发条件**：系统短空闲状态切换时发出
- **使用场景**：系统实时响应短空闲状态变化时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### tlpModeChanged

TLP 模式变化时发出。

- **功能**：通知订阅者 TLP 模式发生了变化
- **触发条件**：TLP 模式切换时发出
- **使用场景**：UI 实时同步 TLP 模式显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### modeChanged

电源模式变化时发出。

- **功能**：通知订阅者电源模式发生了变化
- **触发条件**：电源模式切换时发出
- **使用场景**：UI 实时同步电源模式显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### isHighPerformanceSupportedChanged

高性能模式支持状态变化时发出。

- **功能**：通知订阅者设备是否支持高性能模式的状态发生了变化
- **触发条件**：硬件配置变化时发出
- **使用场景**：UI 实时同步高性能模式可用性时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### isPowerSaveSupportedChanged

节能模式支持状态变化时发出。

- **功能**：通知订阅者设备是否支持节能模式的状态发生了变化
- **触发条件**：硬件配置变化时发出
- **使用场景**：UI 实时同步节能模式可用性时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### isBalanceSupportedChanged

平衡模式支持状态变化时发出。

- **功能**：通知订阅者设备是否支持平衡模式的状态发生了变化
- **触发条件**：硬件配置变化时发出
- **使用场景**：UI 实时同步平衡模式可用性时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### supportSwitchPowerModeChanged

电源模式切换支持状态变化时发出。

- **功能**：通知订阅者是否允许切换电源模式的状态发生了变化
- **触发条件**：系统配置变化时发出
- **使用场景**：UI 实时同步电源模式切换可用性时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### cpuGovernorChanged

CPU 调频策略变化时发出。

- **功能**：通知订阅者 CPU 调频策略发生了变化
- **触发条件**：调频策略切换时发出
- **使用场景**：UI 实时同步 CPU 调频策略显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```

#### cpuBoostChanged

CPU 加速开关变化时发出。

- **功能**：通知订阅者 CPU 加速开关状态发生了变化
- **触发条件**：CPU 加速开启/关闭时发出
- **使用场景**：UI 实时同步 CPU 加速状态显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1
```


---

## 电池设备接口（org.deepin.dde.Power1.Battery）

该接口在 System 总线上提供单个电池设备的详细信息查询能力，包括电池制造商、型号、容量、电压、充放电状态和运行时间信息。每个电池设备在运行时动态注册，对象路径取决于实际电池设备（如 `/org/deepin/dde/Power1/Battery0`）。

### 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Power1` |
| Object path | `/org/deepin/dde/Power1/Battery0`（动态，取决于实际电池设备） |
| Interface | `org.deepin.dde.Power1.Battery` |
| Bus | System |

### 方法

#### Refresh

刷新电池设备信息。

- **功能**：重新读取并更新该电池设备的所有属性
- **触发条件**：需要强制刷新电池信息时调用
- **输入参数**：无
- **返回值**：无
- **使用场景**：电池信息可能不同步时手动刷新

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.deepin.dde.Power1.Battery.Refresh
```

### 属性

#### SysfsPath（属性）

sysfs 设备路径。

- **功能**：返回该电池设备在 sysfs 文件系统中的路径
- **触发条件**：设备注册时确定，不随运行时变化
- **使用场景**：排查电池设备问题时定位 sysfs 路径

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery SysfsPath
```

#### IsPresent（属性）

电池是否存在。

- **功能**：指示该电池设备当前是否存在
- **触发条件**：电池设备插拔时更新
- **使用场景**：UI 判断电池设备是否可用

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery IsPresent
```

#### Manufacturer（属性）

电池制造商。

- **功能**：返回电池设备的制造商名称
- **触发条件**：设备注册时确定
- **使用场景**：UI 显示电池制造商信息

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery Manufacturer
```

#### ModelName（属性）

电池型号。

- **功能**：返回电池设备的型号名称
- **触发条件**：设备注册时确定
- **使用场景**：UI 显示电池型号信息

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery ModelName
```

#### SerialNumber（属性）

电池序列号。

- **功能**：返回电池设备的序列号
- **触发条件**：设备注册时确定
- **使用场景**：电池设备唯一标识

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery SerialNumber
```

#### Name（属性）

电池名称。

- **功能**：返回电池设备的名称
- **触发条件**：设备注册时确定
- **使用场景**：UI 显示电池名称

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery Name
```

#### Technology（属性）

电池技术类型。

- **功能**：返回电池设备的技术类型（如锂离子）
- **触发条件**：设备注册时确定
- **使用场景**：UI 显示电池技术类型

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery Technology
```

#### Energy（属性）

当前能量。

- **功能**：返回电池当前剩余能量（瓦时，Wh）
- **触发条件**：电池能量变化时更新
- **使用场景**：计算电池剩余使用时间

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery Energy
```

#### EnergyFull（属性）

满充能量。

- **功能**：返回电池满充时的实际能量（瓦时，Wh）
- **触发条件**：电池满充能量变化时更新
- **使用场景**：计算电池容量损耗

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery EnergyFull
```

#### EnergyFullDesign（属性）

设计能量。

- **功能**：返回电池设计能量（瓦时，Wh）
- **触发条件**：设备注册时确定
- **使用场景**：计算电池容量损耗百分比

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery EnergyFullDesign
```

#### EnergyRate（属性）

能量速率。

- **功能**：返回电池当前充放电速率（瓦特，W）
- **触发条件**：电池充放电速率变化时更新
- **使用场景**：估算电池剩余使用时间和充满时间

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery EnergyRate
```

#### Voltage（属性）

电压。

- **功能**：返回电池当前电压（伏特，V）
- **触发条件**：电池电压变化时更新
- **使用场景**：电池状态诊断

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery Voltage
```

#### Percentage（属性）

电量百分比。

- **功能**：返回电池剩余电量百分比
- **触发条件**：电池电量变化时更新
- **使用场景**：UI 显示电池电量

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery Percentage
```

#### Capacity（属性）

容量百分比。

- **功能**：返回电池当前容量与设计容量的比值（百分比）
- **触发条件**：电池容量变化时更新
- **使用场景**：UI 显示电池健康度

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery Capacity
```

#### Status（属性）

电池状态。

- **功能**：返回电池当前充放电状态
- **触发条件**：电池充放电状态变化时更新
- **使用场景**：UI 显示电池充电状态

| 属性 | 值 |
|------|------|
| 类型 | `u` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery Status
```

#### TimeToEmpty（属性）

剩余使用时间。

- **功能**：返回电池预计剩余使用时间（秒）
- **触发条件**：电池放电时随电量变化更新
- **使用场景**：UI 显示电池剩余使用时间

| 属性 | 值 |
|------|------|
| 类型 | `t` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery TimeToEmpty
```

#### TimeToFull（属性）

充满时间。

- **功能**：返回电池预计充满所需时间（秒）
- **触发条件**：电池充电时随电量变化更新
- **使用场景**：UI 显示电池充满剩余时间

| 属性 | 值 |
|------|------|
| 类型 | `t` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery TimeToFull
```

#### UpdateTime（属性）

更新时间戳。

- **功能**：返回电池信息最后一次更新的时间戳
- **触发条件**：电池信息刷新时更新
- **使用场景**：判断电池信息是否过期

| 属性 | 值 |
|------|------|
| 类型 | `x` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Power1.Battery UpdateTime
```

### 信号

#### isPresentChanged

电池存在状态变化时发出。

- **功能**：通知订阅者电池设备是否存在的状态发生了变化
- **触发条件**：电池设备插拔时发出
- **使用场景**：UI 实时响应电池设备存在状态变化时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### manufacturerChanged

制造商信息变化时发出。

- **功能**：通知订阅者电池制造商信息发生了变化
- **触发条件**：电池设备更换时发出
- **使用场景**：UI 实时同步电池制造商信息时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### modelNameChanged

型号信息变化时发出。

- **功能**：通知订阅者电池型号信息发生了变化
- **触发条件**：电池设备更换时发出
- **使用场景**：UI 实时同步电池型号信息时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### serialNumberChanged

序列号变化时发出。

- **功能**：通知订阅者电池序列号发生了变化
- **触发条件**：电池设备更换时发出
- **使用场景**：UI 实时同步电池序列号时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### nameChanged

名称变化时发出。

- **功能**：通知订阅者电池名称发生了变化
- **触发条件**：电池设备更换时发出
- **使用场景**：UI 实时同步电池名称时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### technologyChanged

技术类型变化时发出。

- **功能**：通知订阅者电池技术类型发生了变化
- **触发条件**：电池设备更换时发出
- **使用场景**：UI 实时同步电池技术类型时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### energyChanged

能量变化时发出。

- **功能**：通知订阅者电池当前能量发生了变化
- **触发条件**：电池充放电时随能量变化发出
- **使用场景**：UI 实时同步电池能量显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### energyFullChanged

满充能量变化时发出。

- **功能**：通知订阅者电池满充能量发生了变化
- **触发条件**：电池满充能量变化时发出
- **使用场景**：系统实时同步电池容量信息时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### energyFullDesignChanged

设计能量变化时发出。

- **功能**：通知订阅者电池设计能量发生了变化
- **触发条件**：电池设备更换时发出
- **使用场景**：系统实时同步电池设计容量信息时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### energyRateChanged

能量速率变化时发出。

- **功能**：通知订阅者电池充放电速率发生了变化
- **触发条件**：电池充放电速率变化时发出
- **使用场景**：UI 实时同步电池充放电速率显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### voltageChanged

电压变化时发出。

- **功能**：通知订阅者电池电压发生了变化
- **触发条件**：电池电压变化时发出
- **使用场景**：电池状态诊断时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### percentageChanged

电量百分比变化时发出。

- **功能**：通知订阅者电池剩余电量百分比发生了变化
- **触发条件**：电池电量变化时发出
- **使用场景**：UI 实时同步电池电量显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### capacityChanged

容量百分比变化时发出。

- **功能**：通知订阅者电池容量百分比发生了变化
- **触发条件**：电池容量变化时发出
- **使用场景**：UI 实时同步电池健康度显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### statusChanged

电池状态变化时发出。

- **功能**：通知订阅者电池充放电状态发生了变化
- **触发条件**：电池充放电状态切换时发出
- **使用场景**：UI 实时同步电池充电状态显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### timeToEmptyChanged

剩余使用时间变化时发出。

- **功能**：通知订阅者电池剩余使用时间发生了变化
- **触发条件**：电池放电时随电量变化发出
- **使用场景**：UI 实时同步电池剩余使用时间显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### timeToFullChanged

充满时间变化时发出。

- **功能**：通知订阅者电池充满所需时间发生了变化
- **触发条件**：电池充电时随电量变化发出
- **使用场景**：UI 实时同步电池充满时间显示时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```

#### updateTimeChanged

更新时间戳变化时发出。

- **功能**：通知订阅者电池信息更新时间戳发生了变化
- **触发条件**：电池信息刷新时发出
- **使用场景**：判断电池信息是否过期时监听

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Power1 \
  --object-path /org/deepin/dde/Power1/Battery0
```
