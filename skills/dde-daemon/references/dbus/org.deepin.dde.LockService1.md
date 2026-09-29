# org.deepin.dde.LockService1 接口参考

该接口提供锁屏和用户切换能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.LockService1` |
| Object path | `/org/deepin/dde/LockService1` |
| Interface | `org.deepin.dde.LockService1` |
| Bus | System |
### 锁屏服务方法

#### CurrentUser

获取当前用户。

- **功能**：获取当前登录的用户名。
- **触发条件**：当锁屏服务需要确定当前用户以显示锁屏界面时调用。
- **使用场景**：锁屏界面显示当前用户信息。

- **输入参数**: 无
- **返回值**: `s`（string）：当前用户名

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.LockService1 \
  --object-path /org/deepin/dde/LockService1 \
  --method org.deepin.dde.LockService1.CurrentUser
```

#### SwitchToUser

切换到指定用户。

- **功能**：切换到指定用户会话。
- **触发条件**：当用户在锁屏界面选择切换用户时调用。
- **使用场景**：锁屏界面用户切换、多用户环境快速切换。

- **输入参数**: `name`（string, 类型 `s`）：用户名
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.LockService1 \
  --object-path /org/deepin/dde/LockService1 \
  --method org.deepin.dde.LockService1.SwitchToUser "user"
```

