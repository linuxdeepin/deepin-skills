# org.freedesktop.Secret.Service 接口参考

该接口提供 Secret Service API 的会话管理、集合创建、密钥搜索、锁定解锁能力。来源于上游 GNOME 项目。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.secrets` |
| Object path | `/org/freedesktop/Secrets` |
| Interface | `org.freedesktop.Secret.Service` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 会话与集合管理

#### OpenSession

打开密钥服务会话。

- **输入参数**: `algorithm`（string, 类型 `s`）：加密算法；`input`（variant, 类型 `v`）：输入参数
- **返回值**: `(vo)`（元组）：输出和会话路径

```bash
gdbus call --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets \
  --method org.freedesktop.Secret.Service.OpenSession "plain" ""
```

#### CreateCollection

创建密钥集合。

- **输入参数**: `properties`（字典, 类型 `a{sv}`）：集合属性；`alias`（string, 类型 `s`）：别名
- **返回值**: `(oo)`（元组）：集合路径和提示路径

```bash
gdbus call --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets \
  --method org.freedesktop.Secret.Service.CreateCollection {} ""
```

#### SearchItems

搜索密钥项。

- **输入参数**: `attributes`（字典, 类型 `a{ss}`）：搜索属性
- **返回值**: `(aoao)`（元组）：已锁定和已解锁项路径

```bash
gdbus call --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets \
  --method org.freedesktop.Secret.Service.SearchItems {"key":"value"}
```

#### Lock

锁定指定项或集合。

- **输入参数**: `objects`（对象路径数组, 类型 `ao`）：要锁定的对象
- **返回值**: `(aoo)`（元组）：已锁定对象和提示路径

```bash
gdbus call --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets \
  --method org.freedesktop.Secret.Service.Lock ["/org/freedesktop/Secrets/collection/login"]
```

#### Unlock

解锁指定项或集合。

- **输入参数**: `objects`（对象路径数组, 类型 `ao`）：要解锁的对象
- **返回值**: `(aoo)`（元组）：已解锁对象和提示路径

```bash
gdbus call --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets \
  --method org.freedesktop.Secret.Service.Unlock ["/org/freedesktop/Secrets/collection/login"]
```

#### LockService

锁定整个密钥服务。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets \
  --method org.freedesktop.Secret.Service.LockService
```

#### ChangeLock

更改集合锁定密码。

- **输入参数**: `collection`（object, 类型 `o`）：集合路径
- **返回值**: `o`（object path）：提示路径

```bash
gdbus call --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets \
  --method org.freedesktop.Secret.Service.ChangeLock "/org/freedesktop/Secrets/collection/login"
```

#### GetSecrets

获取密钥项的密钥值。

- **输入参数**: `items`（对象路径数组, 类型 `ao`）：项路径；`session`（object, 类型 `o`）：会话路径
- **返回值**: `a{o(oayay)}`（字典）：项路径到密钥的映射

```bash
gdbus call --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets \
  --method org.freedesktop.Secret.Service.GetSecrets ["/org/freedesktop/Secrets/item"] "/org/freedesktop/Secrets/session"
```

#### ReadAlias

读取别名对应的集合。

- **输入参数**: `name`（string, 类型 `s`）：别名
- **返回值**: `o`（object path）：集合路径

```bash
gdbus call --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets \
  --method org.freedesktop.Secret.Service.ReadAlias "default"
```

#### SetAlias

设置别名对应的集合。

- **输入参数**: `name`（string, 类型 `s`）：别名；`collection`（object, 类型 `o`）：集合路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets \
  --method org.freedesktop.Secret.Service.SetAlias "default" "/org/freedesktop/Secrets/collection/login"
```


### 密钥库属性

#### Collections（属性）

密钥集合列表。

| 属性 | 值 |
|------|------|
| 类型 | `ao` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets \
  --method org.freedesktop.DBus.Properties.Get \
  org.freedesktop.Secret.Service Collections
```

### 密钥库信号

#### CollectionCreated

集合创建时发出。

- **参数**: `path`（object, 类型 `o`）：集合路径
- **触发条件**: 创建密钥集合时发出

```bash
gdbus monitor --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets
```

#### CollectionDeleted

集合删除时发出。

- **参数**: `path`（object, 类型 `o`）：集合路径
- **触发条件**: 删除密钥集合时发出

```bash
gdbus monitor --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets
```

#### CollectionChanged

集合变更时发出。

- **参数**: `path`（object, 类型 `o`）：集合路径
- **触发条件**: 密钥集合属性变更时发出

```bash
gdbus monitor --session \
  --dest org.freedesktop.secrets \
  --object-path /org/freedesktop/Secrets
```

