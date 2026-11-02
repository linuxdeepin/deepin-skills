---
name: deepin-ocr
description: 提供图片文件 OCR 接口；截图 OCR 由 deepin-screen-recorder 提供
Categories:
  - Application
---

# OCR 文字识别

提供图片文件 OCR 接口。截图 OCR 由 `deepin-screen-recorder` 提供，本 Skill 不重复暴露该能力。

职责边界：图片文件 OCR 使用 `openFile`；截图 OCR 使用 `deepin-screen-recorder` 的 `OcrScreenshot`。两种接口都不会把识别文本作为 D-Bus 返回值，也不会自动写入剪贴板；任务要求文本时必须报告该能力边界。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：无；`file` 只提交图片给 OCR 应用，当前 D-Bus 调用不返回识别文本。
- 需呼出界面并人工操作：`file` 后需要用户在 OCR 界面查看识别结果。
- 需先启动应用后 D-Bus 才存在：服务前置：需要 `com.deepin.Ocr` 先注册；源封装不会自动启动服务，Agent 必须先启动或确保 OCR 应用服务可用。
- 调用 D-Bus 直接呼出界面：`file` 将图片交给 OCR 应用处理并触发其界面流程。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.Ocr`
- Object path：`/com/deepin/Ocr`
- Interface：`com.deepin.Ocr`

### file

打开图片文件进行 OCR


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `path`（string）：示例值 `$HOME/Pictures/example.png`

接口：
- Method：`openFile`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.Ocr /com/deepin/Ocr com.deepin.Ocr.openFile string:$HOME/Pictures/example.png
```
