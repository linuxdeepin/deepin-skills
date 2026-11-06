# 主题生效机制

本页说明全局主题设置如何到达 Qt、GTK，以及应用为什么会采用不同的外观结果。编写 GTK 配色和样式资源时，使用 [GTK 主题适配](gtk-adaptation.md)。

## 全局配置与应用绘制

控制中心选择全局主题和模式后，外观服务读取对应配置分组、处理字段回退并校验资源，再发布各项外观设置。Qt、GTK 和桌面组件分别使用这些设置。

| 层次 | 内容 | 作用 |
| --- | --- | --- |
| 全局组合 | 应用样式、图标、光标、字体、活动色与壁纸的选择 | 由 DDE 组织一套主题 |
| 设置发布 | 当前资源名称、模式与颜色等值 | 通过平台支持的设置通道传递 |
| 工具包外观 | Qt 调色板与控件样式、GTK CSS | 决定应用控件如何绘制 |
| 桌面外观 | 壁纸、窗口效果等 | 由对应桌面组件处理 |

普通应用不直接读取 DDE 的全局 `index.theme`。主题名同步、亮暗同步、活动色同步和全部控件一致是不同能力，不能互相代替。

## X11 下的设置映射

GTK 3 通过 XSettings 接收标准桌面设置，无需每个应用单独订阅 Appearance1。Qt/DTK 通过平台集成使用对应设置。

| 全局字段或设置 | X11 发布项 | GTK 3 使用方式 | Qt/DTK 使用方式 |
| --- | --- | --- | --- |
| `AppTheme` | `Net/ThemeName` | `gtk-theme-name` 选择样式 | 平台基础主题名 |
| `IconTheme` | `Net/IconThemeName` | `gtk-icon-theme-name` | 平台图标主题 |
| `StandardFont`、`FontSize` | `Gtk/FontName`；Qt 另有 `Qt/FontName`、`Qt/FontPointSize` | `gtk-font-name` 包含字体与字号 | 平台字体与字号 |
| `MonospaceFont` | Qt 侧有 `Qt/MonoFontName` | 取决于应用的等宽字体偏好入口 | 请求系统等宽字体的控件 |
| `CursorTheme`、独立光标大小 | `Gtk/CursorThemeName`、`Gtk/CursorThemeSize` | `gtk-cursor-theme-name`、`gtk-cursor-theme-size` | 平台光标设置 |
| 亮、暗 `ActiveColor` | `Qt/ActiveColor`、`Qt/DarkActiveColor` | 没有自动转换成 CSS 的通用映射 | 参与当前模式的活动色计算 |

`Gtk/ThemeName` 不是 `Net/ThemeName` 的默认别名。桌面配置键、XSettings 键和 GTK 运行时属性有各自的名称，不能自行更换前缀。

有 XSettings 管理器的 X11 会话中，`settings.ini` 不是唯一或优先的实时通知来源。设置保存、发布、被目标进程接收，以及最终绘制是不同阶段。

## Qt 的平台集成、调色板与样式

Qt 的平台插件、平台主题和控件样式承担不同职责，并需要匹配 Qt 主版本。deepin 平台集成提供桌面默认外观，调色板决定颜色角色与状态，Chameleon 等样式负责控件绘制和尺寸。

- `ActiveColor` 可影响选中背景等活动色角色，不能代替窗口背景、文字、按钮、禁用态等完整调色板。
- GTK CSS 不被 Qt Widgets 解析。额外放置一个配色文件，也不会自动使 Qt 使用它；完整自定义调色板需要桌面与平台集成支持对应格式。
- 新配色可以复用已有 Chameleon，改变控件绘制方式则需要相应的样式支持。
- 部分 Qt/DTK 集成通过主题名的 `dark` 后缀识别暗色；`<名称>-light`、`<名称>-dark` 可适配这种命名约定。DDE 分组名和 GTK CSS 自身是否为暗色不能代替该判断。
- 应用固定亮暗模式、自定义调色板、固定颜色或局部样式时，可能覆盖系统偏好。

动态跟随需要平台接收设置变化、更新调色板，并由控件使用新颜色。Qt Quick/QML 使用自己的控件样式和主题绑定，不能直接套用 Widgets 的支持范围。

## GTK 的加载与刷新

GTK 3 收到有效主题名变化后，更新 `gtk-theme-name`，查找对应资源、加载 CSS 并重新计算样式。新进程读取当前设置后加载相同主题。

GTK 3 按以下顺序查找主题 CSS，并尝试版本专用目录、回溯到 `gtk-3.0`：

1. `$XDG_DATA_HOME/themes/<名称>/gtk-<版本>/gtk.css`。
2. `$HOME/.themes/<名称>/gtk-<版本>/gtk.css`。
3. `$XDG_DATA_DIRS` 中各目录下的 `themes/<名称>/gtk-<版本>/gtk.css`。
4. GTK 安装前缀下的 `share/themes/<名称>/gtk-<版本>/gtk.css`。

用户的 `$XDG_CONFIG_HOME/gtk-3.0/gtk.css` 是独立覆盖入口，可能改变所选主题的效果；应用自己的样式同样参与最终绘制。

| 变化 | 对 GTK 3 的作用 |
| --- | --- |
| 切换到有效的新主题名 | 重新选择并加载对应样式 |
| 只修改 DDE `ActiveColor` | 需要已有的颜色到 GTK 样式映射；缺少映射时重启也不会补齐 |
| 修改磁盘 CSS | 新进程可读取；已有进程需要实际重载 |
| 重设同一个主题名 | 不保证产生变化或触发重载 |
| 更新某个进程内的样式 | 影响该进程，不会自动更新其他进程 |
| 设置 `gtk-color-scheme` | GTK 3.8 起该属性已弃用且不再生效 |

后台程序仅为自己加载新样式，不能改变其他应用。要求所有已运行应用实时更新时，需要它们实际接收到并处理主题切换或样式重载。

## 工具包与会话范围

| 消费端 | 适用条件 |
| --- | --- |
| Qt 5 与 Qt 6 | 分别需要对应版本的平台集成和控件样式 |
| 普通 GTK 4 | 使用对应版本的 CSS、设置桥接和刷新方式 |
| libadwaita | 按版本及支持的系统偏好处理，不保证完整替换第三方主题或原样显示任意 RGB |
| Wayland/Treeland | 由相应平台与合成器传递设置；Qt、GTK、XWayland 分别适配，不能照搬 X11 链路 |
| 沙箱应用 | 资源可见性、运行时主题扩展、字体访问及 Portal 都会影响结果 |
| Electron、浏览器、自绘应用 | 取决于应用实际使用的系统偏好及绘制方式 |

支持的工具包可以通过 Settings Portal 的 `org.freedesktop.appearance` 偏好接收亮暗或 `accent-color`。Portal 是读取和通知通道，不负责分发主题文件、字体、图标或完整双模式调色板。

应用强制外观、`GTK_THEME`、用户样式覆盖和 Qt 固定调色板均可能使结果不同于系统主题。支持某一工具包的主题切换，不表示所有应用都采用相同绘制规则。

需要查询这些设置时，按名称使用 `deepin-desktop-environment` Skill 的 Appearance1 外观服务、XSettings1 服务或 Settings Portal 前端能力；具体接口由该 Skill 提供。
