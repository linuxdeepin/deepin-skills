# org.deepin.dde.Authenticate1.Face 接口参考

该接口提供人脸录入、验证、删除和重命名能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Authenticate1` |
| Object path | `/org/deepin/dde/Authenticate1/Face` |
| Interface | `org.deepin.dde.Authenticate1.Face` |
| Bus | System |


### 人脸录入

#### StartEnroll

开始人脸录入。

- **输入参数**: `username`（string, 类型 `s`）：用户名；`serviceName`（string, 类型 `s`）：服务名称；`faceName`（string, 类型 `s`）：人脸特征名称
- **返回值**: `id`（string, 类型 `s`）：录入操作 ID

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.StartEnroll "user1" "service1" "face_001"
```

#### StopEnroll

停止人脸录入。

- **输入参数**: `id`（string, 类型 `s`）：录入操作 ID
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.StopEnroll "enroll_id"
```


### 人脸验证

#### StartVerify

开始人脸验证。

- **输入参数**: `username`（string, 类型 `s`）：用户名；`serviceName`（string, 类型 `s`）：服务名称；`timeout`（int32, 类型 `i`）：超时时间（秒）
- **返回值**: `id`（string, 类型 `s`）：验证操作 ID

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.StartVerify "user1" "service1" 30
```

#### StopVerify

停止人脸验证。

- **输入参数**: `id`（string, 类型 `s`）：验证操作 ID
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.StopVerify "verify_id"
```


### 人脸管理

#### ListFaces

列出指定用户的人脸特征列表。

- **输入参数**: `serviceName`（string, 类型 `s`）：服务名称；`username`（string, 类型 `s`）：用户名
- **返回值**: `faces`（string 数组, 类型 `as`）：人脸特征名称列表

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.ListFaces "service1" "user1"
```

#### RenameFace

重命名指定人脸特征。

- **输入参数**: `serviceName`（string, 类型 `s`）：服务名称；`username`（string, 类型 `s`）：用户名；`oldFace`（string, 类型 `s`）：旧名称；`newFace`（string, 类型 `s`）：新名称
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.RenameFace "service1" "user1" "face_001" "face_renamed"
```

#### DeleteFace

删除指定的人脸特征。

- **输入参数**: `serviceName`（string, 类型 `s`）：服务名称；`username`（string, 类型 `s`）：用户名；`faceName`（string, 类型 `s`）：人脸特征名称
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.DeleteFace "service1" "user1" "face_001"
```

#### DeleteFaces

删除指定用户的所有人脸特征。

- **输入参数**: `serviceName`（string, 类型 `s`）：服务名称；`username`（string, 类型 `s`）：用户名
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.DeleteFaces "service1" "user1"
```


### 共享内存信息

#### GetShareMemInfo

获取人脸识别的共享内存信息。

- **输入参数**: `id`（string, 类型 `s`）：操作 ID
- **返回值**: `sockPath`（string, 类型 `s`）：共享内存套接字路径；`key`（string, 类型 `s`）：共享内存键；`size`（int32, 类型 `i`）：共享内存大小

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.GetShareMemInfo "enroll_id"
```


### 设备与服务配置

#### SetDefaultDevice

设置默认人脸识别设备。

- **输入参数**: `serviceName`（string, 类型 `s`）：服务名称；`device`（string, 类型 `s`）：设备名称
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.SetDefaultDevice "service1" "/dev/video0"
```

#### SetDefaultService

设置默认人脸识别服务。

- **输入参数**: `serviceName`（string, 类型 `s`）：服务名称
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.SetDefaultService "service1"
```


### 人脸属性

#### DefaultDevice（属性）

默认人脸识别设备。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Authenticate1.Face DefaultDevice
```

#### DefaultService（属性）

默认人脸识别服务。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Authenticate1.Face DefaultService
```

#### ServiceList（属性）

可用的人脸识别服务列表（JSON 字符串）。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Authenticate1.Face ServiceList
```


### 人脸状态信号

#### EnrollStatus

人脸录入状态变化时发出。

- **参数**: `id`（string, 类型 `s`）：操作 ID；`user`（string, 类型 `s`）：用户名；`code`（int32, 类型 `i`）：状态码；`msg`（string, 类型 `s`）：状态消息
- **触发条件**: 人脸录入过程中状态变化时发出

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face
```

#### VerifyStatus

人脸验证状态变化时发出。

- **参数**: `id`（string, 类型 `s`）：操作 ID；`user`（string, 类型 `s`）：用户名；`code`（int32, 类型 `i`）：状态码；`msg`（string, 类型 `s`）：状态消息
- **触发条件**: 人脸验证过程中状态变化时发出

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face
```

#### DeviceStatus

设备状态变化时发出。

- **参数**: `serviceName`（string, 类型 `s`）：服务名称；`code`（int32, 类型 `i`）：状态码
- **触发条件**: 人脸识别设备状态变化时发出

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face
```

---
