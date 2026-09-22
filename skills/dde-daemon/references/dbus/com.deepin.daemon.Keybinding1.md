# com.deepin.daemon.Keybinding1 接口参考

该接口提供快捷键绑定、查询和管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `com.deepin.daemon.Keybinding` |
| Object path | `/com/deepin/daemon/Keybinding` |
| Interface | `com.deepin.daemon.Keybinding1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 快捷键管理方法

#### Add

添加快捷键。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID；`type`（string, 类型 `s`）：类型；`keycode`（int32, 类型 `i`）：键码
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.Add "id" "type" 65
```

#### AddCustomShortcut

添加自定义快捷键。

- **输入参数**: `name`（string, 类型 `s`）：名称；`exec`（string, 类型 `s`）：执行命令；`keycode`（int32, 类型 `i`）：键码
- **返回值**: `s`（string）：快捷键 ID

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.AddCustomShortcut "name" "command" 65
```

#### AddShortcutKeystroke

添加快捷键按键。

- **输入参数**: `type`（string, 类型 `s`）：类型；`id`（string, 类型 `s`）：ID；`keystroke`（int32, 类型 `i`）：按键
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.AddShortcutKeystroke "type" "id" 65
```

#### CheckAvaliable

检查快捷键是否可用。

- **输入参数**: `keystroke`（int32, 类型 `i`）：按键
- **返回值**: `b`（bool）：是否可用

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.CheckAvaliable 65
```

#### ClearShortcutKeystrokes

清除快捷键按键。

- **输入参数**: `type`（string, 类型 `s`）：类型；`id`（string, 类型 `s`）：ID
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.ClearShortcutKeystrokes "type" "id"
```

#### Delete

删除快捷键。

- **输入参数**: `type`（string, 类型 `s`）：类型；`id`（string, 类型 `s`）：ID
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.Delete "type" "id"
```

#### DeleteCustomShortcut

删除自定义快捷键。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.DeleteCustomShortcut "id"
```

#### DeleteShortcutKeystroke

删除快捷键按键。

- **输入参数**: `type`（string, 类型 `s`）：类型；`id`（string, 类型 `s`）：ID；`keystroke`（int32, 类型 `i`）：按键
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.DeleteShortcutKeystroke "type" "id" 65
```

#### Disable

禁用快捷键。

- **输入参数**: `type`（string, 类型 `s`）：类型；`id`（string, 类型 `s`）：ID
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.Disable "type" "id"
```

#### EnableSystemShortcut

启用系统快捷键。

- **输入参数**: `id`（string, 类型 `s`）：ID
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.EnableSystemShortcut "id"
```

#### GetCapsLockState

获取大写锁定状态。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否锁定

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.GetCapsLockState
```

#### GetShortcut

获取快捷键信息。

- **输入参数**: `type`（string, 类型 `s`）：类型；`id`（string, 类型 `s`）：ID
- **返回值**: `a{sv}`（字典）：快捷键信息

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.GetShortcut "type" "id"
```

#### GrabScreen

截取屏幕按键。

- **输入参数**: 无
- **返回值**: `i`（int32）：按键码

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.GrabScreen
```

#### List

列出快捷键。

- **输入参数**: 无
- **返回值**: `as`（string 数组）：快捷键列表

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.List
```

#### ListAllShortcuts

列出所有快捷键。

- **输入参数**: 无
- **返回值**: `a{sa{sv}}`（嵌套字典）：快捷键映射

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.ListAllShortcuts
```

#### ListShortcutsByType

按类型列出快捷键。

- **输入参数**: `type`（string, 类型 `s`）：类型
- **返回值**: `a{sa{sv}}`（嵌套字典）：快捷键映射

```bash
gdbus call --session \
  --dest com.deepin.daemon.Keybinding \
  --object-path /com/deepin/daemon/Keybinding \
  --method com.deepin.daemon.Keybinding1.ListShortcutsByType "type"
```

