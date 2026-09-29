# org.freedesktop.impl.portal.Account 接口参考

该接口提供用户信息查询能力，允许沙箱应用获取当前登录用户的基本信息。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Account` |
| Bus | Session |

### 账户方法

#### GetUserInformation

获取当前登录用户的信息。

- **功能**: 从系统 Accounts 服务读取当前用户的信息，返回用户 ID、显示名称和头像路径。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求用户信息时触发。
- **使用场景**: 沙箱应用需要获取当前用户的用户名、显示名称、头像用于显示用户身份信息时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`app_id`（string, 类型 `s`）：应用 ID；`window`（string, 类型 `s`）：父窗口标识；`options`（字典, 类型 `a{sv}`）：选项（可包含 `reason` 字段说明获取用户信息的原因）
- **返回值**: `u`（uint）：响应码；`results`（字典, 类型 `a{sv}`）：用户信息（包含 `id`、`name`、`image`）

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Account.GetUserInformation "/" "app" "" {}
```
