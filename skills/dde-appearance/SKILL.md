---
name: dde-appearance
description: dde-appearance 是 DDE 外观管理组件，通过 Session 总线提供当前用户桌面的外观设置（字体、主题、壁纸、光标、缩放、窗口圆角、不透明度）和工作区背景切换、装饰主题设置、多任务状态控制、窗口显示操作的 D-Bus 读写接口；另提供 dde-fakewm 虚拟窗口管理器作为 dde-appearance 自身的开发调试工具
Categories:
  - Settings
---

# dde-appearance

dde-appearance 是 DDE 桌面环境的外观管理组件。通过 Session 总线提供当前用户桌面的外观设置（字体、主题、壁纸、光标、缩放、窗口圆角、不透明度）和窗口管理器工作区背景切换能力。此外，dde-appearance 项目还包含 dde-fakewm 虚拟窗口管理器，作为 dde-appearance 自身的开发调试工具。

外观设置作用于当前用户的桌面；工作区与窗口操作针对当前窗口管理器。壁纸轮播和处理缓存由相应后端管理；Portal 的壁纸请求使用门户调用契约。外观日常设置使用公开外观接口，不使用 UOS ID 内部同步恢复协议。

## D-Bus 接口

### 外观设置

提供当前用户桌面的字体、主题、壁纸、光标、缩放、窗口圆角、不透明度的读写接口。

详见 [org.deepin.dde.Appearance1.md](references/dbus/org.deepin.dde.Appearance1.md)

### 窗口管理器

提供当前会话的工作区背景切换、装饰主题设置、多任务状态控制和窗口显示操作。

详见 [com.deepin.wm.md](references/dbus/com.deepin.wm.md)

## CLI 命令

### dde-fakewm

dde-appearance 自身的开发调试工具，模拟最小化窗口管理器环境用于测试外观功能。非系统全局服务，仅在开发调试场景使用。

详见 [dde-fakewm.md](references/cli/dde-fakewm.md)
