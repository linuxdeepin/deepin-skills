# dde-app-services

dde-app-services 是 DDE 的 DConfig 配置管理服务组件，提供统一的系统配置管理能力。通过 System 总线提供按应用、资源和用户获取配置管理器对象、配置值读写与重置、元信息查询、配置更新同步、用户配置数据移除、配置热加载能力，以及仅作用于 `dde-dconfig-daemon` 自身的日志规则设置能力。同时提供 `dde-dconfig`、`dde-dconfig-daemon`、`dde-dconfig-editor` 命令行配置管理工具。部分接口需要提权操作。

普通配置访问保持当前用户身份：`acquireManager` 以 D-Bus 调用者 UID 获取对象，`acquireManagerV2` 显式指定 UID。System 总线不表示所有方法都需要 root；管理器可写权限与 key 的 `permissions`、用户和共享标志有关。配置写入影响对应资源及其消费者；`removeUserData` 才会清除指定用户的整组配置数据。

## D-Bus 接口

### 配置管理器

提供按应用、资源和用户获取配置管理器对象、更新、同步、用户配置数据移除和配置热加载能力，以及仅作用于 `dde-dconfig-daemon` 自身的日志规则设置能力。

详见 [org.desktopspec.ConfigManager.md](dbus/org.desktopspec.ConfigManager.md)

### 配置管理器 Manager 接口

提供指定管理器对象的配置值读写、重置和元信息查询能力，作用范围由该对象的用户和配置资源决定。

详见 [org.desktopspec.ConfigManager.Manager.md](dbus/org.desktopspec.ConfigManager.Manager.md)

## CLI 命令

### dde-dconfig

DDE 配置（DConfig）命令行管理工具，用于管理 DTK 提供的配置策略系统（DConfig）。

详见 [dde-dconfig.md](cli/dde-dconfig.md)

### dde-dconfig-daemon

DDE 配置守护进程，是 DConfig 系统的后台服务进程。

详见 [dde-dconfig-daemon.md](cli/dde-dconfig-daemon.md)

### dde-dconfig-editor

DDE 配置编辑器，提供图形化界面用于查看和修改 DConfig 配置项。

详见 [dde-dconfig-editor.md](cli/dde-dconfig-editor.md)
