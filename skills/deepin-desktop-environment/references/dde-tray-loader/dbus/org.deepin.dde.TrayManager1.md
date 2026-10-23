# org.deepin.dde.TrayManager1 接口参考

该接口提供托盘图标管理和通知控制能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.TrayManager1` |
| Object path | `/org/deepin/dde/TrayManager1` |
| Interface | `org.deepin.dde.TrayManager1` |
| Bus | Session |
### 托盘操作

#### EnableNotification

启用或禁用指定托盘图标窗口的通知。

- **功能**: 启用或禁用指定托盘图标窗口的通知，控制该窗口的图标变化是否触发 `Changed` 信号
- **输入参数**: `win`（uint32, 类型 `u`）：窗口 ID；`enabled`（bool, 类型 `b`）：是否启用
- **返回值**: 无
- **触发条件**: 当用户需要屏蔽或恢复某个托盘应用通知时调用
- **使用场景**: 当用户希望控制特定托盘应用的通知行为（如屏蔽某个应用的图标变化通知）时使用

```bash
gdbus call --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1 \
  --method org.deepin.dde.TrayManager1.EnableNotification 12345 true
```

#### GetName

获取指定托盘图标窗口的名称。

- **功能**: 通过 X11 窗口 ID 获取托盘图标对应的应用窗口名称
- **输入参数**: `win`（uint32, 类型 `u`）：窗口 ID
- **返回值**: `s`（string）：窗口名称
- **触发条件**: 当需要获取某个托盘图标的显示名称时调用
- **使用场景**: 当需要在 UI 中显示托盘图标对应的应用名称时使用

```bash
gdbus call --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1 \
  --method org.deepin.dde.TrayManager1.GetName 12345
```

#### Manage

请求重新获取 X11 系统托盘选择权。

- **功能**: 请求重新获取 X11 系统托盘选择权（`_NET_SYSTEM_TRAY` selection ownership）
- **输入参数**: 无
- **返回值**: `b`（bool）：始终返回 `true`
- **触发条件**: 当需要重新接管系统托盘管理权时调用
- **使用场景**: 当托盘异常后需要恢复系统托盘管理权时使用

```bash
gdbus call --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1 \
  --method org.deepin.dde.TrayManager1.Manage
```
### 托盘属性

#### TrayIcons（属性）

当前已注册的托盘图标窗口 ID 列表。

| 属性 | 值 |
|------|------|
| 类型 | `au` |
| 读写权限 | read |

- **功能**: 返回当前已注册的托盘图标窗口 ID 列表
- **触发条件**: 读取该属性时返回当前快照
- **使用场景**: 当需要查询当前系统托盘中有哪些图标时使用

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.TrayManager1 TrayIcons
```

### 托盘信号

#### Inited

托盘初始化完成时发出。

- **功能**: 通知托盘管理器已完成初始化，可以接受托盘图标注册
- **参数**: 无
- **触发条件**: 托盘管理器初始化完成时发出
- **使用场景**: 当需要在托盘初始化完成后执行后续操作（如注册新的托盘图标）时监听此信号

```bash
gdbus monitor --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1
```

#### Added

托盘图标添加时发出。

- **功能**: 通知有新的托盘图标被添加到托盘中
- **参数**: `id`（uint32, 类型 `u`）：窗口 ID
- **触发条件**: 有新窗口添加到托盘时发出
- **使用场景**: 当需要监听新托盘图标出现并做出响应（如更新 UI 显示）时使用

```bash
gdbus monitor --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1
```

#### Removed

托盘图标移除时发出。

- **功能**: 通知有托盘图标从托盘中被移除
- **参数**: `id`（uint32, 类型 `u`）：窗口 ID
- **触发条件**: 托盘图标被移除时发出
- **使用场景**: 当需要监听托盘图标消失并做出响应（如更新 UI 显示）时使用

```bash
gdbus monitor --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1
```

#### Changed

托盘图标变化时发出。

- **功能**: 通知某个托盘图标的属性或状态发生变化
- **参数**: `id`（uint32, 类型 `u`）：窗口 ID
- **触发条件**: 托盘图标属性变化时发出（如图标更新、窗口状态改变），仅当该窗口的 `EnableNotification` 为 `true` 时才发出
- **使用场景**: 当需要监听托盘图标变化并刷新对应图标的显示时使用

```bash
gdbus monitor --session \
  --dest org.deepin.dde.TrayManager1 \
  --object-path /org/deepin/dde/TrayManager1
```

---

## 补充说明

dde-tray-loader 的 D-Bus 接口（Keyboard1、TrayManager1）服务名稳定，无历史别名或兼容性接口。
