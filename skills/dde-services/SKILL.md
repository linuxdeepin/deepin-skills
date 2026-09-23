---
name: dde-services
description: 提供电源管理、X设置、壁纸轮播、快捷键、手势、图像效果、图像模糊、壁纸缓存、环境亮度的 D-Bus 接口
Categories:
  - Settings
---

# dde-services

dde-services 是 DDE 的后端服务组件，通过 Session 总线提供电源管理、X 设置、壁纸轮播、快捷键、手势、图像效果、图像模糊、壁纸缓存和环境亮度能力。

## D-Bus 接口

### 电源管理

提供电源管理能力。

详见 [org.deepin.dde.Power1.md](references/dbus/org.deepin.dde.Power1.md)

### X 设置

提供X 设置能力。

详见 [org.deepin.dde.XSettings1.md](references/dbus/org.deepin.dde.XSettings1.md)

### 壁纸轮播

提供壁纸轮播能力。

详见 [org.deepin.dde.WallpaperSlideshow.md](references/dbus/org.deepin.dde.WallpaperSlideshow.md)

### 快捷键

提供快捷键能力。

详见 [org.deepin.dde.Keybinding1.md](references/dbus/org.deepin.dde.Keybinding1.md)

### 手势

提供手势能力。

详见 [org.deepin.dde.Gesture1.md](references/dbus/org.deepin.dde.Gesture1.md)

### 图像效果

提供图像效果能力。

详见 [org.deepin.dde.ImageEffect1.md](references/dbus/org.deepin.dde.ImageEffect1.md)

### 图像模糊

提供图像模糊能力。

详见 [org.deepin.dde.ImageBlur1.md](references/dbus/org.deepin.dde.ImageBlur1.md)

### 壁纸缓存

提供壁纸缓存能力。

详见 [org.deepin.dde.WallpaperCache.md](references/dbus/org.deepin.dde.WallpaperCache.md)

### 环境亮度

提供环境亮度能力。

详见 [org.deepin.dde.AmbientBrightness1.md](references/dbus/org.deepin.dde.AmbientBrightness1.md)

## CLI 命令

### dde-shortcut-tool

DDE 快捷键工具，通过子命令 + action 模式执行各类系统快捷操作。

详见 [dde-shortcut-tool.md](references/cli/dde-shortcut-tool.md)

### ipwatchd

IP 地址监视守护进程（upstream 开源项目），用于监视网络接口的 IP 地址变化。

详见 [ipwatchd.md](references/cli/ipwatchd.md)

