# org.deepin.dde.XSettings1 接口参考

该接口提供 X 设置的读写能力，包括颜色、整数、字符串、缩放因子。

本接口的属性集合不同于 `xset` 的 X server 参数、`xrdb` 资源和 `xprop` 窗口属性。读取或写入前通过 introspect 确认方法，并用 `ListProps` 确认键名和大小写；不存在的键即使返回 0，也不能据此判断实际配置值。

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
- **返回值**：`aq`：uint16 颜色数组
- **使用场景**：需要读取 X 设置中颜色类属性（如主题颜色）时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.GetColor "gtk-theme-color"
```

#### GetInteger

双击间隔读取 `Net/DoubleClickTime`，单位毫秒；`gtk-double-click-time` 不是对应的 XSettings 键名。

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
  --method org.deepin.dde.XSettings1.GetInteger "Net/DoubleClickTime"
```

#### GetScaleFactor

全局缩放以本方法返回值为准，不通过 Xft.dpi 推算；每屏缩放使用 `GetScreenScaleFactors`。

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
- **返回值**：`a{sd}`：屏幕名到 double 缩放因子的字典
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
  --method org.deepin.dde.XSettings1.GetString "Net/ThemeName"
```

#### ListProps

列出所有属性。

返回的 D-Bus 字符串内容是 JSON：属性名字符串数组按元素计数；若部署返回以属性名为键的对象，取对象键并计数。使用工具的 JSON 输出时，先解码外层 D-Bus 返回，再解析字符串中的 JSON。未知结构先检查原始响应，不猜测数量，也不按输出行数计数。数量随服务配置变化；汇总时分别注明本方法与 `GetScaleFactor` 的结果来源。

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
- **输入参数**：`prop`（string, 类型 `s`）：属性名；`v`（uint16 数组, 类型 `aq`）：颜色值
- **返回值**：无
- **使用场景**：需要修改 X 设置中颜色类属性时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.SetColor "gtk-theme-color" <color_value>
```

#### SetInteger

双击间隔使用 `Net/DoubleClickTime`，单位毫秒。业务取值范围以部署版本的配置元数据为准；记录原值后仅写目标键，并用同键回读验证。

设置整数属性。

此方法无返回值；`busctl --json=short call` 成功时 stdout 可以为空，不能对空输出执行 `json.loads`。先检查退出码，再调用 `GetInteger` 回读同一键；只有回读目标值才能报告生效。

- **功能**：设置指定属性名的整数值
- **触发条件**：需要修改 X 设置中整数类属性时调用
- **输入参数**：`prop`（string, 类型 `s`）：属性名；`v`（int32, 类型 `i`）：属性值
- **返回值**：无
- **使用场景**：需要修改 X 设置中整数类属性时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.XSettings1 \
  --object-path /org/deepin/dde/XSettings1 \
  --method org.deepin.dde.XSettings1.SetInteger "Net/DoubleClickTime" 400
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
- **输入参数**：`factors`（屏幕名到 double 的字典, 类型 `a{sd}`）：缩放因子
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
  --method org.deepin.dde.XSettings1.SetString "Net/ThemeName" "deepin"
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
