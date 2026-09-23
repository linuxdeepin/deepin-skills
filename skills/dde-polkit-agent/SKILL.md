---
name: dde-polkit-agent
description: 提供 polkit 认证代理窗口 ID 设置接口
Categories:
  - Application
---

# dde-polkit-agent

dde-polkit-agent 是 DDE 的 polkit 认证代理组件，通过 Session 总线提供 polkit 认证代理窗口 ID 设置能力。

## D-Bus 接口

### 认证代理

提供 polkit 认证代理窗口 ID 设置能力。

详见 [org.deepin.dde.Polkit1.AuthAgent.md](references/dbus/org.deepin.dde.Polkit1.AuthAgent.md)

## CLI 命令

### dde-polkit-agent

DDE 的 PolicyKit 认证代理，负责在用户执行需要特权的操作时弹出认证对话框。

详见 [dde-polkit-agent.md](references/cli/dde-polkit-agent.md)

