# org.freedesktop.impl.portal.GlobalShortcuts 接口参考

该接口提供全局快捷键会话创建和绑定能力，允许沙箱应用注册全局快捷键并接收快捷键触发事件。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.GlobalShortcuts` |
| Bus | Session |

### 属性

| 属性名 | 类型 | 权限 | 说明 |
|--------|------|------|------|
| `version` | `u` | read | 接口版本号 |

### 全局快捷键方法

#### CreateSession

创建全局快捷键会话。

- **功能**: 为沙箱应用创建一个全局快捷键会话，后续的快捷键绑定和查询操作需基于此会话进行。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求创建全局快捷键会话时触发。
- **使用场景**: 沙箱应用需要注册系统级全局快捷键时，首先调用此方法建立会话。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`session_handle`（object path, 类型 `o`）：会话句柄；`app_id`（string, 类型 `s`）：应用 ID；`options`（字典, 类型 `a{sv}`）：选项
- **返回值**: `u`（uint）：响应码；`results`（字典, 类型 `a{sv}`）：会话创建结果

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.GlobalShortcuts.CreateSession "/" "/" "app" {}
```

#### BindShortCuts

绑定全局快捷键。

- **功能**: 将指定的快捷键绑定到当前会话，绑定后当用户按下对应快捷键时将通过信号通知应用。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求绑定全局快捷键时触发。
- **使用场景**: 沙箱应用需要监听特定全局快捷键（如音量调节、自定义快捷键）时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`session_handle`（object path, 类型 `o`）：会话句柄；`shortcuts`（字典, 类型 `a{sv}`）：快捷键描述；`parent_window`（string, 类型 `s`）：父窗口标识；`options`（字典, 类型 `a{sv}`）：选项
- **返回值**: `a{sv}`（字典）：绑定结果

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.GlobalShortcuts.BindShortCuts "/" "/" {} "" {}
```

#### ListShortCuts

列出已绑定的全局快捷键。

- **功能**: 返回当前会话中已绑定的所有全局快捷键列表。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端查询已绑定的快捷键时触发。
- **使用场景**: 沙箱应用需要确认当前已注册的快捷键列表时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`session_handle`（object path, 类型 `o`）：会话句柄
- **返回值**: `a{sv}`（字典）：已绑定的快捷键列表

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.GlobalShortcuts.ListShortCuts "/" "/"
```
