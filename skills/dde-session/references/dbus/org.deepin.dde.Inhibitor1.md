# org.deepin.dde.Inhibitor1 接口参考

该接口在 **Session 总线**上动态注册，提供会话抑制器的详情查询能力。每个抑制器对象由 `SessionManager1.Inhibit` 方法创建，通过 `SessionManager1.GetInhibitors` 方法可获取所有已注册抑制器的对象路径列表。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.SessionManager1` |
| Object path | `/org/deepin/dde/Inhibitors/Inhibitor_<index>`（`<index>` 为抑制器序号，从 0 开始递增） |
| Interface | `org.deepin.dde.Inhibitor1` |
| Bus | Session |

### GetAppId

获取抑制器的应用 ID。

- **功能**: 返回注册该抑制器时传入的应用 ID 字符串，标识发起抑制操作的应用。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 需要识别是哪个应用注册了该抑制器时使用，例如在抑制状态列表中显示应用名称。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/Inhibitors/Inhibitor_0 \
  --method org.deepin.dde.Inhibitor1.GetAppId
```

### GetClientId

获取抑制器的客户端对象路径。

- **功能**: 返回该抑制器的客户端对象路径，用于标识抑制器在 D-Bus 上的唯一客户端标识。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 需要获取抑制器的 D-Bus 客户端路径以进行进一步操作或标识时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/Inhibitors/Inhibitor_0 \
  --method org.deepin.dde.Inhibitor1.GetClientId
```

### GetFlags

获取抑制器的抑制 flags。

- **功能**: 返回注册该抑制器时传入的位掩码 flags，标识该抑制器阻止的操作类型。flags 取值：`1` 注销、`2` 用户切换、`4` 会话或系统休眠、`8` 会话闲置，多个操作可通过按位或组合。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 需要查询某个抑制器阻止了哪些操作时使用，例如在状态栏显示抑制详情。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/Inhibitors/Inhibitor_0 \
  --method org.deepin.dde.Inhibitor1.GetFlags
```

### GetReason

获取抑制器的抑制原因。

- **功能**: 返回注册该抑制器时传入的原因字符串，描述为何需要抑制相应操作。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 需要向用户展示抑制原因时使用，例如在电源操作被抑制时提示用户原因。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/Inhibitors/Inhibitor_0 \
  --method org.deepin.dde.Inhibitor1.GetReason
```

### GetToplevelXid

获取抑制器的顶层窗口 XID。

- **功能**: 返回注册该抑制器时传入的顶层窗口 XID（X Window Identifier），用于关联抑制操作与具体的窗口。在 Wayland 环境下该值可能为 0。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 需要将抑制器关联到特定窗口时使用，例如在窗口管理中标识发起抑制的窗口。

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionManager1 \
  --object-path /org/deepin/dde/Inhibitors/Inhibitor_0 \
  --method org.deepin.dde.Inhibitor1.GetToplevelXid
```
