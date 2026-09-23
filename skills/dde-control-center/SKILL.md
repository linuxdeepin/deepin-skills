---
name: dde-control-center
description: 提供控制中心窗口显示隐藏切换、页面跳转、模块列表获取和全局搜索接口
Categories:
  - Settings
---

# dde-control-center

dde-control-center 是 DDE 控制中心，通过 Session 总线提供窗口显示控制、页面跳转、模块列表获取和全局搜索能力。

## D-Bus 接口

### 窗口显示与页面跳转

提供控制中心窗口的显示、隐藏、切换、退出，以及页面跳转和模块列表获取能力。

详见 [org.deepin.dde.ControlCenter1.md](references/dbus/org.deepin.dde.ControlCenter1.md)

### 全局搜索

提供控制中心内全局搜索能力，支持搜索、停止搜索和执行搜索动作。

详见 [org.deepin.dde.ControlCenter1.GrandSearch.md](references/dbus/org.deepin.dde.ControlCenter1.GrandSearch.md)

## DConfig 配置项

dde-control-center 通过 DConfig 暴露窗口尺寸、账户、通用信息、日期时间、显示、个性化和声音配置资源。

### 控制中心窗口配置

控制中心窗口宽度和高度配置。

详见 [org.deepin.dde.control-center](references/config/org.deepin.dde.control-center.md)

### 账户配置

用户头像路径配置。

详见 [org.deepin.dde.control-center.accounts](references/config/org.deepin.dde.control-center.accounts.md)

### 通用信息配置

只读保护显示开关配置。

详见 [org.deepin.dde.control-center.commoninfo](references/config/org.deepin.dde.control-center.commoninfo.md)

### 日期时间配置

自定义 NTP 服务器配置。

详见 [org.deepin.dde.control-center.datetime](references/config/org.deepin.dde.control-center.datetime.md)

### 显示配置

亮度最小值配置。

详见 [org.deepin.dde.control-center.display](references/config/org.deepin.dde.control-center.display.md)

### 个性化配置

隐藏图标主题配置。

详见 [org.deepin.dde.control-center.personalization](references/config/org.deepin.dde.control-center.personalization.md)

### 声音配置

设备管理显示开关配置。

详见 [org.deepin.dde.control-center.sound](references/config/org.deepin.dde.control-center.sound.md)

## CLI 命令

### dde-control-center

DDE 控制中心主程序，是 DDE 桌面环境中用于系统设置管理的核心图形应用。

详见 [dde-control-center.md](references/cli/dde-control-center.md)

