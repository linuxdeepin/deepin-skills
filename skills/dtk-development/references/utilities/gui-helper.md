# DGuiApplicationHelper / DApplicationHelper

## 1. 概述与适用场景

`DGuiApplicationHelper`（dtkgui）是 DTK C++ 主题系统的核心入口。v25 的
dtkdeclarative 另提供 `DApplicationHelper` QML 绑定；v20 不提供 DTK QML 绑定。

**适用场景：**
- 获取/切换亮暗主题
- 监听主题变化刷新 UI
- 获取调色板/字体管理器
- 判断平台类型（Wayland/X11/平板）
- 单实例控制

## 2. 类关系

```
DGuiApplicationHelper (dtkgui, C++ 单例)
    │
    ├─ DApplicationHelper (v25 QML 单例)
    │   └─ QML: ApplicationHelper.LightType / DarkType
    │
    └─ DTK (dtkdeclarative, QML 全局对象)
        └─ QML: D.DTK.themeType / D.DTK.fontManager / ...
```

> `DGuiApplicationHelper::instance()` 与 QML `ApplicationHelper` 是同一单例对象。

## 3. ColorType 枚举

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `UnknownType` | 未知 |
| 1 | `LightType` | 浅色主题 |
| 2 | `DarkType` | 深色主题 |

## 4. SizeMode 枚举

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `NormalMode` | 正常模式 |
| 1 | `CompactMode` | 紧凑模式 |

判断紧凑模式快捷方式：

```cpp
if (DGuiApplicationHelper::isCompactMode()) { /* 紧凑模式 */ }
```

## 5. Attribute 枚举（位标志）

### 可写属性

| 值 | 名称 | 说明 |
|----|------|------|
| 1 << 0 | `UseInactiveColorGroup` | 使用非活跃颜色组 |
| 1 << 1 | `ColorCompositing` | 启用颜色合成 |
| 1 << 2 | `DontSaveApplicationTheme` | 不保存应用主题 |

### 只读属性

| 值 | 名称 | 说明 |
|----|------|------|
| 1 << 22 | `IsDeepinPlatformTheme` | 是否 Deepin 平台主题 |
| 1 << 23 | `IsDXcbPlatform` | 是否 DXcb 平台 |
| 1 << 24 | `IsXWindowPlatform` | 是否 X11 |
| 1 << 25 | `IsTableEnvironment` | 是否平板环境 |
| 1 << 26 | `IsDeepinEnvironment` | 是否 Deepin 环境 |
| 1 << 27 | `IsSpecialEffectsEnvironment` | 是否特效环境 |
| 1 << 28 | `IsWaylandPlatform` | 是否 Wayland |
| 1 << 29 | `HasAnimations` | 是否有动画 |
| 1 << 30 | `HasInWindowBlur` | 是否支持窗口内模糊 |

## 6. 核心 API

### 6.1 单例与主题

```cpp
#include <DGuiApplicationHelper>

// 获取单例
auto *helper = DGuiApplicationHelper::instance();

// 获取当前主题类型
DGuiApplicationHelper::ColorType type = helper->themeType();

// 切换主题
helper->setPaletteType(DGuiApplicationHelper::DarkType);
helper->setPaletteType(DGuiApplicationHelper::LightType);
```

### 6.2 监听主题变化

```cpp
connect(DGuiApplicationHelper::instance(),
        &DGuiApplicationHelper::themeTypeChanged,
        this, &MyWidget::onThemeChanged);

void MyWidget::onThemeChanged(DGuiApplicationHelper::ColorType type) {
    if (type == DGuiApplicationHelper::DarkType) {
        // 深色主题处理
    } else {
        // 浅色主题处理
    }
    update();
}
```

### 6.3 调色板操作

```cpp
// 获取应用调色板
DPalette palette = helper->applicationPalette();

// 获取指定主题的调色板
DPalette darkPalette = helper->applicationPalette(DGuiApplicationHelper::DarkType);

// 获取标准调色板（系统默认）
DPalette standardLight = DGuiApplicationHelper::standardPalette(DGuiApplicationHelper::LightType);

// 设置自定义调色板
helper->setApplicationPalette(customPalette);

// 生成调色板颜色
DGuiApplicationHelper::generatePaletteColor(palette, DPalette::TextTitle, DGuiApplicationHelper::LightType);
DGuiApplicationHelper::generatePalette(palette, DGuiApplicationHelper::DarkType);
```

### 6.4 颜色工具

```cpp
// 调整颜色（偏移量 -128 ~ 127）
QColor adjusted = DGuiApplicationHelper::adjustColor(
    baseColor,
    10,   // 色相偏移
    20,   // 饱和度偏移
    -10,  // 明度偏移
    0, 0, 0, 0  // RGBA 偏移
);

// 混合颜色
QColor blended = DGuiApplicationHelper::blendColor(QColor("#FF0000"), QColor("#0000FF"));

// 颜色转主题类型
DGuiApplicationHelper::ColorType type = DGuiApplicationHelper::toColorType(someColor);
```

### 6.5 平台判断

```cpp
// 判断平台
if (DGuiApplicationHelper::testAttribute(DGuiApplicationHelper::IsWaylandPlatform)) {
    // Wayland 特殊处理
}

if (DGuiApplicationHelper::isXWindowPlatform()) {
    // X11 特殊处理
}

if (DGuiApplicationHelper::testAttribute(DGuiApplicationHelper::IsTableEnvironment)) {
    // 平板模式
}

if (DGuiApplicationHelper::testAttribute(DGuiApplicationHelper::IsSpecialEffectsEnvironment)) {
    // 特效环境
}
```

### 6.6 单实例控制

```cpp
// 确保应用只运行一个实例
if (!DGuiApplicationHelper::setSingleInstance("my-app-id")) {
    qWarning() << "Another instance is running";
    exit(0);
}

// 设置检查间隔
DGuiApplicationHelper::setSingleInstanceInterval(3000);
```

### 6.7 窗口效果属性

```cpp
// 设置属性
DGuiApplicationHelper::setAttribute(DGuiApplicationHelper::UseInactiveColorGroup, true);
DGuiApplicationHelper::setAttribute(DGuiApplicationHelper::ColorCompositing, true);

// 查询属性
bool useInactive = DGuiApplicationHelper::testAttribute(DGuiApplicationHelper::UseInactiveColorGroup);
```

### 6.8 尺寸模式

```cpp
// 获取/设置尺寸模式
auto mode = helper->sizeMode();
helper->setSizeMode(DGuiApplicationHelper::CompactMode);
helper->resetSizeMode(); // 恢复系统默认
```

## 7. QML 用法

### 7.1 ApplicationHelper

```qml
import org.deepin.dtk 1.0

// 判断主题类型
if (ApplicationHelper.themeType === ApplicationHelper.LightType) {
    // 浅色主题
} else if (ApplicationHelper.themeType === ApplicationHelper.DarkType) {
    // 深色主题
}

// 切换主题
ApplicationHelper.setPaletteType(ApplicationHelper.DarkType)

// 监听主题变化
Connections {
    target: ApplicationHelper
    function onThemeTypeChanged(type) { /* 刷新 UI */ }
}
```

### 7.2 D.DTK 代理属性

```qml
import org.deepin.dtk 1.0 as D

// 主题类型（同 ApplicationHelper.themeType）
D.DTK.themeType

// 是否有模糊窗口
D.DTK.hasBlurWindow

// 是否有合成
D.DTK.hasComposite

// 是否有动画
D.DTK.hasAnimation
```

## 8. 信号列表

| 信号 | 参数 | 说明 |
|------|------|------|
| `themeTypeChanged` | `ColorType` | 主题类型变化 |
| `paletteTypeChanged` | `ColorType` | 调色板类型变化 |
| `newProcessInstance` | `qint64 pid, QStringList arguments` | 新实例启动 |
| `fontChanged` | `QFont` | 字体变化 |
| `applicationPaletteChanged` | 无 | 调色板变化 |
| `sizeModeChanged` | `SizeMode` | 尺寸模式变化 |

## 9. 常见错误与避坑

### 错误 1：直接使用 QPalette 而非 DPalette

```cpp
// ❌ 错误：QPalette 没有 DTK 扩展颜色
QPalette palette = widget->palette();
QColor color = palette.color(QPalette::Text); // 缺少 TextTitle 等 DTK 颜色

// ✅ 正确：使用 DPalette
DPalette palette = DGuiApplicationHelper::instance()->applicationPalette();
QColor titleColor = palette.color(DPalette::TextTitle);
```

### 错误 2：使用废弃的 setThemeType

```cpp
// ❌ 错误：setThemeType 已废弃
DGuiApplicationHelper::instance()->setThemeType(DGuiApplicationHelper::DarkType);

// ✅ 正确：使用 setPaletteType
DGuiApplicationHelper::instance()->setPaletteType(DGuiApplicationHelper::DarkType);
```

### 错误 3：在错误的线程调用 instance()

```cpp
// ❌ 错误：在非 GUI 线程调用
QThread::create([] {
    auto *helper = DGuiApplicationHelper::instance(); // 可能不安全
})->start();

// ✅ 正确：在 GUI 线程使用，通过信号跨线程
```

## 10. 相关文档

- [palette.md](../theme/palette.md) - 调色板规范
- [font-manager.md](font-manager.md) - 字体管理器
- [theme-switch.md](../theme/theme-switch.md) - 主题切换机制
- [window-manager.md](window-manager.md) - 窗口管理助手
- [dtk-global.md](../declarative/dtk-global.md) - QML DTK 全局对象
