# org.desktopspec.ConfigManager.Internal 接口参考

该接口提供配置项列表查询和变更通知能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ConfigManager` |
| Object path | `/Internal` |
| Interface | `org.desktopspec.ConfigManager.Internal` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

> **注意**：该接口位于 System 总线，调用需要提权。

### 配置项查询

#### configurations

获取所有配置项列表。

- **输入参数**: 无
- **返回值**: `a(sss)`（string 三元组数组）：配置项列表

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /Internal \
  --method org.desktopspec.ConfigManager.Internal.configurations.configurations
```


### 配置项变更信号

#### configurationsChanged

配置项列表变化时发出。

- **参数**: 无
- **触发条件**: 配置项列表变化时发出

```bash
pkexec gdbus monitor --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /Internal
```

---
