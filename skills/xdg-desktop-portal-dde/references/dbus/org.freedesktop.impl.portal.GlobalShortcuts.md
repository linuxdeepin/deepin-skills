# org.freedesktop.impl.portal.GlobalShortcuts 接口参考

该接口提供全局快捷键会话创建和绑定能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.GlobalShortcuts` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 全局快捷键方法

#### CreateSession

创建全局快捷键会话。

- **输入参数**: `parent_handle`（object, 类型 `o`）：父窗口句柄；`options`（字典, 类型 `a{sv}`）：选项
- **返回值**: `o`（object path）：请求路径

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.GlobalShortcuts.CreateSession "" {}
```

#### BindShortcuts

绑定快捷键。

- **输入参数**: `parent_handle`（object, 类型 `o`）：父窗口句柄；`shortcuts`（数组, 类型 `a{sa{sv}}`）：快捷键列表；`options`（字典, 类型 `a{sv}`）：选项
- **返回值**: `o`（object path）：请求路径

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.GlobalShortcuts.BindShortcuts "" {} {}
```

#### ListShortcuts

列出已绑定快捷键。

- **输入参数**: `parent_handle`（object, 类型 `o`）：父窗口句柄
- **返回值**: `o`（object path）：请求路径

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.GlobalShortcuts.ListShortcuts ""
```

