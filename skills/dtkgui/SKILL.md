---
name: dtkgui
description: 提供文件拖拽服务接口，使用动态 baseService 在运行时确定 D-Bus 服务名
Categories:
  - Develop
---

# dtkgui

dtkgui 是 DTK GUI 组件库，通过 Session 总线提供文件拖拽服务接口。该接口使用动态 baseService，D-Bus 服务名在运行时由 `QDBusConnection::sessionBus().baseService()` 确定（如 `:1.23`），无法静态指定固定服务名。

## D-Bus 接口

### 文件拖拽服务

提供文件拖拽 URI 列表查询、进程 ID 查询、状态查询和拖拽控制能力。

详见 [org.deepin.dtk.DFileDragServer.md](references/dbus/org.deepin.dtk.DFileDragServer.md)

