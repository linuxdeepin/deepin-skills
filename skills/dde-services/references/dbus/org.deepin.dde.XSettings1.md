# org.deepin.dde.XSettings1 接口参考

该接口提供 X 设置的读写能力，包括颜色、整数、字符串、缩放因子等。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.XSettings1` |
| Object path | `/org/deepin/dde/XSettings1` |
| Interface | `org.deepin.dde.XSettings1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 属性读取

#### GetColor

获取颜色属性。

- **输入参数**: `prop`（string, 类型 `s`）：属性名
- **返回值**: ArrayOfColor：颜色数组

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.GetColor "gtk-theme-color"
```

#### GetInteger

获取整数属性。

- **输入参数**: `prop`（string, 类型 `s`）：属性名
- **返回值**: `i`（int32）：属性值

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.GetInteger "gtk-double-click-time"
```

#### GetScaleFactor

获取缩放因子。

- **输入参数**: 无
- **返回值**: `d`（double）：缩放因子

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.GetScaleFactor
```

#### GetScreenScaleFactors

获取屏幕缩放因子。

- **输入参数**: 无
- **返回值**: ScaleFactors：缩放因子

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.GetScreenScaleFactors
```

#### GetString

获取字符串属性。

- **输入参数**: `prop`（string, 类型 `s`）：属性名
- **返回值**: `s`（string）：属性值

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.GetString "gtk-theme-name"
```

#### ListProps

列出所有属性。

- **输入参数**: 无
- **返回值**: `s`（string）：属性列表 JSON

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.ListProps
```


### 属性设置

#### SetColor

设置颜色属性。

- **输入参数**: `prop`（string, 类型 `s`）：属性名；`v`（ArrayOfColor, 类型）：颜色值
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.SetColor "gtk-theme-color" <color_value>
```

#### SetInteger

设置整数属性。

- **输入参数**: `prop`（string, 类型 `s`）：属性名；`v`（int32, 类型 `i`）：属性值
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.SetInteger "gtk-double-click-time" 400
```

#### SetScaleFactor

设置缩放因子。

- **输入参数**: `scale`（double, 类型 `d`）：缩放因子
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.SetScaleFactor 1.25
```

#### SetScreenScaleFactors

设置屏幕缩放因子。

- **输入参数**: `factors`（ScaleFactors, 类型）：缩放因子
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.SetScreenScaleFactors <factors_value>
```

#### SetString

设置字符串属性。

- **输入参数**: `prop`（string, 类型 `s`）：属性名；`v`（string, 类型 `s`）：属性值
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.SetString "gtk-theme-name" "deepin"
```


### 缩放信号

#### SetScaleFactorDone

缩放因子设置完成时发出。

- **参数**: 无
- **触发条件**: 缩放因子设置完成时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1
```

#### SetScaleFactorStarted

缩放因子设置开始时发出。

- **参数**: 无
- **触发条件**: 缩放因子设置开始时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1
```

---
