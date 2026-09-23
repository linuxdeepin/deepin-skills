# org.deepin.dde.Uadp1 接口参考

该接口提供 UADP（统一应用数据保护）服务能力，用于应用的加密数据存储与读取。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Uadp1` |
| Object path | `/org/deepin/dde/Uadp1` |
| Interface | `org.deepin.dde.Uadp1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### UADP 方法

#### Available

检查 UADP 服务是否可用。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否可用

```bash
gdbus call --system \
  --dest org.deepin.dde.Uadp1 \
  --object-path /org/deepin/dde/Uadp1 \
  --method org.deepin.dde.Uadp1.Available
```

#### ListName

列出当前调用者的所有数据名称。

- **输入参数**: 无
- **返回值**: `as`（string 数组）：数据名称列表

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Uadp1 \
  --object-path /org/deepin/dde/Uadp1 \
  --method org.deepin.dde.Uadp1.ListName
```

#### Set

设置加密数据。

- **输入参数**: `name`（string, 类型 `s`）：数据名称；`data`（byte 数组, 类型 `ay`）：数据内容
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Uadp1 \
  --object-path /org/deepin/dde/Uadp1 \
  --method org.deepin.dde.Uadp1.Set "mydata" [0x01,0x02,0x03]
```

#### Get

获取解密数据。

- **输入参数**: `name`（string, 类型 `s`）：数据名称
- **返回值**: `ay`（byte 数组）：解密后的数据内容

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Uadp1 \
  --object-path /org/deepin/dde/Uadp1 \
  --method org.deepin.dde.Uadp1.Get "mydata"
```

#### Delete

删除数据。

- **输入参数**: `name`（string, 类型 `s`）：数据名称
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Uadp1 \
  --object-path /org/deepin/dde/Uadp1 \
  --method org.deepin.dde.Uadp1.Delete "mydata"
```

#### Release

释放当前调用者的所有数据。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Uadp1 \
  --object-path /org/deepin/dde/Uadp1 \
  --method org.deepin.dde.Uadp1.Release
```
