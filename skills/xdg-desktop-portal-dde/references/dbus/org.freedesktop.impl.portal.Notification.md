# org.freedesktop.impl.portal.Notification 接口参考

该接口提供桌面通知发送和移除能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Notification` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 通知方法

#### Add

添加通知。

- **输入参数**: `parent_handle`（object, 类型 `o`）：父窗口句柄；`id`（string, 类型 `s`）：通知 ID；`notification`（字典, 类型 `a{sv}`）：通知内容
- **返回值**: `o`（object path）：请求路径

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Notification.Add "" "notif1" {}
```

#### Remove

移除通知。

- **输入参数**: `id`（string, 类型 `s`）：通知 ID
- **返回值**: `o`（object path）：请求路径

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Notification.Remove "notif1"
```

