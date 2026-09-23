---
name: deepin-pw-check
description: 提供用户认证、密码限制策略查询重置和一键登录的接口
Categories:
  - Settings
---

# deepin-pw-check

deepin-pw-check 是 DDE 的用户认证与密码安全策略组件，通过 System 总线提供用户认证、密码限制策略查询与重置、一键登录能力。该接口需要提权操作。

## D-Bus 接口

### 用户认证与密码限制

提供用户认证、密码限制策略查询与重置、一键登录能力。

详见 [org.deepin.dde.Authenticate1.md](references/dbus/org.deepin.dde.Authenticate1.md)
