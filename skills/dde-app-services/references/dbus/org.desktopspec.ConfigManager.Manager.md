# org.desktopspec.ConfigManager.Manager 接口参考

该接口为动态获取的配置管理器对象接口，提供配置值读写、重置和元信息查询能力。对象路径通过 `acquireManager` 或 `acquireManagerV2` 方法获取。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ConfigManager` |
| Object path | `<dynamic_manager_path>` |
| Interface | `org.desktopspec.ConfigManager.Manager` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。


### 配置值读写

#### value

读取指定 key 的配置值。

- **输入参数**: `key`（string, 类型 `s`）：配置键名
- **返回值**: `v`（variant）：配置值

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.value "key_name"
```

#### setValue

设置指定 key 的配置值。

- **输入参数**: `key`（string, 类型 `s`）：配置键名；`value`（variant, 类型 `v`）：新值
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.setValue "key_name" <variant true>
```

#### isDefaultValue

查询指定 key 是否为默认值。

- **输入参数**: `key`（string, 类型 `s`）：配置键名
- **返回值**: `b`（bool）：是否为默认值

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.isDefaultValue "key_name"
```

#### reset

重置指定 key 为默认值。

- **输入参数**: `key`（string, 类型 `s`）：配置键名
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.reset "key_name"
```


### 元信息查询

#### name

获取指定 key 的名称。

- **输入参数**: `key`（string, 类型 `s`）：配置键名；`language`（string, 类型 `s`）：语言
- **返回值**: `s`（string）：名称

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.name "key_name" "zh_CN"
```

#### description

获取指定 key 的描述。

- **输入参数**: `key`（string, 类型 `s`）：配置键名；`language`（string, 类型 `s`）：语言
- **返回值**: `s`（string）：描述

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.description "key_name" "zh_CN"
```

#### visibility

获取指定 key 的可见性。

- **输入参数**: `key`（string, 类型 `s`）：配置键名
- **返回值**: `s`（string）：可见性

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.visibility "key_name"
```

#### permissions

获取指定 key 的权限。

- **输入参数**: `key`（string, 类型 `s`）：配置键名
- **返回值**: `s`（string）：权限

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

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.flags "key_name"
```

#### release

释放管理器对象。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager \
  --method org.desktopspec.ConfigManager.Manager.release
```


### 管理器属性

#### version（属性）

配置版本。

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

配置值变化时发出。

- **参数**: `key`（string, 类型 `s`）：配置键名
- **触发条件**: 配置值被设置时发出

```bash
gdbus monitor --system \
  --dest org.desktopspec.ConfigManager \
  --object-path /path/to/manager
```

---
