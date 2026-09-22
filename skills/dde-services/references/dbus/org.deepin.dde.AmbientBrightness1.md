# org.deepin.dde.AmbientBrightness1 接口参考

该接口提供环境亮度感知能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.AmbientBrightness1` |
| Object path | `/org/deepin/dde/AmbientBrightness1` |
| Interface | `org.deepin.dde.AmbientBrightness1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 环境亮度操作

#### Enable

启用或禁用环境亮度感知。

- **输入参数**: `active`（bool, 类型 `b`）：是否启用
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1 \
  --method org.deepin.dde.AmbientBrightness1.Enable true
```


### 环境亮度属性

#### Supported（属性）

是否支持环境亮度感知。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.AmbientBrightness1 Supported
```
#### State（属性）

环境亮度状态。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.AmbientBrightness1 State
```
#### Enabled（属性）

环境亮度感知是否启用。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.AmbientBrightness1 Enabled
```
#### RecommendedBrightness（属性）

推荐亮度值。

| 属性 | 值 |
|------|------|
| 类型 | `d` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.AmbientBrightness1 RecommendedBrightness
```

### 环境亮度信号

#### supportedChanged

支持状态变化时发出。

- **参数**: `b`（bool, 类型 `b`）：是否支持
- **触发条件**: 支持状态变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1
```

#### stateChanged

状态变化时发出。

- **参数**: `s`（string, 类型 `s`）：新状态
- **触发条件**: 环境亮度状态变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1
```

#### enabledChanged

启用状态变化时发出。

- **参数**: `b`（bool, 类型 `b`）：是否启用
- **触发条件**: 启用状态变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1
```

#### recommendedBrightnessChanged

推荐亮度变化时发出。

- **参数**: `d`（double, 类型 `d`）：新推荐亮度
- **触发条件**: 推荐亮度变化时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1
```

---
