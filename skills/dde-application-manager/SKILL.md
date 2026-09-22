---
name: dde-application-manager
description: 提供应用启动、应用属性管理、任务跟踪、MIME 类型管理和应用更新通知的 D-Bus 接口
Categories:
  - Application
---

# dde-application-manager

dde-application-manager 是 DDE 应用管理器组件，通过 Session 总线提供应用启动、应用属性管理、任务跟踪、MIME 类型管理和应用更新通知能力。

## D-Bus 接口

### 应用管理

提供应用列表查询、应用识别、用户应用增删和应用执行能力。

详见 [org.desktopspec.ApplicationManager1.md](references/dbus/org.desktopspec.ApplicationManager1.md)

### 应用属性

提供应用启动、桌面操作和应用属性查询能力。

详见 [org.desktopspec.ApplicationManager1.Application.md](references/dbus/org.desktopspec.ApplicationManager1.Application.md)

### 任务管理

提供应用启动任务跟踪能力。

详见 [org.desktopspec.JobManager1.md](references/dbus/org.desktopspec.JobManager1.md)

### MIME 类型管理

提供默认应用 MIME 类型设置能力。

详见 [org.desktopspec.MimeManager1.md](references/dbus/org.desktopspec.MimeManager1.md)

### 应用更新通知

提供应用更新完成通知能力。

详见 [org.desktopspec.ApplicationUpdateNotifier1.md](references/dbus/org.desktopspec.ApplicationUpdateNotifier1.md)

## DConfig 配置项

### 资源: `org.deepin.dde.am`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `appsLaunchedTimes` | 应用启动次数记录 | object | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.dde.application-manager -r org.deepin.dde.am -k appsLaunchedTimes --get
# 设置
dde-dconfig -a org.deepin.dde.application-manager -r org.deepin.dde.am -k appsLaunchedTimes -s "<value>"
```

### 资源: `org.deepin.dde.application-manager`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `appEnvironmentsBlacklist` | 应用环境变量黑名单 | array | readwrite |
| `appExtraEnvironments` | 应用额外环境变量 | array | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.dde.application-manager -r org.deepin.dde.application-manager -k appEnvironmentsBlacklist --get
# 设置
dde-dconfig -a org.deepin.dde.application-manager -r org.deepin.dde.application-manager -k appEnvironmentsBlacklist -s "<value>"
```

