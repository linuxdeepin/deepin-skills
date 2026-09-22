# org.deepin.dde.Validator1 接口参考

该接口提供主机名和用户名校验能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Validator1` |
| Object path | `/org/deepin/dde/Validator1` |
| Interface | `org.deepin.dde.Validator1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 校验方法

#### ValidateHostname

校验主机名是否合法。

- **输入参数**: `s`（string, 类型 `s`）：主机名
- **返回值**: `b`（bool）：是否合法

```bash
gdbus call --session \
  --dest org.deepin.dde.Validator1 \
  --object-path /org/deepin/dde/Validator1 \
  --method org.deepin.dde.Validator1.ValidateHostname "myhost"
```

#### ValidateUsername

校验用户名是否合法。

- **输入参数**: `s`（string, 类型 `s`）：用户名
- **返回值**: `b`（bool）：是否合法

```bash
gdbus call --session \
  --dest org.deepin.dde.Validator1 \
  --object-path /org/deepin/dde/Validator1 \
  --method org.deepin.dde.Validator1.ValidateUsername "myuser"
```

