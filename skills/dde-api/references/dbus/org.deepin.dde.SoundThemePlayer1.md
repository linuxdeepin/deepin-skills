# org.deepin.dde.SoundThemePlayer1 接口参考

该接口提供系统声音主题播放控制能力，包括播放指定事件声音、桌面登录音效、关机音效准备、音频状态保存以及声音主题和启用状态的设置。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.SoundThemePlayer1` |
| Object path | `/org/deepin/dde/SoundThemePlayer1` |
| Interface | `org.deepin.dde.SoundThemePlayer1` |
| Bus | System |

## 声音播放方法

### Play

播放指定主题和事件的声音。

- **功能**: 根据声音主题和事件名称播放对应的声音
- **触发条件**: 当需要播放指定主题下的特定事件声音时调用
- **使用场景**: 系统事件提示音播放，如登录、关机、通知音效

- **输入参数**:
  - `theme`（string, 类型 `s`）：声音主题名称
  - `event`（string, 类型 `s`）：事件名称（`desktop-login` 或 `system-shutdown`）
  - `device`（string, 类型 `s`）：音频设备（如 `default` 或 `plughw:CARD=card,DEV=device`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.Play \
  "deepin" "desktop-login" "default"
```

### PlaySoundDesktopLogin

播放桌面登录音效。

- **功能**: 播放桌面登录时的提示音效
- **触发条件**: 在用户登录进入桌面时由 session 管理器触发调用
- **使用场景**: 用户登录桌面时播放欢迎音效

- **输入参数**: 无
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.PlaySoundDesktopLogin
```

### PrepareShutdownSound

为指定用户准备关机音效配置。

- **功能**: 根据用户 UID 准备关机时需要播放的音效配置
- **触发条件**: 在系统关机前由电源管理模块调用，为指定用户准备关机音效配置
- **使用场景**: 关机流程启动前预配置关机音效

- **输入参数**:
  - `uid`（int32, 类型 `i`）：用户 UID
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.PrepareShutdownSound \
  1000
```

### SaveAudioState

保存指定用户的音频播放状态。

- **功能**: 将当前音频播放状态保存到系统，用于关机后恢复音频配置
- **触发条件**: 在关机或会话结束时调用，保存当前音频播放状态以便恢复
- **使用场景**: 关机前保存音频状态，以便下次启动时恢复

- **输入参数**:
  - `activePlayback`（dict<string, variant>, 类型 `a{sv}`）：音频播放状态字典，包含 `card`、`device`、`mute`、`volume` 字段
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.SaveAudioState \
  "{'card': <'PCH'>, 'device': <'PCH'>, 'mute': <false>, 'volume': <1.0>}"
```

### EnableSound

启用或禁用指定事件的声音。

- **功能**: 控制指定事件声音的启用或禁用状态
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 控制中心声音设置中开启或关闭登录音效、关机音效

- **输入参数**:
  - `name`（string, 类型 `s`）：事件名称（空字符串表示整体开关，`desktop-login` 表示登录音效，`system-shutdown` 表示关机音效）
  - `enabled`（bool, 类型 `b`）：是否启用
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.EnableSound \
  "desktop-login" true
```

### EnableSoundDesktopLogin

启用或禁用桌面登录音效。

- **功能**: 专门控制桌面登录音效的启用或禁用，是 `EnableSound` 传入 `desktop-login` 的便捷封装
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 控制中心中单独控制登录音效开关

- **输入参数**:
  - `enabled`（bool, 类型 `b`）：是否启用
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.EnableSoundDesktopLogin \
  true
```

### SetSoundTheme

设置声音主题。

- **功能**: 设置当前系统使用的声音主题名称
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 控制中心个性化设置中切换声音主题

- **输入参数**:
  - `theme`（string, 类型 `s`）：声音主题名称
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --system \
  --dest org.deepin.dde.SoundThemePlayer1 \
  --object-path /org/deepin/dde/SoundThemePlayer1 \
  --method org.deepin.dde.SoundThemePlayer1.SetSoundTheme \
  "deepin"
```
