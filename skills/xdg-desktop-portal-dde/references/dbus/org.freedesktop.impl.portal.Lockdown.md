# org.freedesktop.impl.portal.Lockdown 接口参考

该接口提供锁定模式设置能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Lockdown` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 锁定方法

#### SetLockdown

设置锁定模式。

- **输入参数**: `options`（字典, 类型 `a{sv}`）：锁定选项
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Lockdown.SetLockdown {}
```

