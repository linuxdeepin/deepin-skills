# org.deepin.dde.Audio1 接口参考

该接口提供系统级音频设备管理能力，包括音频设备、音量、端口和音频服务器管理，影响所有应用的音频输入输出，而非仅控制单个应用的音量。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Audio` |
| Object path | `/com/deepin/daemon/Audio` |
| Interface | `org.deepin.dde.Audio1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 音频管理方法

#### IsPortEnabled

查询端口是否启用。

- **输入参数**: `port`（object, 类型 `o`）：端口路径
- **返回值**: `b`（bool）：是否启用

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.IsPortEnabled "/path/to/port"
```

#### NoRestartPulseAudio

设置是否不重启 PulseAudio。

- **输入参数**: `value`（bool, 类型 `b`）：是否不重启
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.NoRestartPulseAudio true
```

#### Reset

重置音频配置。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.Reset
```

#### SetBluetoothAudioMode

设置蓝牙音频模式。

- **输入参数**: `mode`（string, 类型 `s`）：音频模式
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.SetBluetoothAudioMode "a2dp"
```

#### SetPort

设置音频端口。

- **输入参数**: `port`（object, 类型 `o`）：端口路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.SetPort "/path/to/port"
```

#### SetPortEnabled

设置端口启用状态。

- **输入参数**: `port`（object, 类型 `o`）：端口路径；`enabled`（bool, 类型 `b`）：是否启用
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.SetPortEnabled "/path/to/port" true
```

#### SetCurrentAudioServer

设置当前音频服务器。

- **输入参数**: `server`（string, 类型 `s`）：服务器名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.SetCurrentAudioServer "pulseaudio"
```

#### SetMono

设置单声道。

- **输入参数**: `value`（bool, 类型 `b`）：是否单声道
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.SetMono true
```

#### StopAudioService

停止音频服务。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.StopAudioService
```

#### Tick

心跳检测。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.Tick
```

#### GetMeter

获取音量计。

- **输入参数**: 无
- **返回值**: `o`（object path）：音量计路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.GetMeter
```

#### SetBalance

设置声道平衡。

- **输入参数**: `value`（double, 类型 `d`）：平衡值
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.SetBalance 0.5
```

#### SetFade

设置淡入淡出。

- **输入参数**: `value`（double, 类型 `d`）：淡入淡出值
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.SetFade 0.5
```

#### SetMute

设置静音。

- **输入参数**: `value`（bool, 类型 `b`）：是否静音
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.SetMute true
```

#### SetVolume

设置音量。

- **输入参数**: `value`（double, 类型 `d`）：音量值
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio \
  --object-path /com/deepin/daemon/Audio \
  --method org.deepin.dde.Audio1.SetVolume 0.5
```

