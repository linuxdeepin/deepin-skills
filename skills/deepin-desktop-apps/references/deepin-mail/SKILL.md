---
name: deepin-mail
description: 提供邮件客户端中的账户、文件夹、邮件查询、搜索、发送和标记接口
Categories:
  - Application
---

# 邮件客户端

提供账户、邮件查询、邮件详情、搜索、发送和标记接口

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：账户、未读、列表、详情和搜索 action 返回查询结果；`send`、`mark` 返回后表示发送或标记请求已提交。发送邮件、删除邮件等有副作用 action 必须先确认目标和内容。
- 需呼出界面并人工操作：无；本 Skill 不提供需要在邮件客户端窗口继续填写或确认的 action。
- 需先启动应用后 D-Bus 才存在：服务前置：需要 `org.deepin.mail` 先注册；不要求 Agent 人工打开邮件客户端界面，deepin-tools 会尝试启动邮件客户端。
- 调用 D-Bus 直接呼出界面：无；当前接口未声明会打开邮件客户端窗口。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`org.deepin.mail`
- Object path：`/org/deepin/mail`
- Interface：`org.deepin.mail`

### accounts

获取所有账户和文件夹


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`GetAccounts`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.mail /org/deepin/mail org.deepin.mail.GetAccounts
```

### unread

获取账户未读邮件


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `account`（string）：示例值 `account@example.com`

接口：
- Method：`GetUnread`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.mail /org/deepin/mail org.deepin.mail.GetUnread string:account@example.com
```

### unread-count

获取账户未读邮件数量


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `account`（string）：示例值 `account@example.com`

接口：
- Method：`GetUnreadCount`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.mail /org/deepin/mail org.deepin.mail.GetUnreadCount string:account@example.com
```

### list

获取文件夹邮件列表


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `account`（string）：示例值 `account@example.com`
- `folder`（string）：示例值 `INBOX`
- `limit`（int32）（可选）：示例值 `20`

接口：
- Method：`GetMails`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.mail /org/deepin/mail org.deepin.mail.GetMails string:account@example.com string:INBOX int32:20
```

### detail

获取邮件详情


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `account`（string）：示例值 `account@example.com`
- `folder`（string）：示例值 `INBOX`
- `id`（int32）：示例值 `1`

接口：
- Method：`GetMailDetail`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.mail /org/deepin/mail org.deepin.mail.GetMailDetail string:account@example.com string:INBOX int32:1
```

### search

搜索邮件


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `account`（string）：示例值 `account@example.com`
- `keyword`（string）：示例值 `report`
- `limit`（int32）（可选）：示例值 `10`

接口：
- Method：`SearchMails`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.mail /org/deepin/mail org.deepin.mail.SearchMails string:account@example.com string:report int32:10
```

### send

发送邮件


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `account`（string）：示例值 `account@example.com`
- `to`（string）：示例值 `recipient@example.com`
- `subject`（string）：示例值 `主题`
- `body`（string）（可选）：示例值 `正文`
- `cc`（string）（可选）：示例值 ``
- `attachments`（string）（可选）：示例值 ``

接口：
- Method：`SendMail`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.mail /org/deepin/mail org.deepin.mail.SendMail string:account@example.com string:recipient@example.com 'string:主题' 'string:正文' string: string:
```

风险警示：
- 会向指定收件人发送邮件；执行前必须确认账户、收件人、主题、正文和附件。

### mark

标记邮件


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `account`（string）：示例值 `account@example.com`
- `folder`（string）：示例值 `INBOX`
- `ids`（string）：示例值 `1`
- `action`（string）：可选值 `read`、`unread`、`star`、`unstar`、`delete`；示例值 `read`

接口：
- Method：`MarkMails`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.mail /org/deepin/mail org.deepin.mail.MarkMails string:account@example.com string:INBOX string:1 string:read
```

风险警示：
- `delete` 会删除指定邮件且通常不可恢复；执行前必须确认账户、文件夹和邮件 ID。
