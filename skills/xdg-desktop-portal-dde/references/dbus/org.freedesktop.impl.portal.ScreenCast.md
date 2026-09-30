# org.freedesktop.impl.portal.ScreenCast 接口参考

该接口提供屏幕共享能力，允许沙箱应用通过 Portal 接口共享屏幕或窗口内容。仅在 Wayland 环境下可用。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.ScreenCast` |
| Bus | Session |

> **平台可用性**: 仅在 Wayland 环境下可用。

### 属性

| 属性名 | 类型 | 权限 | 说明 |
|--------|------|------|------|
| `version` | `u` | read | 接口版本号 |
| `AvailableSourceTypes` | `u` | read | 可用的屏幕共享源类型（位掩码）。取值为 `1`（DESKTOP，共享整个桌面）、`2`（WINDOW，共享单个窗口），可按位或组合 |
| `AvailableCursorModes` | `u` | read | 可用的光标模式（位掩码）。取值为 `1`（HIDDEN，隐藏光标）、`2`（EMBEDDED，将光标内嵌到画面中）、`4`（METADATA，通过元数据传递光标位置），可按位或组合 |

### 屏幕共享方法

#### CreateSession

创建屏幕共享会话。

- **功能**: 为沙箱应用创建一个屏幕共享会话，后续的源选择和共享启动操作需基于此会话进行。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求创建屏幕共享会话时触发。
- **使用场景**: 沙箱应用需要共享屏幕（如视频会议、远程桌面、屏幕录制）时，首先调用此方法建立会话。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`session_handle`（object path, 类型 `o`）：会话句柄；`app_id`（string, 类型 `s`）：应用 ID；`options`（字典, 类型 `a{sv}`）：选项
- **返回值**: `u`（uint）：响应码；`results`（字典, 类型 `a{sv}`）：会话创建结果

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.ScreenCast.CreateSession "/" "/" "app" {}
```

#### SelectSources

选择屏幕共享源。

- **功能**: 为已创建的屏幕共享会话选择共享源类型和光标模式。通过 `options` 指定源类型（`desktop` 或 `window`）和光标模式。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求选择屏幕共享源时触发。
- **使用场景**: 沙箱应用在创建会话后、启动共享前，需要指定共享整个桌面还是单个窗口以及光标显示方式时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`session_handle`（object path, 类型 `o`）：会话句柄；`app_id`（string, 类型 `s`）：应用 ID；`options`（字典, 类型 `a{sv}`）：选项（支持 `type` 键指定源类型、`cursor-mode` 键指定光标模式）
- **返回值**: `u`（uint）：响应码；`results`（字典, 类型 `a{sv}`）：选择源结果

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.ScreenCast.SelectSources "/" "/" "app" {}
```

#### Start

启动屏幕共享。

- **功能**: 启动已配置好的屏幕共享会话，返回共享流的节点 ID 和选项信息，调用方可基于这些信息获取屏幕画面数据。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求启动屏幕共享时触发。
- **使用场景**: 沙箱应用在选择共享源后，需要实际开始获取屏幕画面数据时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`session_handle`（object path, 类型 `o`）：会话句柄；`app_id`（string, 类型 `s`）：应用 ID；`parent_window`（string, 类型 `s`）：父窗口标识；`options`（字典, 类型 `a{sv}`）：选项
- **返回值**: `u`（uint）：响应码；`results`（字典, 类型 `a{sv}`）：共享结果（包含 `streams` 键，值为共享流信息数组）

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.ScreenCast.Start "/" "/" "app" "" {}
```
