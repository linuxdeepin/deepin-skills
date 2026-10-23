# org.deepin.dde.WMSwitcher1 接口参考

该接口在 **Session 总线**上注册，提供 X11 合成能力查询、兼容状态标签及窗口特效选择请求。Wayland 下不支持此切换流程。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.WMSwitcher1` |
| Object path | `/org/deepin/dde/WMSwitcher1` |
| Interface | `org.deepin.dde.WMSwitcher1` |
| Bus | Session |

### 窗口管理器操作

#### AllowSwitch

查询当前 X11 窗口管理器是否支持合成。

- **功能**: X11 下返回当前窗口管理器是否支持合成；Wayland 下返回 false。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 在提供窗口管理器切换功能前，先检查当前系统是否支持切换，用于控制 UI 中切换按钮的显示状态。

```bash
gdbus call --session \
  --dest org.deepin.dde.WMSwitcher1 \
  --object-path /org/deepin/dde/WMSwitcher1 \
  --method org.deepin.dde.WMSwitcher1.AllowSwitch
```

#### CurrentWM

获取当前 X11 合成状态的兼容标签。

- **功能**: X11 下根据合成启用状态返回兼容标签 `deepin wm` 或 `deepin metacity`；Wayland 下返回空字符串。该标签不是实际窗口管理器可执行文件名。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 需要显示当前使用的窗口管理器信息，或根据当前窗口管理器类型执行不同逻辑时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.WMSwitcher1 \
  --object-path /org/deepin/dde/WMSwitcher1 \
  --method org.deepin.dde.WMSwitcher1.CurrentWM
```

#### RequestSwitchWM

请求显示窗口特效选择界面。

- **功能**: X11 下发送 `SwitchWM` OSD 请求，显示窗口特效选择界面，由相应桌面组件处理选择；Wayland 下不执行操作。不接受目标窗口管理器参数，也不保证替换正在运行的窗口管理器。
- **触发条件**: 由调用方主动调用；请求返回不表示合成状态已经改变。
- **使用场景**: 当前 X11 桌面需要通过窗口特效界面选择效果等级时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.WMSwitcher1 \
  --object-path /org/deepin/dde/WMSwitcher1 \
  --method org.deepin.dde.WMSwitcher1.RequestSwitchWM
```

### 窗口管理器信号

#### WMChanged

合成启用状态变化时发出。

- **功能**: 通知合成启用状态对应的兼容标签变化。
- **参数**: `wmName`（string, 类型 `s`）：合成状态标签（`deepin wm` 或 `deepin metacity`）
- **触发条件**: 当前窗口管理器报告合成启用状态变化时发出。
- **使用场景**: 需要在合成状态变化后更新 UI 指示的应用监听此信号。

```bash
gdbus monitor --session \
  --dest org.deepin.dde.WMSwitcher1 \
  --object-path /org/deepin/dde/WMSwitcher1
```
