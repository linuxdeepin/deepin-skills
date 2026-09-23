# org.deepin.dde.ScreenSaver1 接口参考

该接口提供屏幕保护管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ScreenSaver` |
| Object path | `/com/deepin/daemon/ScreenSaver` |
| Interface | `org.deepin.dde.ScreenSaver1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 屏幕保护方法

#### Start

启动屏保。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ScreenSaver \
  --object-path /com/deepin/daemon/ScreenSaver \
  --method org.deepin.dde.ScreenSaver1.Start
```

#### Stop

停止屏保。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ScreenSaver \
  --object-path /com/deepin/daemon/ScreenSaver \
  --method org.deepin.dde.ScreenSaver1.Stop
```

