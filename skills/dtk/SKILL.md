---
name: dtk
description: DTK 开发套件提供的跨进程文件拖拽 D-Bus 接口和 DTK 应用偏好与区域格式 DConfig 配置能力
Categories:
  - Develop
---

# dtk

DTK（Deepin Tool Kit）是 Deepin 桌面环境的开发套件。本 skill 描述 DTK 对外提供的 D-Bus 接口和 DConfig 公共配置能力。

## D-Bus 接口

### 文件拖拽服务

提供跨进程文件拖拽交互能力。拖拽源进程在 Session 总线上注册此接口对象，文件接收方通过 D-Bus 与拖拽源通信，实现拖拽状态查询、进度同步和数据回传。接口使用动态 baseService（拖拽源进程的唯一连接名），接收方从拖拽 MIME 数据中获取 service 名称和会话 UUID 后调用。

详见 [com.deepin.dtk.FileDrag](references/dbus/com.deepin.dtk.FileDrag.md)

## DConfig 配置

DTK 通过 DConfig 暴露两组公共配置资源（appId 为空，所有 DTK 应用共享）。

### DTK 应用偏好配置

控制以下 DTK 应用的外观与行为：主题、动画、滚动条、标题栏、新特性展示、菜单搜索、日志规则。

详见 [org.deepin.dtk.preference](references/config/org.deepin.dtk.preference.md)

### 区域格式配置

控制以下系统的区域格式：语言、日期、时间、数字、货币、纸张。

详见 [org.deepin.region-format](references/config/org.deepin.region-format.md)

## CLI 命令

### dci

DCI 文件打包/解包工具，用于将符合 DCI 目录规范的图标目录打包为 `.dci` 文件，或将 `.dci` 文件导出为目录结构，还支持以树形结构查看 DCI 文件内容。

详见 [dci.md](references/cli/dci.md)

### dci-image-converter

DCI 图片格式转换工具，用于在 DCI（Deepin Custom Image）格式与 alpha8 格式之间进行相互转换。

详见 [dci-image-converter.md](references/cli/dci-image-converter.md)

### dci-icon-theme

DCI 图标主题构建工具，用于将普通的图标目录结构转换为 DCI 图标主题文件。

详见 [dci-icon-theme.md](references/cli/dci-icon-theme.md)

### dci-iconfinder

DCI 图标查找工具，用于在已安装的 DCI 图标主题中搜索指定名称的图标文件。

详见 [dci-iconfinder.md](references/cli/dci-iconfinder.md)

### image-handler

DTK 图片处理工具，支持图片旋转、应用滤镜效果、查看图片信息三项操作。

详见 [image-handler.md](references/cli/image-handler.md)

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

