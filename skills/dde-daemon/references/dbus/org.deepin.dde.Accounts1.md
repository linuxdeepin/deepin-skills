# org.deepin.dde.Accounts1 接口参考

该接口提供用户和用户组创建、删除、查询和属性管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Accounts1` |
| Object path | `/org/deepin/dde/Accounts1` |
| Interface | `org.deepin.dde.Accounts1` |
| Bus | System |
### 用户管理方法

#### CreateUser

创建用户。

- **功能**：在系统中创建新用户账户，分配指定的用户组和主目录。
- **触发条件**：当控制中心或管理工具请求创建新用户时调用。
- **使用场景**：控制中心添加用户、批量用户管理脚本。

- **输入参数**: `name`（string, 类型 `s`）：用户名；`fullName`（string, 类型 `s`）：全名；`groupType`（int32, 类型 `i`）：用户组类型
- **返回值**: `o`（object path）：用户路径

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Accounts1 \
  --object-path /org/deepin/dde/Accounts1 \
  --method org.deepin.dde.Accounts1.CreateUser "user" "Full Name" 1
```

#### DeleteUser

删除用户。

- **功能**：删除系统中已存在的用户账户，可选择是否同时删除用户主目录。
- **触发条件**：当控制中心或管理工具请求删除用户时调用。
- **使用场景**：控制中心删除用户、用户生命周期管理。

- **输入参数**: `name`（string, 类型 `s`）：用户名；`rmHome`（bool, 类型 `b`）：是否删除主目录
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Accounts1 \
  --object-path /org/deepin/dde/Accounts1 \
  --method org.deepin.dde.Accounts1.DeleteUser "user" true
```

#### FindUserById

通过 UID 查找用户。

- **功能**：通过 UID 查找用户并返回用户的 D-Bus 对象路径。
- **触发条件**：当需要通过 UID 获取用户详细信息时调用。
- **使用场景**：权限管理、用户信息查询。

- **输入参数**: `uid`（string, 类型 `s`）：用户 ID
- **返回值**: `o`（object path）：用户路径

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Accounts1 \
  --object-path /org/deepin/dde/Accounts1 \
  --method org.deepin.dde.Accounts1.FindUserById "1000"
```

#### FindUserByName

通过用户名查找用户。

- **功能**：通过用户名查找用户并返回用户的 D-Bus 对象路径。
- **触发条件**：当需要通过用户名获取用户详细信息时调用。
- **使用场景**：登录验证、用户信息查询。

- **输入参数**: `name`（string, 类型 `s`）：用户名
- **返回值**: `o`（object path）：用户路径

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Accounts1 \
  --object-path /org/deepin/dde/Accounts1 \
  --method org.deepin.dde.Accounts1.FindUserByName "user"
```

#### RandUserIcon

随机获取用户图标。

- **功能**：随机获取一个系统预设的用户头像图标路径。
- **触发条件**：当需要为新用户分配随机头像时调用。
- **使用场景**：用户创建时自动分配头像、头像选择界面。

- **输入参数**: 无
- **返回值**: `s`（string）：图标路径

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Accounts1 \
  --object-path /org/deepin/dde/Accounts1 \
  --method org.deepin.dde.Accounts1.RandUserIcon
```

#### IsUsernameValid

校验用户名是否合法。

- **功能**：校验用户名是否符合系统命名规则，返回是否合法以及建议列表。
- **触发条件**：当用户在创建用户界面输入用户名需要实时校验时调用。
- **使用场景**：控制中心创建用户界面实时校验用户名合法性。

- **输入参数**: `name`（string, 类型 `s`）：用户名
- **返回值**: `(bas)`（元组）：是否合法、错误信息和建议列表

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Accounts1 \
  --object-path /org/deepin/dde/Accounts1 \
  --method org.deepin.dde.Accounts1.IsUsernameValid "user"
```

#### IsPasswordValid

校验密码是否合法。

- **功能**：校验密码是否符合系统密码强度规则，返回是否合法以及建议列表。
- **触发条件**：当用户在修改密码界面输入密码需要实时校验时调用。
- **使用场景**：控制中心修改密码界面实时校验密码强度。

- **输入参数**: `password`（string, 类型 `s`）：密码
- **返回值**: `(bas)`（元组）：是否合法、错误信息和建议列表

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Accounts1 \
  --object-path /org/deepin/dde/Accounts1 \
  --method org.deepin.dde.Accounts1.IsPasswordValid "password"
```
### 用户组管理方法

#### CreateGroup

创建用户组。

- **功能**：在系统中创建新的用户组。
- **触发条件**：当控制中心或管理工具请求创建用户组时调用。
- **使用场景**：用户组管理、权限分配。

- **输入参数**: `groupName`（string, 类型 `s`）：组名；`gid`（uint32, 类型 `u`）：组 GID；`isSystem`（bool, 类型 `b`）：是否为系统组
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Accounts1 \
  --object-path /org/deepin/dde/Accounts1 \
  --method org.deepin.dde.Accounts1.CreateGroup "group" 0 false
```

#### DeleteGroup

删除用户组。

- **功能**：删除系统中已存在的用户组。
- **触发条件**：当控制中心或管理工具请求删除用户组时调用。
- **使用场景**：用户组管理、权限回收。

- **输入参数**: `groupName`（string, 类型 `s`）：组名；`force`（bool, 类型 `b`）：是否强制删除
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Accounts1 \
  --object-path /org/deepin/dde/Accounts1 \
  --method org.deepin.dde.Accounts1.DeleteGroup "group" false
```

#### GetGroups

获取用户组列表。

- **功能**：获取系统中所有用户组的名称列表。
- **触发条件**：当需要展示所有用户组时调用。
- **使用场景**：控制中心用户组列表展示、权限管理界面。

- **输入参数**: 无
- **返回值**: `as`（string 数组）：组列表

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Accounts1 \
  --object-path /org/deepin/dde/Accounts1 \
  --method org.deepin.dde.Accounts1.GetGroups
```

#### GetGroupInfoByName

通过组名获取组信息。

- **功能**：通过组名获取用户组的详细信息（GID、成员列表）。
- **触发条件**：当需要查看特定用户组详情时调用。
- **使用场景**：用户组详情查看、权限管理。

- **输入参数**: `name`（string, 类型 `s`）：组名
- **返回值**: `a{sv}`（字典）：组信息

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Accounts1 \
  --object-path /org/deepin/dde/Accounts1 \
  --method org.deepin.dde.Accounts1.GetGroupInfoByName "group"
```

#### GetPresetGroups

获取预设用户组列表。

- **功能**：获取系统预设的用户组名称列表。
- **触发条件**：当需要展示可选的预设用户组时调用。
- **使用场景**：控制中心创建用户时选择用户组。

- **输入参数**: `accountType`（int32, 类型 `i`）：账户类型
- **返回值**: `as`（string 数组）：预设组列表

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Accounts1 \
  --object-path /org/deepin/dde/Accounts1 \
  --method org.deepin.dde.Accounts1.GetPresetGroups 1
```

