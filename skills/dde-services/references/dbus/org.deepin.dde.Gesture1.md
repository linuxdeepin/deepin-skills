# org.deepin.dde.Gesture1 接口参考

该接口提供手势管理能力，包括手势列表查询、手势动作修改和可用动作查询。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Gesture1` |
| Object path | `/org/deepin/dde/Gesture1` |
| Interface | `org.deepin.dde.Gesture1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 手势查询与修改

#### ListAllGestures

列出所有手势。

- **输入参数**: 无
- **返回值**: `a(GestureInfo)`：手势信息数组

```bash
gdbus call --session \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1 \
  --method org.deepin.dde.Gesture1.ListAllGestures
```

#### ModifyGesture

修改手势动作。

- **输入参数**: `id`（string, 类型 `s`）：手势 ID；`action`（string 数组, 类型 `as`）：动作
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1 \
  --method org.deepin.dde.Gesture1.ModifyGesture "swipe_left_3" ["workspace_next"]
```

#### GetGestureAvaiableActions

获取手势可用动作。

> **待核验**: `actionType` 参数支持固定的动作类型选项，具体选项值待核验源码确认。

- **输入参数**: `actionType`（string, 类型 `s`）：动作类型；`fingerNum`（int32, 类型 `i`）：手指数
- **返回值**: `s`（string）：可用动作 JSON

```bash
gdbus call --session \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1 \
  --method org.deepin.dde.Gesture1.GetGestureAvaiableActions "swipe" 3
```


### 手势信号

#### GestureInfosChanged

手势信息变化时发出。

- **参数**: 无
- **触发条件**: 手势配置变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1
```

#### GestureActivated

手势激活时发出。

- **参数**: `id`（string, 类型 `s`）：手势 ID；`params`（string 数组, 类型 `as`）：参数
- **触发条件**: 手势被触发时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1
```

---
