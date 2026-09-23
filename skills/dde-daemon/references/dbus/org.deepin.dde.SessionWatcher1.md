# org.deepin.dde.SessionWatcher1 接口参考

该接口提供会话状态监控能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.SessionWatcher` |
| Object path | `/com/deepin/daemon/SessionWatcher` |
| Interface | `org.deepin.dde.SessionWatcher1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 会话监控属性

#### Locked（属性）

会话是否锁定。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.SessionWatcher \
  --object-path /com/deepin/daemon/SessionWatcher \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SessionWatcher1 Locked
```

### 会话监控信号

#### Unlock

会话解锁时发出。

- **参数**: 无
- **触发条件**: 会话解锁时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.SessionWatcher \
  --object-path /com/deepin/daemon/SessionWatcher
```

