---
name: dtk
description: DTK 开发套件 D-Bus 接口能力概览，涵盖 dtkcommon、dtkcore、dtkgui、dtkwidget、dtkdeclarative、qtintegration、qtplatform-plugins 各子项目
Categories:
  - Develop
---

# dtk

DTK（Deepin Tool Kit）是 Deepin 桌面环境的开发套件，包含多个子项目，覆盖底层公共定义、核心工具、GUI 组件、控件库、声明式 UI 框架、风格集成插件和平台适配插件。

## 子项目目录

| 子项目目录 | 说明 |
|------------|------|
| `dtkcommon/` | DTK 公共资源（CMake 模块、配置等），纯头文件库，无对外 D-Bus 服务 |
| `dtkcore/` | DTK 核心库，提供基础开发工具，纯 C++ 库，无对外 D-Bus 服务 |
| `dtkgui/` | DTK GUI 组件库，目前唯一有对外 D-Bus 服务接口的子项目（`com.deepin.dtk.FileDrag` 文件拖拽服务） |
| `dtkwidget/` | DTK Widget 控件库，纯 C++/Qt 控件库，无对外 D-Bus 服务 |
| `dtkdeclarative/` | DTK QML 声明式控件库（基于 Qt6），QML/JS 声明式 UI 框架，无自身注册的 D-Bus 服务 |
| `qtintegration/` | DTK 风格集成插件，Qt 风格插件，无 D-Bus 接口 |
| `qtplatform-plugins/` | DTK 平台适配插件，Qt 平台插件（QPA），无 D-Bus 接口 |

## D-Bus 接口概览

目前仅 dtkgui 有对外 D-Bus 服务接口（`com.deepin.dtk.FileDrag` 文件拖拽服务），其余子项目为纯库或插件，无对外 D-Bus 服务。

各子项目详细内容见对应子目录下的 SKILL.md。
