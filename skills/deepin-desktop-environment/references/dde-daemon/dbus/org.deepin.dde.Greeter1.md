# org.deepin.dde.Greeter1 接口参考

更新登录界面的 Qt 主题配置，并同步相关 XSettings 字体、图标主题和 DPI。它处理主题数据，不负责显示器分辨率配置、显示电源或当前用户桌面窗口控制。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Greeter1` |
| Object path | `/org/deepin/dde/Greeter1` |
| Interface | `org.deepin.dde.Greeter1` |
| Bus | System |

服务由登录界面环境提供，客户端可按总线策略调用；服务进程的运行身份与客户端是否需要 root 不应混淆。

## UpdateGreeterQtTheme

- **功能**：从传入文件描述符读取主题内容，最多 100 KiB，覆盖登录界面的 Qt 主题配置，再更新对应 XSettings。
- **输入参数**：`fd`（UnixFD，`h`）：随 D-Bus 消息传递的文件描述符在 FD 列表中的索引。
- **返回值**：无；Qt 主题文件更新失败时返回 D-Bus 错误。请求成功不表示所有 XSettings 字段都已同步。
- **使用场景**：向登录界面同步完整的字体、图标和缩放主题配置。

风险警示：

- 此操作覆盖登录界面主题而非合并部分字段，错误内容会影响后续登录界面的字体与缩放；应保留可恢复的主题配置。

`h` 不接受路径字符串或文本 `"fd"`。客户端必须随消息附加 Unix FD 列表；下面的 Python 示例依赖 PyGObject，先由调用方提供完整主题文件，保存为脚本后用系统 Python 运行：

```python
from gi.repository import Gio, GLib
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: update-greeter-theme.py THEME_FILE")

bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
with open(sys.argv[1], "rb") as theme:
    descriptors = Gio.UnixFDList.new()
    index = descriptors.append(theme.fileno())
    bus.call_with_unix_fd_list_sync(
        "org.deepin.dde.Greeter1", "/org/deepin/dde/Greeter1",
        "org.deepin.dde.Greeter1", "UpdateGreeterQtTheme",
        GLib.Variant("(h)", (index,)), None, Gio.DBusCallFlags.NONE,
        5000, descriptors, None
    )
```

文件使用 INI 格式的 `[Theme]` 节，可包含 `IconThemeName`、`FontSize`、`Font`、`MonoFont`、`ScreenScaleFactors` 与 `ScaleLogicalDpi`。这是服务可用时的更新示例；不会因为传递了描述符而自动完成权限认证或修复不可用的服务。
