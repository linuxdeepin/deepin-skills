# org.deepin.dde.PasswdConf1 接口参考

deepin-pw-check 是 DDE 的密码安全策略组件，负责管理系统级密码校验规则。本接口提供全局密码校验开关、密码长度限制、校验策略、校验规则数量、首字母大写要求的读写及配置管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.PasswdConf1` |
| Object path | `/org/deepin/dde/PasswdConf1` |
| Interface | `org.deepin.dde.PasswdConf1` |
| Bus | System |

## 兼容性接口

**关系类型：兼容**

旧版接口 `com.deepin.daemon.PasswdConf`（对象路径 `/com/deepin/daemon/PasswdConf`，System 总线）通过兼容代理服务提供，功能与 `org.deepin.dde.PasswdConf1` 完全相同，包含相同的 14 个方法。新代码推荐使用 `org.deepin.dde.PasswdConf1`，该接口由原生服务直接提供，旧接口通过代理服务转发。

## 通用配置

### WriteConfig

写入完整配置。将传入的 GKeyFile/INI 格式内容直接写入配置文件 `/etc/deepin/dde.conf`。

- **功能**：覆盖写入完整配置文件内容
- **触发条件**：当需要批量替换全部密码策略配置时调用
- **使用场景**：配置导入、批量配置恢复
- **输入参数**：`data`（string, 类型 `s`）：配置文件内容（GKeyFile/INI 格式）
- **返回值**：无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.WriteConfig '[Password]
PASSWORD_MIN_LENGTH=8'
```

### ReadConfig

读取完整配置。读取配置文件 `/etc/deepin/dde.conf` 的全部内容。

- **功能**：读取当前全部密码安全策略配置（GKeyFile/INI 格式）
- **触发条件**：当需要获取当前完整配置内容时调用
- **使用场景**：配置查看、备份前获取当前配置
- **输入参数**：无
- **返回值**：`s`（string）：配置文件内容（GKeyFile/INI 格式）

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.ReadConfig
```

### Reset

从备份文件 `/etc/deepin/dde.conf.bak` 恢复配置到 `/etc/deepin/dde.conf`。

- **功能**：从备份文件恢复密码安全策略配置
- **触发条件**：当需要将配置恢复到最近一次备份的状态时调用
- **使用场景**：配置回滚、恢复误修改的密码策略
- **输入参数**：无
- **返回值**：无
- **注意**：若从未执行过 Backup，备份文件 `/etc/deepin/dde.conf.bak` 不存在，Reset 会返回错误

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.Reset
```

### Backup

备份配置。将当前配置文件 `/etc/deepin/dde.conf` 复制到备份文件 `/etc/deepin/dde.conf.bak`。

- **功能**：将当前配置文件复制到备份文件
- **触发条件**：在修改密码安全策略配置前需要保存当前配置时调用
- **使用场景**：配置备份、修改前快照
- **输入参数**：无
- **返回值**：无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.Backup
```

## 密码长度限制

### GetLengthLimit

获取密码长度限制范围。

- **功能**：获取当前密码最小长度和最大长度限制
- **触发条件**：当需要查询密码长度限制范围时调用
- **使用场景**：用户修改密码前查询长度要求、密码策略展示
- **输入参数**：无
- **返回值**：`(ii)`（int32, int32）：最小长度和最大长度

```bash
gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.GetLengthLimit
```

示例输出（实际值因系统配置而异）：

```
(1, 510)
```

### SetLengthLimit

设置密码长度限制范围。

- **功能**：设置密码最小长度和最大长度限制
- **触发条件**：当需要调整密码长度要求时调用
- **使用场景**：管理员调整密码长度策略
- **输入参数**：`min`（int32, 类型 `i`）：最小长度；`max`（int32, 类型 `i`）：最大长度
- **返回值**：无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.SetLengthLimit 8 32
```

## 校验策略

### GetValidatePolicy

获取校验策略。

- **功能**：获取当前密码校验所使用的策略（包含允许的字符集）
- **触发条件**：当需要查询密码校验允许的字符集时调用
- **使用场景**：密码策略展示、校验策略查询
- **输入参数**：无
- **返回值**：`s`（string）：分号分隔的字符集字符串

```bash
gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.GetValidatePolicy
```

示例输出（实际值因系统配置而异）：

```
("1234567890;abcdefghijklmnopqrstuvwxyz;ABCDEFGHIJKLMNOPQRSTUVWXYZ;~`!@#$%^&*()-_+=|\\{}[]:\"'<>,.?/",)
```

### SetValidatePolicy

设置校验策略。

- **功能**：设置密码校验所使用的策略（包含允许的字符集）
- **触发条件**：当需要修改密码校验允许的字符集时调用
- **使用场景**：管理员调整密码校验字符集
- **输入参数**：`s`（string, 类型 `s`）：分号分隔的字符集字符串
- **返回值**：无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.SetValidatePolicy '1234567890;abcdefghijklmnopqrstuvwxyz;ABCDEFGHIJKLMNOPQRSTUVWXYZ'
```

### GetValidateRequired

获取校验规则数量。

- **功能**：获取密码必须满足的校验规则数量
- **触发条件**：当需要查询密码需满足的校验规则数量时调用
- **使用场景**：密码策略展示、校验规则查询
- **输入参数**：无
- **返回值**：`i`（int32）：校验规则数量

```bash
gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.GetValidateRequired
```

示例输出（实际值因系统配置而异）：

```
(1,)
```

### SetValidateRequired

设置校验规则数量。

- **功能**：设置密码必须满足的校验规则数量
- **触发条件**：当需要调整密码需满足的校验规则数量时调用
- **使用场景**：管理员调整密码校验严格程度
- **输入参数**：`n`（int32, 类型 `i`）：校验规则数量
- **返回值**：无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.SetValidateRequired 3
```

## 功能开关

### GetEnabled

获取密码校验是否启用。

- **功能**：查询当前是否启用了密码校验功能
- **触发条件**：当需要确认密码校验功能是否开启时调用
- **使用场景**：密码策略展示、校验功能状态查询
- **输入参数**：无
- **返回值**：`b`（bool）：是否启用

```bash
gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.GetEnabled
```

示例输出（实际值因系统配置而异）：

```
(true,)
```

### SetEnabled

设置密码校验是否启用。

- **功能**：开启或关闭密码校验功能
- **触发条件**：当需要开启或关闭密码校验功能时调用
- **使用场景**：管理员开启或关闭密码校验
- **输入参数**：`enabled`（bool, 类型 `b`）：是否启用
- **返回值**：无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.SetEnabled true
```

### GetFirstLetterUpper

获取是否要求首字母大写。

- **功能**：查询当前是否要求密码首字母大写
- **触发条件**：当需要查询密码首字母大写要求时调用
- **使用场景**：密码策略展示、首字母大写要求查询
- **输入参数**：无
- **返回值**：`b`（bool）：是否要求

```bash
gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.GetFirstLetterUpper
```

示例输出（实际值因系统配置而异）：

```
(false,)
```

### SetFirstLetterUpper

设置是否要求首字母大写。

- **功能**：开启或关闭密码首字母大写要求
- **触发条件**：当需要开启或关闭密码首字母大写要求时调用
- **使用场景**：管理员调整密码首字母大写要求
- **输入参数**：`enabled`（bool, 类型 `b`）：是否要求
- **返回值**：无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.PasswdConf1 \
  --object-path /org/deepin/dde/PasswdConf1 \
  --method org.deepin.dde.PasswdConf1.SetFirstLetterUpper true
```

---
