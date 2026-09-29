# org.deepin.dde.InputDevices1 接口参考

该接口提供键盘布局和输入设备管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.InputDevices1` |
| Object path | `/org/deepin/dde/InputDevices1` |
| Interface | `org.deepin.dde.InputDevices1` |
| Bus | Session |
### 输入设备管理方法

#### AddLayoutOption

添加布局选项。

- **功能**：添加键盘布局选项。
- **触发条件**：当用户在控制中心添加键盘布局选项时调用。
- **使用场景**：控制中心键盘布局设置添加选项。
- **输入参数**: `layout`（string, 类型 `s`）：布局名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices1 \
  --object-path /org/deepin/dde/InputDevices1 \
  --method org.deepin.dde.InputDevices1.AddLayoutOption "layout"
```

#### AddUserLayout

添加用户布局。

- **功能**：添加用户键盘布局。
- **触发条件**：当用户在控制中心添加新的键盘布局时调用。
- **使用场景**：控制中心键盘布局添加。
- **输入参数**: `layout`（string, 类型 `s`）：布局名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices1 \
  --object-path /org/deepin/dde/InputDevices1 \
  --method org.deepin.dde.InputDevices1.AddUserLayout "layout"
```

#### ClearLayoutOption

清除布局选项。

- **功能**：清除所有键盘布局选项。
- **触发条件**：当用户在控制中心清除所有布局选项时调用。
- **使用场景**：控制中心键盘布局设置清除选项。
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices1 \
  --object-path /org/deepin/dde/InputDevices1 \
  --method org.deepin.dde.InputDevices1.ClearLayoutOption
```

#### DeleteLayoutOption

删除布局选项。

- **功能**：删除指定的键盘布局选项。
- **触发条件**：当用户在控制中心删除某个键盘布局选项时调用。
- **使用场景**：控制中心键盘布局设置删除选项。
- **输入参数**: `layout`（string, 类型 `s`）：布局名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices1 \
  --object-path /org/deepin/dde/InputDevices1 \
  --method org.deepin.dde.InputDevices1.DeleteLayoutOption "layout"
```

#### DeleteUserLayout

删除用户布局。

- **功能**：删除指定的用户键盘布局。
- **触发条件**：当用户在控制中心删除某个键盘布局时调用。
- **使用场景**：控制中心键盘布局删除。
- **输入参数**: `layout`（string, 类型 `s`）：布局名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices1 \
  --object-path /org/deepin/dde/InputDevices1 \
  --method org.deepin.dde.InputDevices1.DeleteUserLayout "layout"
```

#### GetLayoutDesc

获取布局描述。

- **功能**：获取指定键盘布局的描述信息。
- **触发条件**：当需要在键盘布局列表中展示布局描述时调用。
- **使用场景**：控制中心键盘布局列表显示描述。
- **输入参数**: `layout`（string, 类型 `s`）：布局名称
- **返回值**: `s`（string）：布局描述

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices1 \
  --object-path /org/deepin/dde/InputDevices1 \
  --method org.deepin.dde.InputDevices1.GetLayoutDesc "layout"
```

#### LayoutList

获取布局列表。

- **功能**：获取当前用户已添加的键盘布局列表。
- **触发条件**：当需要展示用户已添加的键盘布局时调用。
- **使用场景**：控制中心键盘布局列表展示。
- **输入参数**: 无
- **返回值**: `a{ss}`（字典）：布局列表（键为布局名称，值为描述）

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices1 \
  --object-path /org/deepin/dde/InputDevices1 \
  --method org.deepin.dde.InputDevices1.LayoutList
```

#### AllLayoutList

获取所有布局列表。

- **功能**：获取系统支持的所有键盘布局列表。
- **触发条件**：当需要展示所有可选键盘布局时调用。
- **使用场景**：控制中心键盘布局选择列表展示。
- **输入参数**: 无
- **返回值**: `a{ss}`（字典）：所有布局列表（键为布局名称，值为描述）

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices1 \
  --object-path /org/deepin/dde/InputDevices1 \
  --method org.deepin.dde.InputDevices1.AllLayoutList
```

#### Reset

重置输入设备配置。

- **功能**：重置输入设备配置到默认状态。
- **触发条件**：当用户在控制中心点击恢复默认输入设备设置时调用。
- **使用场景**：控制中心键盘布局设置恢复默认。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices1 \
  --object-path /org/deepin/dde/InputDevices1 \
  --method org.deepin.dde.InputDevices1.Reset
```

#### ToggleNextLayout

切换到下一个布局。

- **功能**：切换到下一个键盘布局。
- **触发条件**：当用户通过快捷键切换键盘布局时调用。
- **使用场景**：快捷键切换键盘布局。
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices1 \
  --object-path /org/deepin/dde/InputDevices1 \
  --method org.deepin.dde.InputDevices1.ToggleNextLayout
```
