# org.deepin.dde.Launcher1 接口参考

该接口提供启动器的显示、隐藏、切换和模式控制能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Launcher1` |
| Object path | `/org/deepin/dde/Launcher1` |
| Interface | `org.deepin.dde.Launcher1` |
| Bus | Session |

该接口在 Session 总线上注册，由 dde-shell 加载 dde-launchpad applet 后程序化注册，同时提供 DBus service activation 文件（`org.deepin.dde.Launcher1.service`），支持 DBus 自动激活。

### 启动器显示控制

#### Exit

退出启动器。

- **功能**：关闭启动器窗口并退出启动器界面。
- **触发条件**：由外部调用方主动调用，通常在需要通过编程方式关闭启动器时触发。
- **使用场景**：桌面环境组件（如快捷键管理、任务栏）需要在特定操作后关闭启动器界面时调用。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1 \
  --method org.deepin.dde.Launcher1.Exit
```

#### Show

显示启动器。

- **功能**：打开并显示启动器界面。
- **触发条件**：由外部调用方主动调用，通常在需要通过编程方式弹出启动器时触发。
- **使用场景**：桌面环境组件（如快捷键管理、任务栏按钮）需要打开启动器界面时调用。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1 \
  --method org.deepin.dde.Launcher1.Show
```

#### Hide

隐藏启动器。

- **功能**：隐藏启动器界面，不退出启动器进程。
- **触发条件**：由外部调用方主动调用，通常在需要通过编程方式收起启动器时触发。
- **使用场景**：桌面环境组件（如快捷键管理、窗口切换）需要临时收起启动器界面时调用。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1 \
  --method org.deepin.dde.Launcher1.Hide
```

#### Toggle

切换启动器显示状态。

- **功能**：在显示和隐藏状态之间切换启动器界面。
- **触发条件**：由外部调用方主动调用，通常在用户按下启动器快捷键时触发。
- **使用场景**：快捷键管理组件在用户按下启动器热键时调用，实现按一次打开、再按一次关闭的切换行为。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1 \
  --method org.deepin.dde.Launcher1.Toggle
```

#### ShowByMode

按指定模式显示启动器。

- **功能**：按指定模式显示启动器（接口定义 mode 为 0 表示全屏模式，1 表示窗口模式）。注意：当前实现为空操作，不实际改变启动器显示状态，此方法可能已被废弃。
- **触发条件**：由外部调用方主动调用，通常在需要以特定模式弹出启动器时触发。
- **使用场景**：桌面环境组件需要以全屏或窗口模式打开启动器时调用（例如根据屏幕尺寸或用户偏好选择模式）。

- **输入参数**: `mode`（int64, 类型 `x`）：显示模式，0 为全屏模式，1 为窗口模式
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1 \
  --method org.deepin.dde.Launcher1.ShowByMode 'int64 1'
```

### 启动器属性

#### Visible（属性）

启动器是否可见。

- **功能**：标识当前启动器界面是否处于可见状态。
- **触发条件**：启动器显示或隐藏时该属性值发生变化，同时触发 `VisibleChanged` 信号。
- **使用场景**：外部组件需要查询启动器当前可见状态以决定后续操作时读取该属性。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Launcher1 Visible
```

### 启动器信号

#### Closed

启动器关闭时发出。

- **功能**：通知启动器界面已关闭。
- **触发条件**：启动器可见状态变为 false 时发出，通常由 Hide 或 Toggle 方法调用触发，也可由用户操作（如点击窗口外部、按 Esc 键）触发。
- **使用场景**：外部组件（如任务栏）需要在启动器关闭后更新自身状态时监听该信号。

- **参数**: 无

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1
```

#### Shown

启动器显示时发出。

- **功能**：通知启动器界面已显示。
- **触发条件**：启动器界面被显示（通过 Show 或 Toggle 方法调用）后发出。
- **使用场景**：外部组件（如任务栏）需要在启动器显示后更新自身状态时监听该信号。

- **参数**: 无

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1
```

#### VisibleChanged

启动器可见状态变化时发出。

- **功能**：通知启动器的可见状态发生了变化，携带新的可见状态值。
- **触发条件**：启动器显示或隐藏导致 `Visible` 属性值变化时发出。
- **使用场景**：外部组件需要实时感知启动器可见状态变化并做出响应时监听该信号。

- **参数**: `visible`（bool, 类型 `b`）：是否可见

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Launcher1 \
  --object-path /org/deepin/dde/Launcher1
```

