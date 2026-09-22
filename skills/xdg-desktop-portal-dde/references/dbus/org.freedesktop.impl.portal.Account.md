# org.freedesktop.impl.portal.Account 接口参考

该接口提供用户信息查询能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Account` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 账户方法

#### GetUserInformation

获取用户信息。

- **输入参数**: `parent_handle`（object, 类型 `o`）：父窗口句柄；`app_id`（string, 类型 `s`）：应用 ID；`options`（字典, 类型 `a{sv}`）：选项
- **返回值**: `o`（object path）：请求路径

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Account.GetUserInformation "" "app" {}
```

