# org.deepin.dde.Face1 接口参考

该接口提供人脸录入、验证和删除等生物特征识别能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Face1` |
| Object path | `/org/deepin/dde/Face1` |
| Interface | `org.deepin.dde.Face1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。


### 人脸录入

#### EnrollStart

开始人脸录入。

- **输入参数**: `chara`（string, 类型 `s`）：特征标识；`charaType`（int32, 类型 `i`）：特征类型；`actionId`（string, 类型 `s`）：操作 ID
- **返回值**: `h`（handle）：录入句柄

```bash
gdbus call --system \
  --dest org.deepin.dde.Face1 \
  --object-path /org/deepin/dde/Face1 \
  --method org.deepin.dde.Face1.EnrollStart "face_1" 1 "enroll_action"
```

#### EnrollStop

停止人脸录入。

- **输入参数**: `actionId`（string, 类型 `s`）：操作 ID
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.Face1 \
  --object-path /org/deepin/dde/Face1 \
  --method org.deepin.dde.Face1.EnrollStop "enroll_action"
```


### 人脸验证

#### VerifyStart

开始人脸验证。

- **输入参数**: `charas`（string 数组, 类型 `as`）：特征标识列表；`actionId`（string, 类型 `s`）：操作 ID
- **返回值**: `h`（handle）：验证句柄

```bash
gdbus call --system \
  --dest org.deepin.dde.Face1 \
  --object-path /org/deepin/dde/Face1 \
  --method org.deepin.dde.Face1.VerifyStart ["face_1"] "verify_action"
```

#### VerifyStop

停止人脸验证。

- **输入参数**: `actionId`（string, 类型 `s`）：操作 ID
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.Face1 \
  --object-path /org/deepin/dde/Face1 \
  --method org.deepin.dde.Face1.VerifyStop "verify_action"
```


### 人脸删除

#### Delete

删除指定人脸特征。

- **输入参数**: `chara`（string, 类型 `s`）：特征标识
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.Face1 \
  --object-path /org/deepin/dde/Face1 \
  --method org.deepin.dde.Face1.Delete "face_1"
```


### 人脸属性

#### Claim（属性）

是否有正在进行的操作。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Face1 \
  --object-path /org/deepin/dde/Face1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Face1 Claim
```
#### List（属性）

已录入的人脸特征列表。

| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Face1 \
  --object-path /org/deepin/dde/Face1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Face1 List
```
#### CharaType（属性）

特征类型。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.Face1 \
  --object-path /org/deepin/dde/Face1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.Face1 CharaType
```

### 人脸状态信号

#### ErollStatus

录入状态变化时发出。

- **参数**: `chara`（string, 类型 `s`）：特征标识；`code`（int32, 类型 `i`）：状态码；`msg`（string, 类型 `s`）：状态消息
- **触发条件**: 人脸录入过程中状态变化时发出

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Face1 \
  --object-path /org/deepin/dde/Face1
```

#### VerifyStatus

验证状态变化时发出。

- **参数**: `chara`（string, 类型 `s`）：特征标识；`code`（int32, 类型 `i`）：状态码；`msg`（string, 类型 `s`）：状态消息
- **触发条件**: 人脸验证过程中状态变化时发出

```bash
gdbus monitor --system \
  --dest org.deepin.dde.Face1 \
  --object-path /org/deepin/dde/Face1
```

---
