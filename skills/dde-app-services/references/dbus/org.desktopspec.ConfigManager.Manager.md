# org.desktopspec.ConfigManager.Manager 接口参考

该接口为动态获取的 DConfig 配置管理器对象接口，提供配置值读写、重置和元信息查询能力。对象路径通过 `acquireManager` 方法获取（扩充接口 `acquireManagerV2` 可显式指定 uid，按需使用）。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ConfigManager` |
| Object path | `<dynamic_manager_path>` |
| Interface | `org.desktopspec.ConfigManager.Manager` |
| Bus | System |



### 配置值读写

#### value

读取指定 key 的配置值。

- **输入参数**: `key`（string, 类型 `s`）：配置键名
- **返回值**: `v`（variant）：配置值
- **使用场景**: 应用读取自身 DConfig 配置项的当前值，例如读取主题设置、字体大小的用户配置。

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.value "key_name"
```

#### setValue

设置指定 key 的配置值。设置后配置变更会实时生效，并通过 `valueChanged` 信号通知其他监听者。

- **输入参数**: `key`（string, 类型 `s`）：配置键名；`value`（variant, 类型 `v`）：新值
- **返回值**: 无
- **使用场景**: 应用修改自身 DConfig 配置项的值，例如用户在设置界面修改主题后写入配置。

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.setValue "key_name" <"balance">
```

#### isDefaultValue

查询指定 key 是否为默认值。用于判断用户是否修改过该配置项。

- **输入参数**: `key`（string, 类型 `s`）：配置键名
- **返回值**: `b`（bool）：是否为默认值
- **使用场景**: 检查配置项是否被用户自定义修改过，例如在恢复默认设置的逻辑中判断是否需要重置。

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.isDefaultValue "key_name"
```

#### reset

重置指定 key 为默认值。清除用户自定义的值，恢复为 meta 文件中定义的默认值。

- **输入参数**: `key`（string, 类型 `s`）：配置键名
- **返回值**: 无
- **使用场景**: 用户选择"恢复默认设置"时，将指定配置项重置为默认值。

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.reset "key_name"
```


### 元信息查询

#### name

获取指定 key 的显示名称。

- **输入参数**: `key`（string, 类型 `s`）：配置键名；`language`（string, 类型 `s`）：语言
- **返回值**: `s`（string）：名称
- **使用场景**: 配置界面展示配置项的可读名称，支持多语言。

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.name "key_name" "zh_CN"
```

#### description

获取指定 key 的描述信息。

- **输入参数**: `key`（string, 类型 `s`）：配置键名；`language`（string, 类型 `s`）：语言
- **返回值**: `s`（string）：描述
- **使用场景**: 配置界面展示配置项的详细说明，帮助用户理解配置项的作用，支持多语言。

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.description "key_name" "zh_CN"
```

#### visibility

获取指定 key 的可见性。决定配置项是否对用户可见。

- **输入参数**: `key`（string, 类型 `s`）：配置键名
- **返回值**: `s`（string）：可见性
- **使用场景**: 配置界面根据可见性决定是否展示某个配置项，例如隐藏内部调试配置。

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.visibility "key_name"
```

#### permissions

获取指定 key 的权限。决定配置项的读写权限。

- **输入参数**: `key`（string, 类型 `s`）：配置键名
- **返回值**: `s`（string）：权限
- **使用场景**: 判断配置项是否允许当前用户修改，例如只读配置项不允许写入。

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.permissions "key_name"
```

#### flags

获取指定 key 的标志位。

- **输入参数**: `key`（string, 类型 `s`）：配置键名
- **返回值**: `i`（int32）：标志位
- **使用场景**: 获取配置项的附加标志信息，用于判断配置项的特殊属性。

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.flags "key_name"
```

### 对象生命周期管理

#### release

释放管理器对象。通知服务端该管理器对象不再使用，服务端可根据延迟释放策略回收资源。

- **输入参数**: 无
- **返回值**: 无
- **使用场景**: 配置操作完成后释放管理器对象，减少资源占用。配合 `setDelayReleaseTime` 使用，对象会在延迟时间后才真正释放。

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.release
```


### 管理器属性

#### version（属性）

配置版本。

- **使用场景**: 查询当前配置管理器对象的 schema 版本，用于版本兼容性判断或调试。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ConfigManager.Manager version
```
#### keyList（属性）

所有配置键名列表。

- **使用场景**: 遍历当前管理器对象下所有可用的配置键名，用于批量获取配置项或枚举所有配置。

| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ConfigManager.Manager keyList
```

### 配置值变化信号

#### valueChanged

配置值被设置时发出；当 meta 文件更新后执行 reload 或 update 操作时也可能触发此信号。

- **参数**: `key`（string, 类型 `s`）：配置键名
- **触发条件**: 配置值被设置时发出；当 meta 文件更新后执行 reload 或 update 操作时也可能触发此信号
- **使用场景**: 应用监听配置变更以实时响应，例如主题改变后自动刷新界面。

```bash
gdbus monitor --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager
```

---
