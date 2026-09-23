# org.deepin.dde.Greeter1 接口参考

该接口提供 Greeter 主题更新能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Greeter` |
| Object path | `/com/deepin/daemon/Greeter` |
| Interface | `org.deepin.dde.Greeter1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### Greeter 方法

#### UpdateGreeterQtTheme

更新 Greeter Qt 主题。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Greeter \
  --object-path /com/deepin/daemon/Greeter \
  --method org.deepin.dde.Greeter1.UpdateGreeterQtTheme
```

