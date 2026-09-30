# org.deepin.dde.shell.notification.center 接口参考

该接口提供通知中心面板的显示控制能力，支持切换、显示和隐藏通知中心。此接口在 Session 总线上注册，对象路径为 `/org/deepin/dde/shell/notification/center`。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | 无独立 service name，由 dde-shell 进程在 Session 总线上注册 |
| Object path | `/org/deepin/dde/shell/notification/center` |
| Interface | `org.deepin.dde.shell.notification.center` |
| Bus | Session |

> 注意：`--dest` 指定的服务名默认为 `org.deepin.dde.shell`，但实际服务名可能因 dde-shell 启动参数不同而变化（也可能是 `org.deepin.dde.shell.<category>` 或 `org.deepin.dde.shell.random<pid>`）。请根据实际情况调整。

## 接口关系

dde-shell 的通知中心面板还注册了以下旧版兼容接口：

- `org.deepin.dde.Widgets1`（`/org/deepin/dde/Widgets1`）— 旧版通知中心窗口控制接口。

**兼容关系**：`org.deepin.dde.Widgets1` 为兼容旧版调用方而保留，提供与 `org.deepin.dde.shell.notification.center` 相同的 Toggle/Show/Hide 方法和 VisibleChanged 信号，功能无差异。新代码应优先使用 `org.deepin.dde.shell.notification.center`。

## 方法

### Toggle

切换通知中心显示状态：若当前可见则隐藏，若当前隐藏则显示。

- **功能**: 切换通知中心面板的显示与隐藏状态
- **触发条件**: 外部程序调用此方法时执行；执行后会触发 `VisibleChanged` 信号
- **使用场景**: 任务栏或快捷键触发通知中心切换显示
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.shell \
  --object-path /org/deepin/dde/shell/notification/center \
  --method org.deepin.dde.shell.notification.center.Toggle
```

### Show

显示通知中心。

- **功能**: 显示通知中心面板
- **触发条件**: 外部程序调用此方法时执行；执行后会触发 `VisibleChanged` 信号
- **使用场景**: 任务栏点击通知图标后显示通知中心
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.shell \
  --object-path /org/deepin/dde/shell/notification/center \
  --method org.deepin.dde.shell.notification.center.Show
```

### Hide

隐藏通知中心。

- **功能**: 隐藏通知中心面板
- **触发条件**: 外部程序调用此方法时执行；执行后会触发 `VisibleChanged` 信号
- **使用场景**: 用户点击通知中心外部区域或按 Esc 键后隐藏通知中心
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.shell \
  --object-path /org/deepin/dde/shell/notification/center \
  --method org.deepin.dde.shell.notification.center.Hide
```

## 信号

### VisibleChanged

通知中心可见状态变化时发出。

- **功能**: 通知外部程序通知中心面板的可见状态发生了变化，传递新的可见状态
- **触发条件**: 调用 Toggle/Show/Hide 方法后触发
- **使用场景**: 任务栏根据通知中心显示状态更新通知图标的高亮状态
- **参数**:
  - `visible`（bool, 类型 `b`）：是否可见

```bash
gdbus monitor --session \
  --dest org.deepin.dde.shell \
  --object-path /org/deepin/dde/shell/notification/center
```

---
