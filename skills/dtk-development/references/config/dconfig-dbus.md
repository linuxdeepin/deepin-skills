# DConfig DBus 方式

## 版本边界

v20 和 v25 都通过 `dde-dconfig-daemon` 提供 `org.desktopspec.ConfigManager`
接口。具体方法、参数和可选能力必须以目标环境的 DBus introspection 为准。
取得 manager path 后要保持持有连接的 DBus 客户端存活。

## 1. 概述与适用场景

通过 DBus 接口操作配置，适用于非 C++ 环境（如脚本、其他语言）或需要直接访问配置服务的场景。

**适用场景：**
- Shell 脚本读写配置
- 非 DTK 应用访问配置
- 调试和测试配置

**相关接口：**
- `org.desktopspec.ConfigManager` — DBus 服务名
- `acquireManager` / `acquireManagerV2` — 获取配置管理器
- `get` / `set` — 读写配置值

## 1. 获取资源路径

```bash
# acquireManager: 自动识别调用者 UID
DCONFIG_PATH=$(dbus-send --system --type=method_call --print-reply=literal \
    --dest=org.desktopspec.ConfigManager / \
    org.desktopspec.ConfigManager.acquireManager \
    string:'<appId>' string:'<configId>' string:'<subpath>')

# introspection 确认支持时：显式指定 UID
DCONFIG_PATH=$(dbus-send --system --type=method_call --print-reply=literal \
    --dest=org.desktopspec.ConfigManager / \
    org.desktopspec.ConfigManager.acquireManagerV2 \
    uint32:$(id -u) string:'<appId>' string:'<configId>' string:'<subpath>')
```

## 2. 读写操作

```bash
# 读取值
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager $DCONFIG_PATH \
    org.desktopspec.ConfigManager.Manager.value string:'<key>'

# 设置值
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager $DCONFIG_PATH \
    org.desktopspec.ConfigManager.Manager.setValue \
    string:'<key>' variant:boolean:true

# 重置
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager $DCONFIG_PATH \
    org.desktopspec.ConfigManager.Manager.reset string:'<key>'

# introspection 确认支持时：查询是否为默认值
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager $DCONFIG_PATH \
    org.desktopspec.ConfigManager.Manager.isDefaultValue string:'<key>'

# 释放资源
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager $DCONFIG_PATH \
    org.desktopspec.ConfigManager.Manager.release
```

## 3. 元信息查询

```bash
# 权限
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager $DCONFIG_PATH \
    org.desktopspec.ConfigManager.Manager.permissions string:'<key>'

# 可见性
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager $DCONFIG_PATH \
    org.desktopspec.ConfigManager.Manager.visibility string:'<key>'

# flags
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager $DCONFIG_PATH \
    org.desktopspec.ConfigManager.Manager.flags string:'<key>'

# 显示名称
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager $DCONFIG_PATH \
    org.desktopspec.ConfigManager.Manager.name string:'<key>' string:'zh_CN'

# 描述
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager $DCONFIG_PATH \
    org.desktopspec.ConfigManager.Manager.description string:'<key>' string:''
```

## 4. 监听变化

```bash
dbus-monitor --system "type='signal', interface='org.desktopspec.ConfigManager.Manager', member=valueChanged"
```

## 5. 注意事项

- `acquireManager` 返回的 DBus path 有延迟释放机制（默认 30s），多进程使用相同 appId + 配置 ID 时会复用
- 执行第二个步骤时不应释放第一个步骤的 DBus 连接，否则 path 可能失效
- `acquireManagerV2` 允许操作指定 uid 用户的配置

## 6. 相关文档

- [concepts.md](concepts.md) - 核心概念
- [dconfig-cpp.md](dconfig-cpp.md) - C++ 方式
- [dconfig-debug.md](dconfig-debug.md) - 调试
