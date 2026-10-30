# org.deepin.dde.LockService1 接口参考

管理登录界面记录的选中用户名。该接口不直接启动锁屏，不负责创建或切换登录会话，也不验证密码。真实会话切换与锁屏应使用相应会话服务或认证前端。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.LockService1` |
| Object path | `/org/deepin/dde/LockService1` |
| Interface | `org.deepin.dde.LockService1` |
| Bus | System |

服务在登录界面环境运行。总线策略允许客户端调用下列方法，不能仅因使用 System 总线而给所有调用添加客户端提权。

## 登录用户选择

### CurrentUser

- **功能**：读取登录界面保存的选中用户名，不表示当前活动会话用户。
- **输入参数**：无。
- **返回值**：`s`：保存的用户名；读取失败时返回 D-Bus 错误。
- **使用场景**：恢复登录界面此前的用户选择。

```bash
gdbus call --system \
  --dest org.deepin.dde.LockService1 \
  --object-path /org/deepin/dde/LockService1 \
  --method org.deepin.dde.LockService1.CurrentUser
```

### SwitchToUser

- **功能**：保存指定用户名为登录界面的选择，不直接切换活动会话。
- **输入参数**：`username`（`s`）：实际目标用户名。
- **返回值**：无；保存失败时返回 D-Bus 错误。
- **使用场景**：登录界面选择用户并保存该选择。

```bash
gdbus call --system \
  --dest org.deepin.dde.LockService1 \
  --object-path /org/deepin/dde/LockService1 \
  --method org.deepin.dde.LockService1.SwitchToUser \
  "${greeter_username:?请提供登录界面要选中的实际用户名}"
```

### UserChanged

保存不同用户名后，在此前已有非空选择时发出 `UserChanged(username s)`；相同用户名不重复通知。

```bash
gdbus monitor --system \
  --dest org.deepin.dde.LockService1 \
  --object-path /org/deepin/dde/LockService1
```
