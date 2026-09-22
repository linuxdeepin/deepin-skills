# com.deepin.daemon.BacklightHelper1 接口参考

该接口提供背光亮度和 DDCCI 管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `com.deepin.daemon.BacklightHelper` |
| Object path | `/com/deepin/daemon/BacklightHelper` |
| Interface | `com.deepin.daemon.BacklightHelper1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 背光辅助方法

#### CheckCfgSupport

检查配置是否支持。

- **输入参数**: `name`（string, 类型 `s`）：配置名称
- **返回值**: `b`（bool）：是否支持

```bash
pkexec gdbus call --system \
  --dest com.deepin.daemon.BacklightHelper \
  --object-path /com/deepin/daemon/BacklightHelper \
  --method com.deepin.daemon.BacklightHelper1.CheckCfgSupport "name"
```

#### SetBrightness

设置背光亮度。

- **输入参数**: `brightness`（int32, 类型 `i`）：亮度值
- **返回值**: 无

```bash
pkexec gdbus call --system \
  --dest com.deepin.daemon.BacklightHelper \
  --object-path /com/deepin/daemon/BacklightHelper \
  --method com.deepin.daemon.BacklightHelper1.SetBrightness 50
```

