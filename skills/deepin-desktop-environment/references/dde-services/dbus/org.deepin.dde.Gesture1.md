# org.deepin.dde.Gesture1 接口参考

该接口提供手势管理能力，包括手势列表查询、手势动作修改和可用动作查询。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Gesture1` |
| Object path | `/org/deepin/dde/Gesture1` |
| Interface | `org.deepin.dde.Gesture1` |
| Bus | Session |

### 手势查询与修改

#### ListAllGestures

列出所有手势。

- **功能**：返回系统中所有已注册的手势信息列表
- **触发条件**：控制中心手势设置页面加载手势列表时调用
- **输入参数**：无
- **返回值**：`a(GestureInfo)`：手势信息数组
- **使用场景**：控制中心手势设置页面加载手势列表时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1 \
  --method org.deepin.dde.Gesture1.ListAllGestures
```

#### ModifyGesture

修改手势动作。

- **功能**：将指定手势 ID 绑定的动作修改为新动作
- **触发条件**：用户在控制中心修改手势绑定的操作时调用
- **输入参数**：`id`（string, 类型 `s`）：手势 ID；`action`（string 数组, 类型 `as`）：动作
- **返回值**：`b`（bool）：是否成功
- **使用场景**：用户在控制中心修改手势绑定的操作时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1 \
  --method org.deepin.dde.Gesture1.ModifyGesture "swipe_left_3" ["workspace_next"]
```

#### GetGestureAvaiableActions

获取手势可用动作。

- **功能**：根据动作类型和手指数返回该手势可绑定的所有可用动作列表
- **触发条件**：控制中心手势设置页面展示可选动作列表时调用
- **输入参数**：`actionType`（string, 类型 `s`）：动作类型；`fingerNum`（int32, 类型 `i`）：手指数
- **返回值**：`s`（string）：可用动作 JSON
- **使用场景**：控制中心手势设置页面展示可选动作列表时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1 \
  --method org.deepin.dde.Gesture1.GetGestureAvaiableActions "swipe" 3
```

### 手势信号

#### GestureInfosChanged

手势信息变化时发出。

- **功能**：通知手势配置信息已发生变化
- **参数**：无
- **触发条件**：手势配置被修改或重置时发出
- **使用场景**：UI 监听此信号以刷新手势列表显示

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1
```

#### GestureActivated

手势激活时发出。

- **功能**：通知一个手势被触发并执行了对应动作
- **参数**：`id`（string, 类型 `s`）：手势 ID；`params`（string 数组, 类型 `as`）：参数
- **触发条件**：用户执行触控板手势操作时发出
- **使用场景**：调试或日志记录手势触发情况

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Gesture1 \
  --object-path /org/deepin/dde/Gesture1
```

---
