# org.deepin.dde.SessionWatcher1 接口参考

该接口提供会话状态监控能力，包括获取会话列表和检查 X11 会话是否活跃。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.SessionWatcher1` |
| Object path | `/org/deepin/dde/SessionWatcher1` |
| Interface | `org.deepin.dde.SessionWatcher1` |
| Bus | Session |

### 会话监控属性

#### IsActive（属性）

会话是否活跃。

- **功能**：当前会话是否活跃。
- **触发条件**：属性，当会话活跃状态变化时通过 PropertiesChanged 信号通知。
- **使用场景**：会话状态监控、多会话环境状态同步。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionWatcher1 \
  --object-path /org/deepin/dde/SessionWatcher1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SessionWatcher1 IsActive
```

### 会话监控方法

#### GetSessions

获取当前所有会话的对象路径列表。

- **功能**：获取当前所有活跃会话的对象路径列表。
- **触发条件**：当需要枚举系统中所有活跃会话时调用。
- **使用场景**：会话管理、多用户环境会话列表。

- **输入参数**: 无
- **返回值**: `sessions`（`ao`，[]object_path）：会话对象路径列表

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionWatcher1 \
  --object-path /org/deepin/dde/SessionWatcher1 \
  --method org.deepin.dde.SessionWatcher1.GetSessions
```

#### IsX11SessionActive

检查当前 X11 会话是否活跃。

- **功能**：检查当前 X11 会话是否处于活跃状态。
- **触发条件**：当需要判断当前会话是否为 X11 类型且活跃时调用。
- **使用场景**：会话类型判断、Wayland/X11 兼容处理。

- **输入参数**: 无
- **返回值**: `active`（bool, 类型 `b`）：X11 会话是否活跃

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionWatcher1 \
  --object-path /org/deepin/dde/SessionWatcher1 \
  --method org.deepin.dde.SessionWatcher1.IsX11SessionActive
```
