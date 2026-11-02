---
name: deepin-voice-note
description: 提供语音笔记列表查询和基于已有笔记 ID 的语音录制接口
Categories:
  - Application
---

# 语音笔记

提供语音笔记列表查询和语音录制接口。录制需要已有的 `folderId` 和 `noteId`，当前源接口不提供笔记创建能力。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：`list` 返回笔记列表。
- 需呼出界面并人工操作：`record` 发起录音后，用户必须结束录音并确认保存；调用前必须已有有效的 `folderId` 和 `noteId`。
- 需先启动应用后 D-Bus 才存在：服务前置：需要 `org.deepin.voicenote` 先注册；不要求 Agent 人工打开语音笔记界面，deepin-tools 可尝试启动语音笔记应用。
- 调用 D-Bus 直接呼出界面：`record` 调用 `RecordVoice` 后启动指定笔记的录音流程；`list` 不打开界面。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`org.deepin.voicenote`
- Object path：`/org/deepin/voicenote`
- Interface：`org.deepin.voicenote`

### list

获取所有语音笔记列表


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`GetNotesList`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.voicenote /org/deepin/voicenote org.deepin.voicenote.GetNotesList
```

### record

录制语音到指定笔记


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `folderId`（string）：示例值 `folder-1`
- `noteId`（string）：示例值 `note-1`

接口：
- Method：`RecordVoice`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.voicenote /org/deepin/voicenote org.deepin.voicenote.RecordVoice string:folder-1 string:note-1
```

风险警示：
- 会访问麦克风并生成语音数据；执行前必须确认麦克风权限和录音范围。
