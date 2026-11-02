---
name: deepin-picker
description: 提供本机应用使用的屏幕取色器启动接口；当前源接口仅提供启动方法，不提供取色结果读取接口，也不负责沙箱应用的门户取色
Categories:
  - Application
---

# 屏幕取色器

提供本机应用使用的屏幕取色器启动接口。当前源接口仅提供启动方法，不提供取色结果读取接口，也不负责沙箱应用的门户取色。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：无；`pick` 只提交启动取色请求，不返回颜色值。
- 需呼出界面并人工操作：`pick` 启动后，用户必须在屏幕上点击取色；颜色结果通过信号返回调用方。
- 需先启动应用后 D-Bus 才存在：服务前置：需要取色器服务先注册；源封装不负责自动启动，Agent 必须先启动或确保取色器服务可用。
- 调用 D-Bus 直接呼出界面：`pick` 调用 `StartPick` 后直接启动取色交互界面。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.Picker`
- Object path：`/com/deepin/Picker`
- Interface：`com.deepin.Picker`

### pick

启动屏幕取色器


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `appName`（string）（可选）：示例值 `deepin-tools`

接口：
- Method：`StartPick`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Picker /com/deepin/Picker com.deepin.Picker.StartPick string:deepin-tools
```
