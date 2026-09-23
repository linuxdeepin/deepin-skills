# org.deepin.dde.SoundThemePlayer1 接口参考

该接口提供系统声音主题播放、登录音效、关机音效准备和音频状态保存能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.SoundThemePlayer1` |
| Object path | `/org/deepin/dde/SoundThemePlayer1` |
| Interface | `org.deepin.dde.SoundThemePlayer1` |
| Bus | System |


### 声音播放方法

#### Play

播放指定主题和事件的声音。

- **输入参数**: `theme`（string, 类型 `s`）：声音主题名称；`event`（string, 类型 `s`）：声音事件名称；`device`（string, 类型 `s`）：音频设备名称
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.Play "deepin" "message" "default"
```

#### PlaySoundDesktopLogin

播放桌面登录音效。根据当前用户配置决定是否播放。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.PlaySoundDesktopLogin
```


### 关机音效

#### PrepareShutdownSound

准备关机音效配置，供 greeter 界面调用。

- **输入参数**: `uid`（int32, 类型 `i`）：用户 UID
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.PrepareShutdownSound 1000
```


### 音频状态管理

#### SaveAudioState

保存指定用户的音频状态，并准备关机音效。

- **输入参数**: `activePlayback`（dict, 类型 `a{sv}`）：活跃播放设备信息，包含 `card`（string）、`device`（string）、`mute`（bool）字段
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.SaveAudioState \
  "{'card': <'PCH'>, 'device': <'0'>, 'mute': <false>}"
```


### 声音配置

#### EnableSoundDesktopLogin

启用或禁用桌面登录音效。

- **输入参数**: `enabled`（bool, 类型 `b`）：是否启用
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.EnableSoundDesktopLogin true
```

#### EnableSound

启用或禁用指定声音事件。

- **输入参数**: `name`（string, 类型 `s`）：声音事件名称（空字符串表示全部，`desktop-login` 表示登录音，`system-shutdown` 表示关机音）；`enabled`（bool, 类型 `b`）：是否启用
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.EnableSound "desktop-login" true
```

#### SetSoundTheme

设置声音主题。

- **输入参数**: `theme`（string, 类型 `s`）：声音主题名称
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.SetSoundTheme "deepin"
```

---
