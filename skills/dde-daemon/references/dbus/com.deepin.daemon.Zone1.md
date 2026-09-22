# com.deepin.daemon.Zone1 接口参考

该接口提供系统区域设置管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `com.deepin.daemon.Zone` |
| Object path | `/com/deepin/daemon/Zone` |
| Interface | `com.deepin.daemon.Zone1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 区域管理方法

#### SetTimeZone

设置时区。

- **输入参数**: `timezone`（string, 类型 `s`）：时区名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.Zone \
  --object-path /com/deepin/daemon/Zone \
  --method com.deepin.daemon.Zone1.SetTimeZone "Asia/Shanghai"
```

