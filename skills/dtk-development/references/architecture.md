# DTK 核心架构

## 版本边界

本文的共用架构适用于 v20 和 v25。两者都可使用 dtkcore、dtkgui、
dtkwidget 的 C++/QWidget 能力；v20 不提供 `dtkdeclarative`，QML 应用使用 Qt
Quick/Qt Quick Controls 2。v25 才使用 DTK QML 控件、`D.DTK` 全局对象和
`ColorSelector`。平台集成项目的当前名称为 `dde-qtintegration` 和
`dde-qtplatform-plugins`。

同一源码需要分别按目标系统和 Qt/DTK ABI 构建；`DTK_VERSION_MAJOR` 或
`QT_VERSION_MAJOR` 只用于 ABI 分支，不能单独判断 v20/v25。

## 1. 概述

DTK 围绕四个核心系统构建，每个系统遵循相同的架构模式：

```
dtkgui（基础层）  →  dtkwidget / dtkdeclarative（控件层）
  提供核心抽象         在控件中使用，实现自动主题感知
```

- **调色板系统**：dtkgui 提供 `DPalette`/`DGuiApplicationHelper`，dtkwidget 通过 `DStyle`/`DStyleHelper` 在控件中自动处理状态颜色，dtkdeclarative 通过 `Palette`/`ColorSelector` 在 QML 中实现
- **字体系统**：dtkgui 提供 `DFontManager`，dtkwidget 通过 `DFontSizeManager` 绑定控件自动更新，dtkdeclarative 通过 QML `FontManager` 暴露
- **图标系统**：dtkgui 提供 `DDciIcon`/`DIconTheme`/`DDciIconPlayer`，dtkwidget 和 dtkdeclarative 在控件中直接使用
- **平台抽象**：dtkgui 提供 `DPlatformHandle`/`DPlatformTheme`/`DPlatformWindowInterface`，QPA 插件提供底层实现

## 2. 调色板系统

基于 Qt `QPalette` 扩展，实现暗亮色主题自动切换。

| 层次 | 组件 | 所在项目 | 角色 |
|------|------|----------|------|
| 基础 | `DPalette` | dtkgui | 扩展 QPalette，增加 DTK 语义颜色（TextTitle、TextWarning 等） |
| 基础 | `DGuiApplicationHelper` | dtkgui | 主题管理单例，提供 `themeTypeChanged` 信号、`standardPalette()`、`applicationPalette()` |
| 控件(W) | `DStyle` / `DStyleHelper` | dtkwidget | 根据控件状态自动选择调色板颜色（hover/press/disabled） |
| 控件(Q) | `Palette` / `ColorSelector` | dtkdeclarative | QML 调色板定义与自动取色 |

**数据流：**
```
系统主题切换
  → DGuiApplicationHelper::themeTypeChanged
  → DPalette 颜色自动更新
  → DStyleHelper 自动选择状态颜色（Widget）
  → ColorSelector 自动更新颜色属性（QML）
```

> 详细文档：[theme/palette.md](theme/palette.md)、[declarative/color-selector.md](declarative/color-selector.md)

## 3. 字体系统

基于 T1-T11 层级字体大小体系，以 T6（14px）为基准，系统字体变化时所有层级自动按差值缩放。

| 层次 | 组件 | 所在项目 | 角色 |
|------|------|----------|------|
| 基础 | `DFontManager` | dtkgui | 管理 T1-T11 字体大小，根据 baseFont 自动计算 |
| 基础 | `DGuiApplicationHelper` | dtkgui | 监听系统字体变化，驱动 DFontManager 更新 |
| 配置源 | `DPlatformTheme` / `DThemeSettings` | dtkgui / dde-qtintegration | 从 DConf/GSettings 读取系统字体配置 |
| 控件(W) | `DFontSizeManager` | dtkwidget | 单例，`bind(widget, T4)` 绑定控件到字体层级，自动更新 |
| 控件(Q) | `D.DTK.fontManager` | dtkdeclarative | QML 暴露 `fontManager.t1`-`t11`，控件直接引用 |

**字体大小层级：**

| T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | T9 | T10 | T11 |
|----|----|----|----|----|----|----|----|----|-----|-----|
| 40 | 30 | 24 | 20 | 16 | 14 | 13 | 12 | 11 | 10 | 8 |

**数据流：**
```
DConf/GSettings 字体配置
  → DThemeSettings
  → DPlatformTheme::fontName/fontPointSize (dtkgui)
  → QDeepinTheme::font() → QGuiApplication::setFont()
  → DGuiApplicationHelper::fontChanged
  → DFontManager::setBaseFont() → t1()-t11() 自动计算
  → DFontSizeManager::setFontGenericPixelSize() → 所有 bind 的控件自动更新字体（Widget）
  → D.DTK.fontManager.t6 → QML 控件字体自动更新（QML）
```

> 详细文档：[theme/index.md](theme/index.md)（字体部分）、[widgets/index.md](widgets/index.md)（DFontSizeManager）

## 4. 图标系统

支持 dci 图标（主题感知+动画）、builtin 图标（内置资源）、icon theme 图标（XDG 标准）三种方案。

| 层次 | 组件 | 所在项目 | 角色 |
|------|------|----------|------|
| 基础 | `DDciIcon` | dtkgui | dci 图标加载与渲染，支持 Light/Dark 主题和 Normal/Hover/Pressed/Disabled 状态 |
| 基础 | `DDciIconPlayer` | dtkgui | dci 图标动画播放器 |
| 基础 | `DIconTheme` | dtkgui | 图标查找统一入口，支持 dci/builtin/XDG 回退策略 |
| 基础 | `DDciIconPalette` | dtkgui | dci 图标调色板，与 QPalette 互转 |
| 控件(W) | `DIcon` / `DStyle::standardIcon()` | dtkwidget | Widget 层图标使用 |
| 控件(Q) | `DciIcon` / `DciIconImage` | dtkdeclarative | QML 层 dci 图标组件 |

**数据流：**
```
DIconTheme::findQIcon("icon-name")
  → 1. dci 图标（DDciIcon + 当前主题 Light/Dark）
  → 2. builtin 图标（内置资源）
  → 3. QIcon::fromTheme()（XDG 标准）
```

> 详细文档：[theme/index.md](theme/index.md)

## 5. 平台抽象

将窗口操作（圆角、阴影、边框、模糊、无标题栏）和主题配置（字体、颜色、图标主题）抽象为跨平台接口。

| 层次 | 组件 | 所在项目 | 角色 |
|------|------|----------|------|
| 公共 API | `DPlatformHandle` | dtkgui | 窗口操作公共入口（圆角、阴影、边框、模糊等） |
| 公共 API | `DPlatformTheme` | dtkgui | 主题配置公共入口（字体名、字号、活跃色、图标主题等） |
| 抽象接口 | `DPlatformWindowInterface` | dtkgui | 窗口操作抽象基类（虚函数） |
| 抽象接口 | `DPlatformInterface` | dtkgui | 主题配置抽象基类（虚函数） |
| X11 实现 | `DXCBPlatformWindowInterface` | dtkgui | X11 窗口操作实现（dxcb 插件） |
| X11 实现 | `DXCBPlatformInterface` | dtkgui | X11 主题配置实现（XSettings） |
| Treeland 实现 | `DTreeLandPlatformWindowInterface` | dtkgui | Treeland Wayland 窗口操作实现 |
| Treeland 实现 | `DTreelandPlatformInterface` | dtkgui | Treeland Wayland 主题配置实现 |
| QPA 层 | `DPlatformIntegration` | dde-qtplatform-plugins | X11 QPA 插件（扩展 QXcbIntegration） |
| QPA 层 | `DWaylandIntegration` | dde-qtplatform-plugins | Wayland QPA 插件（扩展 QWaylandIntegration） |
| QPA 层 | `DWaylandShellManager` | dde-qtplatform-plugins | KWayland Shell 协议管理 |

**平台分发：**
```
DPlatformHandle 构造
  → 检查 DGuiApplicationHelper::IsXWindowPlatform
    → DXCBPlatformWindowInterface（X11，使用 dxcb 协议）
  → 检查 DGuiApplicationHelper::IsWaylandPlatform
    → DTreeLandPlatformWindowInterface（Treeland，使用 Wayland personalization 协议）
  → 否则
    → DPlatformWindowInterface（空实现，无平台特效）
```

**两层架构：**
```
dtkgui 层（平台抽象）
  DPlatformHandle / DPlatformTheme
    → DPlatformWindowInterface / DPlatformInterface（虚接口）
    → DXCB* / DTreeLand*（具体实现）

QPA 插件层
  DPlatformIntegration（X11 QPA）
  DWaylandIntegration（Wayland QPA）
  → 提供底层窗口系统集成
```

> 详细文档：[platform-abstraction.md](platform-abstraction.md)

## 6. 仓库依赖关系

```
                     dtkcommon (CMake 构建宏 DtkBuildHelper)
                    ╱    │    ╲     ╲
               实线╱  实线│  实线╲  实线╲
                 ╱      │      ╲      ╲
           dtklog ──→ dtkcore ──→ dtkgui
              │                            │
              │                        实线╱   实线╲
              │                         ╱         ╲
              └──────→ dtkcore  dtkdeclarative  dde-qtplatform-plugins
                         │           │
                    实线╱    实线╱    实线╲
                     ╱        ╱         ╲
              dtkgui ←┘ dtkwidget   dtkdeclarative
                        │
                   虚线╱   虚线╲
                      ↓       ↓
               dde-qtintegration dde-qtplatform-plugins
```

| 项目 | 编译依赖 | 运行时/功能关联 |
|------|----------|----------------|
| dtkcommon | 无 | — |
| dtklog | dtkcommon（DtkBuildHelper） | — |
| dtkcore | dtkcommon, dtklog | — |
| dtkgui | dtkcommon, dtkcore | — |
| dtkwidget | dtkcore, dtkgui | dde-qtintegration（Chameleon 风格渲染） |
| dtkdeclarative | dtkcore, dtkgui | — |
| dde-qtintegration | dtkgui, dtkwidget | — |
| dde-qtplatform-plugins | dtkgui | — |

## 7. 相关文档

- [theme/index.md](theme/index.md) — 主题系统（含图标、调色板、字体）
- [platform-abstraction.md](platform-abstraction.md) — 平台抽象层
