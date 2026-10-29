# org.deepin.dde.Keybinding1 接口参考

该接口提供快捷键管理能力，包括快捷键查询、自定义快捷键增删改、快捷键冲突处理和快捷键捕获。

> 同名接口在 X11 与 Treeland 会话下由不同后端提供：X11 为 dde-daemon，Treeland 为 dde-services。两套实现的方法集和返回签名可能不同，不能只依据接口名假定某个方法存在或返回 JSON。调用前先用 `gdbus introspect --session --dest org.deepin.dde.Keybinding1 --object-path /org/deepin/dde/Keybinding1` 核对当前会话的实际契约。本页的签名以 X11 dde-daemon 实现为基线。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Keybinding1` |
| Object path | `/org/deepin/dde/Keybinding1` |
| Interface | `org.deepin.dde.Keybinding1` |
| Bus | Session |

### 类型说明

- `ShortcutInfo`：D-Bus 结构体 `(sssasssbb)`，依次包含快捷键 ID、名称、类别、快捷键字符串数组、显示名称、本地化类别及两个布尔状态。
- `CategoryInfo`：D-Bus 结构体 `(ssib)`，依次包含类别 ID、显示名称、类别编号及一个布尔状态。

结构体字段按 D-Bus 签名顺序返回。部署提供相应方法时，按名称筛选先调用 `ListCategories` 获取实际类别 ID，再传给 `ListShortcutsByCategory`；缺少方法时按 ListCategories 小节的能力分支枚举并在本地筛选。

### 快捷键查询

#### ListAllShortcuts

列出所有快捷键。

- **功能**：返回系统中所有已注册的快捷键列表，包括系统预设快捷键和用户自定义快捷键
- **触发条件**：需要获取系统中所有快捷键列表时调用
- **输入参数**：无
- **返回值**：`a(sssasssbb)`：快捷键结构体数组（`ShortcutInfo`）。不要按 JSON 字符串解析。
- **使用场景**：控制中心快捷键设置界面需要展示所有快捷键列表时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ListAllShortcuts
```

#### ListShortcutsByApp

此方法为可选能力。未提供时可从已读取的快捷键记录筛选；按应用筛选须有应用 ID 字段，不从快捷键 ID 推断。

按应用列出快捷键。

- **功能**：返回指定应用 ID 关联的快捷键列表
- **触发条件**：需要查询指定应用绑定的快捷键时调用
- **输入参数**：`appId`（string, 类型 `s`）：应用 ID
- **返回值**：`a(sssasssbb)`：快捷键结构体数组（`ShortcutInfo`）
- **使用场景**：需要查看某个应用绑定了哪些快捷键时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ListShortcutsByApp "org.deepin.dde"
```

#### ListShortcutsByCategory

此方法为可选能力。未提供时可从已读取的快捷键记录筛选；按应用筛选须有应用 ID 字段，不从快捷键 ID 推断。

按类别列出快捷键。

- **功能**：返回指定类别下的快捷键列表
- **触发条件**：需要按类别筛选快捷键时调用
- **输入参数**：`category`（string, 类型 `s`）：类别 ID，取值来自 `ListCategories` 返回的第一项
- **返回值**：`a(sssasssbb)`：快捷键结构体数组（`ShortcutInfo`）
- **使用场景**：控制中心按类别分组展示快捷键时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ListShortcutsByCategory "System"
```

类别 ID 区分大小写；使用 `"system"` 可能返回空数组。应先读取 `ListCategories`，再使用其返回的类别 ID。

#### ListCategories

此方法为可选能力，调用前通过 introspect 确认。类别统计按以下规则处理：

1. 有 `ListCategories() -> a(ssib)` 时读取类别 ID 和显示名称；按 ID 去重统计，保留大小写。
2. 无此方法时，优先读取无参数 `ListAllShortcuts`，否则读取 introspect 确认无参数的 `List`。结果可能是结构体数组，也可能是包含 JSON 的 `s`。结构体签名为 `a(sssasssbb)` 时第三项是类别 ID、第六项是本地化类别；JSON 对象列表则按实际 `Category` 字段聚合，不能把 `Type` 猜成类别。
3. 聚合得到的是“当前快捷键记录中出现的类别”，不能声称包含未使用的空类别。若结果未提供类别字段，明确无法枚举，不编造类别名称。按类别筛选可在已读取记录上完成；按应用筛选必须有应用 ID 字段，不从快捷键 ID 猜应用。

列出所有快捷键类别。

- **功能**：返回系统中所有快捷键类别的列表
- **触发条件**：需要获取所有快捷键分类时调用
- **输入参数**：无
- **返回值**：`a(ssib)`：类别结构体数组（`CategoryInfo`）
- **使用场景**：控制中心需要获取所有快捷键分类以分组展示时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ListCategories
```

#### GetShortcut

输入签名随后端版本变化，调用前核对 introspect 结果，不默认只接受一个字符串 ID。

获取指定快捷键信息。

- **功能**：根据快捷键 ID 返回该快捷键的详细信息
- **触发条件**：需要查看某个快捷键的详细配置时调用
- **输入参数**：`id`（string, 类型 `s`）：快捷键 ID
- **返回值**：`(sssasssbb)`：快捷键结构体（`ShortcutInfo`）
- **使用场景**：需要查看某个快捷键的具体配置（名称、绑定键、命令）时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.GetShortcut "workspace_switch_left"
```

#### GetShortcutCommand

获取指定快捷键的命令。

- **功能**：根据快捷键 ID 返回该快捷键绑定的执行命令
- **触发条件**：需要获取某个快捷键绑定的执行命令时调用
- **输入参数**：`id`（string, 类型 `s`）：快捷键 ID
- **返回值**：`s`（string）：命令
- **使用场景**：需要获取某个快捷键实际执行的命令字符串时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.GetShortcutCommand "workspace_switch_left"
```

#### LookupConflictShortcut

查找冲突快捷键。

- **功能**：检查指定快捷键组合是否与其他快捷键存在冲突，返回冲突的快捷键信息
- **触发条件**：用户修改快捷键前需要检查是否与已有快捷键冲突时调用
- **输入参数**：`hotkey`（string, 类型 `s`）：快捷键
- **返回值**：`(sssasssbb)`：冲突快捷键结构体（`ShortcutInfo`）
- **使用场景**：用户修改快捷键前需要检查是否与已有快捷键冲突时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.LookupConflictShortcut "<Super>Left"
```

#### SearchShortcuts

搜索快捷键。

- **功能**：根据关键词模糊搜索快捷键，返回匹配的快捷键列表
- **触发条件**：用户在快捷键搜索框中输入关键词搜索时调用
- **输入参数**：`keyword`（string, 类型 `s`）：搜索关键词
- **返回值**：`a(sssasssbb)`：快捷键结构体数组（`ShortcutInfo`）
- **使用场景**：控制中心快捷键搜索框中用户输入关键词搜索时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.SearchShortcuts "workspace"
```

### 快捷键修改

#### ModifyHotkeys

修改快捷键。

- **功能**：修改指定快捷键 ID 的快捷键组合
- **触发条件**：用户在控制中心修改某个快捷键的绑定键时调用
- **输入参数**：`id`（string, 类型 `s`）：快捷键 ID；`newHotkeys`（string 数组, 类型 `as`）：新快捷键列表
- **返回值**：`b`（bool）：是否成功
- **使用场景**：用户在控制中心修改某个快捷键的绑定键时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ModifyHotkeys "workspace_switch_left" ["<Super>Left"]
```

#### Disable

禁用快捷键。

- **功能**：禁用指定快捷键 ID 对应的快捷键，使其不再响应按键
- **触发条件**：用户在控制中心禁用某个快捷键时调用
- **输入参数**：`id`（string, 类型 `s`）：快捷键 ID
- **返回值**：`b`（bool）：是否成功
- **使用场景**：用户在控制中心关闭某个快捷键时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.Disable "workspace_switch_left"
```

### 自定义快捷键

#### AddCustomShortcut

添加自定义快捷键。

- **功能**：添加一条用户自定义快捷键，包含名称、执行命令和快捷键组合
- **触发条件**：用户在控制中心新增自定义快捷键时调用
- **输入参数**：`name`（string, 类型 `s`）：名称；`action`（string, 类型 `s`）：命令；`hotkey`（string, 类型 `s`）：快捷键
- **返回值**：`s`（string）：快捷键 ID
- **使用场景**：用户在控制中心添加新的自定义快捷键时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.AddCustomShortcut "终端" "deepin-terminal" "<Ctrl><Alt>T"
```

#### AddCustomShortcutWithConflict

添加自定义快捷键（带冲突处理）。

- **功能**：添加一条用户自定义快捷键，若与已有快捷键冲突则按预期冲突 ID 覆盖处理
- **触发条件**：用户在控制中心新增自定义快捷键且需要处理冲突时调用
- **输入参数**：`name`（string, 类型 `s`）：名称；`action`（string, 类型 `s`）：命令；`hotkey`（string, 类型 `s`）：快捷键；`expectedConflictId`（string, 类型 `s`）：预期冲突 ID
- **返回值**：`s`（string）：快捷键 ID
- **使用场景**：用户添加自定义快捷键时已知会与某个快捷键冲突，希望覆盖该冲突项时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.AddCustomShortcutWithConflict "终端" "deepin-terminal" "<Ctrl><Alt>T" "existing_id"
```

#### ReplaceHotkey

替换快捷键。

- **功能**：将一个快捷键 ID 的绑定键替换为新的快捷键组合，并指定需要处理的冲突项
- **触发条件**：用户在控制中心替换某个快捷键的绑定键时调用
- **输入参数**：`targetId`（string, 类型 `s`）：目标快捷键 ID；`newHotkey`（string, 类型 `s`）：新快捷键；`conflictId`（string, 类型 `s`）：冲突项 ID，无冲突时按服务端要求传入空值
- **返回值**：`b`（bool）：是否成功
- **使用场景**：用户修改快捷键时需要替换已有绑定键的场合

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ReplaceHotkey "id1" "<Super>Left" ""
```

### 其他方法

当前 X11 实现还提供以下方法。字段含义与详细约束在调用前通过 introspection 或实际返回核对。

- `ModifyCustomShortcut(s id, s name, s action, s hotkey) -> b`
- `ModifyCustomShortcutWithConflict(s id, s name, s action, s hotkey, s expectedConflictId) -> b`
- `DeleteCustomShortcut(s id) -> b`
- `BeginCapture(u timeoutMs) -> b`、`BeginCapture() -> b`、`BeginCapture(t captureId, u timeoutMs) -> b`
- `EndCapture()`
- `SwapHotkeys(s id1, s id2) -> b`

### 配置管理

#### ReloadConfigs

重新加载快捷键配置。

- **功能**：热加载快捷键配置文件的变更，使配置文件修改后立即生效
- **触发条件**：快捷键配置文件发生变更时调用
- **返回值**：无
- **使用场景**：配置文件被外部修改后需要让服务重新加载时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.ReloadConfigs
```

#### Reset

重置快捷键配置。

- **功能**：将所有快捷键配置恢复为系统默认值
- **触发条件**：用户在控制中心重置快捷键到默认值时调用
- **返回值**：无
- **使用场景**：用户在控制中心点击「恢复默认」按钮时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.Reset
```

#### GetNumLockState

获取 NumLock 状态。

- **功能**：返回当前 NumLock 键的状态（开启或关闭）
- **触发条件**：需要获取当前 NumLock 键状态时调用
- **返回值**：`u`（uint32）：NumLock 状态
- **使用场景**：系统需要读取当前 NumLock 状态以在界面上显示时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.GetNumLockState
```

#### GetCapsLockState

获取 CapsLock 状态。

- **功能**：返回当前 CapsLock 键的状态（开启或关闭）
- **触发条件**：需要获取当前 CapsLock 键状态时调用
- **返回值**：`u`（uint32）：CapsLock 状态
- **使用场景**：系统需要读取当前 CapsLock 状态以在界面上显示时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.GetCapsLockState
```

#### SetNumLockState

设置 NumLock 状态。

- **功能**：设置 NumLock 键的开启或关闭状态
- **触发条件**：系统需要程序化控制 NumLock 状态时调用
- **输入参数**：`state`（uint32, 类型 `u`）：NumLock 状态
- **返回值**：无
- **使用场景**：系统需要程序化控制 NumLock 状态时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.SetNumLockState 0
```

#### SetCapsLockState

设置 CapsLock 状态。

- **功能**：设置 CapsLock 键的开启或关闭状态
- **触发条件**：系统需要程序化控制 CapsLock 状态时调用
- **输入参数**：`state`（uint32, 类型 `u`）：CapsLock 状态
- **返回值**：无
- **使用场景**：系统需要程序化控制 CapsLock 状态时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1 \
  --method org.deepin.dde.Keybinding1.SetCapsLockState 0
```

### 键盘锁属性

#### NumLockState（属性）

NumLock 状态。

- **功能**：指示当前 NumLock 键的开启或关闭状态
- **触发条件**：用户按下 NumLock 键或通过 SetNumLockState 方法设置时更新
- **使用场景**：界面组件需要监听 NumLock 状态变化以更新显示时读取

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

- **功能**：指示当前 CapsLock 键的开启或关闭状态
- **触发条件**：用户按下 CapsLock 键或通过 SetCapsLockState 方法设置时更新
- **使用场景**：界面组件需要监听 CapsLock 状态变化以更新显示时读取

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

- **功能**：通知订阅者某个快捷键的配置发生了变更
- **参数**：`id`（string, 类型 `s`）：快捷键 ID；`info`（`(sssasssbb)`，`ShortcutInfo`）：快捷键信息
- **触发条件**：快捷键被修改时发出
- **使用场景**：控制中心快捷键列表需要实时同步快捷键变更时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1
```

#### ShortcutActivated

快捷键激活时发出。

- **功能**：通知订阅者某个快捷键被触发执行
- **参数**：`id`（string, 类型 `s`）：快捷键 ID；`params`（string 数组, 类型 `as`）：参数
- **触发条件**：快捷键被触发时发出
- **使用场景**：调试或统计快捷键使用情况时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1
```

#### ShortcutRemoved

快捷键被移除时发出。

- **功能**：通知订阅者某个快捷键已从配置中移除
- **参数**：`id`（string, 类型 `s`）：快捷键 ID
- **触发条件**：快捷键被删除时发出
- **使用场景**：控制中心需要同步快捷键删除状态时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1
```

#### CaptureFinished

快捷键捕获结果。

- **功能**：通知订阅者快捷键捕获操作的结果，包含捕获会话 ID、结果码和快捷键字符串
- **参数**：`captureId`（uint64, 类型 `t`）：捕获会话 ID；`result`（uint32, 类型 `u`）：结果码；`keystroke`（string, 类型 `s`）：快捷键字符串
- **触发条件**：快捷键捕获完成时发出
- **使用场景**：用户在控制中心录制新快捷键时监听以获取捕获结果

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1
```

#### NumLockStateChanged

NumLock 状态变化时发出。

- **功能**：通知订阅者 NumLock 键状态发生了变化
- **参数**：`state`（uint32, 类型 `u`）：NumLock 状态
- **触发条件**：NumLock 状态变化时发出
- **使用场景**：界面组件需要实时响应 NumLock 状态变化时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1
```

#### CapsLockStateChanged

CapsLock 状态变化时发出。

- **功能**：通知订阅者 CapsLock 键状态发生了变化
- **参数**：`state`（uint32, 类型 `u`）：CapsLock 状态
- **触发条件**：CapsLock 状态变化时发出
- **使用场景**：界面组件需要实时响应 CapsLock 状态变化时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keybinding1 \
  --object-path /org/deepin/dde/Keybinding1
```

---
