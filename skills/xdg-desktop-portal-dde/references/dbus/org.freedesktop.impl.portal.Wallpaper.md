# org.freedesktop.impl.portal.Wallpaper 接口参考

该接口提供壁纸设置能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Wallpaper` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 壁纸方法

#### Set

设置壁纸。

- **输入参数**: `parent_handle`（object, 类型 `o`）：父窗口句柄；`options`（字典, 类型 `a{sv}`）：壁纸选项
- **返回值**: `o`（object path）：请求路径

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Wallpaper.Set "" {}
```

#### SetColor

设置纯色壁纸。

- **输入参数**: `parent_handle`（object, 类型 `o`）：父窗口句柄；`options`（字典, 类型 `a{sv}`）：颜色选项
- **返回值**: `o`（object path）：请求路径

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Wallpaper.SetColor "" {}
```

#### Ensure

确保壁纸设置生效。

- **输入参数**: `self`（string, 类型 `s`）：壁纸标识
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Wallpaper.Ensure "wallpaper_id"
```

