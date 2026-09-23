# org.deepin.dde.LangSelector1 接口参考

该接口提供系统语言选择和切换能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.LangSelector` |
| Object path | `/com/deepin/daemon/LangSelector` |
| Interface | `org.deepin.dde.LangSelector1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 语言选择方法

#### GetLocaleList

获取支持的区域列表。

- **输入参数**: 无
- **返回值**: `as`（string 数组）：区域列表

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector \
  --object-path /com/deepin/daemon/LangSelector \
  --method org.deepin.dde.LangSelector1.GetLocaleList
```

#### GetCurrentLocale

获取当前区域设置。

- **输入参数**: 无
- **返回值**: `s`（string）：当前区域

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector \
  --object-path /com/deepin/daemon/LangSelector \
  --method org.deepin.dde.LangSelector1.GetCurrentLocale
```

#### SetLocale

设置当前区域。

- **输入参数**: `locale`（string, 类型 `s`）：区域名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector \
  --object-path /com/deepin/daemon/LangSelector \
  --method org.deepin.dde.LangSelector1.SetLocale "zh_CN.UTF-8"
```

