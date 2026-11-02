---
name: deepin-terminal
description: 提供在终端应用窗口中执行命令，以及设置该终端的字体、透明度、光标、颜色主题和 Shell 的接口
Categories:
  - Application
---

# 终端模拟器

提供在终端应用窗口中执行命令，以及设置该终端的字体、透明度、光标、颜色主题和 Shell 的接口；不提供系统级命令任务管理能力。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：字体、透明度、光标、颜色主题和 Shell 的读取/写入在调用返回后完成；`execute` 仅表示命令已提交到新终端。
- 需呼出界面并人工操作：`execute` 中的命令若等待输入、确认或持续运行，需要用户在终端中交互或由 Agent 继续检查；命令启动不代表命令完成。
- 需先启动应用后 D-Bus 才存在：服务前置：不要求 Agent 预先打开终端界面；CLI `deepin-terminal -e` 会直接启动终端。使用 D-Bus 设置或回退执行路径时需 `com.deepin.terminal.reborn` 已注册，deepin-tools 会尝试确保服务可用。
- 调用 D-Bus 直接呼出界面：D-Bus `execute` 的 `entry` 在终端窗口执行命令；CLI `deepin-terminal -e` 也会直接打开终端窗口。

## CLI 命令

### execute

在新终端执行命令。源 wrapper 优先使用 CLI；当 `deepin-terminal` CLI 不存在时，回退到 D-Bus `entry` 方法。

执行说明：
- 分类：需呼出界面并人工操作；CLI 或 D-Bus fallback 只提交命令，不代表任务已完成。
- 前置：优先确保 `deepin-terminal` CLI 和当前桌面会话可用；回退路径需确认 `com.deepin.terminal.reborn` 已注册。

参数：
- `command`（string）：示例值 `echo hello`

用例：
```bash
deepin-terminal -e 'echo hello'
```

D-Bus fallback：
- Bus：`session`
- Service：`com.deepin.terminal.reborn`
- Object path：`/window`
- Interface：`com.deepin.terminal.reborn`
- Method：`entry`

```bash
dbus-send --session --print-reply \
  --dest=com.deepin.terminal.reborn \
  /window com.deepin.terminal.reborn.entry \
  array:string:-e,echo,hello
```

风险警示：
- 会启动终端执行任意命令，命令可修改或删除用户数据及系统配置；执行前必须确认命令内容。


## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.terminal.reborn`
- Object path：`/window`
- Interface：`com.deepin.terminal.reborn`

### get-font-size

读取终端字体大小。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`consoleFontSize`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.consoleFontSize
```

### set-font-size

设置终端字体大小。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（int32）：设置值，示例值 `14`

接口：
- Method：`setConsoleFontSize`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.setConsoleFontSize int32:14
```

### get-font-family

读取终端字体名称。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`consoleFontFamily`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.consoleFontFamily
```

### set-font-family

设置终端字体名称。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（string）：设置值，示例值 `Noto Sans CJK SC`

接口：
- Method：`setConsoleFontFamily`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.setConsoleFontFamily 'string:Noto Sans CJK SC'
```

### get-opacity

读取终端透明度。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`consoleOpacity`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.consoleOpacity
```

### set-opacity

设置终端透明度。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（int32）：设置值，示例值 `80`

接口：
- Method：`setConsoleOpacity`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.setConsoleOpacity int32:80
```

### get-cursor-shape

读取终端光标样式。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`consoleCursorShape`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.consoleCursorShape
```

### set-cursor-shape

设置终端光标样式。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（int32）：设置值，示例值 `0`

接口：
- Method：`setConsoleCursorShape`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.setConsoleCursorShape int32:0
```

### get-cursor-blink

读取终端光标闪烁状态。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`consoleCursorBlink`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.consoleCursorBlink
```

### set-cursor-blink

设置终端光标闪烁状态。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（boolean）：设置值，示例值 `true`

接口：
- Method：`setConsoleCursorBlink`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.setConsoleCursorBlink boolean:true
```

### get-color-scheme

读取终端颜色主题。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`consoleColorScheme`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.consoleColorScheme
```

### set-color-scheme

设置终端颜色主题。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（string）：设置值，示例值 `dark`

接口：
- Method：`setConsoleColorScheme`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.setConsoleColorScheme string:dark
```

### get-shell

读取终端 Shell 路径。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`consoleShell`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.consoleShell
```

### set-shell

设置终端 Shell 路径。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（string）：设置值，示例值 `/bin/bash`

接口：
- Method：`setConsoleShell`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.terminal.reborn /window com.deepin.terminal.reborn.setConsoleShell string:/bin/bash
```

