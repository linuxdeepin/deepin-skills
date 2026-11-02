---
name: deepin-editor
description: 提供文本编辑器中的文件标签页打开和新窗口打开接口
Categories:
  - Application
---

# 文本编辑器

提供文本文件标签页打开和新窗口打开接口

`openFilesInTab` 复用编辑器实例并在标签页中打开；`openFilesInWindow` 请求新窗口。文件路径必须在当前玲珑应用会话可见，服务检查必须在目标图形用户会话总线上完成。

## 前置条件：启动玲珑应用

- 先用 `ll-cli list` 检查 `org.deepin.editor` 是否已安装。
- 已安装但服务未注册时，在当前图形用户会话中执行 `ll-cli run org.deepin.editor`。
- 使用 `busctl --user list` 或等价的会话总线检查确认 `com.deepin.Editor` 已注册后再调用接口。
- `ServiceUnknown` 只表示服务当前未注册或应用未运行，不表示应用未安装；不能用 `dpkg`、`which` 或桌面文件是否存在判断玲珑应用是否安装。
- 服务启动超时或应用未安装时应如实报告，不反复重试或改用无关 GUI 操作。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：无；`open`/`open-window` 只提交文件打开请求。
- 需呼出界面并人工操作：`open`/`open-window` 后，用户需要在编辑器中编辑并按需保存。
- 需先启动应用后 D-Bus 才存在：服务前置：需要 `com.deepin.Editor` 先注册；不要求 Agent 人工打开编辑器界面，必须先按前置条件启动玲珑应用。
- 调用 D-Bus 直接呼出界面：`open` 在标签页打开文件，`open-window` 在新窗口打开文件。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.Editor`
- Object path：`/com/deepin/Editor`
- Interface：`com.deepin.Editor`

### open

在标签页打开文本文件


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `files`（array of string）：示例值 `$HOME/Documents/example.txt,$HOME/Documents/second.txt`

接口：
- Method：`openFilesInTab`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Editor /com/deepin/Editor com.deepin.Editor.openFilesInTab array:string:$HOME/Documents/example.txt,$HOME/Documents/second.txt
```

### open-window

在新窗口打开文本文件


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `files`（array of string）：示例值 `$HOME/Documents/example.txt`

接口：
- Method：`openFilesInWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Editor /com/deepin/Editor com.deepin.Editor.openFilesInWindow array:string:$HOME/Documents/example.txt
```
