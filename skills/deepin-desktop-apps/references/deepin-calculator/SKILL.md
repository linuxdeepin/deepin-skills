---
name: deepin-calculator
description: 提供计算器窗口控制、当前模式查询和标准、科学、程序员模式切换接口
Categories:
  - Application
---

# 计算器

提供计算器窗口控制和计算模式切换接口

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：`get-current-mode`、`switch-to-standard-mode`、`switch-to-scientific-mode`、`switch-to-programmer-mode`、`hide-window`、`quit-window` 在调用返回后完成对应状态变化或返回结果。
- 需呼出界面并人工操作：`show-window`/`raise-window` 后，如果目标是进行计算，用户必须在计算器窗口输入表达式并查看结果；本 Skill 不提供表达式输入或结果读取 action。
- 需先启动应用后 D-Bus 才存在：服务可通过 session D-Bus 激活文件启动 `deepin-calculator`，不要求 Agent 预先人工打开计算器；应用启动时会注册 `com.deepin.Calculator`，deepin-tools 的通用调用也会尝试启动应用。若应用启动失败，D-Bus 调用会失败。
- 调用 D-Bus 直接呼出界面：`show-window` 调用 `showWindow` 显示并激活计算器窗口；`raise-window` 调用 `raiseWindow` 显示、置前并激活窗口。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.Calculator`
- Object path：`/`
- Interface：`com.deepin.Calculator`

### show-window

显示计算器窗口


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`showWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calculator / com.deepin.Calculator.showWindow
```

### hide-window

隐藏计算器窗口


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`hideWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calculator / com.deepin.Calculator.hideWindow
```

### raise-window

将计算器窗口置于前台


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`raiseWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calculator / com.deepin.Calculator.raiseWindow
```

### quit-window

退出计算器


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`quitWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calculator / com.deepin.Calculator.quitWindow
```

### get-current-mode

获取当前计算模式


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`getCurrentMode`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calculator / com.deepin.Calculator.getCurrentMode
```

### switch-to-standard-mode

切换到标准模式


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`switchToStandardMode`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calculator / com.deepin.Calculator.switchToStandardMode
```

### switch-to-scientific-mode

切换到科学计算模式


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`switchToScientificMode`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calculator / com.deepin.Calculator.switchToScientificMode
```

### switch-to-programmer-mode

切换到程序员模式


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`switchToProgrammerMode`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calculator / com.deepin.Calculator.switchToProgrammerMode
```
