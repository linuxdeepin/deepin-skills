# org.deepin.dde.Gesture1 接口参考

该接口提供触摸手势管理能力，包括手势输入忽略设置和手势事件信号。该服务在 System 总线上导出。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Gesture1` |
| Object path | `/org/deepin/dde/Gesture1` |
| Interface | `org.deepin.dde.Gesture1` |
| Bus | System |

### 手势管理方法

#### SetEdgeMoveStopDuration

设置触摸屏边缘移动停止的持续时间阈值。

- **功能**：设置触摸屏边缘移动停止判定的时间阈值（单位毫秒），超过此时间后判定为边缘移动停止。
- **触发条件**：当需要调整触摸屏边缘移动停止的灵敏度时调用此方法。
- **使用场景**：触摸屏边缘手势交互调优，如调整从屏幕边缘滑入后停留多久触发边缘移动停止事件。
- **输入参数**: `duration`（int32, 类型 `i`）：持续时间（毫秒）
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1 \
  --method org.deepin.dde.Gesture1.SetEdgeMoveStopDuration 500
```

#### SetInputIgnore

设置指定输入节点是否忽略手势。

- **功能**：控制指定输入设备节点是否忽略手势识别，设置为忽略后该设备的手势事件不再被处理。
- **触发条件**：当需要禁用或恢复特定输入设备的手势识别时调用此方法。
- **使用场景**：排除不需要手势识别的输入设备，如外接触摸板、特定触摸屏设备。
- **输入参数**:
  - `node`（string, 类型 `s`）：输入节点名称
  - `isIgnore`（bool, 类型 `b`）：是否忽略
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1 \
  --method org.deepin.dde.Gesture1.SetInputIgnore "/dev/input/event0" true
```

#### SetShortPressDuration

设置短按持续时间阈值。

- **功能**：设置触摸屏短按判定的时间阈值（单位毫秒），触摸时间小于此值判定为短按。
- **触发条件**：当需要调整触摸屏短按的灵敏度时调用此方法。
- **使用场景**：触摸屏短按交互调优，如调整短按与长按的区分阈值。
- **输入参数**: `duration`（int32, 类型 `i`）：持续时间（毫秒）
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1 \
  --method org.deepin.dde.Gesture1.SetShortPressDuration 300
```

### 手势事件信号

以下信号由 `org.deepin.dde.Gesture1` 接口发出，通过 `gdbus monitor` 监听。

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1
```

#### Event

触摸板手势事件。

- **功能**：报告触摸板或触摸屏检测到的手势事件，包括手势类型、方向和手指数。
- **触发条件**：当触摸板检测到滑动手势、捏合手势或轻触手势时，或触摸屏检测到触摸事件时由底层 libinput 事件触发。
- **使用场景**：窗口管理器或手势引擎监听此信号以执行工作区切换、窗口缩放、通知面板呼出操作。
- **参数**: `name`（string, 类型 `s`）：手势名称；`direction`（string, 类型 `s`）：方向；`fingers`（int32, 类型 `i`）：手指数

#### SwipeMoving

触摸板滑动移动中事件。

- **功能**：报告触摸板滑动过程中的实时加速度信息。
- **触发条件**：当触摸板上多指滑动正在进行时，由底层 libinput 持续触发。
- **使用场景**：窗口管理器监听此信号以实现滑动过程中的实时窗口预览或工作区跟随移动。
- **参数**: `fingers`（int32, 类型 `i`）：手指数；`accelX`（double, 类型 `d`）：X 轴加速度；`accelY`（double, 类型 `d`）：Y 轴加速度

#### SwipeStop

触摸板滑动停止事件。

- **功能**：报告触摸板滑动操作停止或被中断。
- **触发条件**：当触摸板上的多指滑动操作结束（手指抬起）或被系统中断时触发。
- **使用场景**：窗口管理器监听此信号以结束滑动动画或确认工作区切换。
- **参数**: `fingers`（int32, 类型 `i`）：手指数

#### TouchEdgeEvent

触摸屏边缘事件。

- **功能**：报告触摸屏检测到的边缘触摸事件，包括方向和坐标。
- **触发条件**：当触摸屏检测到从屏幕边缘开始的触摸操作时触发。
- **使用场景**：桌面环境监听此信号以实现边缘手势，如从屏幕底部边缘上滑呼出任务栏。
- **参数**: `direction`（string, 类型 `s`）：方向；`scaleX`（double, 类型 `d`）：X 坐标；`scaleY`（double, 类型 `d`）：Y 坐标

#### TouchMovementEvent

触摸屏移动事件。

- **功能**：报告触摸屏检测到的触摸移动事件，包括方向、手指数和起止坐标。
- **触发条件**：当触摸屏检测到多指触摸移动操作完成时触发。
- **使用场景**：桌面环境监听此信号以实现触摸屏上的多指移动手势，如三指上滑显示多任务视图。
- **参数**: `direction`（string, 类型 `s`）：方向；`fingers`（int32, 类型 `i`）：手指数；`startScaleX`（double, 类型 `d`）：起始 X；`startScaleY`（double, 类型 `d`）：起始 Y；`endScaleX`（double, 类型 `d`）：结束 X；`endScaleY`（double, 类型 `d`）：结束 Y

#### TouchMoving

触摸屏移动中事件。

- **功能**：报告触摸屏触摸移动过程中的实时坐标。
- **触发条件**：当触摸屏上有手指正在移动时持续触发。
- **使用场景**：桌面环境监听此信号以实现触摸移动过程中的实时跟随效果。
- **参数**: `scalex`（double, 类型 `d`）：X 坐标；`scaley`（double, 类型 `d`）：Y 坐标

#### TouchSinglePressTimeout

触摸屏单指按下超时事件。

- **功能**：报告触摸屏上单指按下超过设定的短按时间阈值。
- **触发条件**：当触摸屏上单指按下持续时间超过 `SetShortPressDuration` 设定的阈值时触发。
- **使用场景**：桌面环境监听此信号以将短按转换为长按操作，如长按显示右键菜单。
- **参数**: `time`（int32, 类型 `i`）：时间戳；`scaleX`（double, 类型 `d`）：X 坐标；`scaleY`（double, 类型 `d`）：Y 坐标

#### TouchPressTimeout

触摸屏多指按下超时事件。

- **功能**：报告触摸屏上多指按下超过设定的时间阈值。
- **触发条件**：当触摸屏上多指按下持续时间超过设定阈值时触发。
- **使用场景**：桌面环境监听此信号以实现多指长按手势，如三指长按显示工作区切换。
- **参数**: `fingers`（int32, 类型 `i`）：手指数；`time`（int32, 类型 `i`）：时间戳；`scaleX`（double, 类型 `d`）：X 坐标；`scaleY`（double, 类型 `d`）：Y 坐标

#### TouchUpOrCancel

触摸屏抬起或取消事件。

- **功能**：报告触摸屏上的触摸操作结束（手指抬起）或被取消。
- **触发条件**：当触摸屏上的手指抬起或触摸事件被系统取消时触发。
- **使用场景**：桌面环境监听此信号以结束当前触摸交互状态，如取消正在进行的拖拽操作。
- **参数**: `scaleX`（double, 类型 `d`）：X 坐标；`scaleY`（double, 类型 `d`）：Y 坐标

#### TouchEdgeMoveStop

触摸屏边缘移动停止事件。

- **功能**：报告触摸屏边缘移动操作停止，包括方向、坐标和持续时间。
- **触发条件**：当触摸屏边缘移动操作停止且持续时间未超过 `SetEdgeMoveStopDuration` 设定的阈值时触发。
- **使用场景**：桌面环境监听此信号以实现边缘移动停止手势，如从边缘滑入并停留触发特定操作。
- **参数**: `direction`（string, 类型 `s`）：方向；`scaleX`（double, 类型 `d`）：X 坐标；`scaleY`（double, 类型 `d`）：Y 坐标；`duration`（int32, 类型 `i`）：持续时间

#### TouchEdgeMoveStopLeave

触摸屏边缘移动停止并离开事件。

- **功能**：报告触摸屏边缘移动操作停止后手指离开屏幕，包括方向、坐标和持续时间。
- **触发条件**：当触摸屏边缘移动操作停止后手指离开屏幕时触发。
- **使用场景**：桌面环境监听此信号以实现边缘移动停止后离开的手势，如从边缘滑入、停留、然后离开触发特定操作。
- **参数**: `direction`（string, 类型 `s`）：方向；`scaleX`（double, 类型 `d`）：X 坐标；`scaleY`（double, 类型 `d`）：Y 坐标；`duration`（int32, 类型 `i`）：持续时间

#### DbclickDown

触摸板双击按下事件。

- **功能**：报告触摸板上检测到双击按下操作。
- **触发条件**：当触摸板检测到双击（快速连续两次轻触）时触发。
- **使用场景**：桌面环境监听此信号以实现双击手势，如双指双击触发右键菜单。
- **参数**: `fingers`（int32, 类型 `i`）：手指数

#### KeyboardEvent

键盘事件。

- **功能**：报告手势模块捕获到的键盘按键事件。
- **触发条件**：当手势模块监听的特定键盘按键被按下或松开时触发。
- **使用场景**：桌面环境监听此信号以响应与手势相关的键盘快捷键，如功能键切换。
- **参数**: `key`（uint32, 类型 `u`）：按键码；`state`（uint32, 类型 `u`）：状态

#### MouseEvent

鼠标事件。

- **功能**：报告手势模块捕获到的鼠标按键事件。
- **触发条件**：当手势模块监听的特定鼠标按键事件发生时触发。
- **使用场景**：桌面环境监听此信号以响应与手势相关的鼠标操作。
- **参数**: `state`（uint32, 类型 `u`）：状态；`value`（uint32, 类型 `u`）：值
