# org.freedesktop.impl.portal.Request 接口参考

该接口提供标准 portal 请求关闭能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `<dynamic>` |
| Interface | `org.freedesktop.impl.portal.Request` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 请求方法

#### Close

关闭请求。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path <dynamic> \
  --method org.freedesktop.impl.portal.Request.Close
```

