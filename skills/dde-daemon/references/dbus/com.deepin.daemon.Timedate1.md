# com.deepin.daemon.Timedate1 接口参考

该接口提供时区、时间和自动同步设置能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `com.deepin.daemon.Timedate` |
| Object path | `/com/deepin/daemon/Timedate` |
| Interface | `com.deepin.daemon.Timedate1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 定时设置方法

#### SetTimezone

设置时区。

- **输入参数**: `timezone`（string, 类型 `s`）：时区名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.Timedate \
  --object-path /com/deepin/daemon/Timedate \
  --method com.deepin.daemon.Timedate1.SetTimezone "Asia/Shanghai"
```

#### SetNTP

设置 NTP 自动同步。

- **输入参数**: `enable`（bool, 类型 `b`）：是否启用
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.Timedate \
  --object-path /com/deepin/daemon/Timedate \
  --method com.deepin.daemon.Timedate1.SetNTP true
```

#### SetDate

设置日期。

- **输入参数**: `datetime`（int64, 类型 `x`）：时间戳
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.Timedate \
  --object-path /com/deepin/daemon/Timedate \
  --method com.deepin.daemon.Timedate1.SetDate 1609459200
```

