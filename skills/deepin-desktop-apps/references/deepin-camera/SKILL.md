---
name: deepin-camera
description: 提供相机应用中的拍照、录像控制、录像状态查询和窗口控制接口
Categories:
  - Application
---

# 相机

提供拍照、录像状态和相机窗口控制接口

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：`take-photo` 完成一次拍照，`stop-recording` 停止录像，`get-recording-status` 返回录像状态；`hide-window`/`quit-window` 完成对应窗口状态变化。
- 需呼出界面并人工操作：`start-recording` 只启动持续录像，不代表录制结束；必须后续调用 `stop-recording`，或由用户在界面停止并确认录制结果。
- 需先启动应用后 D-Bus 才存在：服务前置：需要 `com.deepin.Camera` 先注册；不要求 Agent 人工打开相机界面，deepin-tools 可尝试启动相机。
- 调用 D-Bus 直接呼出界面：`show-window` 显示相机窗口，`raise-window` 将窗口置前。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.Camera`
- Object path：`/com/deepin/camera`
- Interface：`com.deepin.Camera`

### take-photo

拍照


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`takePhoto`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Camera /com/deepin/camera com.deepin.Camera.takePhoto
```

风险警示：
- 会访问摄像头并生成照片；执行前必须确认摄像头权限和拍摄范围。

### start-recording

开始录像


执行说明：
- 分类：需呼出界面并人工操作；调用返回只表示请求已提交。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`startRecording`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Camera /com/deepin/camera com.deepin.Camera.startRecording
```

风险警示：
- 会访问摄像头并开始生成视频；执行前必须确认摄像头权限和录制范围。

### stop-recording

停止录像


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`stopRecording`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Camera /com/deepin/camera com.deepin.Camera.stopRecording
```

### get-recording-status

获取录像状态


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`getRecordingStatus`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Camera /com/deepin/camera com.deepin.Camera.getRecordingStatus
```

### show-window

显示相机窗口


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`showWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Camera /com/deepin/camera com.deepin.Camera.showWindow
```

### hide-window

隐藏相机窗口


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`hideWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Camera /com/deepin/camera com.deepin.Camera.hideWindow
```

### raise-window

将相机窗口置于前台


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`raiseWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Camera /com/deepin/camera com.deepin.Camera.raiseWindow
```

### quit-window

退出相机窗口


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`quitWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Camera /com/deepin/camera com.deepin.Camera.quitWindow
```
