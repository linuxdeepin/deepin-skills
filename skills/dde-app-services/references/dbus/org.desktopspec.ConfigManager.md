# org.desktopspec.ConfigManager 接口参考

该接口提供全局的 DConfig 配置管理器对象获取、更新、同步、用户配置数据移除和配置热加载能力，以及仅作用于 `dde-dconfig-daemon` 自身的日志规则设置能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ConfigManager` |
| Object path | `/` |
| Interface | `org.desktopspec.ConfigManager` |
| Bus | System |



### 管理器对象获取

#### acquireManager

获取指定应用和资源的配置管理器对象。默认以当前 D-Bus 连接的 uid 为标准，获取该用户的配置管理器对象。**新代码推荐使用此接口。**

- **输入参数**: `appid`（string, 类型 `s`）：应用 ID；`name`（string, 类型 `s`）：资源名；`subpath`（string, 类型 `s`）：子路径
- **返回值**: `o`（object path）：管理器对象路径
- **使用场景**: 大多数场景下，调用方只需操作自身用户的配置，使用此接口即可，无需显式指定 uid。例如：应用读取自身 DConfig 配置、系统服务管理当前用户配置。

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.acquireManager "org.deepin.dde.daemon" "org.deepin.dde.daemon.power" ""
```

#### acquireManagerV2

获取指定用户、应用和资源的配置管理器对象。是 `acquireManager` 的扩充接口，增加了 `uid` 参数，用于需要显式指定目标用户的场景。

- **输入参数**: `uid`（uint32, 类型 `u`）：用户 ID；`appid`（string, 类型 `s`）：应用 ID；`name`（string, 类型 `s`）：资源名；`subpath`（string, 类型 `s`）：子路径
- **返回值**: `o`（object path）：管理器对象路径
- **使用场景**: 当需要操作非当前连接用户（如其他 uid 用户）的配置时使用。例如：系统管理服务为指定用户创建配置管理器对象、多用户场景下跨用户配置管理。

```bash
gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.acquireManagerV2 1000 "org.deepin.dde.daemon" "org.deepin.dde.daemon.power" ""
```

### 接口关系说明

`acquireManager` 与 `acquireManagerV2` 是**扩充关系**，而非兼容性关系：

- `acquireManager`：默认以当前 D-Bus 连接的 uid 为标准，获取该用户的配置管理器对象。**新代码推荐使用此接口。**
- `acquireManagerV2`：在 `acquireManager` 基础上扩充了 `uid` 参数，用于需要显式指定目标用户的场景。

两者功能一致，均为获取配置管理器对象。`acquireManager` 适用于大多数场景（操作当前用户配置），`acquireManagerV2` 适用于需要跨用户操作的场景。

### 配置更新与同步

#### update

更新指定路径的配置。将 meta 文件中的配置定义和默认值同步到运行时配置中，使配置项的元信息变更生效。

- **输入参数**: `path`（string, 类型 `s`）：管理器对象路径
- **返回值**: 无
- **使用场景**: 当应用的 meta 文件更新后（如应用升级后新增了配置项），需要调用此接口使新配置定义生效。通常在应用安装或升级后由系统自动调用。

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.update "/path/to/manager"
```

#### sync

同步指定路径的配置到磁盘。将运行时内存中的配置变更持久化写入磁盘存储。

- **输入参数**: `path`（string, 类型 `s`）：管理器对象路径
- **返回值**: 无
- **使用场景**: 在批量修改配置后，调用此接口确保变更已持久化，防止服务异常退出时数据丢失。

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.sync "/path/to/manager"
```

#### setDelayReleaseTime

设置管理器对象的延迟释放时间。管理器对象在不再被引用后，会延迟指定时间再释放，避免频繁创建销毁。

- **输入参数**: `time`（int32, 类型 `i`）：延迟时间（毫秒）
- **返回值**: 无
- **使用场景**: 调整管理器对象的生命周期管理策略，适用于需要频繁访问配置的场景，通过设置合理的延迟释放时间减少对象重建开销。

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.setDelayReleaseTime 5000
```

#### delayReleaseTime

获取管理器对象的延迟释放时间。

- **输入参数**: 无
- **返回值**: `i`（int32）：延迟时间（毫秒）
- **使用场景**: 查询当前延迟释放策略，用于确认配置或调试。

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.delayReleaseTime
```


### 日志规则设置（仅作用于 `dde-dconfig-daemon` 自身）

> 以下接口仅用于设置 `dde-dconfig-daemon` 自身的日志级别与行为，不影响系统全局日志配置。设置后**实时生效**，**重启服务后失效**。

#### enableVerboseLogging

启用详细日志。是 `setLogRules` 的便捷封装，用于快速开启详细日志输出。

- **输入参数**: 无
- **返回值**: 无
- **使用场景**: 调试 `dde-dconfig-daemon` 问题时，快速开启详细日志以获取更多诊断信息。一般情况下使用此接口即可。

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.enableVerboseLogging
```

#### disableVerboseLogging

禁用详细日志。是 `setLogRules` 的便捷封装，用于快速关闭详细日志输出。

- **输入参数**: 无
- **返回值**: 无
- **使用场景**: 调试完成后恢复正常的日志级别。一般情况下使用此接口即可。

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.disableVerboseLogging
```

#### setLogRules

设置 Qt logging rules 环境变量的值。是 `enableVerboseLogging` 和 `disableVerboseLogging` 的通用写法，可以设置更精细的日志规则。一般情况下使用 `enableVerboseLogging` 和 `disableVerboseLogging` 即可，仅当需要自定义日志规则时使用此接口。设置后**实时生效**，**重启服务后失效**。

- **输入参数**: `rules`（string, 类型 `s`）：Qt logging rules 规则字符串（非 JSON 格式），遵循 Qt 日志规则语法，例如 `*.debug=true;org.deepin.*.debug=false`
- **返回值**: 无
- **使用场景**: 需要精细控制 `dde-dconfig-daemon` 各模块的日志级别时使用，例如仅开启特定模块的调试日志而关闭其他模块。

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.setLogRules '*.debug=true;org.deepin.*.debug=false'
```


### 数据管理

#### removeUserData

移除指定用户的全部配置数据。清除该用户在 DConfig 系统中的所有自定义配置，恢复到初始状态。

- **输入参数**: `uid`（uint32, 类型 `u`）：用户 ID
- **返回值**: 无
- **使用场景**: 用户账户删除或配置重置时，清理该用户的全部 DConfig 配置数据。

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.removeUserData 1000
```

#### reload

热加载 meta 文件的改变。当 meta 文件（配置描述文件）发生变更时触发，重新加载所有 meta 文件使变更生效。如果执行安装脚本，会在安装钩子（hook）中自动执行此接口，无需手动调用。

- **输入参数**: 无
- **返回值**: 无
- **使用场景**: meta 文件被修改后（如应用安装/卸载导致配置描述文件增减），需要重新加载使变更生效。通常由包管理器的安装钩子自动触发，一般不需要手动调用；仅在 meta 文件被手动修改且未经过安装流程时才需手动执行。

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.desktopspec.ConfigManager \
  --object-path / \
  --method org.desktopspec.ConfigManager.reload
```

---
