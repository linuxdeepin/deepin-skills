# Portal 能力边界

Portal 为应用提供文件选择、截图、屏幕共享和壁纸等受授权约束的能力。应用经 `org.freedesktop.portal.Desktop` 前端调用；DDE 的 `org.freedesktop.impl.portal.*` 是前后端协作协议，不应作为直接配置桌面的操作入口，也不能绕过前端授权。

本 Skill 的桌面外观设置使用 [外观接口](../dde-appearance/index.md)，桌面通知使用 [通知接口](../dde-shell/index.md)。Portal Settings 是只读偏好查询；Lockdown 描述门户策略，不能据此宣称已在全系统禁用设备。平台能力以目标会话和部署版本为准。

Portal 应用集成及后端协议开发资料另行整理，本索引不提供后端调用示例。
