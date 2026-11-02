---
name: deepin-screen-recorder
description: 提供截图录屏工具中的可脚本截图、录屏、OCR、滚动截图和对应 CLI 接口，并标明人工交互边界
Categories:
  - Application
---

# 截图录屏

提供本机桌面上的截图、录屏、OCR 和滚动截图接口；不负责沙箱应用通过桌面门户发起的截图请求

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：`fullscreen`、`window`、`delay`、`cli-fullscreen`、`cli-window`、`cli-save-path` 发起截图请求后返回；`record`/`cli-record`、`save`、`ocr`、`scroll`、`cli-ocr`、`cli-scroll` 不表示文件或文本结果已经产生。
- 需呼出界面并人工操作：`interactive` 需要用户框选；`save` 可能弹出保存对话框并需要确认；`ocr`/`cli-ocr` 需要在界面查看识别结果；`scroll`/`cli-scroll` 需要用户框选并手动滚动；`record`/`cli-record` 启动持续录制，必须由用户停止或等待录制流程结束。
- 需先启动应用后 D-Bus 才存在：不要求人工先打开截图主窗口；裸 D-Bus action 前需 `com.deepin.Screenshot` 服务已注册。CLI action 直接运行命令，不依赖该 D-Bus 服务。
- 调用 D-Bus 直接呼出界面：`interactive` 启动选区交互，`scroll` 启动滚动截图交互；其他 D-Bus action 只发起捕获/录制，不保证显示主窗口。

能力矩阵：

| action | 入口 | 是否需人工 | 返回语义 |
|---|---|---:|---|
| `fullscreen`、`window`、`delay` | D-Bus | 否 | 发起截图请求，不承诺文件路径 |
| `cli-save-path` | CLI | 否 | 与截图模式（如 `-f`）组合使用 `-s/--save-path`；检查指定目标文件是否实际生成 |
| `save` | D-Bus | 是 | 只发起保存流程；返回不代表目标文件已落盘 |
| `interactive`、`scroll` | D-Bus | 是 | 启动选区或滚动交互，不返回截图内容 |
| `ocr` | D-Bus | 是 | 结果显示在 OCR 界面，不通过 D-Bus 返回文本，也不写剪贴板 |
| `cli-ocr`、`cli-scroll` | CLI | 是 | 分别等价于 `ocr`、`scroll`，不返回文本或文件结果 |
| `record` | D-Bus/CLI | 是 | 启动持续录制，停止和文件校验需另行完成 |

`SavePathScreenshot` 成功判据是目标文件实际出现并可读取；若超时，只能报告“已发起保存流程，尚未确认落盘”。`ScrollScreenshot` 与 `--scroll` 语义等价，均需要用户操作。

## CLI 命令

本 Skill 面向本机桌面应用，截图、录屏和 OCR 会处理当前屏幕内容；沙箱应用的截图请求应使用对应桌面门户能力。调用前应确认捕获范围。

### cli-fullscreen

使用 CLI 执行全屏截图


执行说明：
- 分类：一步完成；命令返回后取得该接口结果或提交请求。
- 前置：不依赖 D-Bus；确保对应 CLI 和当前桌面会话可用。

参数：
- 无参数。

用例：
```bash
deepin-screen-recorder -f
```

### cli-save-path

使用 CLI 将全屏截图保存到指定路径。`-s/--save-path` 只指定保存路径，需与截图模式参数组合使用。

执行说明：
- 分类：一步完成；命令发起截图后，以指定路径文件实际出现且可读取作为完成判据。
- 前置：不依赖 D-Bus；确保 CLI 和当前桌面会话可用。

参数：
- `path`（string）：目标文件路径，示例值 `$HOME/Pictures/screenshot.png`

用例：
```bash
deepin-screen-recorder -f -s $HOME/Pictures/screenshot.png
```

### cli-window

使用 CLI 执行窗口截图


执行说明：
- 分类：一步完成；命令返回后取得该接口结果或提交请求。
- 前置：不依赖 D-Bus；确保对应 CLI 和当前桌面会话可用。

参数：
- 无参数。

用例：
```bash
deepin-screen-recorder -w
```

### cli-ocr

使用 CLI 执行 OCR 截图


执行说明：
- 分类：需呼出界面并人工操作；CLI 只提交 GUI 或持续任务，不代表任务已完成。
- 前置：不依赖 D-Bus；确保对应 CLI 和当前桌面会话可用。

参数：
- 无参数。

用例：
```bash
deepin-screen-recorder --ocr
```

### cli-record

使用 CLI 执行录屏


执行说明：
- 分类：需呼出界面并人工操作；CLI 只提交 GUI 或持续任务，不代表任务已完成。
- 前置：不依赖 D-Bus；确保对应 CLI 和当前桌面会话可用。

参数：
- 无参数。

用例：
```bash
deepin-screen-recorder --record
```

风险警示：
- 会持续录制全屏内容并写入文件；录制内容包含屏幕信息，执行前必须确认录制范围和保存位置。

### cli-scroll

使用 CLI 执行滚动截图；需要用户框选并手动滚动，方法不返回截图内容。


执行说明：
- 分类：需呼出界面并人工操作；CLI 只提交 GUI 或持续任务，不代表任务已完成。
- 前置：不依赖 D-Bus；确保对应 CLI 和当前桌面会话可用。

参数：
- 无参数。

用例：
```bash
deepin-screen-recorder --scroll
```


## D-Bus 接口

本 Skill 面向本机桌面应用，截图、录屏和 OCR 会处理当前屏幕内容；沙箱应用的截图请求应使用对应桌面门户能力。调用前应确认捕获范围。
接口信息：
- Bus：`session`
- Service：`com.deepin.Screenshot`
- Object path：`/com/deepin/Screenshot`
- Interface：`com.deepin.Screenshot`

### fullscreen

执行全屏截图


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`FullscreenScreenshot`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Screenshot /com/deepin/Screenshot com.deepin.Screenshot.FullscreenScreenshot
```

### window

执行窗口截图


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`TopWindowScreenshot`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Screenshot /com/deepin/Screenshot com.deepin.Screenshot.TopWindowScreenshot
```

### delay

延时执行截图


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `seconds`（int64）：示例值 `3`

接口：
- Method：`DelayScreenshot`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Screenshot /com/deepin/Screenshot com.deepin.Screenshot.DelayScreenshot int64:3
```

### interactive

启动交互式选区截图


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`StartScreenshot`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Screenshot /com/deepin/Screenshot com.deepin.Screenshot.StartScreenshot
```

### save

按指定路径截图


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 结果语义：只发起保存或滚动流程，需按条目说明等待人工操作和结果确认。

参数：
- `path`（string）：示例值 `$HOME/Pictures/screenshot.png`

接口：
- Method：`SavePathScreenshot`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Screenshot /com/deepin/Screenshot com.deepin.Screenshot.SavePathScreenshot string:$HOME/Pictures/screenshot.png
```

### record

录制全屏并保存到指定路径


执行说明：
- 分类：需呼出界面并人工操作；调用返回只表示请求已提交。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `path`（string）：示例值 `$HOME/Videos/screen-record.mp4`

接口：
- Method：`FullScreenRecord`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Screenshot /com/deepin/Screenshot com.deepin.Screenshot.FullScreenRecord string:$HOME/Videos/screen-record.mp4
```

风险警示：
- 会持续录制全屏内容并写入文件；录制内容包含屏幕信息，执行前必须确认录制范围和保存位置。

### ocr

执行截图 OCR；该方法只启动 OCR 界面，识别文本不作为 D-Bus 返回值，也不写入剪贴板。


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 结果语义：识别文本显示在界面中，不通过接口返回，也不写入剪贴板。

参数：
- 无参数。

接口：
- Method：`OcrScreenshot`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Screenshot /com/deepin/Screenshot com.deepin.Screenshot.OcrScreenshot
```

### scroll

执行滚动截图


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 结果语义：只发起保存或滚动流程，需按条目说明等待人工操作和结果确认。

参数：
- 无参数。

接口：
- Method：`ScrollScreenshot`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Screenshot /com/deepin/Screenshot com.deepin.Screenshot.ScrollScreenshot
```
