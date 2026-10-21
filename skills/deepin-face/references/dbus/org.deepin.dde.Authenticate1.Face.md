# org.deepin.dde.Authenticate1.Face 接口参考

该接口在 System 总线上注册，按用户、服务和模板标识管理人脸录入、验证、列出、重命名和删除；默认设备作用于指定服务，默认服务设置作用于认证服务。录入、重命名与删除操作需要授权。

本接口由 `org.deepin.dde.Authenticate1` 服务提供，调用前需确保对应服务已安装并运行。操作对象由用户及人脸标识参数确定，不是对所有用户统一执行。旧版独立 `deepin-face` 接口的关系见 [Face1 说明](org.deepin.dde.Face1.md)。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Authenticate1` |
| Object path | `/org/deepin/dde/Authenticate1/Face` |
| Interface | `org.deepin.dde.Authenticate1.Face` |
| Bus | System |

## 提供方与权限

本接口由 `deepin-authenticate` 包提供；不能仅安装旧版独立人脸组件就假定新服务可用。在 `deepin-authenticate 1:2.0.32` 的总线策略中，`StartVerify`、`ListFaces`、`SetDefaultDevice` 和 `SetDefaultService` 仅允许 root 调用；录入、重命名和删除则按对应的服务端授权规则处理。只读属性并未因此统一要求 root。部署其他版本时仍需使用其实际总线策略。

录入和验证的 ID 来自 `StartEnroll` / `StartVerify`，不是可复用的固定字符串。后续停止、读取图像信息和状态监听应由发起操作的客户端管理；一次性命令片段不能替代完整的认证客户端生命周期。

### 人脸录入

#### StartEnroll

开始人脸录入流程，为指定用户和服务创建一个人脸录入会话。

- **功能**: 启动人脸录入，返回一个操作 ID（id），该 id 用于后续 StopEnroll、GetShareMemInfo 操作，并与 EnrollStatus 信号关联
- **触发条件**: 调用方主动调用此方法时触发
- **使用场景**: 用户在系统设置中添加新人脸数据时，应用调用此方法启动录入流程；录入过程需要 polkit 提权

权限：
- requires_sudo: true

- **输入参数**: `username`（string, 类型 `s`）：用户名；`serviceName`（string, 类型 `s`）：服务名称；`faceName`（string, 类型 `s`）：人脸名称
- **返回值**: `id`（string, 类型 `s`）：录入操作 ID

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.StartEnroll \
  "testuser" "face_service" "my_face"
```

#### StopEnroll

停止进行中的人脸录入流程。仅允许发起录入的调用者停止。

- **功能**: 终止指定操作 ID 对应的录入会话，释放相关资源
- **触发条件**: 调用方主动调用此方法时触发；通常在用户取消录入或录入完成后调用
- **使用场景**: 用户取消人脸录入操作，或应用在录入流程异常时主动终止

- **输入参数**: `id`（string, 类型 `s`）：录入操作 ID
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.StopEnroll \
  "${enroll_id:?请使用发起录入时返回的实际 ID}"
```

### 人脸验证

#### StartVerify

开始人脸验证流程，为指定用户和服务创建一个人脸验证会话。

- **功能**: 启动人脸验证，返回一个操作 ID（id），该 id 用于后续 StopVerify、GetShareMemInfo 操作，并与 VerifyStatus 信号关联
- **触发条件**: 调用方主动调用此方法时触发
- **使用场景**: 用户登录系统或应用需要身份验证时，调用此方法启动人脸验证流程

- **输入参数**: `username`（string, 类型 `s`）：用户名；`serviceName`（string, 类型 `s`）：服务名称；`timeout`（int32, 类型 `i`）：超时时间（秒）
- **返回值**: `id`（string, 类型 `s`）：验证操作 ID

权限：

- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.StartVerify \
  "testuser" "face_service" 30
```

#### StopVerify

停止进行中的人脸验证流程。仅允许发起验证的调用者停止。

- **功能**: 终止指定操作 ID 对应的验证会话，释放相关资源
- **触发条件**: 调用方主动调用此方法时触发；通常在用户取消验证或验证超时后调用
- **使用场景**: 用户取消人脸验证操作，或应用在验证流程异常时主动终止

- **输入参数**: `id`（string, 类型 `s`）：验证操作 ID
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.StopVerify \
  "${verify_id:?请使用发起验证时返回的实际 ID}"
```

### 人脸查询与管理

#### ListFaces

列出指定用户在指定服务下已录入的人脸列表。

- **功能**: 查询指定用户和服务下所有已录入的人脸名称
- **触发条件**: 调用方主动调用此方法时触发
- **使用场景**: 应用在管理界面展示已录入的人脸列表，或在录入/删除前检查现有人脸数据

- **输入参数**: `serviceName`（string, 类型 `s`）：服务名称；`username`（string, 类型 `s`）：用户名
- **返回值**: `faces`（string 数组, 类型 `as`）：人脸名称列表

权限：

- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.ListFaces \
  "face_service" "testuser"
```

#### RenameFace

重命名已录入的人脸。

- **功能**: 将指定用户和服务下的旧人脸名称修改为新名称
- **触发条件**: 调用方主动调用此方法时触发
- **使用场景**: 需要对已录入人脸更改名称时调用，需 polkit 提权

权限：
- requires_sudo: true

- **输入参数**: `serviceName`（string, 类型 `s`）：服务名称；`username`（string, 类型 `s`）：用户名；`oldFace`（string, 类型 `s`）：原人脸名称；`newFace`（string, 类型 `s`）：新人脸名称
- **返回值**: 无

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.RenameFace \
  "face_service" "testuser" "old_name" "new_name"
```

#### DeleteFace

删除指定的人脸。

- **功能**: 删除指定用户和服务下的单个人脸数据
- **触发条件**: 调用方主动调用此方法时触发
- **使用场景**: 删除单个指定人脸，需 polkit 提权

权限：
- requires_sudo: true

- **输入参数**: `serviceName`（string, 类型 `s`）：服务名称；`username`（string, 类型 `s`）：用户名；`faceName`（string, 类型 `s`）：人脸名称
- **返回值**: 无

风险警示：

- 删除指定用户的人脸模板后，该模板不能再用于人脸认证；删除前应保留其他可用认证方式。

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.DeleteFace \
  "face_service" "testuser" "my_face"
```

#### DeleteFaces

删除指定用户在指定服务下的所有人脸。

- **功能**: 批量删除指定用户和服务下的全部人脸数据
- **触发条件**: 调用方主动调用此方法时触发
- **使用场景**: 删除指定用户的所有人脸数据，需 polkit 提权

权限：
- requires_sudo: true

- **输入参数**: `serviceName`（string, 类型 `s`）：服务名称；`username`（string, 类型 `s`）：用户名
- **返回值**: 无

风险警示：

- 批量删除将移除目标用户的多个人脸模板并影响人脸登录；确认用户、模板范围及备用认证方式。

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.DeleteFaces \
  "face_service" "testuser"
```

### 默认设备与服务设置

#### SetDefaultDevice

设置指定服务的默认人脸识别设备。

- **功能**: 将指定服务的人脸识别默认设备设置为指定设备路径
- **触发条件**: 调用方主动调用此方法时触发
- **使用场景**: 多设备场景下指定默认人脸识别设备

- **输入参数**: `serviceName`（string, 类型 `s`）：服务名称；`device`（string, 类型 `s`）：设备路径
- **返回值**: 无

权限：

- requires_sudo: true

风险警示：

- 更改默认认证设备或服务会影响后续人脸认证，需确认目标服务和设备可用并保留其他认证方式。

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.SetDefaultDevice \
  "face_service" "/dev/video0"
```

#### SetDefaultService

设置默认人脸识别服务。

- **功能**: 将指定服务名称设置为系统默认的人脸识别服务
- **触发条件**: 调用方主动调用此方法时触发
- **使用场景**: 多服务场景下指定默认人脸识别服务

- **输入参数**: `serviceName`（string, 类型 `s`）：服务名称
- **返回值**: 无

权限：

- requires_sudo: true

风险警示：

- 更改默认认证设备或服务会影响后续人脸认证，需确认目标服务和设备可用并保留其他认证方式。

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.SetDefaultService \
  "face_service"
```

### 共享内存信息

#### GetShareMemInfo

获取录入或验证操作的共享内存信息，用于读取图像数据。

- **功能**: 返回指定操作 ID 对应的共享内存套接字路径、键和大小，调用方通过这些信息读取人脸图像数据
- **触发条件**: 调用方主动调用此方法时触发；通常在 StartEnroll 或 StartVerify 返回操作 ID 后调用
- **使用场景**: 应用需要获取录入或验证过程中的人脸图像帧进行预览或处理时，通过此接口获取共享内存访问信息

- **输入参数**: `id`（string, 类型 `s`）：操作 ID
- **返回值**: `sockPath`（string, 类型 `s`）：共享内存套接字路径；`key`（string, 类型 `s`）：共享内存键；`size`（int32, 类型 `i`）：共享内存大小

```bash
gdbus call --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face \
  --method org.deepin.dde.Authenticate1.Face.GetShareMemInfo \
  "${operation_id:?请使用仍有效的录入或验证操作 ID}"
```

### 属性

#### DefaultDevice

当前默认设备路径。

- **功能**: 表示当前默认使用的人脸识别设备路径
- **使用场景**: 应用读取此属性以显示当前默认设备信息

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

#### DefaultService

当前默认人脸识别服务名称。

- **功能**: 表示当前默认使用的人脸识别服务名称
- **使用场景**: 应用读取此属性以显示当前默认服务信息

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

#### ServiceList

可用的人脸识别服务列表（JSON 格式字符串）。

- **功能**: 表示系统中所有可用的人脸识别服务列表，以 JSON 格式字符串形式返回
- **使用场景**: 应用读取此属性以获取可用服务列表，供用户选择

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

### 信号

#### EnrollStatus

人脸录入状态变化时发出。

- **功能**: 通知调用方人脸录入的进度和结果状态
- **触发条件**: 在人脸录入过程中，当录入状态发生变化时发出（如录入进度更新、录入成功、录入失败）
- **使用场景**: 应用监听此信号以实时更新录入界面状态和提示信息

- **参数**: `id`（string, 类型 `s`）：操作 ID；`user`（string, 类型 `s`）：用户名；`code`（int32, 类型 `i`）：状态码；`msg`（string, 类型 `s`）：状态消息

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face
```

#### VerifyStatus

人脸验证状态变化时发出。

- **功能**: 通知调用方人脸验证的进度和结果状态
- **触发条件**: 在人脸验证过程中，当验证状态发生变化时发出（如验证进度更新、验证成功、验证失败、验证超时）
- **使用场景**: 应用监听此信号以实时更新验证界面状态和提示信息

- **参数**: `id`（string, 类型 `s`）：操作 ID；`user`（string, 类型 `s`）：用户名；`code`（int32, 类型 `i`）：状态码；`msg`（string, 类型 `s`）：状态消息

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face
```

#### DeviceStatus

设备状态变化时发出。

- **功能**: 通知调用方人脸识别设备的状态变化
- **触发条件**: 当设备状态发生变化时发出（如设备连接、断开、错误）
- **使用场景**: 应用监听此信号以实时响应设备状态变化，如设备热插拔时更新界面提示

- **参数**: `serviceName`（string, 类型 `s`）：服务名称；`code`（int32, 类型 `i`）：设备状态码

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Authenticate1 \
  --object-path /org/deepin/dde/Authenticate1/Face
```

---
