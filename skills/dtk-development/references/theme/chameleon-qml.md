# QML Chameleon（仅 v25）

本页只适用于 v25 的 dtkdeclarative。v20 QML 使用 Qt Quick/Qt Quick Controls 2 及 Qt 提供的 style，不加载本页。

具体 QML 类型、URI、import 版本和插件能力以目标构建环境实际安装的 QML module、`qmldir`、插件元数据及公开接口为准。

## 插件结构

`dtkdeclarative/chameleon/` 是 Qt Quick Controls 2 style 模块，包含插件、`qmldir` 和一组与 Qt Quick Controls 同名的 QML 文件，例如：

- `Button.qml`、`CheckBox.qml`、`RadioButton.qml`、`Switch.qml`；
- `TextField.qml`、`TextArea.qml`、`ComboBox.qml`、`SpinBox.qml`；
- `Slider.qml`、`ProgressBar.qml`、`ScrollBar.qml`；
- `Menu.qml`、`MenuItem.qml`、`Popup.qml`、`ToolTip.qml`；
- `ApplicationWindow.qml`、`Control.qml`、`Pane.qml`、`Frame.qml`。

这些文件不是 QWidget ChameleonStyle 的包装。例如标准 `Button` 可由风格模块映射到 `org.deepin.dtk` 中的 DTK QML 控件；实际的 `background`、`contentItem`、`indicator`、状态绑定和 palette 逻辑由 dtkdeclarative 实现。

## 模块名称与 Qt/DTK 构建差异

源码保留不同 Qt/DTK 主版本的构建路径：

- DTK5 路径安装到 `QtQuick/Controls.2/Chameleon`，对应 `qmldir` 声明 `module QtQuick.Controls.Chameleon`；
- 非 DTK5 路径可通过 `qt_add_qml_module()` 构建 URI 为 `Chameleon` 的模块；
- 使用 `QQuickStylePlugin` 接口时，插件名称为大小写敏感的 `Chameleon`。

这些是 v25 内部仍可能存在的构建差异。不要仅凭示例猜测模块路径，应检查目标环境实际安装的 `qmldir`、QML import path 和插件元数据；也不要把 QWidget 的小写键名 `chameleon` 与 QML 风格名 `Chameleon` 混淆。

## 风格插件与 Style 单例

dtkdeclarative 中的两层 style 职责不同：

| 层次 | 名称 | 职责 |
|---|---|---|
| Qt Quick Controls 2 风格插件 | `Chameleon` | 把标准 Qt Quick Controls 类型映射到 DTK QML 实现 |
| DTK 样式数据单例 | `org.deepin.dtk.style` 中的 `Style` | 提供尺寸、间距、圆角和各状态调色板 |

应用级 `Style` 覆盖方式和调试方法见 [QML Style 单例与应用级样式覆盖](../declarative/style.md)。

## 启用和对比风格

必须在加载 QML、创建第一个 Qt Quick Controls 控件前选择风格：

```bash
QT_QUICK_CONTROLS_STYLE=Chameleon ./my-qml-app
QT_QUICK_CONTROLS_STYLE=Basic ./my-qml-app
QT_QUICK_CONTROLS_STYLE=Fusion ./my-qml-app

./my-qml-app -style Chameleon
./my-qml-app -style Basic
```

代码中可在加载 QML 前调用：

```cpp
QQuickStyle::setStyle("Chameleon");
```

风格初始化后不适合在同一进程内切换。进行视觉对比时分别启动进程。

## 插件加载诊断

```bash
QT_DEBUG_PLUGINS=1 QT_QUICK_CONTROLS_STYLE=Chameleon ./my-qml-app
```

依次检查：

1. 风格是否在创建第一个 Qt Quick Controls 控件前设置；
2. QML import path 中是否存在目标环境发布的 Chameleon module、`qmldir` 和插件；
3. Qt/DTK 主版本、架构和构建配置是否与 QML module 一致；
4. `QML2_IMPORT_PATH` 或对应 Qt 版本的 import path 是否精确指向本地构建/安装目录；
5. 代码、配置文件或启动脚本是否覆盖 `QT_QUICK_CONTROLS_STYLE`。

不要永久加入宽泛的系统 QML 目录，以免加载到另一 Qt/DTK 版本的模块。

## palette 或样式数据不生效时

保持绑定不变，分别以 Chameleon 和 Qt 内置风格启动进程进行对比。若只有 Chameleon 异常，检查 DTK QML 控件读取的属性、局部 palette 覆盖以及 `Style` 单例数据；若各风格均异常，检查属性绑定、控件层级、状态条件和实际参与渲染的对象。

不同风格可能读取不同属性，对比结果只用于定位问题层级，不保证每个 palette role 产生相同视觉效果。

## 相关文档

- [QML 控件索引](../declarative/index.md)
- [QML Style 单例与应用级样式覆盖](../declarative/style.md)
- [palette.md](palette.md) — DTK 调色板语义
- [theme-switch.md](theme-switch.md) — 主题切换
- [dci.md](dci.md) — DCI 图标主题与状态
