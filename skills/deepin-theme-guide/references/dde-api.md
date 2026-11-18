# DDE 外观接口适配说明

## 发现与签名

脚本通过当前用户的 session bus 和 `gdbus introspect --xml` 顺序探测：

| 服务/接口 | 对象路径 |
| --- | --- |
| `org.deepin.dde.Appearance1` | `/org/deepin/dde/Appearance1` |
| `com.deepin.daemon.Appearance` | `/com/deepin/daemon/Appearance` |

只使用运行时实际暴露且参数签名符合要求的接口，不按发行版名称猜测。gdbus 命令使用 argv 调用；标量返回通过受限的 literal 解析，不使用 eval 或 shell。

## 能力映射

| 目标 | 读取 | 写入 |
| --- | --- | --- |
| 主显示器当前工作区壁纸 | `GetCurrentWorkspaceBackground() -> s` | `SetCurrentWorkspaceBackground(s)` |
| 指定显示器当前工作区壁纸 | `GetCurrentWorkspaceBackgroundForMonitor(s) -> s` | `SetCurrentWorkspaceBackgroundForMonitor(s, s)`；参数顺序是 URI、显示器名 |
| 图标主题 | `IconTheme` 字符串属性 | `Set("icon", id)` |
| 光标主题 | `CursorTheme` 字符串属性 | `Set("cursor", id)` |
| 光标尺寸 | `CursorSize` int32 属性 | `org.freedesktop.DBus.Properties.Set`；仅支持可写属性 |
| 新版活动色 | `GetActiveColors() -> s` | `SetActiveColors(s)`；值为浅色和深色的逗号分隔颜色对 |
| 旧版单个活动色 | `QtActiveColor` 字符串属性 | Properties.Set；仅在旧服务且属性可写时使用 |
| 主题清单 | `List("icon" / "cursor" / "background" / "globaltheme") -> s` | 不修改 |
| 主题预览 | `Thumbnail(type, id) -> s` | DDE 自行生成缩略图缓存 |

`IconTheme` 和 `CursorTheme` 在新 XML 中是只读属性，切换应使用 `Set` 方法。不要直接用 Properties.Set 写这些只读属性。

新实现中的 `setQtActiveColor` 会读取配置中的浅色/深色颜色对，不能把 `QtActiveColor` 可写当作任意单色写入一定生效。因此本适配器在新服务优先且仅使用经过探测的 Get/SetActiveColors 方法；缺少该能力就返回不支持。

旧版可能只有 `SetMonitorBackground` 或废弃的 `Set("background", ...)`，缺少可对应读取的工作区壁纸接口。本包在这种情况下将 wallpaper 标记为不支持，以免错误恢复其他工作区的背景；不会用 GNOME picture-uri 替代并宣称 DDE 已修改。旧接口也可能没有 CursorSize，因此光标尺寸是附加能力，不影响可用光标主题的切换。

只要缺少读取、写入或可恢复原值中的任意一项，请求中该项就进入 blocked。此包不承诺所有 UOS/DDE 版本均支持全部字段。

控制中心主题卡片使用 globaltheme 列表。自定义壁纸入库走系统总线 Daemon1 的 SaveCustomWallPaper/GetCustomWallPapers，不能把设置工作区背景或 Appearance 的 background 列表等同于入库；目录、FD 参数及热更新条件见 [control-center.md](control-center.md)。

## 官方来源

实现时核对以下官方源码；远端 master 会变化，目标机的实际 introspection 优先：

- [新版外观服务 XML](https://github.com/linuxdeepin/dde-appearance/blob/master/dbus/org.deepin.dde.Appearance1.xml)
- [新版外观管理器与活动色实现](https://github.com/linuxdeepin/dde-appearance/blob/master/src/service/impl/appearancemanager.cpp)
- [新版主题类别常量](https://github.com/linuxdeepin/dde-appearance/blob/master/src/service/modules/common/commondefine.h)
- [旧版外观方法，5.14.0](https://github.com/linuxdeepin/dde-daemon/blob/5.14.0/appearance/ifc.go)
- [旧版服务名、对象路径与主题类别](https://github.com/linuxdeepin/dde-daemon/blob/5.14.0/appearance/manager.go)

这些方法的存在不保证具体硬件、窗口系统或第三方应用的视觉一致性，必须读回并在目标机观察。特定 Treeland 版本会把部分外观操作转交控制中心，可能需要后续专门适配。
