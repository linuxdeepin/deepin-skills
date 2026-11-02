---
name: dde-calendar
description: 提供日历应用中的日程查询、创建、修改、详情打开、日历视图查询、农历信息查询、提醒查询、窗口激活和窗口置顶接口
Categories:
  - Application
---

# 日历与日程

提供日程查询、创建、修改、打开、日历视图、农历和提醒接口

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：`query`、`create`、`modify`、`view`、`lunar`、`reminders` 调用返回后即可取得结果或完成请求。
- 需呼出界面并人工操作：`open` 只打开日程详情；查看、编辑或确认详情由用户在窗口完成。
- 需先启动应用后 D-Bus 才存在：服务前置：需要 `com.deepin.Calendar` 先注册；不要求 Agent 人工打开日历界面，deepin-tools 的 `_ensure` 会尝试启动日历。
- 调用 D-Bus 直接呼出界面：`open` 打开日程详情，`active` 激活日历窗口，`raise` 将日历窗口置前。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.Calendar`
- Object path：`/com/deepin/Calendar`
- Interface：`com.deepin.Calendar`

### query

查询日程


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `query`（string）：示例值 `today`

接口：
- Method：`QuerySchedules`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calendar /com/deepin/Calendar com.deepin.Calendar.QuerySchedules string:today
```

### create

创建日程


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `json`（string）：示例值 `{"title":"项目会议","start":"2026-09-21T10:00:00+08:00"}`

接口：
- Method：`CreateSchedule`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calendar /com/deepin/Calendar com.deepin.Calendar.CreateSchedule 'string:{"title":"项目会议","start":"2026-09-21T10:00:00+08:00"}'
```

### modify

修改、删除或延后日程


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `id`（string）：示例值 `123`
- `op`（string）：示例值 `update`
- `data`（string）（可选）：示例值 `{"title":"已更新"}`

接口：
- Method：`ModifySchedule`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calendar /com/deepin/Calendar com.deepin.Calendar.ModifySchedule string:123 string:update 'string:{"title":"已更新"}'
```

### open

打开日程详情


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `id`（string）：示例值 `123`

接口：
- Method：`OpenSchedule`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calendar /com/deepin/Calendar com.deepin.Calendar.OpenSchedule string:123
```

### view

获取日历视图


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `view`（string）：示例值 `week`
- `date`（string）：示例值 `2026-09-21`

接口：
- Method：`GetCalendarView`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calendar /com/deepin/Calendar com.deepin.Calendar.GetCalendarView string:week string:2026-09-21
```

### lunar

查询农历和黄历信息


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `date`（string）：示例值 `2026-09-21`

接口：
- Method：`GetLunarInfo`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calendar /com/deepin/Calendar com.deepin.Calendar.GetLunarInfo string:2026-09-21
```

### reminders

查询未来指定小时的提醒


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `hours`（int32）：示例值 `24`

接口：
- Method：`GetReminders`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calendar /com/deepin/Calendar com.deepin.Calendar.GetReminders int32:24
```

### active

激活日历窗口


执行说明：
- 分类：调用 D-Bus 直接呼出界面；接口返回不代表用户已完成窗口内操作。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`ActiveWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calendar /com/deepin/Calendar com.deepin.Calendar.ActiveWindow
```

### raise

将日历窗口置于前台


执行说明：
- 分类：调用 D-Bus 直接呼出界面；接口返回不代表用户已完成窗口内操作。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`RaiseWindow`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Calendar /com/deepin/Calendar com.deepin.Calendar.RaiseWindow
```
