---
name: dde-polkit-agent
description: DDE 的 PolicyKit 图形认证代理，处理服务发起的授权交互，并提供 AgentExtension 扩展接口供第三方开发认证插件。用于认证代理运行说明和插件集成；历史窗口关联方法不作为可用能力。
Categories:
  - Settings
  - Develop
---

# dde-polkit-agent

dde-polkit-agent 是 DDE 的 PolicyKit 认证代理守护进程，负责在用户执行需要特权的操作时弹出图形认证对话框，收集用户密码或指纹认证信息，是 DDE 权限管理的前端组件。该程序在用户会话启动时由 systemd 用户服务 `dde-polkit-agent.service` 自动启动，需要图形显示环境（X11/Wayland）。

本 skill 提供以下内容：

- **服务运行说明**（仅作用于 dde-polkit-agent 自身）：`dde-polkit-agent` 守护进程二进制的基本信息和启动方式说明
- **开发接口**：认证代理扩展插件接口及集成方式

认证代理由当前用户会话服务启动，普通授权请求由需要权限的服务发起。服务启动说明见 [dde-polkit-agent.md](references/cli/dde-polkit-agent.md)；历史窗口关联协议的限制见 [AuthAgent 说明](references/dbus/org.deepin.dde.Polkit1.AuthAgent.md)。

## 开发接口

dde-polkit-agent 是 DDE 桌面环境的 Polkit 认证代理，为需要提权的操作提供图形化认证对话框。项目通过安装公开头文件，允许第三方继承扩展接口并编译为共享库插件，由认证代理在运行时加载，从而自定义认证行为。

### 认证代理扩展接口

C++ 接口参考文档，包含 AgentExtension 和 AgentExtensionProxy 两个公开抽象接口的定位、功能能力和使用场景，以及扩展插件的集成与构建方式。

详见 [agent-extension.md](references/interface/agent-extension.md)
