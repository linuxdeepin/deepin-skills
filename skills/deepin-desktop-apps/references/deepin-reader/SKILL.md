---
name: deepin-reader
description: 提供 PDF 阅读器中的 PDF 和文档文件打开接口
Categories:
  - Application
---

# PDF 阅读器

提供 PDF 和文档文件打开接口

批量语义：一次 `handleFiles` 传入多个路径表示批量提交打开请求；再次调用单个路径表示再次提交单个打开请求。方法返回只表示请求已提交，不表示文档已加载或用户已阅读。

## 前置条件：启动玲珑应用

- 先用 `ll-cli list` 检查 `org.deepin.reader` 是否已安装。
- 已安装但服务未注册时，在当前图形用户会话中执行 `ll-cli run org.deepin.reader`。
- 使用 `busctl --user list` 或等价的会话总线检查确认 `com.deepin.Reader` 已注册后再调用接口。
- `ServiceUnknown` 只表示服务当前未注册或应用未运行，不表示应用未安装；不能用 `dpkg`、`which` 或桌面文件是否存在判断玲珑应用是否安装。
- 服务启动超时或应用未安装时应如实报告，不反复重试或改用无关 GUI 操作。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：无；`open` 只提交文档打开请求，不表示文档已经审阅。
- 需呼出界面并人工操作：`open` 后，用户需要在阅读器窗口查看文档。
- 需先启动应用后 D-Bus 才存在：服务前置：需要 `com.deepin.Reader` 先注册；不要求 Agent 人工打开阅读器界面，必须先按前置条件启动玲珑应用。
- 调用 D-Bus 直接呼出界面：`open` 打开文档并显示阅读器窗口。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.Reader`
- Object path：`/com/deepin/Reader`
- Interface：`com.deepin.Reader`

### open

打开一个或多个文档文件


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `paths`（array of string）：示例值 `$HOME/Documents/example.pdf,$HOME/Documents/second.pdf`

接口：
- Method：`handleFiles`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Reader /com/deepin/Reader com.deepin.Reader.handleFiles array:string:$HOME/Documents/example.pdf,$HOME/Documents/second.pdf
```
