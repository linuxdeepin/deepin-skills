# org.deepin.dde.Uadp1 接口参考

该接口提供 UADP（统一应用数据保护）服务能力，用于应用的加密数据存储与读取。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Uadp1` |
| Object path | `/org/deepin/dde/Uadp1` |
| Interface | `org.deepin.dde.Uadp1` |
| Bus | System |
### UADP 方法

#### Available

检查 UADP 服务是否可用。

- **功能**：检查 UADP 服务是否可用。
- **触发条件**：当需要确认 UADP 加密服务是否正常运行时调用。
- **使用场景**：应用启动时检查加密服务可用性。

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

- **功能**：列出当前调用者的所有加密数据名称。
- **触发条件**：当需要查询已存储的加密数据列表时调用。
- **使用场景**：加密数据管理、查看已存储数据列表。

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

- **功能**：存储加密数据，将指定名称的数据加密后保存。
- **触发条件**：当应用需要安全存储敏感数据时调用。
- **使用场景**：应用加密存储密码、Token、证书密钥、API 密钥。

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

- **功能**：获取并解密指定名称的加密数据。
- **触发条件**：当应用需要读取已存储的加密数据时调用。
- **使用场景**：应用读取已加密存储的密码、Token、证书密钥、API 密钥。

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

- **功能**：删除指定名称的加密数据。
- **触发条件**：当应用需要删除已存储的加密数据时调用。
- **使用场景**：应用清理过期的加密数据、用户注销时清除数据。

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

- **功能**：释放当前调用者持有的所有加密数据资源。
- **触发条件**：当应用退出或不再需要访问加密数据时调用。
- **使用场景**：应用退出时清理加密数据资源。

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
