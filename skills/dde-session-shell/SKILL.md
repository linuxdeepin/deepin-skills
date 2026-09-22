---
name: dde-session-shell
description: 提供锁屏界面显示控制、关机界面显示控制和电源操作接口
Categories:
  - Application
---

# dde-session-shell

dde-session-shell 是 DDE 登录锁屏组件，通过 Session 总线提供锁屏界面显示控制、关机界面显示控制和电源操作能力。

## D-Bus 接口

### 锁屏界面控制

提供锁屏界面显示、用户列表显示、认证状态控制和电源操作能力。

详见 [org.deepin.dde.LockFront1.md](references/dbus/org.deepin.dde.LockFront1.md)

### 关机界面控制

提供关机界面显示和电源操作能力。

详见 [org.deepin.dde.ShutdownFront1.md](references/dbus/org.deepin.dde.ShutdownFront1.md)

## DConfig 配置项

### 资源: `org.deepin.dde.daemon.accounts`

| Key | Name | 类型 | Permissions |
|---|---|---|---|
| `enableQuickLogin` | 是否启用快速登录 | bool | readwrite |

```bash
# 查询
dde-dconfig -a org.deepin.dde.lightdm-deepin-greeter -r org.deepin.dde.daemon.accounts -k enableQuickLogin --get
# 设置
dde-dconfig -a org.deepin.dde.lightdm-deepin-greeter -r org.deepin.dde.daemon.accounts -k enableQuickLogin -s "<value>"
```

