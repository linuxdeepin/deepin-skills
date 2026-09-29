# org.freedesktop.impl.portal.Settings 接口参考

该接口读写桌面环境全局设置（颜色方案、强调色），允许沙箱应用通过 Portal 接口查询桌面环境的外观设置。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Settings` |
| Bus | Session |

### 属性

| 属性名 | 类型 | 权限 | 说明 |
|--------|------|------|------|
| `version` | `u` | read | 接口版本号 |

### 信号

#### SettingChanged

设置值变化信号。

- **功能**: 当桌面环境的外观设置发生变化时通知监听方。当前支持的设置项包括 `org.freedesktop.appearance` 组下的 `color-scheme`（颜色方案，取值为 `0`=无偏好、`1`=深色、`2`=浅色）和 `accent-color`（强调色，取值为包含 `red`、`green`、`blue` 三个 `double` 字段的结构体，取值范围 0.0 到 1.0）。
- **触发条件**: 当系统调色板发生变化（如用户切换深色/浅色主题或更改强调色）时自动触发。
- **使用场景**: 沙箱应用需要实时感知桌面环境外观变化并自适应调整界面主题时监听此信号。
- **参数**: `group`（string, 类型 `s`）：设置组名（当前支持 `org.freedesktop.appearance`）；`key`（string, 类型 `s`）：键名（当前支持 `color-scheme`、`accent-color`）；`value`（variant, 类型 `v`）：设置值

### 设置方法

#### ReadAll

读取所有指定设置组的设置。

- **功能**: 批量读取指定设置组中的所有设置项。当前支持的设置组为 `org.freedesktop.appearance`，返回该组下 `color-scheme` 和 `accent-color` 两个设置项的值。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端批量查询桌面环境设置时触发。
- **使用场景**: 沙箱应用启动时需要一次性获取当前桌面环境的所有外观设置时使用。
- **输入参数**: `groups`（字符串数组, 类型 `as`）：设置组名列表（支持通配符匹配，如 `org.freedesktop.*`）
- **返回值**: `a{sa{sv}}`（字典的字典）：设置组到设置键值映射的映射（外层键为设置组名，内层为设置键到设置值的映射）

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Settings.ReadAll []
```

#### Read

读取指定设置组和键的值。

- **功能**: 读取单个设置项的值。当前支持的设置项为 `org.freedesktop.appearance` 组下的 `color-scheme`（颜色方案，取值为 `0`=无偏好、`1`=深色、`2`=浅色）和 `accent-color`（强调色，取值为包含 `red`、`green`、`blue` 三个 `double` 字段的结构体，取值范围 0.0 到 1.0）。请求不支持的设置项时返回 `UnknownProperty` 错误。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端查询单个桌面环境设置项时触发。
- **使用场景**: 沙箱应用需要获取当前桌面环境的颜色方案或强调色时使用。
- **输入参数**: `group`（string, 类型 `s`）：设置组名（当前支持 `org.freedesktop.appearance`）；`key`（string, 类型 `s`）：键名（当前支持 `color-scheme`、`accent-color`）
- **返回值**: `v`（variant）：设置值

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Settings.Read "org.freedesktop.appearance" "color-scheme"
```
