# org.deepin.dde.InputDevices1 接口参考

该接口提供键盘布局和输入设备管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.InputDevices` |
| Object path | `/com/deepin/daemon/InputDevices` |
| Interface | `org.deepin.dde.InputDevices1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 输入设备管理方法

#### AddLayoutOption

添加布局选项。

- **输入参数**: `layout`（string, 类型 `s`）：布局名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices \
  --object-path /com/deepin/daemon/InputDevices \
  --method org.deepin.dde.InputDevices1.AddLayoutOption "layout"
```

#### AddUserLayout

添加用户布局。

- **输入参数**: `layout`（string, 类型 `s`）：布局名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices \
  --object-path /com/deepin/daemon/InputDevices \
  --method org.deepin.dde.InputDevices1.AddUserLayout "layout"
```

#### ClearLayoutOption

清除布局选项。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices \
  --object-path /com/deepin/daemon/InputDevices \
  --method org.deepin.dde.InputDevices1.ClearLayoutOption
```

#### DeleteLayoutOption

删除布局选项。

- **输入参数**: `layout`（string, 类型 `s`）：布局名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices \
  --object-path /com/deepin/daemon/InputDevices \
  --method org.deepin.dde.InputDevices1.DeleteLayoutOption "layout"
```

#### DeleteUserLayout

删除用户布局。

- **输入参数**: `layout`（string, 类型 `s`）：布局名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices \
  --object-path /com/deepin/daemon/InputDevices \
  --method org.deepin.dde.InputDevices1.DeleteUserLayout "layout"
```

#### GetLayoutDesc

获取布局描述。

- **输入参数**: `layout`（string, 类型 `s`）：布局名称
- **返回值**: `s`（string）：布局描述

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices \
  --object-path /com/deepin/daemon/InputDevices \
  --method org.deepin.dde.InputDevices1.GetLayoutDesc "layout"
```

#### LayoutList

获取布局列表。

- **输入参数**: 无
- **返回值**: `as`（string 数组）：布局列表

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices \
  --object-path /com/deepin/daemon/InputDevices \
  --method org.deepin.dde.InputDevices1.LayoutList
```

#### AllLayoutList

获取所有布局列表。

- **输入参数**: 无
- **返回值**: `as`（string 数组）：所有布局列表

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices \
  --object-path /com/deepin/daemon/InputDevices \
  --method org.deepin.dde.InputDevices1.AllLayoutList
```

#### Reset

重置输入设备配置。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices \
  --object-path /com/deepin/daemon/InputDevices \
  --method org.deepin.dde.InputDevices1.Reset
```

#### ToggleNextLayout

切换到下一个布局。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices \
  --object-path /com/deepin/daemon/InputDevices \
  --method org.deepin.dde.InputDevices1.ToggleNextLayout
```

#### Enable

启用输入设备。

- **输入参数**: `value`（bool, 类型 `b`）：是否启用
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.InputDevices \
  --object-path /com/deepin/daemon/InputDevices \
  --method org.deepin.dde.InputDevices1.Enable true
```

