# org.freedesktop.impl.portal.Inhibit 接口参考

该接口提供会话抑制能力，允许沙箱应用阻止系统执行特定会话管理操作。

本文记录 Portal 后端协作接口，普通应用调用前端 `org.freedesktop.portal.Desktop` 的 `org.freedesktop.portal.*` 接口。后端示例中的应用身份与请求句柄必须来自实际前端请求，不能将演示参数用于应用权限判断。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Inhibit` |
| Bus | Session |

### 属性

| 属性名 | 类型 | 权限 | 说明 |
|--------|------|------|------|
| `version` | `u` | read | 接口版本号 |

### 抑制方法

#### Inhibit

抑制会话管理行为。

- **功能**: 阻止系统执行指定的会话管理操作，底层通过调用 `org.deepin.dde.SessionManager1` 的 Inhibit 方法实现。抑制标志位为位掩码，支持以下取值：`1`（INHIBIT_LOGOUT，禁止登出）、`2`（INHIBIT_SWITCH，禁止用户切换）、`4`（INHIBIT_SUSPEND，禁止挂起）、`8`（INHIBIT_IDLE，禁止空闲）。多个标志可按位或组合使用。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求抑制会话管理操作时触发。
- **使用场景**: 沙箱应用正在执行不可中断的关键操作（如文件下载、系统更新）时，需要阻止系统登出、用户切换、挂起或进入空闲状态。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`app_id`（string, 类型 `s`）：应用 ID；`window`（string, 类型 `s`）：窗口标识；`flags`（uint, 类型 `u`）：抑制标志位（位掩码，取值为 `1`=禁止登出、`2`=禁止用户切换、`4`=禁止挂起、`8`=禁止空闲，可按位或组合）；`options`（字典, 类型 `a{sv}`）：选项（支持 `reason` 键指定抑制原因）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Inhibit.Inhibit "${portal_handle:?请使用前端请求的实际 handle}" "${portal_app_id:?请使用实际请求的应用标识}" "" 4 {}
```

抑制成功后，后端在实际请求 handle 上提供 Request 对象；前端取消该请求时，后端使用保存的 cookie 解除抑制。不能固定 handle 或复用其他请求的对象路径。
