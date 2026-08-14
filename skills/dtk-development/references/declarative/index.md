# QML 控件

> 本目录全部文档仅适用于 v25 的 dtkdeclarative。v20 不支持 DTK QML；
> v20 QML 必须使用 Qt Quick/Qt Quick Controls 2，不导入 `org.deepin.dtk`。

## 触发关键词

本文档适用于以下任务场景：

**自然语言描述：**
- QML按钮/对话框/输入框
- QML菜单/列表/进度条
- DTK QML控件
- Qt Quick DTK样式

**API 接口描述：**
- org.deepin.dtk / DTK QML
- ApplicationWindow / DialogWindow
- Button / TextField / ItemDelegate

---

## 概述

dtkdeclarative 对 Qt Quick Controls 进行 DTK 主题封装并提供自定义控件，用于 Qt Quick 应用。

**适用场景：** DDE Shell 插件、QML 应用、需要动态 UI 的场景。

本文控件集只以 v25 的 dtkdeclarative 为基线。先确认目标工程使用 DTK5/Qt5
还是 DTK6/Qt6，再核对 QML module、import 版本和实际类型。

## 快速决策树

```
需要什么类型的 QML 控件？
    │
    ├─ 窗口 → ApplicationWindow / DialogWindow
    │
    ├─ 按钮 → Button / RecommandButton / WarningButton / FloatingButton
    │
    ├─ 图标按钮 → ToolButton / IconButton / ActionButton
    │
    ├─ 选择 → CheckBox / RadioButton / Switch
    │
    ├─ 输入 → TextField / LineEdit / SearchEdit / PasswordEdit / SpinBox / ComboBox
    │
    ├─ 菜单 → Menu / MenuItem / ThemeMenu
    │
    ├─ 对话框 → DialogWindow / AboutDialog / Popup
    │
    ├─ 消息 → FloatingMessage / AlertToolTip / ToolTip
    │
    ├─ 标题栏 → TitleBar / DialogTitleBar
    │
    ├─ 列表 → ItemDelegate / CheckDelegate
    │
    ├─ 进度 → ProgressBar / WaterProgressBar / BusyIndicator
    │
    └─ 滑动 → Slider / TipsSlider / ScrollBar
```

## 按分类查阅

| 分类 | 文档 | 控件 |
|------|------|------|
| 按钮 | [buttons.md](buttons.md) | Button, RecommandButton, WarningButton, ToolButton, IconButton |
| 输入 | [inputs.md](inputs.md) | TextField, LineEdit, SearchEdit, PasswordEdit, SpinBox, ComboBox |
| 菜单 | [menus.md](menus.md) | Menu, MenuItem, ThemeMenu |
| 对话框与窗口 | [dialogs.md](dialogs.md) | ApplicationWindow, DialogWindow, AboutDialog, TitleBar |
| 面板与视觉 | [panels.md](panels.md) | BoxPanel, FloatingPanel, HighlightPanel |
| 列表 | [lists.md](lists.md) | ItemDelegate, CheckDelegate |
| 进度与滑动 | [progress.md](progress.md) | ProgressBar, WaterProgressBar, Slider |

## 相关文档

- [../theme/chameleon-qml.md](../theme/chameleon-qml.md) — Qt Quick Controls 2 Chameleon 插件、切换与调试
- [style.md](style.md) — Style 单例与应用级样式覆盖
- [dci-icon.md](dci-icon.md) — QML 中使用 dci 图标
- [effects.md](effects.md) — QML 视觉效果
- [dtk-global.md](dtk-global.md) — D.DTK 全局对象
