# org.deepin.dde.Daemon1 接口参考

该接口提供系统级守护进程管理和调试能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Daemon` |
| Object path | `/com/deepin/daemon/Daemon` |
| Interface | `org.deepin.dde.Daemon1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 守护进程方法

#### CallTrace

调用跟踪。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Daemon \
  --object-path /com/deepin/daemon/Daemon \
  --method org.deepin.dde.Daemon1.CallTrace
```

#### StartPart2

启动第二阶段。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Daemon \
  --object-path /com/deepin/daemon/Daemon \
  --method org.deepin.dde.Daemon1.StartPart2
```

