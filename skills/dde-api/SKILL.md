---
name: dde-api
description: dde-api 是 DDE 后端调用库组件，通过 Session 和 System 总线提供图像处理、拼音查询、蓝牙设备管理、区域设置、声音主题播放的 D-Bus 接口，同时提供文件打开、GRUB 主题调整、图片模糊处理、声音主题播放守护进程的 CLI 命令
Categories:
  - Develop
---

# dde-api

dde-api 是 DDE 后端调用库组件，通过 Session 和 System 总线提供图像处理、拼音查询、蓝牙设备管理、区域设置和声音主题播放的全局 D-Bus 接口，同时提供文件打开、GRUB 主题调整、图片模糊处理和声音主题播放守护进程的 CLI 命令。所有 D-Bus 接口和 CLI 工具均为全局系统能力，无仅作用于 dde-api 自身的约束功能。

## D-Bus 接口

### 图像处理

提供图像模糊、裁剪、合成、格式转换、填充、翻转、缩放、旋转、缩略图生成、主色调提取、尺寸获取、颜色转换能力。

详见 [org.deepin.dde.Graphic1.md](references/dbus/org.deepin.dde.Graphic1.md)

### 拼音查询

提供中文拼音搜索能力。

详见 [org.deepin.dde.Pinyin1.md](references/dbus/org.deepin.dde.Pinyin1.md)

### 蓝牙设备管理

提供蓝牙设备阻止状态查询和解锁能力。

详见 [org.deepin.dde.Device1.md](references/dbus/org.deepin.dde.Device1.md)

### 区域设置

提供系统区域设置生成和切换能力。

详见 [org.deepin.dde.LocaleHelper1.md](references/dbus/org.deepin.dde.LocaleHelper1.md)

### 声音主题播放

提供声音主题播放控制能力。对应的 CLI 守护进程为 `sound-theme-player`。

详见 [org.deepin.dde.SoundThemePlayer1.md](references/dbus/org.deepin.dde.SoundThemePlayer1.md)

## CLI 命令

### dde-open

DDE 文件/URL 打开工具，用于通过默认关联应用打开文件或 URL。

详见 [dde-open.md](references/cli/dde-open.md)

### adjust-grub-theme

GRUB 主题调整工具，用于根据屏幕分辨率和语言环境自动调整 GRUB 启动菜单的主题显示。

详见 [adjust-grub-theme.md](references/cli/adjust-grub-theme.md)

### image-blur

图片模糊处理工具，使用高斯模糊算法对图片进行模糊处理。与 `Graphic1` D-Bus 接口的 `BlurImage` 方法不同，该 CLI 工具支持通过 `-sigma` 参数控制模糊强度。

详见 [image-blur.md](references/cli/image-blur.md)

### sound-theme-player

声音主题播放守护进程，启动后提供 `org.deepin.dde.SoundThemePlayer1` D-Bus 接口供其他程序播放系统声音。

详见 [sound-theme-player.md](references/cli/sound-theme-player.md)
