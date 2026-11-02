---
name: deepin-image-viewer
description: 提供图片查看器打开单个图片文件进行查看的接口；不负责相册浏览和图片编辑。
Categories:
  - Application
---

# 图片查看器

提供图片查看器中的图片文件查看接口

`openImageFile` 返回只表示打开请求已提交，不表示用户已经查看或确认图片内容。

## 前置条件：启动玲珑应用

- 先用 `ll-cli list` 检查 `org.deepin.image.viewer` 是否已安装。
- 已安装但服务未注册时，在当前图形用户会话中执行 `ll-cli run org.deepin.image.viewer`。
- 使用 `busctl --user list` 或等价的会话总线检查确认 `com.deepin.imageViewer` 已注册后再调用接口。
- `ServiceUnknown` 只表示服务当前未注册或应用未运行，不表示应用未安装；不能用 `dpkg`、`which` 或桌面文件是否存在判断玲珑应用是否安装。
- 服务启动超时或应用未安装时应如实报告，不反复重试或改用无关 GUI 操作。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：无；`open-image-file` 只提交图片打开请求。
- 需呼出界面并人工操作：`open-image-file` 后，用户需要在图片查看器窗口查看或确认图片内容。
- 需先启动应用后 D-Bus 才存在：服务前置：需要 `com.deepin.imageViewer` 先注册；不要求 Agent 人工打开图片查看器界面，必须先按前置条件启动玲珑应用。
- 调用 D-Bus 直接呼出界面：`open-image-file` 打开图片并显示图片查看器窗口。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.imageViewer`
- Object path：`/`
- Interface：`com.deepin.imageViewer`

### open-image-file

打开单个图片文件进行查看


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `path`（string）：示例值 `$HOME/Pictures/example.png`

接口：
- Method：`openImageFile`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.imageViewer / com.deepin.imageViewer.openImageFile string:$HOME/Pictures/example.png
```
