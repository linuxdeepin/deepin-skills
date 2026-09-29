# org.deepin.dde.WMSwitcher1 接口参考

该接口在 **Session 总线**上注册，提供窗口管理器查询和切换能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.WMSwitcher1` |
| Object path | `/org/deepin/dde/WMSwitcher1` |
| Interface | `org.deepin.dde.WMSwitcher1` |
| Bus | Session |

### 窗口管理器操作

#### AllowSwitch

查询是否允许切换窗口管理器。

- **功能**: 返回当前系统是否允许切换窗口管理器。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 在提供窗口管理器切换功能前，先检查当前系统是否支持切换，用于控制 UI 中切换按钮的显示状态。

```bash
gdbus call --session \
  --dest org.deepin.dde.WMSwitcher1 \
  --object-path /org/deepin/dde/WMSwitcher1 \
  --method org.deepin.dde.WMSwitcher1.AllowSwitch
```

#### CurrentWM

获取当前窗口管理器名称。

- **功能**: 返回当前正在运行的窗口管理器的名称字符串。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 需要显示当前使用的窗口管理器信息，或根据当前窗口管理器类型执行不同逻辑时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.WMSwitcher1 \
  --object-path /org/deepin/dde/WMSwitcher1 \
  --method org.deepin.dde.WMSwitcher1.CurrentWM
```

#### RequestSwitchWM

请求切换窗口管理器。

- **功能**: 请求将当前窗口管理器切换为另一个可用的窗口管理器。
- **触发条件**: 由调用方主动调用触发；切换完成后会发出 `WMChanged` 信号。
- **使用场景**: 用户在控制中心或第三方应用中主动请求切换窗口管理器时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.WMSwitcher1 \
  --object-path /org/deepin/dde/WMSwitcher1 \
  --method org.deepin.dde.WMSwitcher1.RequestSwitchWM
```

### 窗口管理器信号

#### WMChanged

窗口管理器切换时发出。

- **功能**: 通知窗口管理器已切换为新的窗口管理器。
- **参数**: `wmName`（string, 类型 `s`）：切换后的新窗口管理器名称
- **触发条件**: 窗口管理器切换成功完成后自动发出。
- **使用场景**: 需要在窗口管理器切换后更新 UI 显示或执行初始化逻辑的应用监听此信号。

```bash
gdbus monitor --session \
  --dest org.deepin.dde.WMSwitcher1 \
  --object-path /org/deepin/dde/WMSwitcher1
```
