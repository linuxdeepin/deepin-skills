---
name: dde-api
description: 提供图形信息查询、拼音搜索、设备管理、区域设置和声音主题播放的 D-Bus 接口
Categories:
  - Develop
---

# dde-api

dde-api 是 DDE 后端调用库组件，通过 Session 和 System 总线提供图形处理、拼音查询、设备管理、区域设置和声音主题播放能力。

## D-Bus 接口

### 图形处理

提供图像裁剪、缩放、旋转、模糊、圆角处理能力。

详见 [org.deepin.dde.Graphic1.md](references/dbus/org.deepin.dde.Graphic1.md)

### 拼音查询

提供中文拼音搜索能力。

详见 [org.deepin.dde.Pinyin1.md](references/dbus/org.deepin.dde.Pinyin1.md)

### 设备管理

提供蓝牙设备阻止状态查询和解锁能力。

详见 [org.deepin.dde.Device1.md](references/dbus/org.deepin.dde.Device1.md)

### 区域设置

提供系统区域设置生成和切换能力。

详见 [org.deepin.dde.LocaleHelper1.md](references/dbus/org.deepin.dde.LocaleHelper1.md)

### 声音主题播放

提供声音主题播放控制能力。

详见 [org.deepin.dde.SoundThemePlayer1.md](references/dbus/org.deepin.dde.SoundThemePlayer1.md)

