# org.deepin.dde.SoundEffect1 接口参考

该接口提供系统声音效果管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.SoundEffect` |
| Object path | `/com/deepin/daemon/SoundEffect` |
| Interface | `org.deepin.dde.SoundEffect1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 声音效果方法

#### PlaySound

播放指定声音效果。

- **输入参数**: `name`（string, 类型 `s`）：声音名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SoundEffect \
  --object-path /com/deepin/daemon/SoundEffect \
  --method org.deepin.dde.SoundEffect1.PlaySound "message"
```

#### EnableAllSound

启用所有声音效果。

- **输入参数**: `enabled`（bool, 类型 `b`）：是否启用
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.SoundEffect \
  --object-path /com/deepin/daemon/SoundEffect \
  --method org.deepin.dde.SoundEffect1.EnableAllSound true
```

