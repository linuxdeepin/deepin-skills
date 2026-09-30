---
name: dde-launchpad
description: dde-launchpad 是 DDE 桌面环境的启动器组件，以 dde-shell applet 形式运行。提供启动器显示隐藏切换的 D-Bus 接口（含已废弃的模式控制方法），以及按桌面条目 ID 搜索的 DConfig 配置项
Categories:
  - Application
---

# dde-launchpad

dde-launchpad 是 DDE 桌面环境的启动器组件，以 dde-shell applet 形式运行，为用户提供应用启动入口。通过 Session 总线提供启动器的显示、隐藏、切换能力，以及已废弃的模式控制方法（ShowByMode），并通过 DConfig 管理启动器自身的按桌面条目 ID 搜索行为。其 DConfig 配置仅作用于 dde-launchpad 自身应用行为，不影响系统全局配置。

## D-Bus 接口

### 启动器控制

提供启动器的显示、隐藏、切换能力，以及已废弃的模式控制方法（ShowByMode）。

详见 [org.deepin.dde.Launcher1.md](references/dbus/org.deepin.dde.Launcher1.md)

## DConfig 配置项

dde-launchpad 通过 DConfig 暴露启动器自身应用行为配置，配置资源挂载在 appId `org.deepin.dde.shell` 下。

### 启动器应用配置

控制启动器的按桌面条目 ID 搜索开关。

详见 [org.deepin.ds.launchpad.md](references/config/org.deepin.ds.launchpad.md)
