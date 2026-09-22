---
name: dde-tray-loader
description: 提供键盘布局切换、布局列表查询和托盘插件管理的 D-Bus 接口
Categories:
  - Application
---

# dde-tray-loader

dde-tray-loader 是 DDE 托盘加载器组件，通过 Session 总线提供键盘布局切换和托盘插件管理能力。

## D-Bus 接口

### 键盘布局

提供键盘布局切换和状态查询能力。

详见 [org.deepin.dde.Keyboard1.md](references/dbus/org.deepin.dde.Keyboard1.md)

### 托盘管理

提供托盘图标管理和通知控制能力。

详见 [org.deepin.dde.TrayManager1.md](references/dbus/org.deepin.dde.TrayManager1.md)

## DConfig 配置项

### 资源: `org.deepin.dde.dock.plugin.common`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `defaultDockedPlugins` | 默认驻留任务栏插件 | array | readonly |

```bash
# 查询
dde-dconfig -a org.deepin.dde.tray-loader -r org.deepin.dde.dock.plugin.common -k defaultDockedPlugins --get
```

### 资源: `org.deepin.dde.dock.plugin.power`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `chargingProtectThreshold` | 充电保护电量阈值 | number | readwrite |
| `showTimeToFull` | 显示电池时间信息 | bool | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.dde.tray-loader -r org.deepin.dde.dock.plugin.power -k chargingProtectThreshold --get
# 设置
dde-dconfig -a org.deepin.dde.tray-loader -r org.deepin.dde.dock.plugin.power -k chargingProtectThreshold -s "<value>"
```

