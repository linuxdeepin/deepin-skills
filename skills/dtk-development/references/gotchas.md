# DTK 常见陷阱与反模式

> 适用场景：排查 DTK 应用中与预期不符的行为，或实现前快速了解常见错误。以下按风险等级排列，高优先级项应先检查。

---

## 1. 版本与构建

### 1.1 DTK5/Qt5 与 DTK6/Qt6 混用

**症状：** 链接错误、运行时崩溃、控件行为异常。

**错误做法：**
```cmake
# ❌ 混用 Qt5 和 DTK6
find_package(Qt5 REQUIRED COMPONENTS Widgets)
find_package(Dtk6Widget REQUIRED)
```

**正确做法：**
```cmake
# ✅ 版本一致
find_package(Qt6 REQUIRED COMPONENTS Widgets)
find_package(Dtk6Widget REQUIRED)
```

CMake 包名、链接库、头文件、安装路径必须全部匹配同一 Qt/DTK 主版本。详见 [dtksrc-compile-debug.md](dtksrc-compile-debug.md) 第 1.2 节。

### 1.2 修改 DTK 源码后未验证实际加载

**症状：** 编译成功但运行时行为未变化。

**原因：** 系统可能仍加载了 `/usr/lib` 下的已安装版本，而非构建产物。

**验证方法：**
```bash
# 运行时检查实际加载的库路径
ldd ./myapp | grep dtk
# 或用 LD_LIBRARY_PATH 指向构建目录
LD_LIBRARY_PATH=<build-dir>/lib ./myapp
```

---

## 2. 主题与样式

### 2.1 使用 QSS 而非 DPalette

**症状：** 颜色不随主题切换更新，暗色主题下控件不可见。

**错误做法：**
```cpp
// ❌ QSS 硬编码颜色，不响应主题切换
widget->setStyleSheet("background-color: #f0f0f0; color: #000000;");
```

**正确做法：**
```cpp
// ✅ 使用 DPalette + DGuiApplicationHelper
auto palette = DGuiApplicationHelper::instance()->applicationPalette();
widget->setBackgroundRole(DPalette::ItemBackground);
```

详见 [theme/palette.md](theme/palette.md) 第 7 节。

### 2.2 直接使用 QPalette 而非 DPalette

**症状：** `TextTitle`、`TextWarning` 等 DTK 语义颜色不可用。

**错误做法：**
```cpp
// ❌ Qt 原生调色板缺少 DTK 语义色
QPalette pal = widget->palette();
QColor c = pal.color(QPalette::WindowText);
```

**正确做法：**
```cpp
// ✅ 使用 DPalette
auto dPal = DGuiApplicationHelper::instance()->applicationPalette();
QColor c = dPal.color(DPalette::TextTitle);
```

详见 [utilities/gui-helper.md](utilities/gui-helper.md) 第 9 节。

### 2.3 QML 中硬编码字体大小

**症状：** 系统字体缩放后 UI 比例失调。

**错误做法：**
```qml
// ❌ 硬编码像素大小
font.pixelSize: 14
```

**正确做法：**
```qml
// ✅ 使用 fontManager
font: D.DTK.fontManager.t6
```

详见 [declarative/dtk-global.md](declarative/dtk-global.md) 第 8 节。

### 2.4 QML 中硬编码主题颜色

**症状：** 暗色主题下文字不可见，或颜色不跟随系统。

**错误做法：**
```qml
// ❌ 硬编码颜色
color: "#f0f0f0"
```

**正确做法：**
```qml
// ✅ 使用 Palette + ColorSelector
backgroundColor: Palette {
    normal: D.DTK.makeColor(Color.Highlight)
    normalDark: D.DTK.makeColor(Color.Highlight)
}
```

详见 [declarative/color-selector.md](declarative/color-selector.md)。

### 2.5 QWidget Chameleon 与 QML Chameleon 名称混淆

**症状：** QML 加载不到风格，或 QWidget 设置风格名无效。

**关键区别：**
- QWidget: 风格键名为小写 `chameleon`（`-style chameleon`）
- QML: 风格名为首字母大写 `Chameleon`
- 不要把 `QT_QPA_PLATFORMTHEME` 和 `QT_STYLE_OVERRIDE` 的值混淆

详见 [theme/chameleon-qml.md](theme/chameleon-qml.md) 第 2 节。

### 2.6 不要把系统目录永久加入 QT_PLUGIN_PATH

**症状：** 加载到另一 Qt 版本的插件，导致崩溃或行为异常。

**错误做法：**
```bash
# ❌ 永久加入环境变量
export QT_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt6/plugins
```

**正确做法：**
```bash
# ✅ 仅在当前会话临时使用，或通过构建配置指定
./myapp -style chameleon
```

详见 [theme/chameleon-widget.md](theme/chameleon-widget.md)。

---

## 3. 图标系统

### 3.1 DCI 图标搜索路径滥用

**症状：** 调用 `setDciThemeSearchPaths()` 后图标查找行为异常。

**注意事项：**
- `DIconTheme::setDciThemeSearchPaths()` 影响整个进程的图标查找行为
- 常规应用应按 DCI 规范组织资源，不使用此 API
- 不要为了修复图标名称、目录或资源组织错误而调用它
- 不要把 `:/icons`、`/usr/share/icons` 等不符合 DCI 规则的目录当作通用配置

详见 [theme/dci.md](theme/dci.md) 第 2 节。

### 3.2 使用绝对路径而非基础名称查找图标

**症状：** 图标找不到，或主题切换后图标不更新。

**错误做法：**
```cpp
// ❌ 使用资源绝对路径
auto icon = DIconTheme::findQIcon(":/dsg/built-in-icons/default.dci");
```

**正确做法：**
```cpp
// ✅ 传基础名称，由 DTK 查找链路处理
auto icon = DIconTheme::findQIcon("default");
```

详见 [theme/dci.md](theme/dci.md) 第 3 节。

### 3.3 builtin 图标名称与 XDG 图标主题名称混淆

**症状：** 图标查找失败，返回空图标。

**注意：** `DBuiltinIconEngine` 使用 `icon_warning`、`icon_fail` 等内建名称，与 XDG 图标主题的 `dialog-warning`、`dialog-error` 不同。不要混用。

详见 [theme/builtin.md](theme/builtin.md)。

---

## 4. 配置系统

### 4.1 用 QSettings 替代 DConfig

**症状：** 配置无法被系统策略覆盖，不兼容 dde-application-manager。

**错误做法：**
```cpp
// ❌ 绕过 DConfig
QSettings settings("myapp", "settings");
bool canExit = settings.value("canExit", true).toBool();
```

**正确做法：**
```cpp
// ✅ 使用 DConfig + meta fallback
auto *config = new DConfig("org.example.settings", QString(), this);
bool canExit = config->isValid()
             ? config->value("canExit", true).toBool()
             : true;
```

详见 [config/concepts.md](config/concepts.md)。

### 4.2 配置服务不可用时阻塞主窗口

**症状：** DConfig 初始化失败时应用卡死或无法启动。

**正确做法：** 配置服务不可用时使用代码中的 fallback 默认值，通过日志记录原因，不阻塞主窗口创建。

详见 [config/dconfig-cpp.md](config/dconfig-cpp.md) 第 1.2 节。

### 4.3 appId 与配置 ID 混淆

**症状：** 配置读不到或读到错误的配置。

**关键区别：**
- `appId`：应用身份标识，由 `DSGApplication::id()` 或 `DSG_APP_ID` 定义
- `configId`（配置 ID）：DConfig 的配置标识，采用倒置域名格式如 `org.deepin.example.settings`
- 避免使用 `settings`、`example` 等全局泛化名称

**插件特别注意**：插件不是独立应用，必须使用**宿主应用**的 `appId`
（宿主是独立进程时以该进程自身为宿主应用，如 dde-tray-loader 的 appId
为 `org.deepin.dde.tray-loader`）。`appId` 会被 `dde-dconfig-daemon`
用于权限认证，随意构造会导致配置读写失败。

详见 [config/index.md](config/index.md) 步骤 1 和。

**插件 appId 检查清单**：
1. 确认代码运行在哪个宿主进程内（谁加载了这个模块）
2. 查找宿主应用的 desktop 文件 basename 或 `DSG_APP_ID`，作为 `appId`
3. 不确定时参见 [config/index.md](config/index.md) 步骤 1 的 appId 确定流程
4. 插件的 `configId` 在宿主命名空间下增加插件后缀，如
   `org.deepin.dde.control-center.myplugin`

### 4.4 版本升级缓存失效

**症状：** 版本升级后配置值回退为 meta 默认值。

**原因：** 缓存路径变化可能导致已有缓存失效。应确保 meta 默认值合理，并在代码中检测配置回退情况。

详见 [config/dconfig-debug.md](config/dconfig-debug.md)。

---

## 5. 窗口与平台

### 5.1 DWindow.enabled 未设置

**症状：** QML 窗口圆角、阴影、模糊等 DTK 特性不生效。

**错误做法：**
```qml
// ❌ 未启用 DTK 窗口样式
ApplicationWindow {
    DWindow.windowRadius: 18  // 不生效
}
```

**正确做法：**
```qml
// ✅ 先启用
ApplicationWindow {
    DWindow.enabled: true
    DWindow.windowRadius: 18
}
```

详见 [declarative/dwindow.md](declarative/dwindow.md) 第 8 节。

### 5.2 模糊窗口未设置半透明背景

**症状：** 模糊效果不正确或无效果。

**正确做法：**
```qml
DWindow.enableBlurWindow: true
DWindow.translucentBackground: true  // 必须同时设置
```

详见 [declarative/dwindow.md](declarative/dwindow.md) 第 8 节。

### 5.3 Wayland 与 X11 平台差异

**症状：** 窗口装饰、模糊效果、圆角在不同平台表现不一致。

**注意事项：**
- Wayland 下窗口装饰由 compositor 控制，部分 `DWindow` 属性行为不同
- 模糊效果依赖 compositor 支持
- 平台相关代码通过 `DPlatformHandle` / `DPlatformWindowInterface` 抽象

详见 [platform-abstraction.md](platform-abstraction.md)。

---

## 6. 字体

### 6.1 手动 setFont 而不使用 DFontSizeManager::bind

**症状：** 系统字体变化后控件字体不更新。

**错误做法：**
```cpp
// ❌ 手动设置字体，不跟随系统
QFont f = widget->font();
f.setPixelSize(14);
widget->setFont(f);
```

**正确做法：**
```cpp
// ✅ 绑定到字体层级
DFontSizeManager::instance()->bind(widget, DFontSizeManager::T6);
```

详见 [utilities/font-manager.md](utilities/font-manager.md) 第 8 节。

---

## 7. 应用初始化

### 7.1 使用 QApplication 而非 DApplication

**症状：** 主题不生效、单实例无效、字体不跟随系统。

**错误做法：**
```cpp
// ❌ 缺少 DTK 初始化
QApplication app(argc, argv);
```

**正确做法：**
```cpp
// ✅ DApplication 额外处理主题、字体、单实例
DApplication app(argc, argv);
```

详见 [app-dev-with-dtk.md](app-dev-with-dtk.md) 第 3.2 节。

### 7.2 翻译加载时机错误

**症状：** 菜单、窗口标题等未翻译。

**正确做法：** `DApplication::loadTranslator()` 必须在创建窗口、菜单和其他可翻译对象前调用。

详见 [app-dev-with-dtk.md](app-dev-with-dtk.md) 第 2.2 节。

---

## 8. Style 与自定义绘制

### 8.1 从鼠标位置而非 QStyleOption::state 判断状态

**症状：** 自定义控件 hover/press 状态不准确。

**正确做法：** 从 `QStyleOption::state` 读取状态，不查询鼠标位置。

详见 [widgets/style.md](widgets/style.md) 第 6 节。

### 8.2 initFrom() 不自动补齐 checked/down/selected

**症状：** 自定义 StyleOption 状态缺失。

**正确做法：** `initFrom()` 之后需手动设置 `checked`、`down`、`selected` 状态。

详见 [widgets/style.md](widgets/style.md) 第 6 节。

---

## 9. 日志

### 9.1 使用 dDebug 宏而非 Qt 原生日志

**症状：** 日志不输出或格式问题。

**正确做法：** DTK 应用使用 Qt 原生日志宏（`qDebug`/`qInfo`/`qWarning`），通过 `DLogManager` 注册 Appender。CMake 依赖 `Dtk6::Core`，不需要 `Dtk6::Log`。

详见 [app-dev-with-dtk.md](app-dev-with-dtk.md) 第 2.3 节。

---

## 10. debian 打包

### 10.1 QML 运行时包遗漏

**症状：** 安装后 QML 模块找不到。

**正确做法：** QML 运行时包（如 `qml6-module-qtquick-controls2-styles-chameleon`）放在 `Depends` 中，因为不会被 `${shlibs:Depends}` 自动推导。

详见 [app-dev-with-dtk.md](app-dev-with-dtk.md) 第 4.3 节。

---

## 相关文档

- [architecture.md](architecture.md) — 架构概览与问题定位
- [app-dev-with-dtk.md](app-dev-with-dtk.md) — 项目配置与最小示例
- [dtksrc-compile-debug.md](dtksrc-compile-debug.md) — 源码编译与调试
