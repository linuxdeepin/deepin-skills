# org.deepin.region-format 配置参考

DTK 区域格式配置，控制系统的语言、日期、时间、数字、货币等区域格式。该资源为公共资源（appId 为空），可被所有 DTK 应用共享使用。部分配置项标记为 `user-public`，表示用户级公共配置。

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
dconfig read -d "" -r org.deepin.region-format country
```

```bash
dconfig write -d "" -r org.deepin.region-format country "CN"
```

### currencyFormat

配置区域格式中的货币符号显示方式。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.region-format currencyFormat
```

```bash
dconfig write -d "" -r org.deepin.region-format currencyFormat "¥"
```

### firstDayOfWeek

配置区域格式中每周的第一天是星期几。

| 字段 | 值 |
|------|------|
| 类型 | number |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dconfig read -d "" -r org.deepin.region-format firstDayOfWeek
```

```bash
dconfig write -d "" -r org.deepin.region-format firstDayOfWeek 1
```

### languageRegion

配置系统的语言和区域设置。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dconfig read -d "" -r org.deepin.region-format languageRegion
```

```bash
dconfig write -d "" -r org.deepin.region-format languageRegion "zh_CN"
```

### localeName

配置系统的 locale 名称，格式为 language[_script][_country][.codeset][@modifier]。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dconfig read -d "" -r org.deepin.region-format localeName
```

```bash
dconfig write -d "" -r org.deepin.region-format localeName "zh_CN.UTF-8"
```

### longDateFormat

配置区域格式中的长日期显示格式。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dconfig read -d "" -r org.deepin.region-format longDateFormat
```

```bash
dconfig write -d "" -r org.deepin.region-format longDateFormat "yyyy年M月d日"
```

### longTimeFormat

配置区域格式中的长时间显示格式。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dconfig read -d "" -r org.deepin.region-format longTimeFormat
```

```bash
dconfig write -d "" -r org.deepin.region-format longTimeFormat "HH:mm:ss"
```

### numberFormat

配置区域格式中的数字显示格式。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.region-format numberFormat
```

```bash
dconfig write -d "" -r org.deepin.region-format numberFormat "#,##0.00"
```

### paperFormat

配置区域格式中的纸张大小规格。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |

```bash
dconfig read -d "" -r org.deepin.region-format paperFormat
```

```bash
dconfig write -d "" -r org.deepin.region-format paperFormat "A4"
```

### shortDateFormat

配置区域格式中的短日期显示格式。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dconfig read -d "" -r org.deepin.region-format shortDateFormat
```

```bash
dconfig write -d "" -r org.deepin.region-format shortDateFormat "yyyy/M/d"
```

### shortTimeFormat

配置区域格式中的短时间显示格式。

| 字段 | 值 |
|------|------|
| 类型 | string |
| 读写权限 | readwrite |
| Flags | `user-public` |

```bash
dconfig read -d "" -r org.deepin.region-format shortTimeFormat
```

```bash
dconfig write -d "" -r org.deepin.region-format shortTimeFormat "HH:mm"
```
