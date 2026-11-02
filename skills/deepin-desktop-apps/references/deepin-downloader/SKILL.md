---
name: deepin-downloader
description: 提供下载器中的 URL 下载任务创建、torrent 或 metalink 文件打开和窗口显示接口，支持下载器应用能力
Categories:
  - Application
---

# 下载器

提供 URL 下载任务、种子或 metalink 文件打开和下载器窗口控制接口；相较通用 URL 下载命令，额外提供 torrent、metalink 和下载器应用窗口能力。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：`download` 只创建下载任务并返回请求结果，不代表文件已经下载完成；完成状态须另行查询或确认。
- 需呼出界面并人工操作：`open-file` 后若界面要求确认或选择任务，由用户完成；下载完成也需要另行查询或由用户在界面确认。
- 需先启动应用后 D-Bus 才存在：服务前置：需要 `com.downloader.service` 先注册；不要求 Agent 人工打开下载器界面，deepin-tools 可尝试启动 `downloader`。
- 调用 D-Bus 直接呼出界面：`open-file` 打开 torrent/metalink 文件并进入下载器界面，`raise` 显示下载器窗口。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.downloader.service`
- Object path：`/downloader/path`
- Interface：`local.downloader.MainFrame`

### download

从 URL 创建下载任务


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `url`（string）：示例值 `https://example.com/example.iso`

接口：
- Method：`onReceiveExtentionUrl`

用例：
```bash
dbus-send --session --print-reply --dest=com.downloader.service /downloader/path local.downloader.MainFrame.onReceiveExtentionUrl string:https://example.com/example.iso
```

### open-file

打开 torrent 或 metalink 文件


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `path`（string）：示例值 `$HOME/Downloads/example.torrent`

接口：
- Method：`OpenFile`

用例：
```bash
dbus-send --session --print-reply --dest=com.downloader.service /downloader/path local.downloader.MainFrame.OpenFile string:$HOME/Downloads/example.torrent
```

### raise

显示下载器窗口


执行说明：
- 分类：调用 D-Bus 直接呼出界面；接口返回不代表用户已完成窗口内操作。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`Raise`

用例：
```bash
dbus-send --session --print-reply --dest=com.downloader.service /downloader/path local.downloader.MainFrame.Raise
```
