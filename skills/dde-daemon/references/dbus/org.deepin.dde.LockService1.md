# org.deepin.dde.LockService1 接口参考

该接口提供锁屏和用户切换能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.LockService` |
| Object path | `/com/deepin/daemon/LockService` |
| Interface | `org.deepin.dde.LockService1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 锁屏服务方法

#### CurrentUser

获取当前用户。

- **输入参数**: 无
- **返回值**: `s`（string）：当前用户名

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.LockService \
  --object-path /com/deepin/daemon/LockService \
  --method org.deepin.dde.LockService1.CurrentUser
```

#### SwitchToUser

切换到指定用户。

- **输入参数**: `name`（string, 类型 `s`）：用户名
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.LockService \
  --object-path /com/deepin/daemon/LockService \
  --method org.deepin.dde.LockService1.SwitchToUser "user"
```

