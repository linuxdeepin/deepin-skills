# org.freedesktop.Notifications 接口参考

该接口实现 freedesktop.org 桌面通知规范，提供桌面通知的发送、关闭和能力查询功能。dde-shell 的 NotificationManager 在 Session 总线上注册此标准接口，与 `org.deepin.dde.Notification1` 共用同一对象实例。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.Notifications` |
| Object path | `/org/freedesktop/Notifications` |
| Interface | `org.freedesktop.Notifications` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

## 方法

### GetCapabilities

获取通知服务器支持的能力列表。

- **输入参数**: 无
- **返回值**: `as`（string 数组）：能力名称列表

```bash
gdbus call --session \
  --dest org.freedesktop.Notifications \
  --object-path /org/freedesktop/Notifications \
  --method org.freedesktop.Notifications.GetCapabilities
```

### Notify

发送桌面通知，或使用已有通知 ID 替换通知。

- **输入参数**:
  - `appName`（string, 类型 `s`）：应用名称
  - `replacesId`（uint, 类型 `u`）：要替换的通知 ID，`0` 表示创建新通知
  - `appIcon`（string, 类型 `s`）：应用图标路径或图标名称
  - `summary`（string, 类型 `s`）：通知标题
  - `body`（string, 类型 `s`）：通知正文
  - `actions`（string 数组, 类型 `as`）：动作键与动作标题组成的列表
  - `hints`（字典, 类型 `a{sv}`）：通知提示信息
  - `expireTimeout`（int32, 类型 `i`）：超时时间，单位为毫秒；`-1` 使用服务器默认值
- **返回值**: `u`（uint）：通知 ID

```bash
gdbus call --session \
  --dest org.freedesktop.Notifications \
  --object-path /org/freedesktop/Notifications \
  --method org.freedesktop.Notifications.Notify \
  "my-app" 0 "dialog-information" "通知标题" "通知正文" \
  "[]" "{}" 5000
```

### CloseNotification

关闭指定通知。

- **输入参数**:
  - `id`（uint, 类型 `u`）：通知 ID
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.Notifications \
  --object-path /org/freedesktop/Notifications \
  --method org.freedesktop.Notifications.CloseNotification 1
```

### GetServerInformation

获取通知服务器的名称、厂商、版本和所实现的通知规范版本。

- **输入参数**: 无
- **返回值**: `(ssss)`：服务器名称、厂商、版本、通知规范版本

```bash
gdbus call --session \
  --dest org.freedesktop.Notifications \
  --object-path /org/freedesktop/Notifications \
  --method org.freedesktop.Notifications.GetServerInformation
```

## 信号

### ActionInvoked

用户触发通知动作时发出。

- **参数**:
  - `id`（uint, 类型 `u`）：通知 ID
  - `actionKey`（string, 类型 `s`）：动作键

```bash
gdbus monitor --session \
  --dest org.freedesktop.Notifications \
  --object-path /org/freedesktop/Notifications
```

### NotificationClosed

通知关闭时发出。

- **参数**:
  - `id`（uint, 类型 `u`）：通知 ID
  - `reason`（uint, 类型 `u`）：关闭原因；`1` 表示过期，`2` 表示用户关闭，`3` 表示调用方关闭，`4` 表示原因未定义

```bash
gdbus monitor --session \
  --dest org.freedesktop.Notifications \
  --object-path /org/freedesktop/Notifications
```

---
