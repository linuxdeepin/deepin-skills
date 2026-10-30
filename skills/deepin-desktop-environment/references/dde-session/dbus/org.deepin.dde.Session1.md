# org.deepin.dde.Session1 接口参考

该接口在 **Session 总线**上注册，提供会话级管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Session1` |
| Object path | `/org/deepin/dde/Session1` |
| Interface | `org.deepin.dde.Session1` |
| Bus | Session |

### 会话操作

#### Logout

请求退出当前会话管理进程。

- **功能**: 请求会话管理程序退出，不经过 `SessionManager1.RequestLogout` 的注销准备和清理流程。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 会话生命周期管理需要退出管理进程时使用；普通用户注销应调用 `SessionManager1.RequestLogout`。

风险警示：

- 退出会话管理程序会影响当前桌面会话，未保存工作存在丢失风险；此方法不能作为完整注销清理的替代。

```bash
gdbus call --session \
  --dest org.deepin.dde.Session1 \
  --object-path /org/deepin/dde/Session1 \
  --method org.deepin.dde.Session1.Logout
```

#### GetSessionPid

获取 DDE 会话进程 PID。该值以本方法为准；`loginctl` 的 `Leader` 是 logind 会话领导进程，`ps` 按名称找到的进程也不保证是同一对象，不能替代此返回值。只读查询不发送信号、不调用 Logout。

- **功能**: 返回当前会话进程的 PID。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 需要监控会话进程状态、发送信号给会话进程或进行进程级管理时使用。

```bash
gdbus call --session \
  --dest org.deepin.dde.Session1 \
  --object-path /org/deepin/dde/Session1 \
  --method org.deepin.dde.Session1.GetSessionPid
```

#### GetSessionPath

获取会话路径。

- **功能**: 返回当前会话的 D-Bus 对象路径字符串。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 需要获取会话的对象路径以进行后续 D-Bus 操作时使用，例如构造其他接口调用所需的路径参数。

```bash
gdbus call --session \
  --dest org.deepin.dde.Session1 \
  --object-path /org/deepin/dde/Session1 \
  --method org.deepin.dde.Session1.GetSessionPath
```
