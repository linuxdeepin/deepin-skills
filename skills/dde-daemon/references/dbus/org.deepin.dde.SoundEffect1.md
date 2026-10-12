# org.deepin.dde.SoundEffect1 接口参考

该接口提供系统声音效果管理能力，包括播放声音、启用/禁用声音效果、获取声音文件路径、获取所有声音效果启用状态。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.SoundEffect1` |
| Object path | `/org/deepin/dde/SoundEffect1` |
| Interface | `org.deepin.dde.SoundEffect1` |
| Bus | Session |

### 声音效果方法

#### PlaySound

播放指定声音效果。

- **功能**：播放指定名称的声音效果。
- **触发条件**：当系统事件触发需要播放音效时调用。
- **使用场景**：消息通知音效、操作反馈音效播放。

- **输入参数**: `name`（string, 类型 `s`）：声音名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SoundEffect1 \
  --object-path /org/deepin/dde/SoundEffect1 \
  --method org.deepin.dde.SoundEffect1.PlaySound "message"
```

#### PlaySystemSound

播放指定系统声音效果。

- **功能**：播放指定名称的系统声音效果。
- **触发条件**：当系统级事件（如登录、关机）触发需要播放音效时调用。
- **使用场景**：系统登录音效、系统关机音效播放。

- **输入参数**: `name`（string, 类型 `s`）：声音名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SoundEffect1 \
  --object-path /org/deepin/dde/SoundEffect1 \
  --method org.deepin.dde.SoundEffect1.PlaySystemSound "message"
```

#### EnableSound

启用或禁用指定声音效果。

- **功能**：启用或禁用指定声音效果。
- **触发条件**：当用户在控制中心开启或关闭特定音效时调用。
- **使用场景**：控制中心音效设置开关。

- **输入参数**:
  - `name`（string, 类型 `s`）：声音名称
  - `enabled`（bool, 类型 `b`）：是否启用
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SoundEffect1 \
  --object-path /org/deepin/dde/SoundEffect1 \
  --method org.deepin.dde.SoundEffect1.EnableSound "message" true
```

#### IsSoundEnabled

检查指定声音效果是否启用。

- **功能**：检查指定声音效果是否已启用。
- **触发条件**：当需要查询特定音效的启用状态时调用。
- **使用场景**：控制中心音效设置显示开关状态。

- **输入参数**: `name`（string, 类型 `s`）：声音名称
- **返回值**: `enabled`（bool, 类型 `b`）：是否启用

```bash
gdbus call --session \
  --dest org.deepin.dde.SoundEffect1 \
  --object-path /org/deepin/dde/SoundEffect1 \
  --method org.deepin.dde.SoundEffect1.IsSoundEnabled "message"
```

#### GetSoundFile

获取指定声音效果的文件路径。

- **功能**：获取指定声音效果的音频文件路径。
- **触发条件**：当需要获取音效文件进行自定义播放时调用。
- **使用场景**：音效文件管理、第三方播放器播放音效。

- **输入参数**: `name`（string, 类型 `s`）：声音名称
- **返回值**: `file`（string, 类型 `s`）：声音文件路径

```bash
gdbus call --session \
  --dest org.deepin.dde.SoundEffect1 \
  --object-path /org/deepin/dde/SoundEffect1 \
  --method org.deepin.dde.SoundEffect1.GetSoundFile "message"
```

#### GetSystemSoundFile

获取指定系统声音效果的文件路径。

- **功能**：获取指定系统声音效果的音频文件路径。
- **触发条件**：当需要获取系统音效文件进行自定义播放时调用。
- **使用场景**：系统音效文件管理、第三方播放器播放系统音效。

- **输入参数**: `name`（string, 类型 `s`）：声音名称
- **返回值**: `file`（string, 类型 `s`）：声音文件路径

```bash
gdbus call --session \
  --dest org.deepin.dde.SoundEffect1 \
  --object-path /org/deepin/dde/SoundEffect1 \
  --method org.deepin.dde.SoundEffect1.GetSystemSoundFile "message"
```

#### GetSoundEnabledMap

获取所有声音效果的启用状态。

- **功能**：获取所有声音效果的启用状态映射表。
- **触发条件**：当需要批量获取音效启用状态时调用。
- **使用场景**：控制中心音效设置列表初始化。

- **输入参数**: 无
- **返回值**: `result`（`a{sb}`，map[string]bool）：声音名称到启用状态的映射

```bash
gdbus call --session \
  --dest org.deepin.dde.SoundEffect1 \
  --object-path /org/deepin/dde/SoundEffect1 \
  --method org.deepin.dde.SoundEffect1.GetSoundEnabledMap
```
