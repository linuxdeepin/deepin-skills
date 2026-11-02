---
name: deepin-compressor
description: 提供压缩工具中的文件压缩、压缩包解压、内容查询、完整性测试和窗口控制接口，支持应用级格式识别和图形窗口控制
Categories:
  - Application
---

# 压缩工具

提供压缩工具窗口控制和压缩包处理入口。当前 CLI `compress`、`extract`、`list`、`test` 会启动 GUI 流程，标准输出不返回压缩包内容，可能阻塞等待用户确认；窗口控制 D-Bus action 可脚本调用。CLI `extract` 的目标目录参数不保证被 GUI 采用，必须在界面中确认实际目标目录。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：D-Bus `hide`/`quit` 在调用返回后完成窗口状态变化；CLI `compress`、`extract`、`list`、`test` 只提交 GUI 流程，不表示内容处理完成。
- 需呼出界面并人工操作：CLI `compress`、`extract`、`list`、`test` 会进入 GUI，需用户在窗口中确认或继续操作；`show`/`raise` 只控制窗口。
- 需先启动应用后 D-Bus 才存在：服务前置：需要 `com.deepin.Compressor` 先注册；不要求 Agent 人工打开压缩工具界面，但 CLI 内容操作进入 GUI 后必须由用户继续确认。
- 调用 D-Bus 直接呼出界面：`show` 显示窗口，`raise` 将窗口置前。

能力矩阵：

| action | 是否可脚本判定完成 | 说明 |
|---|---:|---|
| `show`、`raise`、`hide`、`quit` | 是 | D-Bus 窗口控制，返回表示请求完成 |
| `compress`、`list`、`test` | 否 | CLI 只启动 GUI，可能阻塞，stdout 不提供内容结果，需人工确认 |
| `extract` | 否 | CLI 只启动 GUI；目标目录参数可能不生效，必须人工确认实际目录并检查文件落盘 |

需要脚本化读取或校验压缩包时，应使用系统工具（如 `zipfile` 或 `zipinfo`）；这不属于本 Skill 的能力。

## CLI 命令

### compress

压缩一个或多个文件


执行说明：
- 分类：需呼出界面并人工操作；CLI 只提交 GUI 或持续任务，不代表任务已完成。
- 前置：不依赖 D-Bus；确保对应 CLI 和当前桌面会话可用。

参数：
- `file1`（path）：示例值 `$HOME/Documents/report.txt`
- `file2...`（path）（可选）：示例值 `$HOME/Documents/data.csv`

用例：
```bash
deepin-compressor $HOME/Documents/report.txt compress
```

### extract

将压缩包解压到目标目录


执行说明：
- 分类：需呼出界面并人工操作；CLI 只提交 GUI 或持续任务，不代表任务已完成。
- 前置：不依赖 D-Bus；确保对应 CLI 和当前桌面会话可用。
- 完成判据：用户在 GUI 中确认目标目录，解压后必须检查目标目录实际生成的文件；若落到默认目录而非请求目录，应判为目标路径失败。

参数：
- `archive`（path）：示例值 `$HOME/Downloads/archive.zip`
- `dest`（path）（可选）：示例值 `$HOME/Downloads/extracted`

用例：
```bash
deepin-compressor $HOME/Downloads/archive.zip $HOME/Downloads/extracted
```

风险警示：
- 会向目标目录写入文件，目标目录中的同名文件会被覆盖；执行前必须确认目标路径。

### list

列出压缩包内容


执行说明：
- 分类：需呼出界面并人工操作；CLI 只提交 GUI 或持续任务，不代表任务已完成。
- 前置：不依赖 D-Bus；确保对应 CLI 和当前桌面会话可用。

参数：
- `archive`（path）：示例值 `$HOME/Downloads/archive.zip`

用例：
```bash
deepin-compressor $HOME/Downloads/archive.zip list
```

### test

测试压缩包完整性


执行说明：
- 分类：需呼出界面并人工操作；CLI 只提交 GUI 或持续任务，不代表任务已完成。
- 前置：不依赖 D-Bus；确保对应 CLI 和当前桌面会话可用。

参数：
- `archive`（path）：示例值 `$HOME/Downloads/archive.zip`

用例：
```bash
deepin-compressor $HOME/Downloads/archive.zip test
```


## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.Compressor`
- Object path：`/com/deepin/Compressor`
- Interface：`com.deepin.Compressor`

### show

显示压缩工具窗口


执行说明：
- 分类：调用 D-Bus 直接呼出界面；接口返回不代表用户已完成窗口内操作。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`showWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Compressor /com/deepin/Compressor com.deepin.Compressor.showWindow
```

### hide

隐藏压缩工具窗口


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`hideWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Compressor /com/deepin/Compressor com.deepin.Compressor.hideWindow
```

### raise

将窗口置于前台


执行说明：
- 分类：调用 D-Bus 直接呼出界面；接口返回不代表用户已完成窗口内操作。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`raiseWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Compressor /com/deepin/Compressor com.deepin.Compressor.raiseWindow
```

### quit

退出压缩工具


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`quitWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Compressor /com/deepin/Compressor com.deepin.Compressor.quitWindow
```
