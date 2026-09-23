# org.freedesktop.impl.portal.Secret 接口参考

该接口提供密钥检索能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Secret` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 密钥方法

#### RetrieveSecret

检索密钥。

- **输入参数**: `parent_handle`（object, 类型 `o`）：父窗口句柄；`namespace`（string, 类型 `s`）：命名空间；`path`（string, 类型 `s`）：密钥路径
- **返回值**: `o`（object path）：请求路径

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Secret.RetrieveSecret "" "ns" "path"
```

