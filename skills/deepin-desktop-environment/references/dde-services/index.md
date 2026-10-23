# dde-services

dde-services 是 DDE 的后端服务组件，在 Treeland 会话下替代 dde-daemon 的部分后端功能。提供全局电源管理、X 设置、壁纸轮播、快捷键管理、手势管理、壁纸缓存和环境亮度感知的 D-Bus 接口（电源管理同时注册在 Session 和 System 总线上），提供快捷键操作执行和 IP 地址监视的 CLI 命令，并提供电源管理和环境亮度的 DConfig 配置项。

同名接口按实际会话服务分流，调用前确认目标 Bus 和服务归属。System Power1 的电池状态查询、性能模式和 CPU 调频控制与会话关机请求不同；写操作按部署版本的服务端授权策略处理。只读查询不统一提权，调用方白名单登记属于受限服务协作。

## CLI 命令

### dde-shortcut-tool

全局快捷键执行工具，通过子命令 + action 模式执行各类系统快捷操作。系统级工具，通常由快捷键守护进程自动调用。

详见 [dde-shortcut-tool.md](cli/dde-shortcut-tool.md)

### ipwatchd

IP 地址监视守护进程（upstream 开源项目），用于监视网络接口的 IP 地址变化。系统级工具，作为网络管理的底层辅助组件。

详见 [ipwatchd.md](cli/ipwatchd.md)

## D-Bus 接口

以下接口主要在 Session 总线上注册，电源管理接口同时注册在 System 总线上，在 Treeland 会话下全局生效。其中 org.deepin.dde.Power1、org.deepin.dde.Keybinding1 和 org.deepin.dde.Gesture1 与 dde-daemon 存在接口重名，属于 Treeland/X11 双轨分流设计：在 Treeland 会话下由 dde-services 提供，在 X11 会话下由 dde-daemon 提供，并非兼容性别名接口。

### 电源管理

全局电源管理能力，包括 Session 总线上的电源状态查询、延时配置、电源操作和低电量告警配置，以及 System 总线上的系统级电源管理、电池设备管理和 CPU 调频控制。

详见 [org.deepin.dde.Power1.md](dbus/org.deepin.dde.Power1.md)

### X 设置

全局 X 设置读写能力，包括颜色、整数、字符串、缩放因子的读取和设置。

详见 [org.deepin.dde.XSettings1.md](dbus/org.deepin.dde.XSettings1.md)

### 壁纸轮播

全局壁纸轮播配置能力。

详见 [org.deepin.dde.WallpaperSlideshow.md](dbus/org.deepin.dde.WallpaperSlideshow.md)

### 快捷键

全局快捷键管理能力，包括快捷键查询、自定义快捷键增删改、快捷键冲突处理和快捷键捕获。

详见 [org.deepin.dde.Keybinding1.md](dbus/org.deepin.dde.Keybinding1.md)

### 手势

全局手势管理能力，包括手势列表查询、手势动作修改和可用动作查询。

详见 [org.deepin.dde.Gesture1.md](dbus/org.deepin.dde.Gesture1.md)

### 壁纸缓存

全局壁纸缓存能力，包括处理后图像路径获取和模糊处理。

详见 [org.deepin.dde.WallpaperCache.md](dbus/org.deepin.dde.WallpaperCache.md)

### 环境亮度

全局环境亮度感知能力。

详见 [org.deepin.dde.AmbientBrightness1.md](dbus/org.deepin.dde.AmbientBrightness1.md)

## DConfig 配置

以下 DConfig 配置项通过 DConfig 服务统一管理，提供电源管理和环境亮度的配置读写能力。

### 电源管理配置

电源管理的 DConfig 配置项，包括 CPU 调频、节能模式、定时关机、屏幕延时、低电量策略、电源按键动作配置。

详见 [org.deepin.dde.daemon.power.md](config/org.deepin.dde.daemon.power.md)

### 环境亮度配置

环境亮度感知的 DConfig 配置项，包括自动亮度开关、映射模式、加权窗口、lux-亮度曲线、滞回比例和防抖时间。

详见 [org.deepin.dde.daemon.ambient-brightness.md](config/org.deepin.dde.daemon.ambient-brightness.md)
