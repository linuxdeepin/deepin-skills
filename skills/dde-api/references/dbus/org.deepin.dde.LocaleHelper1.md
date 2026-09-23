# org.deepin.dde.LocaleHelper1 接口参考

该接口提供系统区域设置生成和切换能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.LocaleHelper1` |
| Object path | `/org/deepin/dde/LocaleHelper1` |
| Interface | `org.deepin.dde.LocaleHelper1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 区域设置方法

#### GenerateLocale

生成区域设置。

- **输入参数**: `s`（string, 类型 `s`）：区域名称
- **返回值**: `s`（string）：生成的区域设置

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.LocaleHelper1 \
  --object-path /org/deepin/dde/LocaleHelper1 \
  --method org.deepin.dde.LocaleHelper1.GenerateLocale "zh_CN.UTF-8"
```

#### SetLocale

设置系统区域。

- **输入参数**: `s`（string, 类型 `s`）：区域名称
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.LocaleHelper1 \
  --object-path /org/deepin/dde/LocaleHelper1 \
  --method org.deepin.dde.LocaleHelper1.SetLocale "zh_CN.UTF-8"
```

#### SetAllowCaller

设置允许的调用者。

- **输入参数**: `s`（string, 类型 `s`）：调用者
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.LocaleHelper1 \
  --object-path /org/deepin/dde/LocaleHelper1 \
  --method org.deepin.dde.LocaleHelper1.SetAllowCaller "myapp"
```

