# org.deepin.dde.Timedate1 接口参考

该接口提供时区、时间和自动同步设置能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Timedate1` |
| Object path | `/org/deepin/dde/Timedate1` |
| Interface | `org.deepin.dde.Timedate1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 定时设置方法

#### SetTimezone

设置时区。

- **输入参数**: `timezone`（string, 类型 `s`）：时区名称；`message`（string, 类型 `s`）：消息
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Timedate1 \
  --object-path /org/deepin/dde/Timedate1 \
  --method org.deepin.dde.Timedate1.SetTimezone "Asia/Shanghai" ""
```

#### SetLocalRTC

设置硬件时钟是否使用本地时间。

- **输入参数**: `enabled`（bool, 类型 `b`）：是否启用本地 RTC；`fixSystem`（bool, 类型 `b`）：是否修正系统时间；`message`（string, 类型 `s`）：消息
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Timedate1 \
  --object-path /org/deepin/dde/Timedate1 \
  --method org.deepin.dde.Timedate1.SetLocalRTC true false ""
```

#### SetNTP

设置 NTP 自动同步。

- **输入参数**: `enabled`（bool, 类型 `b`）：是否启用；`message`（string, 类型 `s`）：消息
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.Timedate1 \
  --object-path /org/deepin/dde/Timedate1 \
  --method org.deepin.dde.Timedate1.SetNTP true ""
```

#### SetNTPServer

设置 NTP 服务器。

- **输入参数**: `server`（string, 类型 `s`）：NTP 服务器地址；`message`（string, 类型 `s`）：消息
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Timedate1 \
  --object-path /org/deepin/dde/Timedate1 \
  --method org.deepin.dde.Timedate1.SetNTPServer "ntp.aliyun.com" ""
```

#### SetTime

设置系统时间。

- **输入参数**: `usec`（int64, 类型 `x`）：微秒时间戳；`relative`（bool, 类型 `b`）：是否相对时间；`message`（string, 类型 `s`）：消息
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.Timedate1 \
  --object-path /org/deepin/dde/Timedate1 \
  --method org.deepin.dde.Timedate1.SetTime 1609459200000000 false ""
```
