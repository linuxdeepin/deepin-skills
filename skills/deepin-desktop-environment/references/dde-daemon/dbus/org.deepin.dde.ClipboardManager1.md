# org.deepin.dde.ClipboardManager1 接口参考

该接口提供剪贴板目标管理能力，包括成为剪贴板拥有者、移除目标、保存剪贴板内容和写入内容。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ClipboardManager1` |
| Object path | `/org/deepin/dde/ClipboardManager1` |
| Interface | `org.deepin.dde.ClipboardManager1` |
| Bus | Session |

### 剪贴板管理方法

#### BecomeClipboardOwner

成为剪贴板拥有者。

- **功能**：使当前调用者成为剪贴板的拥有者。
- **触发条件**：当应用需要接管剪贴板控制权时调用。
- **使用场景**：应用接管剪贴板，获取剪贴板内容变更通知。
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ClipboardManager1 \
  --object-path /org/deepin/dde/ClipboardManager1 \
  --method org.deepin.dde.ClipboardManager1.BecomeClipboardOwner
```

#### RemoveTarget

移除剪贴板目标。

- **功能**：移除指定的剪贴板目标。
- **触发条件**：当需要取消某个剪贴板目标的监听时调用。
- **使用场景**：剪贴板目标管理，取消目标监听。
- **输入参数**: `target`（uint32, 类型 `u`）：目标标识
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ClipboardManager1 \
  --object-path /org/deepin/dde/ClipboardManager1 \
  --method org.deepin.dde.ClipboardManager1.RemoveTarget 1
```

#### SaveClipboard

保存当前剪贴板内容。

- **功能**：将当前剪贴板内容保存到持久化存储。
- **触发条件**：当剪贴板内容发生变化时由剪贴板管理器调用。
- **使用场景**：剪贴板历史记录管理、重启后恢复剪贴板内容。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ClipboardManager1 \
  --object-path /org/deepin/dde/ClipboardManager1 \
  --method org.deepin.dde.ClipboardManager1.SaveClipboard
```

#### WriteContent

写入剪贴板内容。

- **功能**：将持久化存储的剪贴板内容写回系统剪贴板。
- **触发条件**：当用户从剪贴板历史中选择恢复某条记录时调用。
- **使用场景**：剪贴板历史记录恢复。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ClipboardManager1 \
  --object-path /org/deepin/dde/ClipboardManager1 \
  --method org.deepin.dde.ClipboardManager1.WriteContent
```
