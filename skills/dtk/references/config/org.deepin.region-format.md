# org.deepin.region-format 配置参考

DTK 区域格式配置，控制以下系统的区域格式：语言、日期、时间、数字、货币、纸张。该资源为公共资源（appId 为空），可被所有 DTK 应用共享使用。部分配置项标记为 `user-public`，表示用户级公共配置。

| 字段 | 值 |
|------|------|
| App ID | （公共资源，appId 为空） |
| Resource ID | `org.deepin.region-format` |

## 配置项

### country

配置系统区域设置中的国家或地区。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dde-dconfig get -a org.deepin.region-format -k country
```

```bash
dde-dconfig set -a org.deepin.region-format -k country -v "CN"
```

### currencyFormat

配置区域格式中的货币符号显示方式。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |

```bash
dde-dconfig get -a org.deepin.region-format -k currencyFormat
```

```bash
dde-dconfig set -a org.deepin.region-format -k currencyFormat -v "¥"
```

### firstDayOfWeek

配置区域格式中每周的第一天是星期几。

| 字段 | 值 |
|------|------|
| 类型 | number |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dde-dconfig get -a org.deepin.region-format -k firstDayOfWeek
```

```bash
dde-dconfig set -a org.deepin.region-format -k firstDayOfWeek -v 1
```

### languageRegion

配置系统的语言和区域设置。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dde-dconfig get -a org.deepin.region-format -k languageRegion
```

```bash
dde-dconfig set -a org.deepin.region-format -k languageRegion -v "zh_CN"
```

### localeName

配置系统的 locale 名称，格式为 language[_script][_country][.codeset][@modifier]。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dde-dconfig get -a org.deepin.region-format -k localeName
```

```bash
dde-dconfig set -a org.deepin.region-format -k localeName -v "zh_CN.UTF-8"
```

### longDateFormat

配置区域格式中的长日期显示格式。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dde-dconfig get -a org.deepin.region-format -k longDateFormat
```

```bash
dde-dconfig set -a org.deepin.region-format -k longDateFormat -v "yyyy年M月d日"
```

### longTimeFormat

配置区域格式中的长时间显示格式。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dde-dconfig get -a org.deepin.region-format -k longTimeFormat
```

```bash
dde-dconfig set -a org.deepin.region-format -k longTimeFormat -v "HH:mm:ss"
```

### numberFormat

配置区域格式中的数字显示格式。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |

```bash
dde-dconfig get -a org.deepin.region-format -k numberFormat
```

```bash
dde-dconfig set -a org.deepin.region-format -k numberFormat -v "#,##0.00"
```

### paperFormat

配置区域格式中的纸张大小规格。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |

```bash
dde-dconfig get -a org.deepin.region-format -k paperFormat
```

```bash
dde-dconfig set -a org.deepin.region-format -k paperFormat -v "A4"
```

### shortDateFormat

配置区域格式中的短日期显示格式。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dde-dconfig get -a org.deepin.region-format -k shortDateFormat
```

```bash
dde-dconfig set -a org.deepin.region-format -k shortDateFormat -v "yyyy/M/d"
```

### shortTimeFormat

配置区域格式中的短时间显示格式。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dde-dconfig get -a org.deepin.region-format -k shortTimeFormat
```

```bash
dde-dconfig set -a org.deepin.region-format -k shortTimeFormat -v "HH:mm"
```
