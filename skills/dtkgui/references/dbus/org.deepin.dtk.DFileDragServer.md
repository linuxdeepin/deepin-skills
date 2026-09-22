# org.deepin.dtk.DFileDragServer 接口参考

该接口提供文件拖拽服务能力。使用动态 baseService，服务名为 `QDBusConnection::sessionBus().baseService()`（如 `:1.23`），对象路径在运行时动态确定，无法静态指定。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `<dynamic baseService>` |
| Object path | `<dynamic>` |
| Interface | `org.deepin.dtk.DFileDragServer` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

> **动态 baseService 限制**：该接口的 D-Bus 服务名在运行时由 `QDBusConnection::sessionBus().baseService()` 确定，对象路径也是动态的。以下示例中使用 `:1.23` 作为占位符，实际使用时需替换为运行时获取的 baseService。

### 文件拖拽方法

#### GetURIList

获取拖拽的 URI 列表。

- **输入参数**: 无
- **返回值**: `as`（string 数组）：URI 列表

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /dfiledragserver \
  --method org.deepin.dtk.DFileDragServer.GetURIList
```

#### GetProcessID

获取拖拽源进程 ID。

- **输入参数**: 无
- **返回值**: `u`（uint32）：进程 ID

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /dfiledragserver \
  --method org.deepin.dtk.DFileDragServer.GetProcessID
```

#### GetState

获取拖拽状态。

- **输入参数**: 无
- **返回值**: `i`（int32）：拖拽状态

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /dfiledragserver \
  --method org.deepin.dtk.DFileDragServer.GetState
```

#### Proceed

继续拖拽操作。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /dfiledragserver \
  --method org.deepin.dtk.DFileDragServer.Proceed
```

#### Abort

中止拖拽操作。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /dfiledragserver \
  --method org.deepin.dtk.DFileDragServer.Abort
```

#### Clear

清除拖拽数据。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /dfiledragserver \
  --method org.deepin.dtk.DFileDragServer.Clear
```


### 文件拖拽属性

#### state（属性）

拖拽状态。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /dfiledragserver \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dtk.DFileDragServer state
```
设置示例：

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /dfiledragserver \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dtk.DFileDragServer state 0
```
#### supportedActions（属性）

支持的动作列表。

| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /dfiledragserver \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dtk.DFileDragServer supportedActions
```
设置示例：

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /dfiledragserver \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dtk.DFileDragServer supportedActions ["copy"]
```

### 文件拖拽信号

#### stateChanged

拖拽状态变化时发出。

- **参数**: `i`（int32, 类型 `i`）：新状态
- **触发条件**: 拖拽状态变化时发出

```bash
gdbus monitor --session \
  --dest :1.23 \
  --object-path /dfiledragserver
```

