# org.deepin.dde.SoundThemePlayer1 接口参考

该接口提供声音主题播放控制能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.SoundThemePlayer1` |
| Object path | `/org/deepin/dde/SoundThemePlayer1` |
| Interface | `org.deepin.dde.SoundThemePlayer1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 声音播放方法

#### Play

播放指定声音。

- **输入参数**: `s`（string, 类型 `s`）：声音名称
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.Play "message"
```

#### Stop

停止播放。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.Stop
```

#### PausePlay

暂停播放。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.PausePlay
```

#### SetVolume

设置音量。

- **输入参数**: `d`（double, 类型 `d`）：音量值
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.SetVolume 0.5
```

#### GetVolume

获取音量。

- **输入参数**: 无
- **返回值**: `d`（double）：音量值

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.GetVolume
```

#### SetMute

设置静音。

- **输入参数**: `b`（bool, 类型 `b`）：是否静音
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.SetMute true
```

#### GetMute

获取静音状态。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否静音

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.GetMute
```

