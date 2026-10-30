# org.deepin.dde.Clipboard1 接口参考

该接口在 Session 总线上注册，对象路径为 `/org/deepin/dde/Clipboard1`，用于控制 DDE 剪贴板前端服务的显示状态，提供剪贴板窗口的切换、显示和隐藏能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Clipboard1` |
| Object path | `/org/deepin/dde/Clipboard1` |
| Interface | `org.deepin.dde.Clipboard1` |
| Bus | Session |

## 方法

### Toggle

**功能**：切换剪贴板窗口的显示状态。若窗口当前隐藏则显示，若当前显示则隐藏。

**触发条件**：由外部 D-Bus 调用触发，通常由 Dock 剪贴板插件或快捷键调用。

**使用场景**：用户点击 Dock 栏的剪贴板图标时，通过此方法切换剪贴板窗口的显示/隐藏状态。

用例：
```bash
dbus-send --session --print-reply \
  --dest=org.deepin.dde.Clipboard1 \
  /org/deepin/dde/Clipboard1 \
  org.deepin.dde.Clipboard1.Toggle
```

### Show

**功能**：显示剪贴板窗口。若窗口已显示则不产生额外效果。

**触发条件**：由外部 D-Bus 调用触发。

**使用场景**：其他组件需要主动弹出剪贴板窗口时调用，例如从其他应用跳转到剪贴板管理界面。

用例：
```bash
dbus-send --session --print-reply \
  --dest=org.deepin.dde.Clipboard1 \
  /org/deepin/dde/Clipboard1 \
  org.deepin.dde.Clipboard1.Show
```

### Hide

**功能**：隐藏剪贴板窗口。若窗口已隐藏则不产生额外效果。

**触发条件**：由外部 D-Bus 调用触发。

**使用场景**：其他组件需要主动关闭剪贴板窗口时调用，例如用户点击窗口外部区域或切换到其他应用时由窗口管理逻辑触发。

用例：
```bash
dbus-send --session --print-reply \
  --dest=org.deepin.dde.Clipboard1 \
  /org/deepin/dde/Clipboard1 \
  org.deepin.dde.Clipboard1.Hide
```

## 属性

### clipboardVisible

**功能**：剪贴板窗口当前的可见状态。

**触发条件**：当通过 Toggle、Show、Hide 方法或窗口管理逻辑导致剪贴板窗口显示/隐藏状态切换时，此属性值随之更新。

**使用场景**：其他组件可通过读取此属性判断剪贴板窗口是否处于显示状态，以决定是否需要调用 Show 或 Hide 方法。

| 属性 | 值 |
|------|------|
| 类型 | bool |
| 访问权限 | read |

用例：
```bash
dbus-send --session --print-reply \
  --dest=org.deepin.dde.Clipboard1 \
  /org/deepin/dde/Clipboard1 \
  org.freedesktop.DBus.Properties.Get \
  string:"org.deepin.dde.Clipboard1" \
  string:"clipboardVisible"
```

## 信号

### clipboardVisibleChanged

**功能**：剪贴板窗口可见状态发生变化时发出，携带最新的可见状态。

**触发条件**：当剪贴板窗口通过 Toggle、Show、Hide 方法或用户交互导致显示/隐藏状态切换时发出。

**使用场景**：其他组件需要监听剪贴板窗口的显示状态变化，例如 Dock 剪贴板插件根据此信号更新图标的激活状态。

参数：
- `visible`（bool）：当前是否可见，`true` 表示可见，`false` 表示不可见

用例：
```bash
dbus-monitor --session \
  "type='signal',interface='org.deepin.dde.Clipboard1',member='clipboardVisibleChanged'"
```
