# org.deepin.dde.Keyboard1 接口参考

该接口提供当前会话的键盘布局指示器查询和布局选择菜单。`layout` 属性保存指示器显示值；直接写入该属性不修改实际输入布局。用户在菜单中选择布局后才向键盘后端发起切换。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Keyboard1` |
| Object path | `/org/deepin/dde/Keyboard1` |
| Interface | `org.deepin.dde.Keyboard1` |
| Bus | Session |
### 键盘布局操作

#### onClicked

在指定坐标位置弹出键盘布局切换菜单。

- **功能**: 在指定坐标位置弹出键盘布局切换菜单，仅当用户已配置的布局数量 ≥ 2 且 fcitx 输入法未运行时才弹出菜单
- **输入参数**: `button`（int32, 类型 `i`）：按钮（当前未被使用）；`x`（int32, 类型 `i`）：X 坐标；`y`（int32, 类型 `i`）：Y 坐标
- **返回值**: 无
- **触发条件**: 当前端点击任务栏键盘布局指示器时调用
- **使用场景**: 当用户需要切换当前键盘布局时使用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keyboard1 \
  --object-path /org/deepin/dde/Keyboard1 \
  --method org.deepin.dde.Keyboard1.onClicked 1 100 200
```
### 键盘属性

#### layout（属性）

当前键盘布局指示器的显示值。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |

- **功能**: 获取或更新指示器显示文字，布局数量 < 2 时返回空字符串；实际布局值由键盘后端更新
- **触发条件**: 读取时返回指示器值，设置时只更新缓存并发出 `layoutChanged` 信号
- **使用场景**: 前端读取或更新任务栏指示器文字；实际输入布局切换由键盘后端负责

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Keyboard1 \
  --object-path /org/deepin/dde/Keyboard1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Keyboard1 layout
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Keyboard1 \
  --object-path /org/deepin/dde/Keyboard1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Keyboard1 layout "<'us'>"
```
#### fcitxRunning（属性）

指示 fcitx 输入法是否正在运行。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

- **功能**: 指示 fcitx 输入法是否正在运行
- **触发条件**: 读取时返回 fcitx 当前运行状态
- **使用场景**: 前端据此决定是否显示键盘布局指示器

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Keyboard1 \
  --object-path /org/deepin/dde/Keyboard1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Keyboard1 fcitxRunning
```

### 键盘信号

#### layoutChanged

键盘布局变化时发出。

- **功能**: 通知键盘布局指示器的显示值变化，不代表实际输入布局已完成切换
- **参数**: `text`（string, 类型 `s`）：新的指示器显示值
- **触发条件**: 键盘后端更新布局指示器，或调用方写入 `layout` 属性后发出
- **使用场景**: 当需要监听键盘布局切换事件并更新 UI 显示（如任务栏布局指示器）时使用

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keyboard1 \
  --object-path /org/deepin/dde/Keyboard1
```

#### fcitxStatusChanged

fcitx 运行状态变化时发出。

- **功能**: 通知 fcitx 输入法的运行状态发生变化
- **参数**: `running`（bool, 类型 `b`）：是否正在运行
- **触发条件**: fcitx 启动或停止时发出
- **使用场景**: 当需要监听 fcitx 输入法框架的启停状态并更新 UI 显示时使用

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keyboard1 \
  --object-path /org/deepin/dde/Keyboard1
```

---
