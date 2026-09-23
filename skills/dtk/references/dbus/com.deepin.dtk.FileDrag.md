# com.deepin.dtk.FileDrag 接口参考

该接口提供跨进程文件拖拽交互能力。拖拽源进程在 Session 总线上注册此接口对象，文件接收方（拖放目标）通过 D-Bus 与拖拽源通信，实现拖拽状态查询、进度同步和数据回传。

> **动态 Service 说明**：该接口未注册 well-known service name，D-Bus 服务名为拖拽源进程的 baseService（即 `QDBusConnection::sessionBus().baseService()`，形如 `:1.23`）。接收方从拖拽事件的 MIME 数据中获取 service 名称（MIME key: `x-dtk-file-drag/service`）和会话 UUID（MIME key: `x-dtk-file-drag/uuid`）后，方可调用此接口。以下示例中 `:1.23` 为占位符，实际使用时需替换为运行时获取的 baseService。

## 接口信息

| 字段 | 值 |
|------|------|
| Bus | Session |
| Service | `<dynamic baseService>`（如 `:1.23`） |
| Object path | `/Ddnd` |
| Interface | `com.deepin.dtk.FileDrag` |

> **待核验声明**：本文档接口信息基于 dtkgui 源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

## 方法

### setData

接收方向拖拽源设置数据，通过 UUID 指定拖拽会话。当值发生变化时，拖拽源会发出 `targetDataChanged` 信号。

- **输入参数**:
  - `uuid` (string): 拖拽会话 UUID
  - `key` (string): 数据键名
  - `value` (string): 数据值
- **返回值**: 无

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /Ddnd \
  --method com.deepin.dtk.FileDrag.setData \
  "550e8400-e29b-41d4-a716-446655440000" "targetUrl" "file:///home/user/file.txt"
```

### state

查询指定拖拽会话的状态。

- **输入参数**:
  - `uuid` (string): 拖拽会话 UUID
- **返回值**: `i` (int32): 拖拽状态，取值见下方 DFileDragState 枚举

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /Ddnd \
  --method com.deepin.dtk.FileDrag.state \
  "550e8400-e29b-41d4-a716-446655440000"
```

### progress

查询指定拖拽会话的进度。

- **输入参数**:
  - `uuid` (string): 拖拽会话 UUID
- **返回值**: `i` (int32): 进度值

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /Ddnd \
  --method com.deepin.dtk.FileDrag.progress \
  "550e8400-e29b-41d4-a716-446655440000"
```

## 信号

### serverDestroyed

拖拽源对象销毁时发出，通知接收方拖拽会话已结束。

- **参数**:
  - `uuid` (string): 被销毁的拖拽会话 UUID
- **触发条件**: DFileDragServer 对象析构时发出

```bash
gdbus monitor --session \
  --dest :1.23 \
  --object-path /Ddnd
```

### stateChanged

拖拽会话状态变化时发出。

- **参数**:
  - `uuid` (string): 拖拽会话 UUID
  - `state` (int32): 新状态，取值见 DFileDragState 枚举
- **触发条件**: 拖拽源调用 setState 改变状态时发出

```bash
gdbus monitor --session \
  --dest :1.23 \
  --object-path /Ddnd
```

### progressChanged

拖拽会话进度变化时发出。

- **参数**:
  - `uuid` (string): 拖拽会话 UUID
  - `progress` (int32): 当前进度
- **触发条件**: 拖拽源调用 setProgress 更新进度时发出

```bash
gdbus monitor --session \
  --dest :1.23 \
  --object-path /Ddnd
```

### targetDataChanged

拖拽会话的目标数据变更时发出。

- **参数**:
  - `key` (string): 变更的数据键名
- **触发条件**: 接收方调用 setData 设置数据且值发生变化时由拖拽源发出

```bash
gdbus monitor --session \
  --dest :1.23 \
  --object-path /Ddnd
```

## DFileDragState 枚举

| 枚举值 | 数值 | 说明 |
|--------|------|------|
| Failed | -1 | 拖拽失败 |
| Stalled | 0 | 拖拽停滞 |
| Paused | 1 | 拖拽暂停 |
| Running | 2 | 拖拽进行中 |
| Finished | 3 | 拖拽完成 |
| CustomState | 0x100 | 自定义状态起始值 |
