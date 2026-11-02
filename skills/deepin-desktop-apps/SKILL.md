---
name: deepin-desktop-apps
description: >-
  用于调用 deepin/UOS 原生桌面应用公开的 D-Bus/CLI 能力，按用户意图查询或操作。覆盖日历日程、提醒、农历与视图；文件管理、设备安全弹出、保险箱、最近文件、撤销/重做及文件名/全文搜索；计算器模式与窗口、相机拍照录像、文件压缩解压与下载；Deb 包安装/卸载和字体安装；硬件、GPU、驱动、磁盘分区与 SMART 查询；图片编辑标注、文本编辑、图片/PDF 查看；日志查询读取/导出、邮件查询/搜索/发送、帮助手册搜索；音乐/视频播放控制；图片和截图 OCR、截图/录屏/滚动截图、取色器启动；CPU/内存/进程资源监控、终端命令与终端设置、语音笔记查询/录制。操作前按对应参考页核对服务、权限、参数和 GUI/人工交互条件，操作后验证结果。本技能面向已安装应用的接口操作，不负责应用/插件开发或 DDE 全局设置。注意：取色器接口只启动、不返回色值；图片文件 OCR 与截图 OCR 使用不同接口；设备管理器不提供 CPU/内存/进程运行时监控。
Categories:
  - Application
---

# deepin 桌面应用操作

根据用户意图选择对应应用的接口说明。具体方法、参数、服务名、路径、类型、交互行为与前置条件以该应用参考页为准；不要仅凭方法名推断行为。

## 能力边界

本 Skill 用于操作现有桌面应用的公开接口，不负责 DDE 全局外观、电源和会话设置，也不负责开发应用或桌面插件。系统设置使用 `$deepin-desktop-environment`；DTK 应用开发使用 `$dtk-development`；控制中心、Shell、托盘插件开发分别使用 `$dde-control-center-development`、`$dde-shell-development`、`$dde-tray-development`。

## 应用与参考页

| 技能 | 覆盖范围 | 参考页 |
| --- | --- | --- |
| `dde-calendar`（日历与日程） | 提供日历应用中的日程查询、创建、修改、详情打开、日历视图查询、农历信息查询、提醒查询、窗口激活和窗口置顶接口 | [接口说明](references/dde-calendar/SKILL.md) |
| `dde-file-manager`（文件管理器） | 提供文件管理器中的块设备、协议设备安全弹出、保险箱、最近文件、操作撤销重做和全文索引接口 | [接口说明](references/dde-file-manager/SKILL.md) |
| `deepin-anything`（极速文件搜索） | 提供基于文件名索引的关键词搜索、通配符搜索（`-w`）和 systemd 服务状态查询接口 | [接口说明](references/deepin-anything/SKILL.md) |
| `deepin-calculator`（计算器） | 提供计算器窗口控制、当前模式查询和标准、科学、程序员模式切换接口 | [接口说明](references/deepin-calculator/SKILL.md) |
| `deepin-camera`（相机） | 提供相机应用中的拍照、录像控制、录像状态查询和窗口控制接口 | [接口说明](references/deepin-camera/SKILL.md) |
| `deepin-compressor`（压缩工具） | 提供压缩工具中的文件压缩、压缩包解压、内容查询、完整性测试和窗口控制接口，支持应用级格式识别和图形窗口控制 | [接口说明](references/deepin-compressor/SKILL.md) |
| `deepin-deb-installer`（Deb 包安装器） | 提供 Deb 安装器中的安装状态、安装、批量安装和卸载接口；驱动包、架构、签名、依赖和 Deb 有效性检查由设备管理器或系统包管理工具提供 | [接口说明](references/deepin-deb-installer/SKILL.md) |
| `deepin-devicemanager`（设备管理器） | 提供系统硬件设备的信息查询、状态检查、GPU 查询、可移除设备查询、驱动包检查和 Deb 包检查接口；不负责系统版本信息或 CPU、内存、进程运行时资源占用查询 | [接口说明](references/deepin-devicemanager/SKILL.md) |
| `deepin-diskmanager`（磁盘管理器） | 提供磁盘管理器中的磁盘、分区和硬盘 SMART 信息查询接口 | [接口说明](references/deepin-diskmanager/SKILL.md) |
| `deepin-downloader`（下载器） | 提供下载器中的 URL 下载任务创建、torrent 或 metalink 文件打开和窗口显示接口，支持下载器应用能力 | [接口说明](references/deepin-downloader/SKILL.md) |
| `deepin-draw`（画板） | 提供画板中的图片编辑、标注、单个图片打开和多个图片批量打开接口，不负责单纯图片查看 | [接口说明](references/deepin-draw/SKILL.md) |
| `deepin-editor`（文本编辑器） | 提供文本编辑器中的文件标签页打开和新窗口打开接口 | [接口说明](references/deepin-editor/SKILL.md) |
| `deepin-font-manager`（字体管理器） | 提供面向最终用户的字体管理器中的一个或多个字体文件安装接口 | [接口说明](references/deepin-font-manager/SKILL.md) |
| `deepin-image-viewer`（图片查看器） | 提供图片查看器打开单个图片文件进行查看的接口；不负责相册浏览和图片编辑。 | [接口说明](references/deepin-image-viewer/SKILL.md) |
| `deepin-log-viewer`（日志查看器） | 提供日志查看器中的日志文件信息、存在性、大小、行数、流式读取、导出和路径白名单接口 | [接口说明](references/deepin-log-viewer/SKILL.md) |
| `deepin-mail`（邮件客户端） | 提供邮件客户端中的账户、文件夹、邮件查询、搜索、发送和标记接口 | [接口说明](references/deepin-mail/SKILL.md) |
| `deepin-manual`（帮助手册） | 提供应用帮助手册的打开、显示、实验性搜索和存在性查询接口 | [接口说明](references/deepin-manual/SKILL.md) |
| `deepin-movie`（视频播放器） | 提供视频播放器中的视频文件和 URI 打开、MPRIS 播放控制、播放位置、音量、播放速率、状态、元数据和窗口控制接口 | [接口说明](references/deepin-movie/SKILL.md) |
| `deepin-music`（音乐播放器） | 提供音乐播放器中的音乐文件打开、MPRIS 播放控制、播放位置、音量、状态、元数据和窗口控制接口 | [接口说明](references/deepin-music/SKILL.md) |
| `deepin-ocr`（OCR 文字识别） | 提供图片文件 OCR 接口；截图 OCR 由 deepin-screen-recorder 提供 | [接口说明](references/deepin-ocr/SKILL.md) |
| `deepin-picker`（屏幕取色器） | 提供本机应用使用的屏幕取色器启动接口；当前源接口仅提供启动方法，不提供取色结果读取接口，也不负责沙箱应用的门户取色 | [接口说明](references/deepin-picker/SKILL.md) |
| `deepin-reader`（PDF 阅读器） | 提供 PDF 阅读器中的 PDF 和文档文件打开接口 | [接口说明](references/deepin-reader/SKILL.md) |
| `deepin-screen-recorder`（截图录屏） | 提供截图录屏工具中的可脚本截图、录屏、OCR、滚动截图和对应 CLI 接口，并标明人工交互边界 | [接口说明](references/deepin-screen-recorder/SKILL.md) |
| `deepin-system-monitor`（系统监视器） | 提供系统监视器中的 CPU 占用率、内存占用率、进程资源占用、系统检查、告警触发、系统保护和窗口跳转接口 | [接口说明](references/deepin-system-monitor/SKILL.md) |
| `deepin-terminal`（终端模拟器） | 提供在终端应用窗口中执行命令，以及设置该终端的字体、透明度、光标、颜色主题和 Shell 的接口 | [接口说明](references/deepin-terminal/SKILL.md) |
| `deepin-voice-note`（语音笔记） | 提供语音笔记列表查询和基于已有笔记 ID 的语音录制接口 | [接口说明](references/deepin-voice-note/SKILL.md) |

## 操作流程

1. **识别应用与目标。** 从上表选择应用；涉及多个应用时，只读取相关参考页。
2. **读取接口说明。** 调用前确认 Bus、服务名、对象路径、接口、方法、参数类型及是否会打开界面。
3. **核对服务前置条件。** 按参考页确认应用是否安装、服务是否已注册以及是否需要启动；服务未注册不能当作应用未安装。不要把一个应用的启动或总线规则套用到其他应用。
4. **执行并验证。** 仅调用文档列出的公开接口；按接口能力回读或检查结果。涉及删除、发送、录制、安装等有影响的操作，遵循对应参考页的授权和确认要求。
5. **如实报告。** 区分应用未安装、服务未注册、权限不足和接口失败；不把请求提交成功当作最终结果。

接口细节维护在 `references/<skill-name>/SKILL.md`。
