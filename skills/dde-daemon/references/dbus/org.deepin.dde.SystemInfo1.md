# org.deepin.dde.SystemInfo1 接口参考

该接口提供系统硬件和软件信息查询能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.SystemInfo` |
| Object path | `/com/deepin/daemon/SystemInfo` |
| Interface | `org.deepin.dde.SystemInfo1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 系统信息方法

#### GetSystemVersion

获取系统版本。

- **输入参数**: 无
- **返回值**: `s`（string）：版本号

```bash
gdbus call --session \
  --dest org.deepin.dde.SystemInfo \
  --object-path /com/deepin/daemon/SystemInfo \
  --method org.deepin.dde.SystemInfo1.GetSystemVersion
```

#### GetProcessorModel

获取处理器型号。

- **输入参数**: 无
- **返回值**: `s`（string）：处理器型号

```bash
gdbus call --session \
  --dest org.deepin.dde.SystemInfo \
  --object-path /com/deepin/daemon/SystemInfo \
  --method org.deepin.dde.SystemInfo1.GetProcessorModel
```

#### GetMemoryCapacity

获取内存容量。

- **输入参数**: 无
- **返回值**: `d`（double）：内存容量（GB）

```bash
gdbus call --session \
  --dest org.deepin.dde.SystemInfo \
  --object-path /com/deepin/daemon/SystemInfo \
  --method org.deepin.dde.SystemInfo1.GetMemoryCapacity
```

