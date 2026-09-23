# org.deepin.dde.EventLog1 接口参考

该接口提供系统事件日志记录能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.EventLog` |
| Object path | `/com/deepin/daemon/EventLog` |
| Interface | `org.deepin.dde.EventLog1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 事件日志方法

#### WriteEventLog

写入事件日志。

- **输入参数**: `event`（string, 类型 `s`）：事件 JSON 字符串
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.EventLog \
  --object-path /com/deepin/daemon/EventLog \
  --method org.deepin.dde.EventLog1.WriteEventLog "{}"
```

