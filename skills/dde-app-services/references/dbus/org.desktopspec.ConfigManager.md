# org.desktopspec.ConfigManager 接口参考

该接口提供配置管理器对象获取、更新、同步和日志规则设置能力。dde-app-services 是 DDE 提供的全局系统配置管理服务，可读写 DConfig 配置。其中日志配置用于设置 dde-app-services 自身的日志级别/行为，而非系统全局日志。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ConfigManager` |
| Object path | `/` |
| Interface | `org.desktopspec.ConfigManager` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。


### 管理器对象获取

#### acquireManagerV2

获取指定用户、应用和资源的配置管理器对象（V2）。

- **输入参数**: `uid`（uint32, 类型 `u`）：用户 ID；`appid`（string, 类型 `s`）：应用 ID；`name`（string, 类型 `s`）：资源名；`subpath`（string, 类型 `s`）：子路径
- **返回值**: `o`（object path）：管理器对象路径

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.acquireManagerV2 1000 "org.deepin.dde.daemon" "org.deepin.dde.daemon.power" ""
```

#### acquireManager

获取指定应用和资源的配置管理器对象。

- **输入参数**: `appid`（string, 类型 `s`）：应用 ID；`name`（string, 类型 `s`）：资源名；`subpath`（string, 类型 `s`）：子路径
- **返回值**: `o`（object path）：管理器对象路径

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.acquireManager "org.deepin.dde.daemon" "org.deepin.dde.daemon.power" ""
```


### 配置更新与同步

#### update

更新指定路径的配置。

- **输入参数**: `path`（string, 类型 `s`）：管理器对象路径
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.update "/path/to/manager"
```

#### sync

同步指定路径的配置到磁盘。

- **输入参数**: `path`（string, 类型 `s`）：管理器对象路径
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.sync "/path/to/manager"
```

#### setDelayReleaseTime

设置延迟释放时间。

- **输入参数**: `time`（int32, 类型 `i`）：延迟时间（毫秒）
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.setDelayReleaseTime 5000
```

#### delayReleaseTime

获取延迟释放时间。

- **输入参数**: 无
- **返回值**: `i`（int32）：延迟时间（毫秒）

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.delayReleaseTime
```


### 日志与数据管理

#### enableVerboseLogging

启用详细日志。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.enableVerboseLogging
```

#### disableVerboseLogging

禁用详细日志。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.disableVerboseLogging
```

#### setLogRules

设置日志规则。

- **输入参数**: `rules`（string, 类型 `s`）：日志规则 JSON
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.setLogRules '{"rules":"*=true"}'
```

#### removeUserData

移除指定用户的配置数据。

- **输入参数**: `uid`（uint32, 类型 `u`）：用户 ID
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.removeUserData 1000
```

#### reload

重新加载配置。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.reload
```

---
