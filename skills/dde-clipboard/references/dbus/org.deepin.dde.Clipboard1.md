# org.deepin.dde.Clipboard1 接口参考

该接口提供 DDE 剪贴板历史服务的显示/隐藏控制能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Clipboard1` |
| Object path | `/org/deepin/dde/Clipboard1` |
| Interface | `org.deepin.dde.Clipboard1` |
| Bus | Session |


### 窗口控制

#### Toggle

切换剪贴板管理界面的显示/隐藏状态。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Clipboard1 \
  --object-path /org/deepin/dde/Clipboard1 \
  --method org.deepin.dde.Clipboard1.Toggle
```

#### Show

显示剪贴板管理界面。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Clipboard1 \
  --object-path /org/deepin/dde/Clipboard1 \
  --method org.deepin.dde.Clipboard1.Show
```

#### Hide

隐藏剪贴板管理界面。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Clipboard1 \
  --object-path /org/deepin/dde/Clipboard1 \
  --method org.deepin.dde.Clipboard1.Hide
```


### 属性

#### clipboardVisible（属性）

剪贴板管理界面是否可见。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Clipboard1 \
  --object-path /org/deepin/dde/Clipboard1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Clipboard1 clipboardVisible
```


### 信号

#### clipboardVisibleChanged

剪贴板管理界面可见状态变化时发出。

- **参数**: `visible`（boolean, 类型 `b`）：界面是否可见
- **触发条件**: 剪贴板管理界面显示或隐藏时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Clipboard1 \
  --object-path /org/deepin/dde/Clipboard1
```

---
