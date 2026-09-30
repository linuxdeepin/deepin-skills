# org.deepin.dde.ClipboardLoader1 接口参考

该接口在 Session 总线上注册，对象路径为 `/org/deepin/dde/ClipboardLoader1`，提供剪贴板守护进程的剪贴板数据接收与恢复能力。dde-clipboard-daemon 监听系统剪贴板变化，将新数据通过 `dataComing` 信号发送给前端；前端可通过 `dataReborned` 方法将指定数据恢复到系统剪贴板。

> 注意：`dataComing` 信号和 `dataReborned` 方法传输的 `buf` 参数为字节数组类型，内部为 dde-clipboard 组件自定义的序列化格式，包含剪贴板条目的格式映射、类型、URL、图片、文本、创建时间信息，非标准数据格式。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ClipboardLoader1` |
| Object path | `/org/deepin/dde/ClipboardLoader1` |
| Interface | `org.deepin.dde.ClipboardLoader1` |
| Bus | Session |

## 方法

### dataReborned

**功能**：将指定的剪贴板数据恢复到系统剪贴板。前端从剪贴板历史列表中选择一条记录后，通过此方法将该项数据写回系统剪贴板，实现重新粘贴历史内容的功能。参数为 dde-clipboard 组件内部序列化格式的字节数组。

**触发条件**：由前端 D-Bus 调用触发，当用户在剪贴板历史界面点击某条历史记录时调用。

**使用场景**：用户在剪贴板管理界面选择一条历史记录进行重新粘贴时，前端调用此方法将数据恢复到系统剪贴板，随后用户即可在其他应用中执行粘贴操作。

参数：
- `buf`（字节数组）：剪贴板条目数据的序列化字节数组

用例：
```bash
dbus-send --session --print-reply \
  --dest=org.deepin.dde.ClipboardLoader1 \
  /org/deepin/dde/ClipboardLoader1 \
  org.deepin.dde.ClipboardLoader1.dataReborned \
  array:byte:
```

## 信号

### dataComing

**功能**：系统剪贴板数据发生变化时发出，携带新的剪贴板条目数据的序列化字节数组。

**触发条件**：当用户执行复制或剪切操作导致系统剪贴板内容更新时，守护进程检测到变化并发出此信号。在 X11 和 Wayland 会话环境下均会触发。

**使用场景**：前端监听此信号以实时获取新的剪贴板内容，将其添加到剪贴板历史列表中供用户后续查看和选择。

参数：
- `buf`（字节数组）：剪贴板条目数据的序列化字节数组

用例：
```bash
dbus-monitor --session \
  "type='signal',interface='org.deepin.dde.ClipboardLoader1',member='dataComing'"
```
