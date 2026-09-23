---
name: dde-app-services
description: 提供配置管理器对象获取、配置值读写、配置更新同步、日志规则设置的 DConfig 管理服务接口
Categories:
  - Develop
---

# dde-app-services

dde-app-services 是 DDE 的 DConfig 管理服务组件，通过 System 总线提供配置管理器对象获取、配置值读写、配置更新同步和日志规则设置能力。该接口需要提权操作。

## D-Bus 接口

### 配置管理器

提供配置管理器对象获取、更新、同步和日志规则设置能力。dde-app-services 是 DDE 提供的全局系统配置管理服务，可读写 DConfig 配置。其中日志配置用于设置 dde-app-services 自身的日志级别/行为，而非系统全局日志。

详见 [org.desktopspec.ConfigManager.md](references/dbus/org.desktopspec.ConfigManager.md)

### 配置管理器 Manager 接口

提供配置值读写、重置和元信息查询能力。

详见 [org.desktopspec.ConfigManager.Manager.md](references/dbus/org.desktopspec.ConfigManager.Manager.md)

## CLI 命令

### dde-dconfig

DDE 配置（dconfig）命令行管理工具，用于管理 DTK 提供的配置策略系统（dconfig）。

详见 [dde-dconfig.md](references/cli/dde-dconfig.md)

### dde-dconfig-daemon

DDE 配置守护进程，是 dconfig 系统的后台服务进程。

详见 [dde-dconfig-daemon.md](references/cli/dde-dconfig-daemon.md)

### dde-dconfig-editor

DDE 配置编辑器，提供图形化界面用于查看和修改 dconfig 配置项。

详见 [dde-dconfig-editor.md](references/cli/dde-dconfig-editor.md)

