# org.freedesktop.impl.portal.Access 接口参考

该接口提供访问对话框能力，用于沙箱应用向用户请求访问受限资源的确认。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Access` |
| Bus | Session |

### 访问方法

#### AccessDialog

显示访问对话框，供沙箱应用向用户展示标题、副标题、正文信息并获取用户的选择结果。

- **功能**: 弹出一个访问对话框，展示标题、副标题、正文，并返回用户的选择结果。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求访问受限资源时触发。
- **使用场景**: 沙箱应用需要用户确认后才能访问某项系统资源（如网络、文件系统路径）时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`app_id`（string, 类型 `s`）：应用 ID；`parent_window`（string, 类型 `s`）：父窗口标识；`title`（string, 类型 `s`）：标题；`subtitle`（string, 类型 `s`）：副标题；`body`（string, 类型 `s`）：正文；`options`（字典, 类型 `a{sv}`）：选项
- **返回值**: `u`（uint）：响应码；`results`（字典, 类型 `a{sv}`）：对话框结果

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Access.AccessDialog "/" "app" "" "标题" "副标题" "正文" {}
```
