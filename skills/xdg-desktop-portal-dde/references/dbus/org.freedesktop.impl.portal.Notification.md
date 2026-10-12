# org.freedesktop.impl.portal.Notification 接口参考

该接口仅作用于 portal 通道的通知发送与移除，允许沙箱应用通过 Portal 接口发送桌面通知并接收通知交互回调。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Notification` |
| Bus | Session |

### 通知方法

#### AddNotification

添加桌面通知。

- **功能**: 将指定通知内容转发到桌面通知服务（`org.freedesktop.Notifications`）进行展示。通知内容字典支持的键包括：`title`（通知标题）、`body`（通知正文）、`icon`（通知图标）、`default-action`（默认动作名称）、`default-action-target`（默认动作参数）、`buttons`（按钮列表，每个按钮为包含 `label` 键的字典）。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求发送桌面通知时触发。
- **使用场景**: 沙箱应用需要向用户展示桌面通知（如消息提醒、下载完成提示）时使用。
- **输入参数**: `app_id`（string, 类型 `s`）：应用 ID；`id`（string, 类型 `s`）：通知 ID（用于后续移除通知）；`notification`（字典, 类型 `a{sv}`）：通知内容（包含 `title`、`body`、`icon`、`default-action`、`default-action-target`、`buttons`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Notification.AddNotification "app" "notif1" "{'title': <'测试通知'>, 'body': <'通知正文'>, 'icon': <'dialog-information'>}"
```

#### RemoveNotification

移除桌面通知。

- **功能**: 根据 `app_id` 和通知 ID 移除已发送的桌面通知。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求移除已发送的通知时触发。
- **使用场景**: 沙箱应用需要撤回之前发送的通知时使用。
- **输入参数**: `app_id`（string, 类型 `s`）：应用 ID；`id`（string, 类型 `s`）：通知 ID
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Notification.RemoveNotification "app" "notif1"
```

### 信号

#### ActionInvoked

通知动作触发信号。

- **功能**: 当用户点击通知上的按钮或默认动作时，通知服务回调触发此信号，通知沙箱应用用户已与通知进行交互。
- **触发条件**: 当用户在通知上点击按钮或执行默认动作时，由通知服务回调触发。
- **使用场景**: 沙箱应用发送通知后，需要响应用户对通知的点击操作（如点击"回复"按钮打开对话窗口）时监听此信号。
- **参数**: `app_id`（string, 类型 `s`）：应用 ID；`id`（string, 类型 `s`）：通知 ID；`action`（string, 类型 `s`）：动作名称（`default` 表示默认动作，其他为按钮对应的动作）；`parameter`（变体数组, 类型 `av`）：动作参数
