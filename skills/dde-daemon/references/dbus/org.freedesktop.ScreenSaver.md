# org.freedesktop.ScreenSaver 接口参考

该接口提供屏幕保护管理能力，包括空闲抑制、用户活动模拟和超时设置。

> **说明**：`Inhibit`、`UnInhibit`、`SimulateUserActivity` 为 freedesktop ScreenSaver 标准方法。`SetTimeout` 方法及 `IdleOn`、`CycleActive`、`IdleOff` 信号为 DDE 扩展，非 freedesktop 标准。标准 `ActiveChanged` 信号由规范定义，但 DDE 实现未发射该信号。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.ScreenSaver` |
| Object path | `/org/freedesktop/ScreenSaver` |
| Interface | `org.freedesktop.ScreenSaver` |
| Bus | Session |
### 抑制空闲

#### Inhibit

抑制空闲计时器，使系统不再检测是否空闲。返回一个 cookie 用于后续取消抑制。

- **功能**：阻止屏幕保护程序在系统空闲时激活，返回一个唯一 cookie 用于后续取消抑制。
- **触发条件**：当应用程序需要防止屏幕变暗或锁屏时调用此方法。
- **使用场景**：视频播放器播放视频时阻止屏幕保护，演示文稿全屏展示时保持屏幕常亮。
- **输入参数**: `name`（string, 类型 `s`）：抑制空闲的程序名称；`reason`（string, 类型 `s`）：抑制原因
- **返回值**: `cookie`（uint32, 类型 `u`）：此次操作对应的 ID，用于取消抑制

```bash
gdbus call --session \
  --dest org.freedesktop.ScreenSaver \
  --object-path /org/freedesktop/ScreenSaver \
  --method org.freedesktop.ScreenSaver.Inhibit "myapp" "playing video"
```

#### UnInhibit

根据 cookie 取消对应的空闲抑制操作。

- **功能**：通过之前 `Inhibit` 返回的 cookie 取消空闲抑制，恢复屏幕保护的正常空闲检测。
- **触发条件**：当应用程序不再需要阻止屏幕保护时调用此方法。
- **使用场景**：视频播放器暂停或停止播放后恢复屏幕保护，演示文稿退出全屏后恢复空闲检测。
- **输入参数**: `cookie`（uint32, 类型 `u`）：Inhibit 返回的操作 ID
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.ScreenSaver \
  --object-path /org/freedesktop/ScreenSaver \
  --method org.freedesktop.ScreenSaver.UnInhibit 1
```

### 空闲管理

#### SimulateUserActivity

模拟用户操作，让系统处于使用状态，重新开始空闲计时器。

- **功能**：向屏幕保护服务发送模拟用户活动信号，重置空闲计时器。
- **触发条件**：当应用程序需要模拟用户输入以重置空闲计时器时调用此方法。
- **使用场景**：远程控制软件接收到远程输入时模拟本地用户活动，脚本自动化操作中防止屏幕锁屏。
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.ScreenSaver \
  --object-path /org/freedesktop/ScreenSaver \
  --method org.freedesktop.ScreenSaver.SimulateUserActivity
```

#### SetTimeout

> **DDE 扩展，非 freedesktop 标准**

设置空闲计时器的超时时间。

- **功能**：设置屏幕保护的空闲超时时间、壁纸切换间隔和是否黑屏。
- **触发条件**：当用户在系统设置中修改屏幕保护超时时间时调用此方法。
- **使用场景**：控制中心屏幕保护设置页面修改超时时间、壁纸切换间隔和黑屏选项。
- **输入参数**: `seconds`（uint32, 类型 `u`）：超时时间，以秒为单位；`interval`（uint32, 类型 `u`）：屏保模式下背景更换的间隔时间；`blank`（bool, 类型 `b`）：是否黑屏
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.ScreenSaver \
  --object-path /org/freedesktop/ScreenSaver \
  --method org.freedesktop.ScreenSaver.SetTimeout 300 0 false
```

### 信号

#### ActiveChanged

> **freedesktop 标准信号**（DDE 实现未发射此信号）

当屏幕保护激活状态发生变化时发出。

- **功能**：通知屏幕保护激活状态的变化。
- **触发条件**：当屏幕保护从激活变为未激活或从未激活变为激活时触发（DDE 实现未发射此信号）。
- **使用场景**：应用程序监听此信号以在屏幕保护激活/取消激活时执行相应操作，如暂停后台任务。
- **参数**: `active`（bool, 类型 `b`）：屏幕保护是否已激活

```bash
gdbus monitor --session \
  --dest org.freedesktop.ScreenSaver \
  --object-path /org/freedesktop/ScreenSaver
```

#### IdleOn

> **DDE 扩展，非 freedesktop 标准**

空闲定时器超时信号，当系统在给定时间内未被使用时发出。

- **功能**：通知系统空闲超时，触发屏幕保护激活。
- **触发条件**：当系统在 `SetTimeout` 设定的超时时间内没有任何用户输入时触发。
- **使用场景**：屏幕保护程序监听此信号以启动屏幕保护动画或锁屏。
- **参数**: 无

```bash
gdbus monitor --session \
  --dest org.freedesktop.ScreenSaver \
  --object-path /org/freedesktop/ScreenSaver
```

#### CycleActive

> **DDE 扩展，非 freedesktop 标准**

空闲超时时，如果设置了壁纸切换，则发出此信号。

- **功能**：通知屏幕保护在激活状态下切换壁纸。
- **触发条件**：当屏幕保护处于激活状态且到达壁纸切换间隔时间时触发。
- **使用场景**：屏幕保护程序监听此信号以执行壁纸切换动画。
- **参数**: 无

#### IdleOff

> **DDE 扩展，非 freedesktop 标准**

空闲超时后，如果系统被使用则发出此信号，重新开始空闲计时器。

- **功能**：通知屏幕保护因用户活动而退出空闲状态，重新开始空闲计时。
- **触发条件**：当屏幕保护处于空闲激活状态后检测到用户输入时触发。
- **使用场景**：屏幕保护程序监听此信号以退出屏幕保护动画并恢复正常桌面。
- **参数**: 无

## 接口说明

`org.freedesktop.ScreenSaver` 是 dde-daemon 实现的 freedesktop 标准屏幕保护接口，非兼容接口。dde-daemon 在 Session 总线上实现了 freedesktop ScreenSaver 规范定义的标准方法（`Inhibit`、`UnInhibit`、`SimulateUserActivity`），并扩展了 `SetTimeout` 方法及 `IdleOn`、`CycleActive`、`IdleOff` 信号。
