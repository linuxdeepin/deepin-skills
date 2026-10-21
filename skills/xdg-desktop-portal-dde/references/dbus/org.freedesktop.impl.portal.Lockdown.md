# org.freedesktop.impl.portal.Lockdown 接口参考

该接口报告门户后端的禁用策略状态。属性写入只更新当前后端进程内状态，服务重启后恢复默认值；不修改系统设备权限，也不保证在整个系统范围禁用相应资源。

本文记录 Portal 后端协作接口，普通应用调用前端 `org.freedesktop.portal.Desktop` 的 `org.freedesktop.portal.*` 接口。后端示例中的应用身份与请求句柄必须来自实际前端请求，不能将演示参数用于应用权限判断。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Lockdown` |
| Bus | Session |

### 属性

属性均为 `b`（bool），当前 DDE 后端提供读写，默认 `false`。值用于向门户前端报告策略意图，不等于强制限制任意应用；调试写入不持久化，也不替代管理员权限策略。

| 属性名 | 类型 | 权限 | 说明 |
|--------|------|------|------|
| `disable_printing` | `b` | readwrite | 报告打印禁用状态。 |
| `disable_save_to_disk` | `b` | readwrite | 报告保存到磁盘的禁用状态。 |
| `disable_application_handlers` | `b` | readwrite | 报告应用处理器禁用状态。 |
| `disable_location` | `b` | readwrite | 报告定位禁用状态。 |
| `disable_camera` | `b` | readwrite | 报告摄像头禁用状态。 |
| `disable_microphone` | `b` | readwrite | 报告麦克风禁用状态。 |
| `disable_sound_output` | `b` | readwrite | 报告声音输出禁用状态。 |

### 使用示例

#### 读取所有锁定属性

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.DBus.Properties.GetAll "org.freedesktop.impl.portal.Lockdown"
```

#### 读取单个锁定属性

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.DBus.Properties.Get "org.freedesktop.impl.portal.Lockdown" "disable_printing"
```

#### 调试后端进程内状态

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.DBus.Properties.Set "org.freedesktop.impl.portal.Lockdown" "disable_printing" "<true>"
```
