# QWidget Chameleon

本页适用于 v20 和 v25 的 QWidget 技术栈。具体接口、枚举和控件是否可用，以目标构建环境实际发布且由编译器使用的公共头文件为准。

## 实现结构

```text
QCommonStyle
└── DStyle                         dtkwidget
    └── ChameleonStyle             dde-qtintegration

QStylePlugin
└── ChameleonStylePlugin
    └── create("chameleon") → ChameleonStyle
```

`DStyle` 提供 DTK 扩展元素、度量、标准图标和状态画刷；`ChameleonStyle` 实现 `drawPrimitive()`、`drawControl()`、`drawComplexControl()`、布局、命中测试、动画和 widget polish。插件键名为小写 `chameleon`，安装在 Qt styles 插件目录。

Deepin 平台主题通常把它作为 QWidget 首选风格，`DApplication` 也可能在应用初始化阶段选择该风格。因此诊断实际风格时同时检查显式设置、平台主题和应用初始化逻辑。

自定义控件复用 `DStyle`、`DStyleHelper`、`QStyleOption` 和 palette 的方法见 [DStyle / ChameleonStyle 使用指南](../widgets/style.md)。

## 临时指定和对比风格

优先通过启动参数或环境变量临时切换，不把诊断设置写入业务代码：

```bash
./my-widget-app -style chameleon
./my-widget-app -style fusion

QT_STYLE_OVERRIDE=chameleon ./my-widget-app
QT_STYLE_OVERRIDE=fusion ./my-widget-app
```

也可在创建普通控件前调用 `QApplication::setStyle("chameleon")`。输出实际加载结果和可用键名：

```cpp
qInfo() << "current style:" << QApplication::style()->objectName();
qInfo() << "available styles:" << QStyleFactory::keys();
```

## 插件加载诊断

```bash
QT_DEBUG_PLUGINS=1 ./my-widget-app -style chameleon
```

依次检查：

1. `QStyleFactory::keys()` 是否包含 `chameleon`，实际 style 的 `objectName()` 是否符合预期；
2. Qt 是否扫描到包含 Chameleon 的 `styles` 插件目录；
3. 应用使用的 Qt 主版本、架构和构建配置是否与插件一致；
4. 代码中的 `setStyle()`、平台主题或启动脚本是否再次覆盖风格；
5. 测试本地构建时，`QT_PLUGIN_PATH` 是否只指向精确的构建或安装目录。

不要把整个系统目录永久加入 `QT_PLUGIN_PATH`，否则可能加载到另一 Qt 版本的插件。

## palette 不生效时

保持业务代码和 palette 设置不变，只替换风格进行对比：

```bash
./my-widget-app -style chameleon
./my-widget-app -style fusion
```

如果 palette 在 Fusion 下生效、在 Chameleon 下不生效，检查对应 `drawPrimitive()`、`drawControl()` 或 `drawComplexControl()` 分支实际读取的 palette role、`DPalette::ColorType`、DCI 或专用绘制逻辑。

如果两种风格都不生效，优先检查：

- palette 是否设置到真正参与绘制的内部控件；
- model/delegate 或 Style Sheet 是否覆盖颜色；
- Active、Inactive、Disabled 颜色组是否正确；
- 自绘区域是否与 `subControlRect()` 和 `hitTestComplexControl()` 一致。

切换风格的结果用于定位问题层级，不代表所有 palette role 在不同风格中必须呈现完全相同的效果。

## 相关文档

- [DStyle / ChameleonStyle 使用指南](../widgets/style.md) — 自定义控件绘制与状态颜色
- [palette.md](palette.md) — DTK 语义色和 palette
- [theme-switch.md](theme-switch.md) — 主题切换
- [dci.md](dci.md) — DCI 图标主题与状态
