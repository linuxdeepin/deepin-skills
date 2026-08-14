# 示例

DTK 提供可运行的示例应用，帮助理解控件使用方式。推荐通过包管理器安装。

## QWidget 示例

dtkwidget 提供 `collections` 示例，一个包含 16 个分类、64+ 子示例的完整 Demo 应用。

**安装：**
```bash
sudo apt install dtkwidget5-examples    # DTK5
sudo apt install dtk6widget-examples    # DTK6
```

**运行：**
```bash
/usr/lib/*/dtk5/DWidget/examples/collections   # DTK5
/usr/lib/*/dtk6/DWidget/examples/collections   # DTK6
```

**分类总览：**

| 分类 | 演示控件 |
|------|----------|
| Button | DPushButton, DWarningButton, DSuggestButton, DToolButton, DIconButton, DButtonBox, DFloatingButton, DSwitchButton, DRadioButton, DCheckBox, DComboBox, DFontComboBox, DSearchComboBox |
| Edit | DSearchEdit, DLineEdit, DIpv4LineEdit, DPasswordEdit, DFileChooserEdit, DSpinBox, DTextEdit, DCrumbEdit, DKeySequenceEdit |
| Slider | DSlider（水平/垂直、图标、刻度） |
| Menu | DMenu（右键菜单、子菜单、动画高亮） |
| ListView | DListView, DStandardItem, DViewItemAction, DBackgroundGroup, DTreeView, DHeaderView, DColumnView |
| Window | DTitlebar（4 种样式）, DMainWindow, DStatusBar, DTabBar |
| ToolTip | DToolTip, DArrowRectangle |
| Spinner | DSpinner（5 种尺寸） |
| Dialog | DDialog, DFileDialog, DMessageManager, DFloatingMessage |
| ProgressBar | DProgressBar, DWaterProgress, DColoredProgressBar, DIndeterminateProgressbar |
| Layout | DFrame, DSplitter, DVerticalLine, DHorizontalLine |
| ScrollBar | DScrollArea |
| RubberBand | DRubberBand |
| Widget | DCalendarWidget, DTableWidget, DMPRISControl |
| LCDNumber | DLCDNumber |
| ImageViewer | DImageViewer（缩放/旋转/裁剪） |

**源码路径：** `dtkwidget/examples/collections/`，随 dtkwidget 主项目编译（cmake option `BUILD_EXAMPLES`，默认 ON）。

## v25 QML 示例

> 仅适用于 v25。v20 没有 DTK QML 示例，QML 应直接参考 Qt Quick 与
> Qt Quick Controls 2 示例。

dtkdeclarative 提供 `exhibition` 应用，一个完整的 DTK QML 控件画廊，带源代码查看功能。

**安装：**
```bash
sudo apt install dtk-exhibition       # DTK5
sudo apt install dtk6-exhibition      # DTK6
```

**运行：**
```bash
dtk-exhibition                        # DTK5
/usr/lib/*/dtk6/DDeclarative/dtk6-exhibition  # DTK6
```

**分类总览：**

| 分类 | 演示内容 |
|------|----------|
| Buttons | 所有按钮类型、Switch、ComboBox、CheckBox、RadioButton、ButtonBox，含 CrystalColor 族 |
| Lists | ItemDelegate（背景/指示器/级联选中/四角/内容流），CheckDelegate + ButtonGroup |
| Menus | 右键菜单、搜索过滤菜单（ObjectModelProxy）、级联子菜单、动态菜单 |
| Notify | 系统通知（DTK.sendSystemMessage）、应用通知（FloatingMessage）、应用角标 |
| Dialogs | 8 种 DialogWindow（通知/授权/警告/组合/进度/WiFi/错误/关于） |
| Popups | 浮动面板（勿扰/蓝牙/音量/网络）、文件属性对话框 |
| Sliders | 水平/垂直 Slider（6 种 HandleType）、TipsSlider 刻度 |
| Inputs | LineEdit（alert）、SearchEdit、IpV4LineEdit、PasswordEdit、PlusMinusSpinBox、TextArea |
| KeySequence | 快捷键编辑 |
| SideBar | 侧边栏面板（收藏/书签/标签/磁盘） |
| Progress | BusyIndicator（多尺寸/亮暗）、ProgressBar/EmbeddedProgressBar/WaterProgressBar |
| Mask | 自定义窗口形状（DWindow.clipPath） |
| ToolBar | TitleBar 变体 + FloatingPanel 工具栏 |
| Group | ControlGroup + ControlGroupItem 折叠组 |

**源码路径：** `dtkdeclarative/examples/exhibition/`，随 dtkdeclarative 主项目编译。

## 相关文档

- [widgets/index.md](widgets/index.md) — QWidget 控件文档
- [declarative/index.md](declarative/index.md) — v25 DTK QML 控件文档
