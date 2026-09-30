# org.deepin.dde.Timedate1 接口参考

该接口提供时区、时间和自动同步设置能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Timedate1` |
| Object path | `/org/deepin/dde/Timedate1` |
| Interface | `org.deepin.dde.Timedate1` |
| Bus | System |
### 定时设置方法

#### SetTimezone

设置时区。

- **功能**：设置系统时区。
- **触发条件**：当用户在控制中心修改时区时调用。
- **使用场景**：控制中心时间日期设置修改时区。

- **输入参数**: `zone`（string, 类型 `s`）：时区名称；`message`（string, 类型 `s`）：操作说明消息
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Timedate1 \
  --object-path /org/deepin/dde/Timedate1 \
  --method org.deepin.dde.Timedate1.SetTimezone "Asia/Shanghai" "message"
```

#### SetLocalRTC

设置硬件时钟是否使用本地时间。

- **功能**：设置硬件时钟（RTC）是否使用本地时间，可选择是否修正系统时间。
- **触发条件**：当用户在控制中心切换硬件时钟使用本地时间或 UTC 时调用。
- **使用场景**：控制中心时间设置切换 RTC 时间标准。

- **输入参数**: `localRTC`（bool, 类型 `b`）：是否启用本地 RTC；`fixSystem`（bool, 类型 `b`）：是否修正系统时间；`message`（string, 类型 `s`）：操作说明消息
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Timedate1 \
  --object-path /org/deepin/dde/Timedate1 \
  --method org.deepin.dde.Timedate1.SetLocalRTC true false "message"
```

#### SetNTP

设置 NTP 自动同步。

- **功能**：启用或禁用 NTP 自动时间同步。
- **触发条件**：当用户在控制中心开启或关闭自动同步时间时调用。
- **使用场景**：控制中心时间设置 NTP 开关。

- **输入参数**: `useNTP`（bool, 类型 `b`）：是否启用；`message`（string, 类型 `s`）：操作说明消息
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.Timedate1 \
  --object-path /org/deepin/dde/Timedate1 \
  --method org.deepin.dde.Timedate1.SetNTP true "message"
```

#### SetNTPServer

设置 NTP 服务器。

- **功能**：设置 NTP 时间同步服务器地址。
- **触发条件**：当用户在控制中心修改 NTP 服务器时调用。
- **使用场景**：控制中心时间设置修改 NTP 服务器。

- **输入参数**: `server`（string, 类型 `s`）：NTP 服务器地址；`message`（string, 类型 `s`）：操作说明消息
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Timedate1 \
  --object-path /org/deepin/dde/Timedate1 \
  --method org.deepin.dde.Timedate1.SetNTPServer "ntp.aliyun.com" "message"
```

#### SetTime

设置系统时间。

- **输入参数**: `usec`（int64, 类型 `x`）：微秒时间戳；`relative`（bool, 类型 `b`）：是否相对时间；`message`（string, 类型 `s`）：操作说明消息
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.Timedate1 \
  --object-path /org/deepin/dde/Timedate1 \
  --method org.deepin.dde.Timedate1.SetTime 1609459200000000 false "message"
```
