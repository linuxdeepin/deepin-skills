# com.deepin.daemon.ClipboardManager1 接口参考

该接口提供剪贴板目标管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `com.deepin.daemon.ClipboardManager` |
| Object path | `/com/deepin/daemon/ClipboardManager` |
| Interface | `com.deepin.daemon.ClipboardManager1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 剪贴板管理方法

#### BecomeClipboardOwner

成为剪贴板拥有者。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.ClipboardManager \
  --object-path /com/deepin/daemon/ClipboardManager \
  --method com.deepin.daemon.ClipboardManager1.BecomeClipboardOwner
```

#### RemoveTarget

移除剪贴板目标。

- **输入参数**: `target`（string, 类型 `s`）：目标名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.ClipboardManager \
  --object-path /com/deepin/daemon/ClipboardManager \
  --method com.deepin.daemon.ClipboardManager1.RemoveTarget "target"
```

