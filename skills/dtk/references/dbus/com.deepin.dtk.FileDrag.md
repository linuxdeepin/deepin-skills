# com.deepin.dtk.FileDrag 接口参考

该接口提供跨进程文件拖拽交互能力。拖拽源进程在 Session 总线上注册此接口对象，文件接收方（拖放目标）通过 D-Bus 与拖拽源通信，实现拖拽状态查询、进度同步和数据回传。

> **兼容性说明**：dtkgui 仅注册了 `com.deepin.dtk.FileDrag` 一个 D-Bus 接口（对象路径 `/Ddnd`），为当前正在使用的唯一接口，不存在为兼容旧版本而保留的别名或废弃接口。该接口的服务名为动态 baseService（由 D-Bus 守护进程在运行时分配），无固定的 well-known service name，亦无历史兼容服务名。

> **动态 Service 说明**：该接口未注册 well-known service name，D-Bus 服务名为拖拽源进程的 baseService（即拖拽源进程的唯一连接名，形如 `:1.23`）。接收方从拖拽事件的 MIME 数据中获取 service 名称（MIME key: `x-dtk-file-drag/service`）和会话 UUID（MIME key: `x-dtk-file-drag/uuid`）后，方可调用此接口。以下示例中 `:1.23` 为占位符，实际使用时需替换为运行时获取的 baseService。

## 接口信息

| 字段 | 值 |
|------|------|
| Bus | Session |
| Service | `<dynamic baseService>`（如 `:1.23`） |
| Object path | `/Ddnd` |
| Interface | `com.deepin.dtk.FileDrag` |

## 方法

### setData

接收方向拖拽源设置数据，通过 UUID 指定拖拽会话。当值发生变化时，拖拽源进程内部会进行相应处理（此过程不通过 D-Bus 传输）。

- **功能**：接收方向拖拽源回传数据，通过 UUID 和键值对指定要设置的数据。
- **触发条件**：接收方在拖放操作中需要向拖拽源传递目标数据时调用。
- **使用场景**：拖放目标接收到文件后，需要将文件路径或自定义数据回传给拖拽源进程的场景。

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

- **功能**：获取拖拽会话的当前状态，返回值为拖拽状态枚举（见下方枚举定义）。
- **触发条件**：接收方主动查询时调用。
- **使用场景**：接收方需要判断拖拽操作当前处于进行中、暂停、完成还是失败状态，以决定后续处理逻辑。

- **输入参数**:
  - `uuid` (string): 拖拽会话 UUID
- **返回值**: `i` (int32): 拖拽状态，取值见下方拖拽状态枚举

```bash
gdbus call --session \
  --dest :1.23 \
  --object-path /Ddnd \
  --method com.deepin.dtk.FileDrag.state \
  "550e8400-e29b-41d4-a716-446655440000"
```

### progress

查询指定拖拽会话的进度。

- **功能**：获取拖拽会话的当前进度值。
- **触发条件**：接收方主动查询时调用。
- **使用场景**：接收方需要显示拖拽操作进度或根据进度判断是否完成传输的场景。

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

- **功能**：通知接收方拖拽源对象已销毁，对应的拖拽会话不再有效。
- **触发条件**：拖拽源对象销毁时发出。
- **使用场景**：接收方收到此信号后应清理与该拖拽会话相关的本地资源，停止对该会话的后续查询和调用。

- **参数**:
  - `uuid` (string): 被销毁的拖拽会话 UUID

```bash
gdbus monitor --session \
  --dest :1.23 \
  --object-path /Ddnd
```

### stateChanged

拖拽会话状态变化时发出。

- **功能**：通知接收方拖拽会话状态已变更，接收方可据此更新 UI 或调整处理逻辑。
- **触发条件**：拖拽源状态发生变化时发出。
- **使用场景**：接收方需要实时感知拖拽状态切换（如从进行中变为完成或失败）以更新界面提示的场景。

- **参数**:
  - `uuid` (string): 拖拽会话 UUID
  - `state` (int32): 新状态，取值见下方拖拽状态枚举

```bash
gdbus monitor --session \
  --dest :1.23 \
  --object-path /Ddnd
```

### progressChanged

拖拽会话进度变化时发出。

- **功能**：通知接收方拖拽传输进度已更新，接收方可据此刷新进度显示。
- **触发条件**：拖拽源进度发生变化时发出。
- **使用场景**：接收方需要实时展示拖拽传输进度条或百分比的场景。

- **参数**:
  - `uuid` (string): 拖拽会话 UUID
  - `progress` (int32): 当前进度

```bash
gdbus monitor --session \
  --dest :1.23 \
  --object-path /Ddnd
```

## 拖拽状态枚举

| 枚举值 | 数值 | 说明 |
|--------|------|------|
| Failed | -1 | 拖拽失败 |
| Stalled | 0 | 拖拽停滞 |
| Paused | 1 | 拖拽暂停 |
| Running | 2 | 拖拽进行中 |
| Finished | 3 | 拖拽完成 |
| CustomState | 0x100 | 自定义状态起始值 |
