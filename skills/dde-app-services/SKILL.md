---
name: dde-app-services
description: dde-app-services 是 DDE 的 DConfig 配置管理服务组件，提供统一的系统配置管理能力。通过 D-Bus 接口提供配置管理器对象获取、配置值读写与重置、元信息查询、配置更新同步、用户配置数据移除、配置热加载、管理器对象延迟释放时间设置的全局 DConfig 管理功能，以及仅作用于 `dde-dconfig-daemon` 自身的日志规则设置功能；同时提供 `dde-dconfig`、`dde-dconfig-daemon`、`dde-dconfig-editor` 命令行配置管理工具
Categories:
  - Settings
---

# dde-app-services

dde-app-services 是 DDE 的 DConfig 配置管理服务组件，提供统一的系统配置管理能力。通过 System 总线提供全局的配置管理器对象获取、配置值读写与重置、元信息查询、配置更新同步、用户配置数据移除、配置热加载能力，以及仅作用于 `dde-dconfig-daemon` 自身的日志规则设置能力。同时提供 `dde-dconfig`、`dde-dconfig-daemon`、`dde-dconfig-editor` 命令行配置管理工具。部分接口需要提权操作。

## D-Bus 接口

### 配置管理器

提供全局的配置管理器对象获取、更新、同步、用户配置数据移除和配置热加载能力，以及仅作用于 `dde-dconfig-daemon` 自身的日志规则设置能力。

详见 [org.desktopspec.ConfigManager.md](references/dbus/org.desktopspec.ConfigManager.md)

### 配置管理器 Manager 接口

提供全局的配置值读写、重置和元信息查询能力。

详见 [org.desktopspec.ConfigManager.Manager.md](references/dbus/org.desktopspec.ConfigManager.Manager.md)

## CLI 命令

### dde-dconfig

DDE 配置（DConfig）命令行管理工具，用于管理 DTK 提供的配置策略系统（DConfig）。

详见 [dde-dconfig.md](references/cli/dde-dconfig.md)

### dde-dconfig-daemon

DDE 配置守护进程，是 DConfig 系统的后台服务进程。

详见 [dde-dconfig-daemon.md](references/cli/dde-dconfig-daemon.md)

### dde-dconfig-editor

DDE 配置编辑器，提供图形化界面用于查看和修改 DConfig 配置项。

详见 [dde-dconfig-editor.md](references/cli/dde-dconfig-editor.md)
