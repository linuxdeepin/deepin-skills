# org.deepin.dde.Gesture1 接口参考

该接口提供触摸手势管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Gesture` |
| Object path | `/com/deepin/daemon/Gesture` |
| Interface | `org.deepin.dde.Gesture1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 手势管理信号

#### TouchSinglePressGesture

单指按下手势触发。

- **参数**: `time`（int32, 类型 `i`）：时间戳；`mode`（int32, 类型 `i`）：模式
- **触发条件**: 单指按下时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Gesture \
  --object-path /com/deepin/daemon/Gesture
```

#### TouchLongPressGesture

长按手势触发。

- **参数**: `time`（int32, 类型 `i`）：时间戳；`mode`（int32, 类型 `i`）：模式
- **触发条件**: 长按时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Gesture \
  --object-path /com/deepin/daemon/Gesture
```

