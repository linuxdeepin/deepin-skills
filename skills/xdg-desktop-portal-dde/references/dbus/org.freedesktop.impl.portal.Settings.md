# org.freedesktop.impl.portal.Settings 接口参考

该接口提供桌面环境设置读写能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Settings` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 设置方法

#### ReadAll

读取所有指定命名空间的设置。

- **输入参数**: `names`（string 数组, 类型 `as`）：命名空间列表
- **返回值**: `a{sa{sv}}`（嵌套字典）：设置键值

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Settings.ReadAll [""]
```

#### Read

读取指定命名空间和键的设置。

- **输入参数**: `namespace`（string, 类型 `s`）：命名空间；`key`（string, 类型 `s`）：键名
- **返回值**: `v`（variant）：设置值

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Settings.Read "ns" "key"
```

#### Set

设置指定命名空间和键的值。

- **输入参数**: `namespace`（string, 类型 `s`）：命名空间；`key`（string, 类型 `s`）：键名；`value`（variant, 类型 `v`）：值
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Settings.Set "ns" "key" <value>
```

