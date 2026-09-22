# org.deepin.dde.Keybinding1 接口参考

该接口提供快捷键管理能力，包括快捷键查询、自定义快捷键增删改、快捷键冲突处理和快捷键捕获。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Keybinding1` |
| Object path | `/org/deepin/dde/Keybinding1` |
| Interface | `org.deepin.dde.Keybinding1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 快捷键查询

#### ListAllShortcuts

列出所有快捷键。

- **输入参数**: 无
- **返回值**: `a(ShortcutInfo)`：快捷键信息数组

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ListAllShortcuts
```

#### ListShortcutsByApp

按应用列出快捷键。

- **输入参数**: `appId`（string, 类型 `s`）：应用 ID
- **返回值**: `a(ShortcutInfo)`：快捷键信息数组

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ListShortcutsByApp "org.deepin.dde"
```

#### ListShortcutsByCategory

按类别列出快捷键。

- **输入参数**: `category`（string, 类型 `s`）：类别名称
- **返回值**: `a(ShortcutInfo)`：快捷键信息数组

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ListShortcutsByCategory "system"
```

#### ListCategories

列出所有快捷键类别。

- **输入参数**: 无
- **返回值**: `a(CategoryInfo)`：类别信息数组

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ListCategories
```

#### GetShortcut

获取指定快捷键信息。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID
- **返回值**: ShortcutInfo：快捷键信息

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.GetShortcut "workspace_switch_left"
```

#### GetShortcutCommand

获取指定快捷键的命令。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID
- **返回值**: `s`（string）：命令

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.GetShortcutCommand "workspace_switch_left"
```

#### LookupConflictShortcut

查找冲突快捷键。

- **输入参数**: `hotkey`（string, 类型 `s`）：快捷键
- **返回值**: ShortcutInfo：冲突快捷键信息

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.LookupConflictShortcut "<Super>Left"
```

#### SearchShortcuts

搜索快捷键。

- **输入参数**: `keyword`（string, 类型 `s`）：搜索关键词
- **返回值**: `a(ShortcutInfo)`：快捷键信息数组

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.SearchShortcuts "workspace"
```


### 快捷键修改

#### ModifyHotkeys

修改快捷键。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID；`newHotkeys`（string 数组, 类型 `as`）：新快捷键列表
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ModifyHotkeys "workspace_switch_left" ["<Super>Left"]
```

#### Disable

禁用快捷键。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.Disable "workspace_switch_left"
```


### 自定义快捷键

#### AddCustomShortcut

添加自定义快捷键。

- **输入参数**: `name`（string, 类型 `s`）：名称；`action`（string, 类型 `s`）：命令；`hotkey`（string, 类型 `s`）：快捷键
- **返回值**: `s`（string）：快捷键 ID

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.AddCustomShortcut "终端" "deepin-terminal" "<Ctrl><Alt>T"
```

#### AddCustomShortcutWithConflict

添加自定义快捷键（带冲突处理）。

- **输入参数**: `name`（string, 类型 `s`）：名称；`action`（string, 类型 `s`）：命令；`hotkey`（string, 类型 `s`）：快捷键；`expectedConflictId`（string, 类型 `s`）：预期冲突 ID
- **返回值**: `s`（string）：快捷键 ID

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.AddCustomShortcutWithConflict "终端" "deepin-terminal" "<Ctrl><Alt>T" ""
```

#### ModifyCustomShortcut

修改自定义快捷键。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID；`name`（string, 类型 `s`）：名称；`action`（string, 类型 `s`）：命令；`hotkey`（string, 类型 `s`）：快捷键
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ModifyCustomShortcut "custom_1" "终端" "deepin-terminal" "<Ctrl><Alt>T"
```

#### ModifyCustomShortcutWithConflict

修改自定义快捷键（带冲突处理）。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID；`name`（string, 类型 `s`）：名称；`action`（string, 类型 `s`）：命令；`hotkey`（string, 类型 `s`）：快捷键；`expectedConflictId`（string, 类型 `s`）：预期冲突 ID
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ModifyCustomShortcutWithConflict "custom_1" "终端" "deepin-terminal" "<Ctrl><Alt>T" ""
```

#### DeleteCustomShortcut

删除自定义快捷键。

- **输入参数**: `id`（string, 类型 `s`）：快捷键 ID
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.DeleteCustomShortcut "custom_1"
```


### 快捷键捕获与冲突处理

#### BeginCapture

开始捕获快捷键。

- **输入参数**: `timeoutMs`（uint32, 类型 `u`）：超时时间（毫秒）
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.BeginCapture 5000
```

#### EndCapture

结束捕获快捷键。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.EndCapture
```

#### SwapHotkeys

交换两个快捷键。

- **输入参数**: `id1`（string, 类型 `s`）：快捷键 ID 1；`id2`（string, 类型 `s`）：快捷键 ID 2
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.SwapHotkeys "id1" "id2"
```

#### ReplaceHotkey

替换快捷键。

- **输入参数**: `targetId`（string, 类型 `s`）：目标快捷键 ID；`newHotkey`（string, 类型 `s`）：新快捷键；`conflictId`（string, 类型 `s`）：冲突 ID
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ReplaceHotkey "id1" "<Super>Left" ""
```


### 配置管理

#### ReloadConfigs

重新加载快捷键配置。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ReloadConfigs
```

#### Reset

重置快捷键配置。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.Reset
```

#### GetNumLockState

获取 NumLock 状态。

- **输入参数**: 无
- **返回值**: `u`（uint32）：NumLock 状态

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.GetNumLockState
```

#### GetCapsLockState

获取 CapsLock 状态。

- **输入参数**: 无
- **返回值**: `u`（uint32）：CapsLock 状态

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.GetCapsLockState
```

#### SetNumLockState

设置 NumLock 状态。

- **输入参数**: `state`（uint32, 类型 `u`）：NumLock 状态
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.SetNumLockState 0
```

#### SetCapsLockState

设置 CapsLock 状态。

- **输入参数**: `state`（uint32, 类型 `u`）：CapsLock 状态
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.SetCapsLockState 0
```


### 键盘锁属性

#### NumLockState（属性）

NumLock 状态。

| 属性 | 值 |
|------|------|
| 类型 | `u` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Keybinding1 NumLockState
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Keybinding1 NumLockState <uint32 0>
```
#### CapsLockState（属性）

CapsLock 状态。

| 属性 | 值 |
|------|------|
| 类型 | `u` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Keybinding1 CapsLockState
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Keybinding1 CapsLockState <uint32 0>
```

### 快捷键信号

#### ShortcutChanged

快捷键变化时发出。

- **参数**: `id`（string, 类型 `s`）：快捷键 ID；`info`（ShortcutInfo, 类型）：快捷键信息
- **触发条件**: 快捷键被修改时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1
```

#### ShortcutActivated

快捷键激活时发出。

- **参数**: `id`（string, 类型 `s`）：快捷键 ID；`params`（string 数组, 类型 `as`）：参数
- **触发条件**: 快捷键被触发时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1
```

#### ShortcutDisabled

快捷键禁用时发出。

- **参数**: `id`（string, 类型 `s`）：快捷键 ID
- **触发条件**: 快捷键被禁用时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1
```

#### CaptureResult

快捷键捕获结果。

- **参数**: `code`（uint32, 类型 `u`）：结果码；`press`（uint32, 类型 `u`）：按键状态；`keystr`（string, 类型 `s`）：快捷键字符串
- **触发条件**: 快捷键捕获完成时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1
```

#### NumLockStateChanged

NumLock 状态变化时发出。

- **参数**: `state`（uint32, 类型 `u`）：NumLock 状态
- **触发条件**: NumLock 状态变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1
```

#### CapsLockStateChanged

CapsLock 状态变化时发出。

- **参数**: `state`（uint32, 类型 `u`）：CapsLock 状态
- **触发条件**: CapsLock 状态变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1
```

---
