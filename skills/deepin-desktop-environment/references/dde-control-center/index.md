# dde-control-center

dde-control-center 是 DDE 控制中心，提供控制中心应用的启动与模块查看 CLI 命令，通过 Session 总线提供窗口显示控制、页面跳转、模块列表获取和全局搜索的 D-Bus 接口，以及控制中心应用自身的窗口尺寸、模块显隐、个性化图标主题隐藏、账户头像、只读保护显示、开机壁纸编辑和 GRUB 用户名显示、亮度调节下限、自定义 NTP 地址记录、声音设备管理入口显隐的 DConfig 配置项。

## CLI 命令

### dde-control-center

DDE 控制中心主程序，是 DDE 桌面环境中用于系统设置管理的核心图形应用。


详见 [dde-control-center.md](cli/dde-control-center.md)


## D-Bus 接口

### 窗口显示与页面跳转

提供控制中心窗口的显示、隐藏、切换、退出，以及页面跳转和模块列表获取能力。

详见 [org.deepin.dde.ControlCenter1.md](dbus/org.deepin.dde.ControlCenter1.md)

### 全局搜索

提供控制中心内全局搜索能力，支持搜索、停止搜索和执行搜索动作。

详见 [org.deepin.dde.ControlCenter1.GrandSearch.md](dbus/org.deepin.dde.ControlCenter1.GrandSearch.md)

## DConfig 配置项

以下 DConfig 配置项均为控制中心应用自身的配置，用于控制控制中心窗口尺寸、各设置模块的显示行为、个性化图标主题隐藏、账户头像、只读保护显示、开机壁纸编辑和 GRUB 用户名显示、亮度调节下限、自定义 NTP 地址记录、声音设备管理入口显隐。`flags: global` 表示对应资源中共享的配置值，其消费对象仍是控制中心；不能据此推断能够修改其他组件的所有设置。

### 控制中心窗口配置

控制中心窗口尺寸、侧边栏宽度与模块显隐配置。均为控制中心应用自身配置。

详见 [org.deepin.dde.control-center](config/org.deepin.dde.control-center.md)

### 账户配置

用户头像路径配置。为控制中心应用自身配置。

详见 [org.deepin.dde.control-center.accounts](config/org.deepin.dde.control-center.accounts.md)

### 通用信息配置

只读保护显示、开机壁纸编辑和 GRUB 用户名显示配置。为控制中心应用自身配置。

详见 [org.deepin.dde.control-center.commoninfo](config/org.deepin.dde.control-center.commoninfo.md)

### 日期时间配置

记录控制中心使用的自定义 NTP 地址。实际系统 NTP 服务器由时间后端设置；单独修改此记录不应用系统时间服务配置。

详见 [org.deepin.dde.control-center.datetime](config/org.deepin.dde.control-center.datetime.md)

### 显示配置

控制中心亮度调节范围的最小比例，不直接修改当前屏幕亮度。

详见 [org.deepin.dde.control-center.display](config/org.deepin.dde.control-center.display.md)

### 个性化配置

图标主题隐藏配置。该配置为全局配置（`flags: global`）。

详见 [org.deepin.dde.control-center.personalization](config/org.deepin.dde.control-center.personalization.md)

### 声音配置

设备管理显示开关配置。为控制中心应用自身配置。

详见 [org.deepin.dde.control-center.sound](config/org.deepin.dde.control-center.sound.md)
