# org.deepin.dde.XEventMonitor1 接口参考

该接口提供 X 事件区域监控能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.XEventMonitor1` |
| Object path | `/org/deepin/dde/XEventMonitor1` |
| Interface | `org.deepin.dde.XEventMonitor1` |
| Bus | Session |
### X 事件监控方法

#### RegisterArea

注册监控区域。

- **功能**：注册一个屏幕区域的全局 X 事件监控。
- **触发条件**：当需要监控指定屏幕区域内的鼠标事件时调用。
- **使用场景**：热区触发、屏幕边缘手势监控。

- **输入参数**: `x1`（int32, 类型 `i`）：左上角 X 坐标；`y1`（int32, 类型 `i`）：左上角 Y 坐标；`x2`（int32, 类型 `i`）：右下角 X 坐标；`y2`（int32, 类型 `i`）：右下角 Y 坐标；`flag`（int32, 类型 `i`）：标志
- **返回值**: `s`（string）：区域 ID

```bash
gdbus call --session \
  --dest org.deepin.dde.XEventMonitor1 \
  --object-path /org/deepin/dde/XEventMonitor1 \
  --method org.deepin.dde.XEventMonitor1.RegisterArea 0 0 100 100 0
```

#### UnregisterArea

取消注册监控区域。

- **功能**：取消注册的屏幕区域 X 事件监控。
- **触发条件**：当不再需要监控指定区域时调用。
- **使用场景**：热区监控取消、区域监控清理。

- **输入参数**: `id`（string, 类型 `s`）：区域 ID
- **返回值**: `b`（bool）：是否成功取消

```bash
gdbus call --session \
  --dest org.deepin.dde.XEventMonitor1 \
  --object-path /org/deepin/dde/XEventMonitor1 \
  --method org.deepin.dde.XEventMonitor1.UnregisterArea "region_id"
```
