# org.deepin.dde.BlackScreen1 接口参考

该接口提供黑屏显示控制能力，包括黑屏窗口的显示、隐藏、退出和抓取设备释放。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.BlackScreen1` |
| Object path | `/org/deepin/dde/BlackScreen1` |
| Interface | `org.deepin.dde.BlackScreen1` |
| Bus | Session |

### Raise

将黑屏窗口提升到最前层。

- **功能**: 将黑屏窗口提升到所有窗口的最上层，确保黑屏遮罩覆盖整个屏幕
- **触发条件**: 由系统组件主动调用，当需要确保黑屏窗口处于最前层时触发
- **使用场景**: 系统从休眠唤醒过程中，将黑屏窗口置顶以避免唤醒过程中的画面闪烁
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.BlackScreen1 \
  --object-path /org/deepin/dde/BlackScreen1 \
  --method org.deepin.dde.BlackScreen1.Raise
```

### Quit

退出黑屏程序。

- **功能**: 关闭黑屏窗口并退出黑屏程序进程
- **触发条件**: 由系统组件主动调用，当系统确认可以完全退出黑屏模式时触发
- **使用场景**: 系统唤醒完成且显示就绪后，退出黑屏程序
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.BlackScreen1 \
  --object-path /org/deepin/dde/BlackScreen1 \
  --method org.deepin.dde.BlackScreen1.Quit
```

### setActive

设置黑屏窗口的显示或隐藏状态。

- **功能**: 控制黑屏窗口的显示或隐藏，不退出黑屏程序进程
- **触发条件**: 由系统组件主动调用，当需要动态切换黑屏显示状态时触发
- **使用场景**: 系统在休眠过程中显示黑屏，在部分唤醒阶段暂时隐藏黑屏
- **输入参数**: `visible`（bool, 类型 `b`）：是否显示黑屏
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.BlackScreen1 \
  --object-path /org/deepin/dde/BlackScreen1 \
  --method org.deepin.dde.BlackScreen1.setActive true
```

### quitDBusService

注销 D-Bus 服务并退出黑屏程序。

- **功能**: 注销黑屏程序在 Session 总线上的 D-Bus 服务名，然后退出黑屏程序进程
- **触发条件**: 由系统组件主动调用，当需要完全释放黑屏 D-Bus 服务并退出时触发
- **使用场景**: 系统确认黑屏流程完全结束，需要释放 D-Bus 服务名以供后续重新激活
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.BlackScreen1 \
  --object-path /org/deepin/dde/BlackScreen1 \
  --method org.deepin.dde.BlackScreen1.quitDBusService
```

### blackScreenVisible

查询黑屏是否正在显示。

- **功能**: 返回黑屏窗口当前的可见状态
- **触发条件**: 由系统组件主动调用以查询黑屏状态
- **使用场景**: 系统在唤醒流程中检查黑屏是否仍在显示，以决定下一步操作
- **输入参数**: 无
- **返回值**: `b`（bool）：黑屏是否可见

```bash
gdbus call --session \
  --dest org.deepin.dde.BlackScreen1 \
  --object-path /org/deepin/dde/BlackScreen1 \
  --method org.deepin.dde.BlackScreen1.blackScreenVisible
```

### releaseGrabDevices

释放黑屏程序抓取的键盘和鼠标设备。

- **功能**: 释放黑屏程序对键盘和鼠标输入设备的独占抓取，恢复其他程序的输入能力
- **触发条件**: 由系统组件主动调用，当黑屏期间需要将输入设备交给其他程序时触发
- **使用场景**: 系统唤醒过程中需要将输入设备控制权交给锁屏或会话管理器
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.BlackScreen1 \
  --object-path /org/deepin/dde/BlackScreen1 \
  --method org.deepin.dde.BlackScreen1.releaseGrabDevices
```

### releaseGrabDevicesHideBlack

释放抓取设备并隐藏黑屏窗口。

- **功能**: 释放键盘和鼠标设备的独占抓取，同时隐藏黑屏窗口
- **触发条件**: 由系统组件主动调用，当需要同时释放设备抓取和隐藏黑屏时触发
- **使用场景**: 系统唤醒完成，需要一步完成释放输入设备和隐藏黑屏遮罩
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.BlackScreen1 \
  --object-path /org/deepin/dde/BlackScreen1 \
  --method org.deepin.dde.BlackScreen1.releaseGrabDevicesHideBlack
```
