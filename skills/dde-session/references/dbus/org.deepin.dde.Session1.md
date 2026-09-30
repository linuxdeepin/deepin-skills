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

注销当前会话。

- **功能**: 注销当前登录的桌面会话，终止当前用户的会话进程并返回登录界面。
- **触发条件**: 由调用方主动调用触发。
- **使用场景**: 需要通过程序化方式注销当前用户会话时使用，例如脚本自动化注销或第三方应用提供注销按钮。

```bash
gdbus call --session \
  --dest org.deepin.dde.Session1 \
  --object-path /org/deepin/dde/Session1 \
  --method org.deepin.dde.Session1.Logout
```

#### GetSessionPid

获取会话进程 PID。

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
