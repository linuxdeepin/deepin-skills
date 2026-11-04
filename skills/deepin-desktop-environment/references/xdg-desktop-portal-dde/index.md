# Portal 能力边界

Portal 为应用提供文件选择、截图、屏幕共享和壁纸等受授权约束的能力。应用经 `org.freedesktop.portal.Desktop` 前端调用；DDE 的 `org.freedesktop.impl.portal.*` 是前后端协作协议，不应作为直接配置桌面的操作入口，也不能绕过前端授权。

本 Skill 的桌面外观设置使用 dde-appearance 的 `org.deepin.dde.Appearance1` 接口，桌面通知使用 dde-shell 的 `org.deepin.dde.Notification1` 接口。Portal Settings 是只读偏好查询；Lockdown 描述门户策略，不能据此宣称已在全系统禁用设备。平台能力以目标会话和部署版本为准。

## D-Bus 接口

前端 `Account`、`Background`、`Notification` 分别涉及用户信息请求、后台运行能力和门户通知，先确认部署是否提供。`Settings` 提供外观命名空间枚举与配色方案读取；`GlobalShortcuts` 是否可用以当前前端暴露的接口为准。服务、对象路径、方法签名和调用示例见 [Portal 前端接口](dbus/org.freedesktop.portal.Desktop.md)。通用服务探测遵循 Skill 入口的状态来源约束。

Portal 应用集成及后端协议开发不在本页范围内。
