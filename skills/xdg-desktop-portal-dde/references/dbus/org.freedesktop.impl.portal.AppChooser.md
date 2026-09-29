# org.freedesktop.impl.portal.AppChooser 接口参考

该接口提供应用选择器能力，允许沙箱应用弹出应用选择对话框供用户选择目标应用。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.AppChooser` |
| Bus | Session |

### 应用选择方法

#### ChooseApplication

显示应用选择对话框，供用户从候选应用列表中选择一个应用。

- **功能**: 弹出应用选择对话框，展示候选应用列表，返回用户选择的应用。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求选择目标应用时触发。
- **使用场景**: 沙箱应用需要用户从多个应用中选择一个来打开文件或链接时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`app_id`（string, 类型 `s`）：应用 ID；`parent_window`（string, 类型 `s`）：父窗口标识；`choices`（字符串数组, 类型 `as`）：候选应用 ID 列表；`options`（字典, 类型 `a{sv}`）：附加选项
- **返回值**: `u`（uint）：响应码；`results`（字典, 类型 `a{sv}`）：选择结果

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.AppChooser.ChooseApplication "/" "app" "" [] {}
```

#### UpdateChoices

更新应用选择对话框中的候选应用列表。

- **功能**: 更新已打开的应用选择对话框中的候选应用列表。
- **触发条件**: 当沙箱应用需要在应用选择对话框仍然打开时动态更新候选应用列表时触发。
- **使用场景**: 沙箱应用在应用选择对话框打开后发现可用应用列表发生变化，需要刷新候选列表时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`choices`（字符串数组, 类型 `as`）：更新的候选应用 ID 列表
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.AppChooser.UpdateChoices "/" []
```
