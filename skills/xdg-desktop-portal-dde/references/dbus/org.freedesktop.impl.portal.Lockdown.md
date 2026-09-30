# org.freedesktop.impl.portal.Lockdown 接口参考

该接口提供锁定模式设置能力，通过读写属性来控制各项系统功能的禁用状态。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Lockdown` |
| Bus | Session |

### 属性

所有属性均为 `b`（bool）类型，可读可写。属性值为 `true` 时表示禁用对应功能，`false` 时表示允许使用。

| 属性名 | 类型 | 权限 | 说明 |
|--------|------|------|------|
| `disable_printing` | `b` | readwrite | 禁止打印。设为 `true` 后沙箱应用无法使用打印功能。 |
| `disable_save_to_disk` | `b` | readwrite | 禁止保存到磁盘。设为 `true` 后沙箱应用无法将文件保存到磁盘。 |
| `disable_application_handlers` | `b` | readwrite | 禁止应用处理器。设为 `true` 后沙箱应用无法注册或使用应用处理器。 |
| `disable_location` | `b` | readwrite | 禁止定位。设为 `true` 后沙箱应用无法访问地理位置信息。 |
| `disable_camera` | `b` | readwrite | 禁止摄像头。设为 `true` 后沙箱应用无法访问摄像头设备。 |
| `disable_microphone` | `b` | readwrite | 禁止麦克风。设为 `true` 后沙箱应用无法访问麦克风设备。 |
| `disable_sound_output` | `b` | readwrite | 禁止声音输出。设为 `true` 后沙箱应用无法输出音频。 |

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

#### 设置锁定属性

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.DBus.Properties.Set "org.freedesktop.impl.portal.Lockdown" "disable_printing" "<true>"
```
