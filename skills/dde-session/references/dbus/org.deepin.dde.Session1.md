# org.deepin.dde.Session1 接口参考

该接口提供会话级管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Session1` |
| Object path | `/org/deepin/dde/Session1` |
| Interface | `org.deepin.dde.Session1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 会话操作

#### Logout

注销当前会话。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Session1 \
  --object-path /org/deepin/dde/Session1 \
  --method org.deepin.dde.Session1.Logout
```

#### GetSessionPid

获取会话进程 PID。

- **输入参数**: 无
- **返回值**: `i`（int32）：会话进程 PID

```bash
gdbus call --session \
  --dest org.deepin.dde.Session1 \
  --object-path /org/deepin/dde/Session1 \
  --method org.deepin.dde.Session1.GetSessionPid
```

#### GetSessionPath

获取会话路径。

- **输入参数**: 无
- **返回值**: `s`（string）：会话路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Session1 \
  --object-path /org/deepin/dde/Session1 \
  --method org.deepin.dde.Session1.GetSessionPath
```

