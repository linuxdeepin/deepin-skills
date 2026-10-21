# org.freedesktop.impl.portal.FileChooser 接口参考

该接口提供文件打开和保存对话框能力，允许沙箱应用通过系统标准的文件选择对话框选择文件。

本文记录 Portal 后端协作接口，普通应用调用前端 `org.freedesktop.portal.Desktop` 的 `org.freedesktop.portal.*` 接口。后端示例中的应用身份与请求句柄必须来自实际前端请求，不能将演示参数用于应用权限判断。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.FileChooser` |
| Bus | Session |

### 文件选择方法

#### OpenFile

打开文件选择对话框。

- **功能**: 弹出文件打开对话框，供用户选择一个或多个文件，返回所选文件的 URI 列表。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求打开文件选择对话框时触发。
- **使用场景**: 沙箱应用需要用户选择要打开的文件时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`app_id`（string, 类型 `s`）：应用 ID；`parent_window`（string, 类型 `s`）：父窗口标识；`title`（string, 类型 `s`）：标题；`options`（字典, 类型 `a{sv}`）：选项
- **返回值**: `u`（uint）：响应码；`results`（字典, 类型 `a{sv}`）：文件选择结果

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.FileChooser.OpenFile "${portal_handle:?请使用前端请求的实际 handle}" "${portal_app_id:?请使用实际请求的应用标识}" "" "选择文件" {}
```

#### SaveFile

打开文件保存对话框。

- **功能**: 弹出文件保存对话框，供用户指定保存位置和文件名，返回用户选择的保存路径。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求保存文件时触发。
- **使用场景**: 沙箱应用需要用户指定文件保存位置时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`app_id`（string, 类型 `s`）：应用 ID；`parent_window`（string, 类型 `s`）：父窗口标识；`title`（string, 类型 `s`）：标题；`options`（字典, 类型 `a{sv}`）：选项
- **返回值**: `u`（uint）：响应码；`results`（字典, 类型 `a{sv}`）：文件保存结果

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.FileChooser.SaveFile "${portal_handle:?请使用前端请求的实际 handle}" "${portal_app_id:?请使用实际请求的应用标识}" "" "保存文件" {}
```

#### SaveFiles

打开多文件保存对话框。

- **功能**: 弹出文件保存对话框，供用户为多个文件指定保存位置，返回用户选择的保存路径。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求保存多个文件时触发。
- **使用场景**: 沙箱应用需要用户指定多个文件的保存位置时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`app_id`（string, 类型 `s`）：应用 ID；`parent_window`（string, 类型 `s`）：父窗口标识；`title`（string, 类型 `s`）：标题；`options`（字典, 类型 `a{sv}`）：选项
- **返回值**: `u`（uint）：响应码；`results`（字典, 类型 `a{sv}`）：文件保存结果

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.FileChooser.SaveFiles "${portal_handle:?请使用前端请求的实际 handle}" "${portal_app_id:?请使用实际请求的应用标识}" "" "保存多个文件" {}
```
