# org.deepin.dde.Audio1 接口参考

该接口提供系统级音频设备管理能力，包括音频设备、音量、端口和音频服务器管理，影响所有应用的音频输入输出，而非仅控制单个应用的音量。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Audio1` |
| Object path | `/org/deepin/dde/Audio1` |
| Interface | `org.deepin.dde.Audio1` |
| Bus | Session |
### 音频管理方法

#### IsPortEnabled

查询端口是否启用。

- **功能**：查询指定音频端口是否已启用。
- **触发条件**：当需要检查特定端口可用性时调用。
- **使用场景**：音频设备管理、端口状态检查。

- **输入参数**: `cardId`（uint32, 类型 `u`）：声卡 ID；`portName`（string, 类型 `s`）：端口名称
- **返回值**: `b`（bool）：是否启用

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio1 \
  --object-path /org/deepin/dde/Audio1 \
  --method org.deepin.dde.Audio1.IsPortEnabled 0 "speaker"
```

#### NoRestartPulseAudio

设置是否不重启 PulseAudio。

- **功能**：设置是否在音频配置变更时不重启 PulseAudio。
- **触发条件**：当需要控制音频配置变更后是否重启 PulseAudio 服务时调用。
- **使用场景**：音频服务管理，避免重启 PulseAudio 导致声音中断。
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio1 \
  --object-path /org/deepin/dde/Audio1 \
  --method org.deepin.dde.Audio1.NoRestartPulseAudio
```

#### Reset

重置音频配置。

- **功能**：重置音频配置到默认状态。
- **触发条件**：当用户在控制中心点击恢复默认音频设置时调用。
- **使用场景**：控制中心声音设置恢复默认。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio1 \
  --object-path /org/deepin/dde/Audio1 \
  --method org.deepin.dde.Audio1.Reset
```

#### SetBluetoothAudioMode

设置蓝牙音频模式。

- **功能**：设置蓝牙音频设备的音频模式（如 A2DP 或 HFP）。
- **触发条件**：当用户切换蓝牙音频设备的模式时调用。
- **使用场景**：控制中心蓝牙音频模式切换。
- **输入参数**: `mode`（string, 类型 `s`）：音频模式
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio1 \
  --object-path /org/deepin/dde/Audio1 \
  --method org.deepin.dde.Audio1.SetBluetoothAudioMode "a2dp"
```

#### SetPort

设置音频端口。

- **功能**：设置当前音频输出或输入端口。
- **触发条件**：当用户在控制中心选择音频输出或输入设备端口时调用。
- **使用场景**：控制中心声音设置选择输出/输入端口。
- **输入参数**: `cardId`（uint32, 类型 `u`）：声卡 ID；`portName`（string, 类型 `s`）：端口名称；`direction`（int32, 类型 `i`）：方向（0=输出，1=输入）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio1 \
  --object-path /org/deepin/dde/Audio1 \
  --method org.deepin.dde.Audio1.SetPort 0 "speaker" 0
```

#### SetPortEnabled

设置端口启用状态。

- **功能**：启用或禁用指定音频端口。
- **触发条件**：当用户在控制中心切换端口开关时调用。
- **使用场景**：控制中心音频端口管理。

- **输入参数**: `cardId`（uint32, 类型 `u`）：声卡 ID；`portName`（string, 类型 `s`）：端口名称；`enabled`（bool, 类型 `b`）：是否启用
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio1 \
  --object-path /org/deepin/dde/Audio1 \
  --method org.deepin.dde.Audio1.SetPortEnabled 0 "speaker" true
```

#### SetCurrentAudioServer

设置当前音频服务器。

- **功能**：设置当前使用的音频服务器（如 PulseAudio 或 PipeWire）。
- **触发条件**：当用户在控制中心切换音频服务器时调用。
- **使用场景**：控制中心音频服务器切换。
- **输入参数**: `server`（string, 类型 `s`）：服务器名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio1 \
  --object-path /org/deepin/dde/Audio1 \
  --method org.deepin.dde.Audio1.SetCurrentAudioServer "pulseaudio"
```

#### SetMono

设置单声道。

- **功能**：设置音频是否使用单声道模式。
- **触发条件**：当用户在控制中心切换单声道/立体声时调用。
- **使用场景**：控制中心声音设置单声道开关。
- **输入参数**: `value`（bool, 类型 `b`）：是否单声道
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio1 \
  --object-path /org/deepin/dde/Audio1 \
  --method org.deepin.dde.Audio1.SetMono true
```

#### StopAudioService

停止音频服务。

- **功能**：停止音频服务。
- **触发条件**：当需要停止音频服务（如切换音频服务器前）时调用。
- **使用场景**：音频服务管理，切换音频服务器前停止当前服务。
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Audio1 \
  --object-path /org/deepin/dde/Audio1 \
  --method org.deepin.dde.Audio1.StopAudioService
```
