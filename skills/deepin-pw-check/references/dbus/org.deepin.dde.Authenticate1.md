# org.deepin.dde.Authenticate1 接口参考

该接口提供用户认证、密码限制策略查询与重置、一键登录能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Authenticate1` |
| Object path | `/org/deepin/dde/Authenticate1` |
| Interface | `org.deepin.dde.Authenticate1` |
| Bus | System |


### 用户认证

#### Authenticate

发起用户认证请求，返回认证会话路径。

- **输入参数**: `username`（string, 类型 `s`）：用户名；`authFlags`（int32, 类型 `i`）：认证标志位；`appType`（int32, 类型 `i`）：应用类型
- **返回值**: `result`（string, 类型 `s`）：认证会话路径

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1 \
  --method org.deepin.dde.Authenticate1.Authenticate "user1" 1 0
```


### 密码限制策略

#### GetLimits

获取指定用户的密码限制策略。返回 JSON 字符串，包含限制类型、解锁时间、最大尝试次数、动态限制及动态解锁时间。

- **输入参数**: `username`（string, 类型 `s`）：用户名
- **返回值**: `limitsInfo`（string, 类型 `s`）：限制策略 JSON 字符串

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1 \
  --method org.deepin.dde.Authenticate1.GetLimits "user1"
```

#### ResetLimits

重置指定用户的密码限制策略。

- **输入参数**: `username`（string, 类型 `s`）：用户名
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1 \
  --method org.deepin.dde.Authenticate1.ResetLimits "user1"
```


### 一键登录

#### PreOneKeyLogin

预一键登录，根据标志位返回可一键登录的用户名。

- **输入参数**: `flag`（int32, 类型 `i`）：标志位
- **返回值**: `username`（string, 类型 `s`）：可一键登录的用户名

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1 \
  --method org.deepin.dde.Authenticate1.PreOneKeyLogin 1
```


### 认证属性

#### SupportEncrypts（属性）

支持的加密方式（JSON 字符串）。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Authenticate1 SupportEncrypts
```

#### FrameworkState（属性）

认证框架状态。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Authenticate1 FrameworkState
```

#### SupportedFlags（属性）

支持的认证标志位。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Authenticate1 SupportedFlags
```


### 认证状态信号

#### LimitUpdated

用户密码限制策略更新时发出。

- **参数**: `username`（string, 类型 `s`）：用户名
- **触发条件**: 密码限制策略发生变化时发出

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1
```

#### DeviceChange

设备状态变化时发出。

- **参数**: `deviceFlag`（int32, 类型 `i`）：设备标志位；`action`（int32, 类型 `i`）：动作
- **触发条件**: 认证设备状态变化时发出

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1
```

---
