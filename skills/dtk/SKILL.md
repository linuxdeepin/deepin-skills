---
name: dtk
description: DTK（Deepin Tool Kit）是 Deepin 桌面环境的开发套件，提供 CLI 工具、D-Bus 接口和 DConfig 公共配置能力。本 skill 提供 DCI 图标打包解包查看、DCI 图标主题构建与查找、X11 窗口属性读写、KWin 调试信息输出、DConfig 配置 C++ 代码生成、D-Bus 接口 C++ 代码生成、DTK 设置翻译代码与 GSettings schema 生成、中文转拼音、系统信息查询、SVG 转 PNG 的 CLI 命令，DTK 应用间跨进程文件拖拽 D-Bus 接口，DTK 应用偏好 DConfig 配置（作用范围为 DTK 应用）和系统区域格式 DConfig 配置（作用范围为系统全局），提供 dtkcore C++ 基础库、dtkgui GUI 基础库、dtkwidget 控件库、dtkdeclarative 声明式控件库及 org.deepin.dtk 和 org.deepin.dtk.settings QML 模块开发接口
Categories:
  - Develop
---

# dtk

DTK（Deepin Tool Kit）是 Deepin 桌面环境的开发套件。本 skill 描述 DTK 对外提供的 CLI 命令、D-Bus 接口和 DConfig 公共配置能力。

## CLI 命令

### dci

DCI 文件打包/解包工具，用于将符合 DCI 目录规范的图标目录打包为 `.dci` 文件，或将 `.dci` 文件导出为目录结构，还支持以树形结构查看 DCI 文件内容。

详见 [dci.md](references/cli/dci.md)

### dci-icon-theme

DCI 图标主题构建工具，用于将普通的图标目录结构转换为 DCI 图标主题文件。

详见 [dci-icon-theme.md](references/cli/dci-icon-theme.md)

### dci-iconfinder

DCI 图标查找工具，用于在已安装的 DCI 图标主题中搜索指定名称的图标文件。

详见 [dci-iconfinder.md](references/cli/dci-iconfinder.md)

### deepin-gui-settings

DTK GUI 设置工具，用于读写 X11 窗口属性设置。

详见 [deepin-gui-settings.md](references/cli/deepin-gui-settings.md)

### dde-kwin-bug

DDE KWin 调试工具，用于输出 KWin 窗口管理器的调试信息。

详见 [dde-kwin-bug.md](references/cli/dde-kwin-bug.md)

### dtk-settings

DTK 设置工具，用于从 DTK 设置 JSON 配置文件生成翻译代码（C++）和 GSettings schema（XML）。

详见 [dtk-settings.md](references/cli/dtk-settings.md)

### ch2py

中文转拼音工具，将输入的中文字符串转换为拼音。

详见 [ch2py.md](references/cli/ch2py.md)

### deepin-os-release

系统信息查询工具，用于输出 deepin/UOS 操作系统的各项信息。

详见 [deepin-os-release.md](references/cli/deepin-os-release.md)

### dconfig2cpp

DConfig 转 C++ 代码生成器，从 DConfig JSON 配置文件生成 C++ 头文件，将 DConfig 配置项封装为类型安全的 C++ 类。

详见 [dconfig2cpp.md](references/cli/dconfig2cpp.md)

### qdbusxml2cpp-fix

D-Bus XML 转 C++ 代码生成器，是 Qt 自带 `qdbusxml2cpp` 的增强版本。

详见 [qdbusxml2cpp-fix.md](references/cli/qdbusxml2cpp-fix.md)

### dtk6-svgc

SVG 转 PNG 转换工具，将 SVG 矢量图渲染为 PNG 位图。

详见 [dtk6-svgc.md](references/cli/dtk6-svgc.md)


## D-Bus 接口

### 文件拖拽服务

提供跨进程文件拖拽交互能力。拖拽源进程在 Session 总线上注册此接口对象，文件接收方通过 D-Bus 与拖拽源通信，实现拖拽状态查询、进度同步和数据回传。接口使用动态 baseService（拖拽源进程的唯一连接名），接收方从拖拽 MIME 数据中获取 service 名称和会话 UUID 后调用。

详见 [com.deepin.dtk.FileDrag](references/dbus/com.deepin.dtk.FileDrag.md)

## DConfig 配置项

DTK 通过 DConfig 暴露两组公共配置资源（appId 为空，所有 DTK 应用共享）。两组配置的作用范围不同：DTK 应用偏好配置仅作用于 DTK 应用，区域格式配置作用于系统全局。

### DTK 应用偏好配置

控制 DTK 应用的外观与行为：主题、动画、滚动条、标题栏、新特性展示、菜单搜索、日志规则。作用范围为 DTK 应用。

详见 [org.deepin.dtk.preference](references/config/org.deepin.dtk.preference.md)

### 区域格式配置

控制系统的区域格式：语言、日期、时间、数字、货币、纸张。作用范围为系统全局。

详见 [org.deepin.region-format](references/config/org.deepin.region-format.md)

## 开发接口

### dtkcore

dtkcore 是基于 Qt 的 C++ 基础库，提供配置与设置、日志、文件与目录、系统信息、DBus 通信、通知、文本处理和线程调度能力。界面控件与视觉主题由上层库提供。

详见 [dtkcore-dev.md](interface/dtkcore/dtkcore-dev.md)

#### 配置与设置

提供统一的配置读写入口、配置缓存与文件访问、配置元信息查询，以及基于后端抽象的设置模型管理，支持分组层级结构与多种持久化后端。

详见 [config-and-settings.md](interface/dtkcore/dtkcore-dev/config-and-settings.md)

#### DBus 通信

提供链式 DBus 调用构造、异步方法提交、远端属性读写、扩展接口代理（含属性缓存与批量获取）以及接口导出能力。

详见 [dbus-communication.md](interface/dtkcore/dtkcore-dev/dbus-communication.md)

#### DCI 与文本处理

提供 DCI 容器的加载、节点查询与数据读写，文本编码探测与字符集转换，以及安全字符串管理能力。

详见 [dci-and-text-processing.md](interface/dtkcore/dtkcore-dev/dci-and-text-processing.md)

#### 文件与路径

提供文件与目录监视、文件服务、桌面条目解析、标准路径定位、路径拼接工具、回收站操作和最近使用记录管理。

详见 [file-and-path.md](interface/dtkcore/dtkcore-dev/file-and-path.md)

#### 日志与通知

提供日志规则设置、日志文件定位和桌面通知发送能力。

详见 [logging-and-notification.md](interface/dtkcore/dtkcore-dev/logging-and-notification.md)

#### 系统信息与许可

提供发行版、产品、组织、架构及硬件运行状态查询，应用标识查询，以及组件级许可信息读取能力。

详见 [system-info-and-license.md](interface/dtkcore/dtkcore-dev/system-info-and-license.md)

#### 工具与线程

提供单位换算与格式化、线程投递、单例基类模板、对象基类、虚函数表操作以及路径拼接工具。

详见 [tools-and-threading.md](interface/dtkcore/dtkcore-dev/tools-and-threading.md)

### dtkdeclarative

dtkdeclarative 是基于 Qt Quick 的 C++ 库，为 DTK QML 声明式控件提供底层支撑。它提供 DTK 应用的 QML 加载器、应用主窗口与预加载接口、QML 场景中的帧缓冲区位块传输与视口裁剪渲染、DTK 窗口附加属性以及平台主题代理。QML 控件本身以 `org.deepin.dtk` QML 模块的形式发布，设置控件以 `org.deepin.dtk.settings` QML 模块的形式发布。

详见 [dtkdeclarative-dev.md](interface/dtkdeclarative/dtkdeclarative-dev.md)

#### 应用加载

提供 DTK QML 应用的加载器、应用主窗口接口和应用预加载扩展接口。

详见 [app-loading.md](interface/dtkdeclarative/dtkdeclarative-dev/app-loading.md)

#### DTK5 主题兼容

提供平台主题代理和系统调色板 QML 项，仅在 DTK5 中提供，DTK6 已移除。

详见 [dtk5-theme-compat.md](interface/dtkdeclarative/dtkdeclarative-dev/dtk5-theme-compat.md)

#### 快速渲染

提供 QML 场景中的帧缓冲区位块传输渲染和视口裁剪渲染能力。

详见 [fast-rendering.md](interface/dtkdeclarative/dtkdeclarative-dev/fast-rendering.md)

#### QML 窗口

提供 DTK 窗口及其附加属性，用于在 QML 场景中控制窗口外观与行为。

详见 [qml-window.md](interface/dtkdeclarative/dtkdeclarative-dev/qml-window.md)

### org.deepin.dtk QML 模块

详见 [org.deepin.dtk.md](interface/dtkdeclarative/org.deepin.dtk.md)

#### 按钮控件

提供图标、语义化、开关切换、浮动操作按钮及按钮组容器，覆盖常见交互触发场景。

详见 [buttons.md](interface/dtkdeclarative/org.deepin.dtk/buttons.md)

#### 对话框与窗口控件

窗口与对话框控件涵盖模态/非模态对话框、弹窗、抽屉、应用主窗口、标题栏和关于对话框。

详见 [dialogs-and-windows.md](interface/dtkdeclarative/org.deepin.dtk/dialogs-and-windows.md)

#### 输入控件

输入控件涵盖文本编辑、密码、搜索、IP 地址、快捷键、数值微调、复选、单选、开关、下拉选择和滑动条。

详见 [input-controls.md](interface/dtkdeclarative/org.deepin.dtk/input-controls.md)

#### 列表与视图控件

列表与导航视图涵盖滚动视图、堆栈视图、滑动视图、列表项代理、排序过滤模型、标签页栏和页面指示器。

详见 [list-and-views.md](interface/dtkdeclarative/org.deepin.dtk/list-and-views.md)

#### 菜单与动作控件

标准动作和动作组涵盖上下文菜单、菜单栏、菜单项分隔、主题切换菜单以及关于/帮助/退出。

详见 [menus-and-actions.md](interface/dtkdeclarative/org.deepin.dtk/menus-and-actions.md)

#### 视觉效果与渲染控件

视觉效果与渲染控件涵盖阴影、面板、圆角裁剪、高斯模糊、进度指示、动画、标签和提示。

详见 [visual-effects-and-rendering.md](interface/dtkdeclarative/org.deepin.dtk/visual-effects-and-rendering.md)

### org.deepin.dtk.settings QML 模块

详见 [org.deepin.dtk.settings.md](interface/dtkdeclarative/org.deepin.dtk.settings.md)

### dtkgui

dtkgui 是基于 Qt GUI 模块的 C++ 库，提供 DTK 图形界面层面的能力，包括 DCI 图标渲染与播放、调色板管理、窗口装饰与平台主题、文件拖拽、字体管理、缩略图生成、SVG 渲染、区域监视和任务栏控制。控件级别的功能由上层 dtkwidget 提供。

详见 [dtkgui-dev.md](interface/dtkgui/dtkgui-dev.md)

#### DCI 图标

提供 DCI 图标资源的加载、渲染与动画播放能力，包括图标容器、单帧图像访问、图像序列播放器、内嵌调色板和整体动画播放器。

详见 [dci-icons.md](interface/dtkgui/dtkgui-dev/dci-icons.md)

#### 文件拖拽、字体与缩略图

提供跨进程文件拖拽的客户端与服务端、字体安装与管理以及文件缩略图异步生成能力。

详见 [file-drag-font-and-thumbnail.md](interface/dtkgui/dtkgui-dev/file-drag-font-and-thumbnail.md)

#### 图标与 SVG 渲染

提供 DTK 图标加载、图标主题缓存管理、SVG 渲染和图像格式处理能力。

详见 [icon-and-svg-rendering.md](interface/dtkgui/dtkgui-dev/icon-and-svg-rendering.md)

#### 调色板与主题

提供 DTK 扩展调色板角色、应用级主题管理、原生设置读写和平台主题属性访问能力。

详见 [palette-and-theme.md](interface/dtkgui/dtkgui-dev/palette-and-theme.md)

#### 系统服务

提供系统服务调用（打开文件管理器、播放系统提示音）、屏幕区域监视和任务栏进度与计数控制能力。

详见 [system-services.md](interface/dtkgui/dtkgui-dev/system-services.md)

#### 窗口与平台

提供窗口平台属性控制、窗口管理器功能查询、跨进程窗口分组和外部窗口引用能力。

详见 [window-and-platform.md](interface/dtkgui/dtkgui-dev/window-and-platform.md)

### dtkwidget

dtkwidget 是基于 Qt Widgets 模块的 C++ 控件库，提供 DTK 风格的对话框、窗口、按钮、输入框、列表、视图、样式、动画效果、打印预览、设置界面和辅助工具这些控件级别的功能。图形界面层面的非控件能力（调色板、DCI 图标、窗口装饰）由下层 dtkgui 提供。

详见 [dtkwidget-dev.md](interface/dtkwidget/dtkwidget-dev.md)

#### 按钮

提供图标、语义化（建议/警告）、开关切换、命令链接、浮动操作、方向箭头按钮及按钮组容器，覆盖常见交互触发场景。

详见 [buttons.md](interface/dtkwidget/dtkwidget-dev/buttons.md)

#### 容器与布局

提供框架、分隔线、分组背景三类结构化容器，以及抽屉、展开组两类可折叠内容区域和锚点布局、标签页栏两类布局工具，帮助组织界面层级和空间分配。

详见 [containers-and-layout.md](interface/dtkwidget/dtkwidget-dev/containers-and-layout.md)

#### 对话框

提供模态与非模态对话框基类框架，并内置关于、文件选择、文本输入、许可证展示和功能特性介绍五类常用专用对话框。

详见 [dialogs.md](interface/dtkwidget/dtkwidget-dev/dialogs.md)

#### 输入控件

为文本、数值和选择类输入提供 DTK 风格的编辑控件，支持单行与多行文本、密码、搜索、IP 地址、文件路径、快捷键、面包屑导航以及数值滑动和组合选择场景。

详见 [input-controls.md](interface/dtkwidget/dtkwidget-dev/input-controls.md)

#### 列表与视图

提供列表展示和项渲染能力，支持标准项和自定义样式化项代理，适用于设置面板、文件浏览这类结构化数据展示场景。

详见 [list-and-views.md](interface/dtkwidget/dtkwidget-dev/list-and-views.md)

#### 浮层与提示

提供浮动在主界面之上的临时消息和提示控件，支持消息停留、自动消失和吐司式通知，适用于不阻塞用户操作的轻量反馈场景。

详见 [overlays-and-tooltips.md](interface/dtkwidget/dtkwidget-dev/overlays-and-tooltips.md)

#### 打印预览

提供打印预览对话框及关联的页面设置能力，支持在预览界面中调整打印参数并实时查看效果。

详见 [print-preview.md](interface/dtkwidget/dtkwidget-dev/print-preview.md)

#### 设置界面

提供从配置模型自动生成设置界面的框架，通过设置对话框和控件工厂将配置项映射为复选框、下拉框两类界面控件。

详见 [settings-ui.md](interface/dtkwidget/dtkwidget-dev/settings-ui.md)

#### 样式与主题

管理 DTK 样式引擎、调色板、主题切换、尺寸模式、字号规格和水印效果，并为无障碍检查提供开发辅助工具。

详见 [style-and-theme.md](interface/dtkwidget/dtkwidget-dev/style-and-theme.md)

#### 工具与辅助

提供标签显示、图片查看、文件图标获取三类辅助控件和控件操作工具函数，补充核心控件库未覆盖的通用界面需求。

详见 [tools-and-helpers.md](interface/dtkwidget/dtkwidget-dev/tools-and-helpers.md)

#### 视觉效果与进度

为控件和窗口添加高斯模糊、圆角裁剪、投影阴影三类视觉增强效果，并提供弹跳动画、水波进度、加载指示器和进度条四类动态反馈控件。

详见 [visual-effects-and-progress.md](interface/dtkwidget/dtkwidget-dev/visual-effects-and-progress.md)

#### 窗口与标题栏

提供 DTK 风格的主窗口框架和自定义标题栏，集成窗口装饰和交互能力，包括窗口圆角、阴影、拖拽、最大化/最小化/关闭按钮。

详见 [window-and-titlebar.md](interface/dtkwidget/dtkwidget-dev/window-and-titlebar.md)
