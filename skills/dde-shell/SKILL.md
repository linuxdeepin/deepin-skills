---
name: dde-shell
description: 提供任务栏控制、桌面通知发送与关闭、通知能力查询、应用与系统通知配置、通知记录状态、OSD 显示和任务管理接口
Categories:
  - Application
---

# dde-shell

dde-shell 是 DDE 桌面的 Shell 组件，通过 Session 总线上的多个 D-Bus 服务提供任务栏（Dock）、通知、OSD 和任务管理能力。

## D-Bus 接口

### 任务栏控制

控制 Dock 的显示、插件重载、位置、几何区域和主屏显示属性。

详见 [org.deepin.ds.Dock](references/dbus/org.deepin.ds.Dock.md)

### 桌面通知与通知配置

提供桌面通知的发送、更新和关闭能力，可查询通知服务支持的能力与服务器信息；支持按应用读取和修改通知开关及展示配置，读取和修改系统级通知配置，查询通知记录数量，并监听通知处理状态、应用配置和系统配置的变化。

详见 [org.deepin.dde.Notification1](references/dbus/org.deepin.dde.Notification1.md)

### OSD 显示

控制屏幕显示（On-Screen Display）提示。

详见 [org.deepin.dde.Osd1](references/dbus/org.deepin.dde.Osd1.md)

### 任务管理

管理 Dock 任务栏中运行窗口的属性和操作。

详见 [org.deepin.ds.Dock.TaskManager](references/dbus/org.deepin.ds.Dock.TaskManager.md)

## DConfig 配置项

### 资源: `org.deepin.dde.shell.notification`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `appsInfo` | 应用通知信息 | object | readwrite |
| `bubbleContentRowCount` | 气泡内容行数 | number | readwrite |
| `bubbleCount` | 气泡数量 | number | readwrite |
| `dndMode` | 勿扰模式 | bool | readwrite |
| `endTime` | 勿扰结束时间 | string | readwrite |
| `lockScreenOpenDndMode` | 锁屏开启勿扰模式 | bool | readwrite |
| `maxCount` | 最大通知数量 | number | readwrite |
| `notificationCleanupDays` | 通知清理天数 | number | readwrite |
| `notificationClosed` | 通知是否关闭 | bool | readwrite |
| `openByTimeInterval` | 按时间段开启 | bool | readwrite |
| `startTime` | 勿扰开始时间 | string | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.dde.shell -r org.deepin.dde.shell.notification -k appsInfo --get
# 设置
dde-dconfig -a org.deepin.dde.shell -r org.deepin.dde.shell.notification -k appsInfo -s "<value>"
```

### 资源: `org.deepin.ds.launchpad`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `searchByDesktopId` | 是否按 Desktop ID 搜索 | bool | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.dde.shell -r org.deepin.ds.launchpad -k searchByDesktopId --get
# 设置
dde-dconfig -a org.deepin.dde.shell -r org.deepin.ds.launchpad -k searchByDesktopId -s "<value>"
```

### 覆盖说明

- `org.deepin.ds.dock` 覆盖 `Item_Alignment` 配置项
- `org.deepin.ds.dock.taskmanager` 覆盖 `Docked_Items` 配置项
- `org.deepin.ds.launchpad` 覆盖 `excludeAppIdList` 配置项
