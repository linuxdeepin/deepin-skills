# org.deepin.dtk.preference 配置参考

DTK 应用偏好配置，控制以下 DTK 应用的外观与行为：主题、动画、滚动条、标题栏、新特性展示、菜单搜索、日志规则。该资源为公共资源（appId 为空），可被所有 DTK 应用共享使用。

| 字段 | 值 |
|------|------|
| App ID | （公共资源，appId 为空） |
| Resource ID | `org.deepin.dtk.preference` |

## 配置项

### autoDisplayFeature

控制应用是否在更新后自动展示一次新特性内容，启用时应用首次启动会展示新功能引导。

| 字段 | 值 |
|------|------|
| 类型 | bool |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.dtk.preference autoDisplayFeature
```

```bash
dconfig write -d "" -r org.deepin.dtk.preference autoDisplayFeature true
```

### defaultColorMode

配置 DTK 应用的默认色彩模式，影响应用初始的主题色调。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.dtk.preference defaultColorMode
```

```bash
dconfig write -d "" -r org.deepin.dtk.preference defaultColorMode "light"
```

### enableDtkAnimations

控制是否启用 DTK 控件动画效果，修改后需重启应用才能生效。

| 字段 | 值 |
|------|------|
| 类型 | bool |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.dtk.preference enableDtkAnimations
```

```bash
dconfig write -d "" -r org.deepin.dtk.preference enableDtkAnimations false
```

### featureUpdated

标记应用是否有新功能更新，配合 autoDisplayFeature 使用以决定是否展示新特性引导。

| 字段 | 值 |
|------|------|
| 类型 | bool |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.dtk.preference featureUpdated
```

```bash
dconfig write -d "" -r org.deepin.dtk.preference featureUpdated true
```

### keyboardsearchDisabled

控制是否禁用通过键盘输入直接搜索菜单项的功能，禁用后需按 Shift 或 Alt 才能触发菜单项搜索。

| 字段 | 值 |
|------|------|
| 类型 | bool |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.dtk.preference keyboardsearchDisabled
```

```bash
dconfig write -d "" -r org.deepin.dtk.preference keyboardsearchDisabled true
```

### rules

配置 DTK 应用的日志输出规则，控制日志类别和输出级别，遵循 Qt 日志规则格式。该配置项标记为 `global`，影响所有 DTK 应用。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `global` |

```bash
dconfig read -d "" -r org.deepin.dtk.preference rules
```

```bash
dconfig write -d "" -r org.deepin.dtk.preference rules "*.debug=true"
```

### scrollBarPolicy

配置 DTK 应用的滚动条显示策略，其值遵循 Qt::ScrollBarPolicy 枚举行为。

| 字段 | 值 |
|------|------|
| 类型 | number |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.dtk.preference scrollBarPolicy
```

```bash
dconfig write -d "" -r org.deepin.dtk.preference scrollBarPolicy 0
```

### sizeMode

配置是否开启紧凑模式，0 为禁用、1 为启用，启用后控件以紧凑尺寸显示。

| 字段 | 值 |
|------|------|
| 类型 | number |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.dtk.preference sizeMode
```

```bash
dconfig write -d "" -r org.deepin.dtk.preference sizeMode 1
```

### themeType

配置应用主题颜色类型，0 为跟随系统、1 为浅色、2 为深色，默认跟随系统。

| 字段 | 值 |
|------|------|
| 类型 | number |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.dtk.preference themeType
```

```bash
dconfig write -d "" -r org.deepin.dtk.preference themeType 2
```

### titlebarHeight

配置 DTK 应用窗口标题栏的高度（像素）。

| 字段 | 值 |
|------|------|
| 类型 | number |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.dtk.preference titlebarHeight
```

```bash
dconfig write -d "" -r org.deepin.dtk.preference titlebarHeight 40
```

### underlineShortcut

控制是否在菜单和按钮文字中为快捷键字符显示下划线。

| 字段 | 值 |
|------|------|
| 类型 | bool |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.dtk.preference underlineShortcut
```

```bash
dconfig write -d "" -r org.deepin.dtk.preference underlineShortcut true
```
