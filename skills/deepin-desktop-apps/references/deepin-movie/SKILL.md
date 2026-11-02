---
name: deepin-movie
description: 提供视频播放器中的视频文件和 URI 打开、MPRIS 播放控制、播放位置、音量、播放速率、状态、元数据和窗口控制接口
Categories:
  - Application
---

# 视频播放器

提供视频文件、视频 URI、MPRIS 播放控制、播放状态和窗口控制接口。播放控制仅作用于视频播放器，不控制系统音量。

沙箱边界：`open-uri` 支持范围取决于 URI scheme、沙箱可见路径和 MIME 类型。主机路径的 `file://` URI 可能返回 `NotSupported`；优先使用 `openFile`，或传入应用沙箱内可见的 URI。

## 前置条件：启动玲珑应用

- 先用 `ll-cli list` 检查 `org.deepin.movie` 是否已安装。
- 已安装但服务未注册时，在当前图形用户会话中执行 `ll-cli run org.deepin.movie`。
- 使用 `busctl --user list` 或等价的会话总线检查确认 `org.mpris.MediaPlayer2.Deepinmovie` 已注册后再调用接口。
- `ServiceUnknown` 只表示服务当前未注册或应用未运行，不表示应用未安装；不能用 `dpkg`、`which` 或桌面文件是否存在判断玲珑应用是否安装。
- 服务启动超时或应用未安装时应如实报告，不反复重试或改用无关 GUI 操作。

## 跨应用编排

与视频播放器或截图工具组合调用时，按“检查服务注册→执行本应用 action→回读本应用状态→汇总”的顺序处理。某一应用未安装或未就绪时如实报告并继续独立可执行的部分，不无限重试。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：`play`、`pause`、`toggle`、`stop`、`next`、`prev`、`seek`、音量/速率设置及状态、元数据、位置读取在调用返回后完成或返回结果；`quit` 完成退出请求。
- 需呼出界面并人工操作：`open`、`open-files`、`open-uri` 后若目标是观看内容，用户需要在播放器窗口人工观看或检查；持续播放的结束不由调用返回表示。
- 需先启动应用后 D-Bus 才存在：服务前置：需要播放器服务先注册；不要求 Agent 人工打开播放器界面，必须先按前置条件启动玲珑应用。
- 调用 D-Bus 直接呼出界面：`open`、`open-files`、`open-uri` 打开媒体，`raise` 将播放器窗口置前。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.movie`
- Object path：`/`
- Interface：`com.deepin.movie`

### open

打开视频文件


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `path`（string）：示例值 `$HOME/Videos/example.mp4`

接口：
- Method：`openFile`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.movie / com.deepin.movie.openFile string:$HOME/Videos/example.mp4
```

### open-files

批量打开视频文件


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `paths`（array of string）：示例值 `$HOME/Videos/a.mp4,$HOME/Videos/b.mp4`

接口：
- Method：`openFiles`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.movie / com.deepin.movie.openFiles array:string:$HOME/Videos/a.mp4,$HOME/Videos/b.mp4
```

接口信息：
- Bus：`session`
- Service：`org.mpris.MediaPlayer2.Deepinmovie`
- Object path：`/org/mpris/MediaPlayer2`
- Interface：`org.mpris.MediaPlayer2.Player`

### open-uri

打开视频 URI。支持范围取决于沙箱可见路径和 MIME 类型；主机路径的 `file://` URI 可能返回 `NotSupported`，应优先使用 `openFile` 或沙箱内可见路径。


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `uri`（string）：示例值 `https://example.com/video.mp4`

接口：
- Method：`OpenUri`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.OpenUri string:https://example.com/video.mp4
```

### play

开始播放


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`Play`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play
```

### pause

暂停播放


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`Pause`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause
```

### toggle

切换播放和暂停


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`PlayPause`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause
```

### stop

停止播放


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`Stop`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Stop
```

### next

播放下一个


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`Next`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next
```

### prev

播放上一个


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`Previous`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous
```

### seek

按微秒调整播放位置；正数向前，负数向后。源 wrapper 的 `seek <seconds>` 会先把秒转换为微秒，直接调用 D-Bus 时必须传微秒。调用后必须回读 `Position` 和播放状态；若 `Seek` 返回成功但位置未变化、播放停止或元数据被清空，应报告应用接口异常。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `microseconds`（int64）：相对当前位置的偏移量，示例值 `10000000`（10 秒）。

接口：
- Method：`Seek`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Seek int64:10000000
```

接口信息：
- Bus：`session`
- Service：`org.mpris.MediaPlayer2.Deepinmovie`
- Object path：`/org/mpris/MediaPlayer2`
- Interface：`org.freedesktop.DBus.Properties`

### get-volume

读取当前音量。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`Get`

用例：
```bash
dbus-send --session --print-reply \
  --dest=org.mpris.MediaPlayer2.Deepinmovie \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Get \
  string:org.mpris.MediaPlayer2.Player \
  string:Volume
```

### set-volume

设置当前音量。该应用实现使用 `0` 到 `100` 的刻度，不要套用 MPRIS 常见的 `0.0` 到 `1.0` 刻度；设置后必须回读 `Volume`。Set 返回成功但回读值未变化时，应报告应用接口异常。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（double）：设置值，范围 `0` 到 `100`，示例值 `50.0`。

接口：
- Method：`Set`

用例：
```bash
dbus-send --session --print-reply \
  --dest=org.mpris.MediaPlayer2.Deepinmovie \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Set \
  string:org.mpris.MediaPlayer2.Player \
  string:Volume \
  variant:double:50.0
```

### get-rate

读取当前播放速率。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`Get`

用例：
```bash
dbus-send --session --print-reply \
  --dest=org.mpris.MediaPlayer2.Deepinmovie \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Get \
  string:org.mpris.MediaPlayer2.Player \
  string:Rate
```

### set-rate

设置当前播放速率。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（double）：设置值，示例值 `1.0`。

接口：
- Method：`Set`

用例：
```bash
dbus-send --session --print-reply \
  --dest=org.mpris.MediaPlayer2.Deepinmovie \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Set \
  string:org.mpris.MediaPlayer2.Player \
  string:Rate \
  variant:double:1.0
```

### status

读取播放状态


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `interface`（string）：示例值 `org.mpris.MediaPlayer2.Player`
- `property`（string）：示例值 `PlaybackStatus`

接口：
- Method：`Get`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:org.mpris.MediaPlayer2.Player string:PlaybackStatus
```

### metadata

读取当前视频元数据


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `interface`（string）：示例值 `org.mpris.MediaPlayer2.Player`
- `property`（string）：示例值 `Metadata`

接口：
- Method：`Get`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:org.mpris.MediaPlayer2.Player string:Metadata
```

### position

读取当前播放位置


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `interface`（string）：示例值 `org.mpris.MediaPlayer2.Player`
- `property`（string）：示例值 `Position`

接口：
- Method：`Get`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:org.mpris.MediaPlayer2.Player string:Position
```

接口信息：
- Bus：`session`
- Service：`org.mpris.MediaPlayer2.Deepinmovie`
- Object path：`/org/mpris/MediaPlayer2`
- Interface：`org.mpris.MediaPlayer2`

### raise

将播放器窗口置于前台


执行说明：
- 分类：调用 D-Bus 直接呼出界面；接口返回不代表用户已完成窗口内操作。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`Raise`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Raise
```

### quit

退出播放器


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`Quit`

用例：
```bash
dbus-send --session --print-reply --dest=org.mpris.MediaPlayer2.Deepinmovie /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Quit
```
