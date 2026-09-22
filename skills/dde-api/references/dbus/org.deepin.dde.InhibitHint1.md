# org.deepin.dde.InhibitHint1 接口参考

该接口提供抑制提示查询能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.InhibitHint1` |
| Object path | `/org/deepin/dde/InhibitHint1` |
| Interface | `org.deepin.dde.InhibitHint1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### Inhibit 提示方法

#### Get

获取抑制提示信息。

- **输入参数**: 无
- **返回值**: `a{sv}`（字典）：抑制提示信息

```bash
gdbus call --session \
  --dest org.deepin.dde.InhibitHint1 \
  --object-path /org/deepin/dde/InhibitHint1 \
  --method org.deepin.dde.InhibitHint1.Get
```

