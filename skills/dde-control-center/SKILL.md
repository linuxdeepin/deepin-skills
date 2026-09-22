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

### 资源: `org.deepin.dde.control-center`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `height` | 窗口高度 | number | readwrite |
| `width` | 窗口宽度 | number | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k height --get
# 设置
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center -k height -s "<value>"
```

### 资源: `org.deepin.dde.control-center.accounts`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `avatarPath` | 头像路径 | string | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.accounts -k avatarPath --get
# 设置
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.accounts -k avatarPath -s "<value>"
```

### 资源: `org.deepin.dde.control-center.commoninfo`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `showReadOnlyProtection` | 显示只读保护 | bool | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.commoninfo -k showReadOnlyProtection --get
# 设置
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.commoninfo -k showReadOnlyProtection -s "<value>"
```

### 资源: `org.deepin.dde.control-center.datetime`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `customNtpServer` | 自定义 NTP 服务器 | string | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.datetime -k customNtpServer --get
# 设置
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.datetime -k customNtpServer -s "<value>"
```

### 资源: `org.deepin.dde.control-center.display`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `minBrightnessValue` | 最小亮度值 | number | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.display -k minBrightnessValue --get
# 设置
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.display -k minBrightnessValue -s "<value>"
```

### 资源: `org.deepin.dde.control-center.personalization`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `hideIconThemes` | 隐藏图标主题 | array | readonly |

```bash
# 查询
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.personalization -k hideIconThemes --get
```

### 资源: `org.deepin.dde.control-center.sound`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `showDeviceManager` | 显示设备管理器 | bool | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.sound -k showDeviceManager --get
# 设置
dde-dconfig -a org.deepin.dde.control-center -r org.deepin.dde.control-center.sound -k showDeviceManager -s "<value>"
```

