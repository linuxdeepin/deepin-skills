# org.freedesktop.impl.portal.Screenshot 接口参考

该接口提供屏幕截图和屏幕取色能力，允许沙箱应用通过 Portal 接口获取屏幕截图或拾取屏幕颜色。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Screenshot` |
| Bus | Session |

### 截图方法

#### Screenshot

进行屏幕截图。

- **功能**: 截取全屏图像，将截图保存为临时文件并返回文件 URI。返回结果字典中包含 `uri` 键，值为截图文件的 `file://` URI。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求屏幕截图时触发。
- **使用场景**: 沙箱应用需要获取当前屏幕截图（如截图分享、屏幕录制缩略图）时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`app_id`（string, 类型 `s`）：应用 ID；`parent_window`（string, 类型 `s`）：父窗口标识；`options`（字典, 类型 `a{sv}`）：截图选项
- **返回值**: `u`（uint）：响应码（`0` 表示成功，`1` 表示失败）；`results`（字典, 类型 `a{sv}`）：截图结果（包含 `uri` 键，值为截图文件的 `file://` URI）

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Screenshot.Screenshot "/" "app" "" {}
```

#### PickColor

进行屏幕取色。

- **功能**: 让用户在屏幕上拾取一个像素颜色。返回结果字典中包含 `color` 键，值为 RGB 颜色结构体（包含 `red`、`green`、`blue` 三个 `double` 类型字段，取值范围为 0.0 到 1.0）。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求屏幕取色时触发。
- **使用场景**: 沙箱应用需要让用户从屏幕上拾取颜色（如取色器工具、绘图应用）时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`app_id`（string, 类型 `s`）：应用 ID；`parent_window`（string, 类型 `s`）：父窗口标识；`options`（字典, 类型 `a{sv}`）：取色选项
- **返回值**: `u`（uint）：响应码（`0` 表示成功，`1` 表示失败）；`results`（字典, 类型 `a{sv}`）：取色结果（包含 `color` 键，值为 RGB 颜色结构体，包含 `red`、`green`、`blue` 三个 `double` 字段，取值范围 0.0 到 1.0）

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Screenshot.PickColor "/" "app" "" {}
```
