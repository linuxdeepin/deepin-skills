# org.deepin.dde.XSettings1 接口参考

该接口提供 X 设置的读写能力，包括颜色、整数、字符串、缩放因子。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.XSettings1` |
| Object path | `/org/deepin/dde/XSettings1` |
| Interface | `org.deepin.dde.XSettings1` |
| Bus | Session |

### 属性读取

#### GetColor

获取颜色属性。

- **功能**：根据属性名返回对应的颜色值数组
- **触发条件**：需要读取 X 设置中颜色类属性时调用
- **输入参数**：`prop`（string, 类型 `s`）：属性名
- **返回值**：ArrayOfColor：颜色数组
- **使用场景**：需要读取 X 设置中颜色类属性（如主题颜色）时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.GetColor "gtk-theme-color"
```

#### GetInteger

获取整数属性。

- **功能**：根据属性名返回对应的整数值
- **触发条件**：需要读取 X 设置中整数类属性时调用
- **输入参数**：`prop`（string, 类型 `s`）：属性名
- **返回值**：`i`（int32）：属性值
- **使用场景**：需要读取 X 设置中整数类属性（如双击时间间隔）时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.GetInteger "gtk-double-click-time"
```

#### GetScaleFactor

获取缩放因子。

- **功能**：返回当前全局缩放因子
- **触发条件**：界面组件需要获取当前全局缩放因子时调用
- **输入参数**：无
- **返回值**：`d`（double）：缩放因子
- **使用场景**：界面组件需要获取当前缩放比例以正确渲染时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.GetScaleFactor
```

#### GetScreenScaleFactors

获取屏幕缩放因子。

- **功能**：返回各屏幕的缩放因子配置
- **触发条件**：多显示器环境下需要获取各屏幕缩放因子时调用
- **输入参数**：无
- **返回值**：ScaleFactors：缩放因子
- **使用场景**：多显示器环境下需要获取各屏幕独立缩放比例时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.GetScreenScaleFactors
```

#### GetString

获取字符串属性。

- **功能**：根据属性名返回对应的字符串值
- **触发条件**：需要读取 X 设置中字符串类属性时调用
- **输入参数**：`prop`（string, 类型 `s`）：属性名
- **返回值**：`s`（string）：属性值
- **使用场景**：需要读取 X 设置中字符串类属性（如主题名称）时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.GetString "gtk-theme-name"
```

#### ListProps

列出所有属性。

- **功能**：返回所有 X 设置属性的列表，以 JSON 字符串形式返回
- **触发条件**：需要查看当前所有 X 设置属性的完整列表时调用
- **输入参数**：无
- **返回值**：`s`（string）：属性列表 JSON
- **使用场景**：需要查看当前所有 X 设置属性的完整列表时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.ListProps
```

### 属性设置

#### SetColor

设置颜色属性。

- **功能**：设置指定属性名的颜色值
- **触发条件**：需要修改 X 设置中颜色类属性时调用
- **输入参数**：`prop`（string, 类型 `s`）：属性名；`v`（ArrayOfColor, 类型）：颜色值
- **返回值**：无
- **使用场景**：需要修改 X 设置中颜色类属性时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.SetColor "gtk-theme-color" <color_value>
```

#### SetInteger

设置整数属性。

- **功能**：设置指定属性名的整数值
- **触发条件**：需要修改 X 设置中整数类属性时调用
- **输入参数**：`prop`（string, 类型 `s`）：属性名；`v`（int32, 类型 `i`）：属性值
- **返回值**：无
- **使用场景**：需要修改 X 设置中整数类属性时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.SetInteger "gtk-double-click-time" 400
```

#### SetScaleFactor

设置缩放因子。

- **功能**：设置全局缩放因子，修改后触发 SetScaleFactorStarted 和 SetScaleFactorDone 信号
- **触发条件**：用户在控制中心修改全局缩放比例时调用
- **输入参数**：`scale`（double, 类型 `d`）：缩放因子
- **返回值**：无
- **使用场景**：用户在控制中心修改全局缩放比例时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.SetScaleFactor 1.25
```

#### SetScreenScaleFactors

设置屏幕缩放因子。

- **功能**：设置各屏幕的缩放因子配置
- **触发条件**：多显示器环境下需要为各屏幕设置独立缩放比例时调用
- **输入参数**：`factors`（ScaleFactors, 类型）：缩放因子
- **返回值**：无
- **使用场景**：多显示器环境下需要为各屏幕设置独立缩放比例时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.SetScreenScaleFactors <factors_value>
```

#### SetString

设置字符串属性。

- **功能**：设置指定属性名的字符串值
- **触发条件**：需要修改 X 设置中字符串类属性时调用
- **输入参数**：`prop`（string, 类型 `s`）：属性名；`v`（string, 类型 `s`）：属性值
- **返回值**：无
- **使用场景**：需要修改 X 设置中字符串类属性（如主题名称）时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.SetString "gtk-theme-name" "deepin"
```

### 缩放信号

#### SetScaleFactorDone

缩放因子设置完成时发出。

- **功能**：通知订阅者全局缩放因子设置操作已完成
- **参数**：无
- **触发条件**：SetScaleFactor 方法执行完成时发出
- **使用场景**：界面组件需要在缩放因子变更完成后重新布局时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1
```

#### SetScaleFactorStarted

缩放因子设置开始时发出。

- **功能**：通知订阅者全局缩放因子设置操作已开始
- **参数**：无
- **触发条件**：SetScaleFactor 方法开始执行时发出
- **使用场景**：界面组件需要在缩放变更过程中显示过渡动画或禁用交互时监听

```bash
gdbus monitor --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1
```

---
