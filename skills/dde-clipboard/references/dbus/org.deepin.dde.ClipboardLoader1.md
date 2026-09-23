# org.deepin.dde.ClipboardLoader1 接口参考

该接口提供剪贴板守护进程的数据加载能力，负责剪贴板数据的接收和恢复。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ClipboardLoader1` |
| Object path | `/org/deepin/dde/ClipboardLoader1` |
| Interface | `org.deepin.dde.ClipboardLoader1` |
| Bus | Session |


### 数据管理

#### dataReborned

恢复剪贴板数据。将之前保存的剪贴板数据重新写入剪贴板。

- **输入参数**: `buf`（byte array, 类型 `ay`）：序列化的剪贴板数据
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ClipboardLoader1 \
  --object-path /org/deepin/dde/ClipboardLoader1 \
  --method org.deepin.dde.ClipboardLoader1.dataReborned \
  "b'<data>'"
```


### 信号

#### dataComing

新剪贴板数据到达时发出。守护进程检测到剪贴板内容变化时，通过此信号通知前端。

- **参数**: `buf`（byte array, 类型 `ay`）：序列化的剪贴板数据
- **触发条件**: 剪贴板内容发生变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.ClipboardLoader1 \
  --object-path /org/deepin/dde/ClipboardLoader1
```

---
