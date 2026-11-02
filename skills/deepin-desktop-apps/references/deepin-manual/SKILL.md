---
name: deepin-manual
description: 提供应用帮助手册的打开、显示、实验性搜索和存在性查询接口
Categories:
  - Application
---

# 帮助手册

提供应用帮助手册打开、显示、实验性搜索和存在性查询接口。搜索接口当前不返回搜索文本。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：`exists` 返回存在性结果；`search` 只提交搜索请求且当前部署不返回搜索文本；`open`/`show` 只提交打开或显示手册请求。
- 需呼出界面并人工操作：`open`/`show` 后，用户需要在手册窗口阅读内容。
- 需先启动应用后 D-Bus 才存在：先用 `ll-cli list` 检查 `org.deepin.manual`，必要时在当前图形会话执行 `ll-cli run org.deepin.manual`，等待 `com.deepin.Manual.Open` 注册后再调用；不能把服务未注册判断为接口不存在。
- 调用 D-Bus 直接呼出界面：`open`/`show` 打开或显示帮助手册窗口。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.Manual.Open`
- Object path：`/com/deepin/Manual/Open`
- Interface：`com.deepin.Manual.Open`

### open

打开或显示指定应用的帮助手册


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `appName`（string）：示例值 `deepin-music`

接口：
- Methods：`Open`（打开）、`ShowManual`（显示）

用例：Open
```bash
dbus-send --session --print-reply --dest=com.deepin.Manual.Open /com/deepin/Manual/Open com.deepin.Manual.Open.Open string:deepin-music
```

用例：ShowManual
```bash
dbus-send --session --print-reply --dest=com.deepin.Manual.Open /com/deepin/Manual/Open com.deepin.Manual.Open.ShowManual string:deepin-music
```

### search

提交帮助手册搜索请求；当前部署的 `Search` 方法只返回空 method return，不返回搜索结果。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `keyword`（string）：示例值 `network`

接口：
- Method：`Search`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Manual.Open /com/deepin/Manual/Open com.deepin.Manual.Open.Search string:network
```


说明：若任务必须获得文本结果，先说明 D-Bus 搜索接口无返回值，再按需检索由部署环境提供的本地手册资源目录 `${MANUAL_ASSETS_DIR}`；本地检索不属于该 D-Bus 方法的返回结果。


接口信息：
- Bus：`session`
- Service：`com.deepin.Manual.Search`
- Object path：`/com/deepin/Manual/Search`
- Interface：`com.deepin.Manual.Search`

### exists

检查应用帮助手册是否存在


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `appName`（string）：示例值 `deepin-music`

接口：
- Method：`ManualExists`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Manual.Search /com/deepin/Manual/Search com.deepin.Manual.Search.ManualExists string:deepin-music
```
