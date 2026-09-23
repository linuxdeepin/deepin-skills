# org.deepin.dde.Keyboard1 接口参考

该接口提供键盘布局切换和状态查询能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Keyboard1` |
| Object path | `/org/deepin/dde/Keyboard1` |
| Interface | `org.deepin.dde.Keyboard1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 键盘布局操作

#### onClicked

处理键盘布局点击事件。

- **输入参数**: `button`（int32, 类型 `i`）：按钮；`x`（int32, 类型 `i`）：X 坐标；`y`（int32, 类型 `i`）：Y 坐标
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Keyboard1 \
  --object-path /org/deepin/dde/Keyboard1 \
  --method org.deepin.dde.Keyboard1.onClicked 1 100 200
```


### 键盘属性

#### layout（属性）

当前键盘布局。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Keyboard1 \
  --object-path /org/deepin/dde/Keyboard1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Keyboard1 layout
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Keyboard1 \
  --object-path /org/deepin/dde/Keyboard1 \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.Keyboard1 layout "us"
```
#### fcitxRunning（属性）

fcitx 输入法是否正在运行。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.Keyboard1 \
  --object-path /org/deepin/dde/Keyboard1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Keyboard1 fcitxRunning
```

### 键盘信号

#### layoutChanged

键盘布局变化时发出。

- **参数**: `text`（string, 类型 `s`）：新布局名称
- **触发条件**: 键盘布局被切换时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keyboard1 \
  --object-path /org/deepin/dde/Keyboard1
```

#### fcitxStatusChanged

fcitx 运行状态变化时发出。

- **参数**: `running`（bool, 类型 `b`）：是否正在运行
- **触发条件**: fcitx 启动或停止时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Keyboard1 \
  --object-path /org/deepin/dde/Keyboard1
```

---
