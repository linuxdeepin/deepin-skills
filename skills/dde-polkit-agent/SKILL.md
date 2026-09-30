---
name: dde-polkit-agent
description: dde-polkit-agent 是 DDE 的 PolicyKit 认证代理组件，负责在用户执行需要特权的操作时弹出图形认证对话框，收集用户密码或指纹认证信息。本 skill 提供 polkit 认证代理窗口 ID 设置能力及认证代理守护进程的启动方式说明。
Categories:
  - Settings
---

# dde-polkit-agent

dde-polkit-agent 是 DDE 的 PolicyKit 认证代理守护进程，负责在用户执行需要特权的操作时弹出图形认证对话框，收集用户密码或指纹认证信息，是 DDE 权限管理的前端组件。该程序在用户会话启动时由 systemd 用户服务 `dde-polkit-agent.service` 自动启动，需要图形显示环境（X11/Wayland）。

本 skill 提供以下内容：

- **CLI 命令**（仅作用于 dde-polkit-agent 自身）：`dde-polkit-agent` 守护进程二进制的基本信息和启动方式说明
- **D-Bus 接口**（仅作用于 dde-polkit-agent 自身认证窗口）：polkit 认证代理窗口 ID 设置接口

## CLI 命令

### dde-polkit-agent

DDE 的 PolicyKit 认证代理守护进程二进制，由 systemd 用户服务 `dde-polkit-agent.service` 在会话启动时自动启动，通常无需手动运行。

详见 [dde-polkit-agent.md](references/cli/dde-polkit-agent.md)

## D-Bus 接口

### 认证代理

dde-polkit-agent 在 Session 总线上注册 D-Bus 服务 `org.deepin.dde.Polkit1.AuthAgent`（对象路径 `/com/deepin/dde/Polkit1/AuthAgent`），提供 polkit 认证代理窗口 ID 设置能力，供外部应用调用以关联认证窗口（仅作用于 dde-polkit-agent 自身认证窗口）。

详见 [org.deepin.dde.Polkit1.AuthAgent.md](references/dbus/org.deepin.dde.Polkit1.AuthAgent.md)
