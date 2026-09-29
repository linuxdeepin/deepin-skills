# org.deepin.dde.AmbientBrightness1 接口参考

该接口提供环境亮度感知能力，用于根据环境光传感器数据自动调节屏幕亮度。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.AmbientBrightness1` |
| Object path | `/org/deepin/dde/AmbientBrightness1` |
| Interface | `org.deepin.dde.AmbientBrightness1` |
| Bus | Session |

### 环境亮度操作

#### Enable

启用或禁用环境亮度感知功能。

- **功能**：开启或关闭环境亮度自动调节，启用后系统会根据环境光传感器数据自动调整屏幕亮度
- **触发条件**：用户在控制中心开启或关闭环境亮度自动调节时调用
- **输入参数**：`active`（bool, 类型 `b`）：是否启用
- **返回值**：无
- **使用场景**：用户在控制中心开启或关闭「自动亮度」时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1 \
  --method org.deepin.dde.AmbientBrightness1.Enable true
```

### 环境亮度属性

#### Supported（属性）

是否支持环境亮度感知。

- **功能**：指示当前设备是否具备环境光传感器硬件支持
- **触发条件**：硬件探测完成时确定，设备未变更时保持不变

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

- **功能**：返回当前环境亮度状态字符串，用于描述环境光的明暗程度
- **触发条件**：环境光传感器数据变化时更新

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

- **功能**：指示环境亮度自动调节功能当前是否处于启用状态
- **触发条件**：调用 `Enable` 方法后更新

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

- **功能**：根据当前环境光传感器数据计算出的推荐屏幕亮度值
- **触发条件**：环境光传感器数据变化时更新

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

- **功能**：通知环境亮度感知的支持状态发生变化
- **参数**：`b`（bool, 类型 `b`）：是否支持
- **触发条件**：设备硬件支持状态发生变化时发出
- **使用场景**：UI 需要根据设备是否支持自动亮度来显示或隐藏相关设置项

```bash
gdbus monitor --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1
```

#### stateChanged

状态变化时发出。

- **功能**：通知环境亮度状态发生变化
- **参数**：`s`（string, 类型 `s`）：新状态
- **触发条件**：环境光传感器数据变化导致状态变化时发出
- **使用场景**：UI 显示当前环境亮度状态

```bash
gdbus monitor --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1
```

#### enabledChanged

启用状态变化时发出。

- **功能**：通知环境亮度感知的启用状态发生变化
- **参数**：`b`（bool, 类型 `b`）：是否启用
- **触发条件**：调用 `Enable` 方法改变启用状态时发出
- **使用场景**：UI 同步显示自动亮度开关状态

```bash
gdbus monitor --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1
```

#### recommendedBrightnessChanged

推荐亮度变化时发出。

- **功能**：通知推荐亮度值发生变化
- **参数**：`d`（double, 类型 `d`）：新推荐亮度
- **触发条件**：环境光传感器数据变化导致推荐亮度更新时发出
- **使用场景**：自动亮度调节模块根据推荐值调整屏幕亮度

```bash
gdbus monitor --session \
  --dest org.deepin.dde.AmbientBrightness1 \
  --object-path /org/deepin/dde/AmbientBrightness1
```

---
