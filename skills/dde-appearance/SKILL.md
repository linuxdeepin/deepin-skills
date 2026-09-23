---
name: dde-appearance
description: 提供字体、主题、壁纸、光标、缩放、深色模式、窗口圆角、不透明度、窗口模糊效果的外观设置读写接口
Categories:
  - Settings
---

# dde-appearance

dde-appearance 是 DDE 外观管理组件，通过 Session 总线提供外观设置（字体、主题、壁纸、光标、缩放、深色模式、窗口圆角、不透明度、窗口模糊效果）和窗口管理器工作区背景切换能力。

## D-Bus 接口

### 外观设置

提供字体、主题、壁纸、光标、缩放、深色模式、窗口圆角、不透明度和窗口模糊效果的读写接口。

详见 [org.deepin.dde.Appearance1.md](references/dbus/org.deepin.dde.Appearance1.md)

### 窗口管理器

提供工作区背景切换、装饰主题设置、多任务状态控制和窗口显示操作。

详见 [com.deepin.wm.md](references/dbus/com.deepin.wm.md)

## CLI 命令

### dde-fakewm

DDE 虚拟窗口管理器，是 dde-appearance 项目中的开发/调试工具。

详见 [dde-fakewm.md](references/cli/dde-fakewm.md)

