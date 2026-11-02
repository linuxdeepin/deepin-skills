---
name: deepin-system-monitor
description: 提供系统监视器中的 CPU 占用率、内存占用率、进程资源占用、系统检查、告警触发、系统保护和窗口跳转接口
Categories:
  - Application
---

# 系统监视器

提供 CPU 占用率、内存占用率、进程资源占用、系统检查、告警触发、系统保护和监视器窗口接口；告警通知由系统监视器应用负责展示，不是通用通知服务接口。`getCpuUsage`/`getMemoryUsage` 属于常驻的 `SystemMonitorDaemon` 数据端点，不需要打开 GUI；`show`/`detail`/`process` 才需要 GUI 端点。不要用 `top` 或 `free` 替代这些 D-Bus 数据源。

采样说明：CPU 和内存值受采样周期影响，首次读取可能返回初始化值或 `0`；读取后应等待一个采样周期再回读。若 `getCpuUsage` 在完成采样后仍连续返回 `0`，应报告 CPU 接口数据不可用，不得用 `top`、`/proc/stat` 或其他旁路命令替代本接口结果。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：CPU、内存、进程查询，告警阈值/间隔/保护状态读写及 `cpu-notify`/`memory-notify` 请求在调用返回后完成或返回结果；通知显示不等于用户已查看。
- 需呼出界面并人工操作：`show`、`detail`、`process` 后，用户需要在系统监视器窗口查看或继续操作。
- 需先启动应用后 D-Bus 才存在：服务前置：数据/通知端点可独立调用；`show`/`detail`/`process` 的 GUI 端点调用前必须先注册。源工具未提供统一自动启动，若 GUI 端点未注册，Agent 需先启动系统监视器应用。
- 调用 D-Bus 直接呼出界面：`show` 显示窗口，`detail` 跳转详情页，`process` 跳转进程页；`cpu-notify`/`memory-notify` 只显示通知。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`org.deepin.SystemMonitorDaemon`
- Object path：`/org/deepin/SystemMonitorDaemon`
- Interface：`org.deepin.SystemMonitorDaemon`

### cpu

获取 CPU 占用率


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 结果校验：CPU 值应在等待采样后回读；连续恒为 `0` 时报告接口异常，不以旁路命令结果补齐。

参数：
- 无参数。

接口：
- Method：`getCpuUsage`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.SystemMonitorDaemon /org/deepin/SystemMonitorDaemon org.deepin.SystemMonitorDaemon.getCpuUsage
```

### memory

获取内存占用率


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`getMemoryUsage`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.SystemMonitorDaemon /org/deepin/SystemMonitorDaemon org.deepin.SystemMonitorDaemon.getMemoryUsage
```

### get-cpu-alarm

读取CPU 告警阈值。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`getAlarmUsageOfCpu`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.SystemMonitorDaemon /org/deepin/SystemMonitorDaemon org.deepin.SystemMonitorDaemon.getAlarmUsageOfCpu
```

### set-cpu-alarm

设置CPU 告警阈值。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（int32）：设置值，示例值 `80`

接口：
- Method：`setAlarmUsageOfCpu`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.SystemMonitorDaemon /org/deepin/SystemMonitorDaemon org.deepin.SystemMonitorDaemon.setAlarmUsageOfCpu int32:80
```

### get-memory-alarm

读取内存告警阈值。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`getAlarmUsageOfMemory`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.SystemMonitorDaemon /org/deepin/SystemMonitorDaemon org.deepin.SystemMonitorDaemon.getAlarmUsageOfMemory
```

### set-memory-alarm

设置内存告警阈值。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（int32）：设置值，示例值 `80`

接口：
- Method：`setAlarmUsageOfMemory`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.SystemMonitorDaemon /org/deepin/SystemMonitorDaemon org.deepin.SystemMonitorDaemon.setAlarmUsageOfMemory int32:80
```

### get-alarm-interval

读取告警通知间隔。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`getAlarmMsgInterval`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.SystemMonitorDaemon /org/deepin/SystemMonitorDaemon org.deepin.SystemMonitorDaemon.getAlarmMsgInterval
```

### set-alarm-interval

设置告警通知间隔。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（int32）：设置值，示例值 `60`

接口：
- Method：`setAlarmMsgInterval`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.SystemMonitorDaemon /org/deepin/SystemMonitorDaemon org.deepin.SystemMonitorDaemon.setAlarmMsgInterval int32:60
```

### get-protection

读取系统保护状态。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`getSystemProtectionStatus`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.SystemMonitorDaemon /org/deepin/SystemMonitorDaemon org.deepin.SystemMonitorDaemon.getSystemProtectionStatus
```

### set-protection

设置系统保护状态。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（boolean）：设置值，示例值 `true`

接口：
- Method：`setSystemProtectionStatus`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.SystemMonitorDaemon /org/deepin/SystemMonitorDaemon org.deepin.SystemMonitorDaemon.setSystemProtectionStatus boolean:true
```

风险警示：
- 会修改系统保护状态；执行前必须确认目标状态及其对系统监视保护的影响。

接口信息：
- Bus：`system`
- Service：`org.deepin.SystemMonitorSystemServer`
- Object path：`/org/deepin/SystemMonitorSystemServer`
- Interface：`org.deepin.SystemMonitorSystemServer`

### process-info

批量获取进程信息


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- `pids`（array of int32）：示例值 `1234,5678`

接口：
- Method：`getProcessInfoBatch`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=org.deepin.SystemMonitorSystemServer /org/deepin/SystemMonitorSystemServer org.deepin.SystemMonitorSystemServer.getProcessInfoBatch array:int32:1234,5678
```

接口信息：
- Bus：`session`
- Service：`com.deepin.systemMonitor`
- Object path：`/com/deepin/systemMonitor`
- Interface：`com.deepin.systemMonitor`

### show

显示系统监视器窗口


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`handleWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.systemMonitor /com/deepin/systemMonitor com.deepin.systemMonitor.handleWindow
```

接口信息：
- Bus：`session`
- Service：`com.deepin.SystemMonitorMain`
- Object path：`/com/deepin/SystemMonitorMain`
- Interface：`com.deepin.SystemMonitorMain`

### detail

跳转到系统监视器详情页


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `page`（string）：示例值 `cpu`

接口：
- Method：`slotJumpDetailWidget`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.SystemMonitorMain /com/deepin/SystemMonitorMain com.deepin.SystemMonitorMain.slotJumpDetailWidget string:cpu
```

### process

跳转到进程管理页


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `value`（string）：示例值 ``

接口：
- Method：`slotJumpProcessWidget`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.SystemMonitorMain /com/deepin/SystemMonitorMain com.deepin.SystemMonitorMain.slotJumpProcessWidget string:
```

接口信息：
- Bus：`session`
- Service：`com.deepin.SystemMonitorServer`
- Object path：`/com/deepin/SystemMonitorServer`
- Interface：`com.deepin.SystemMonitorServer`

### cpu-notify

显示 CPU 告警通知


执行说明：
- 分类：调用 D-Bus 直接呼出界面；接口返回不代表用户已完成窗口内操作。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `message`（string）：示例值 `CPU 使用率过高`

接口：
- Method：`showCpuAlarmNotify`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.SystemMonitorServer /com/deepin/SystemMonitorServer com.deepin.SystemMonitorServer.showCpuAlarmNotify 'string:CPU 使用率过高'
```

### memory-notify

显示内存告警通知


执行说明：
- 分类：调用 D-Bus 直接呼出界面；接口返回不代表用户已完成窗口内操作。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `message`（string）：示例值 `内存使用率过高`

接口：
- Method：`showMemoryAlarmNotify`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.SystemMonitorServer /com/deepin/SystemMonitorServer com.deepin.SystemMonitorServer.showMemoryAlarmNotify 'string:内存使用率过高'
```
