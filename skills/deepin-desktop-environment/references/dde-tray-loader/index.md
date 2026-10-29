# dde-tray-loader

dde-tray-loader 是 DDE 桌面环境的托盘插件加载器组件，负责加载和管理系统托盘区域的插件。本参考索引提供以下能力：

- **键盘布局指示与菜单**：通过 Session D-Bus 接口查询布局指示器状态、弹出布局选择菜单，监听布局变化与 fcitx 输入法运行状态
- **托盘图标管理**：通过 Session D-Bus 接口管理 X11 系统托盘选择权、查询托盘图标列表、监听图标增删与变化
- **电源管理配置**：通过 DConfig 配置充电保护电量阈值和电池时间信息显示
- **默认驻留插件管理**：通过 DConfig 配置默认驻留在任务栏上的插件列表

## CLI 命令

### 键盘布局

提供当前会话的键盘布局指示器状态查询与菜单显示接口。`layout` 写入只更新指示器文字；程序化修改实际键盘布局应使用键盘后端的布局设置接口。

详见 [org.deepin.dde.Keyboard1.md](dbus/org.deepin.dde.Keyboard1.md)

### 托盘管理

提供全局的托盘图标管理和通知控制 Session D-Bus 接口。

详见 [org.deepin.dde.TrayManager1.md](dbus/org.deepin.dde.TrayManager1.md)

## DConfig 配置项

DConfig 配置由对应托盘插件消费。界面显示和默认驻留列表作用于托盘自身；充电保护阈值作用于电源插件管理的电池充电行为。

### 任务栏插件通用配置

默认驻留任务栏插件列表配置。

详见 [org.deepin.dde.dock.plugin.common](config/org.deepin.dde.dock.plugin.common.md)

### 电源插件配置

充电保护电量阈值和电池时间信息显示配置。

详见 [org.deepin.dde.dock.plugin.power](config/org.deepin.dde.dock.plugin.power.md)

只读巡检的充电保护阈值入口：`dde-dconfig get -a org.deepin.dde.tray-loader -r org.deepin.dde.dock.plugin.power -k chargingProtectThreshold`。这是配置阈值，不是当前电池电量；硬件是否支持充电保护需另外探测。
