# org.freedesktop.impl.portal.Wallpaper 接口参考

该接口提供壁纸设置能力，允许沙箱应用通过 Portal 接口设置桌面壁纸或锁屏壁纸。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Wallpaper` |
| Bus | Session |

### 壁纸方法

#### SetWallpaperURI

设置壁纸 URI。

- **功能**: 根据指定的本地文件 URI 设置壁纸。通过 `options` 中的 `set-on` 键指定壁纸作用位置，支持以下取值：`background`（桌面壁纸）、`lockscreen`（锁屏壁纸）、`both`（同时设置桌面和锁屏壁纸）。URI 必须为有效的本地文件 `file://` URI。底层通过 Wayland 壁纸管理器协议（Treeland Wallpaper Manager）将壁纸应用到所有屏幕。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求设置壁纸时触发。
- **使用场景**: 沙箱应用（如壁纸管理应用、个性化设置应用）需要为用户设置桌面壁纸或锁屏壁纸时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`app_id`（string, 类型 `s`）：应用 ID；`parent_window`（string, 类型 `s`）：父窗口标识；`uri`（string, 类型 `s`）：壁纸文件的本地 URI（必须为 `file://` 格式）；`options`（字典, 类型 `a{sv}`）：壁纸选项（支持 `set-on` 键，取值为 `background`、`lockscreen`、`both`）
- **返回值**: `u`（uint）：响应码（`0` 表示成功，`1` 表示失败）

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Wallpaper.SetWallpaperURI "/" "app" "" "file:///usr/share/wallpapers/deepin/desktop.jpg" "{'set-on': <'background'>}"
```
