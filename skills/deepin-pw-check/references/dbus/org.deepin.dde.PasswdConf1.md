# org.deepin.dde.PasswdConf1 接口参考

该接口提供密码安全策略的读写和管理能力，包括密码长度限制、校验策略、校验规则数量和首字母大写要求。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.PasswdConf1` |
| Object path | `/org/deepin/dde/PasswdConf1` |
| Interface | `org.deepin.dde.PasswdConf1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。


### 通用配置

#### WriteConfig

写入完整配置。

- **输入参数**: `data`（string, 类型 `s`）：配置 JSON
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.WriteConfig '{"min_length":8}'
```

#### ReadConfig

读取完整配置。

- **输入参数**: 无
- **返回值**: `s`（string）：配置 JSON

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.ReadConfig
```

#### Reset

重置配置为默认值。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.Reset
```

#### Backup

备份配置。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.Backup
```


### 密码长度限制

#### GetLengthLimit

获取密码长度限制范围。

- **输入参数**: 无
- **返回值**: `(ii)`（int32, int32）：最小长度和最大长度

```bash
gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.GetLengthLimit
```

#### SetLengthLimit

设置密码长度限制范围。

- **输入参数**: `min`（int32, 类型 `i`）：最小长度；`max`（int32, 类型 `i`）：最大长度
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.SetLengthLimit 8 32
```


### 校验策略

#### GetValidatePolicy

获取校验策略。

- **输入参数**: 无
- **返回值**: `s`（string）：校验策略 JSON

```bash
gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.GetValidatePolicy
```

#### SetValidatePolicy

设置校验策略。

- **输入参数**: `s`（string, 类型 `s`）：校验策略 JSON
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.SetValidatePolicy '{"policy":"strict"}'
```

#### GetValidateRequired

获取校验规则数量。

- **输入参数**: 无
- **返回值**: `i`（int32）：校验规则数量

```bash
gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.GetValidateRequired
```

#### SetValidateRequired

设置校验规则数量。

- **输入参数**: `n`（int32, 类型 `i`）：校验规则数量
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.SetValidateRequired 3
```


### 功能开关

#### GetEnabled

获取密码校验是否启用。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否启用

```bash
gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.GetEnabled
```

#### SetEnabled

设置密码校验是否启用。

- **输入参数**: `enabled`（bool, 类型 `b`）：是否启用
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.SetEnabled true
```

#### GetFirstLetterUpper

获取是否要求首字母大写。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否要求

```bash
gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.GetFirstLetterUpper
```

#### SetFirstLetterUpper

设置是否要求首字母大写。

- **输入参数**: `enabled`（bool, 类型 `b`）：是否要求
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.SetFirstLetterUpper true
```

---
