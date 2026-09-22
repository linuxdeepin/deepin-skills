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

提供配置管理器对象获取、更新、同步和日志规则设置能力。

详见 [org.desktopspec.ConfigManager.md](references/dbus/org.desktopspec.ConfigManager.md)

### 配置管理器内部接口

提供配置项列表查询和变更通知能力。

详见 [org.desktopspec.ConfigManager.Internal.md](references/dbus/org.desktopspec.ConfigManager.Internal.md)

### 配置管理器 Manager 接口

提供配置值读写、重置和元信息查询能力。

详见 [org.desktopspec.ConfigManager.Manager.md](references/dbus/org.desktopspec.ConfigManager.Manager.md)

