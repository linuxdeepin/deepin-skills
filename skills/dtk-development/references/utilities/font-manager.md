# DFontSizeManager / DFontManager

## 1. 概述与适用场景

DTK 提供两级字体管理：`DFontManager`（dtkgui）和 `DFontSizeManager`（dtkwidget）。

**适用场景：**
- 统一应用字体大小
- 响应系统字体变化
- 按语义选择字体大小（标题/正文/提示等）

## 2. 两个类的关系

| 特性 | DFontManager (dtkgui) | DFontSizeManager (dtkwidget) |
|------|----------------------|------------------------------|
| 访问方式 | `DGuiApplicationHelper::instance()->fontManager()` | `DFontSizeManager::instance()` |
| 继承 QObject | 是 | 否 |
| bind()/unbind() | 不支持 | 支持（自动更新 QWidget 字体） |
| QML 访问 | v25：`D.DTK.fontManager`；v20 无 DTK QML 绑定 | 无直接 QML 绑定 |
| 基准字体 | baseFont()/setBaseFont() | setFontGenericPixelSize() |
| 字体变化信号 | fontChanged() | 无（不是 QObject） |

## 3. SizeType 枚举与像素大小

| 枚举 | 像素大小 | 语义用途 |
|------|---------|---------|
| `T1` | 40 px | 超大标题 |
| `T2` | 30 px | 大标题 |
| `T3` | 24 px | 中标题 |
| `T4` | 20 px | 小标题 |
| `T5` | 16 px | 强调文本 |
| `T6` | 14 px | 正文（系统默认基准） |
| `T7` | 13 px | 辅助文本 |
| `T8` | 12 px | 小号文本 |
| `T9` | 11 px | 提示文本 |
| `T10` | 10 px | 极小文本 |
| `T11` | 8 px | 标注文本 |

> 实际像素大小 = 基准值 + fontPixelSizeDiff。当系统字体大小改变时，`fontPixelSizeDiff` 自动计算偏移。

## 4. DFontSizeManager (dtkwidget) 用法

### 4.1 绑定控件字体

```cpp
#include <DFontSizeManager>

auto *label = new DLabel("标题");
DFontSizeManager::instance()->bind(label, DFontSizeManager::T4);

auto *desc = new DLabel("描述");
DFontSizeManager::instance()->bind(desc, DFontSizeManager::T7);
```

绑定后，系统字体变化时控件字体自动更新。也可指定字重：

```cpp
DFontSizeManager::instance()->bind(label, DFontSizeManager::T4, QFont::Bold);
```

### 4.2 解绑

```cpp
DFontSizeManager::instance()->unbind(widget);
```

### 4.3 获取字体

```cpp
auto *mgr = DFontSizeManager::instance();

// 获取指定大小的字体
QFont titleFont = mgr->get(DFontSizeManager::T3);
QFont bodyFont = mgr->get(DFontSizeManager::T6);

// 便捷方法
QFont f1 = mgr->t1();  // 等价于 get(T1)
QFont f4 = mgr->t4();  // 等价于 get(T4)
QFont t6 = mgr->t6();  // 等价于 get(T6)

// 指定基准字体和字重
QFont customFont = mgr->get(DFontSizeManager::T4, QFont::Medium, baseFont);
```

### 4.4 修改像素大小

```cpp
// 修改某个级别的像素大小
mgr->setFontPixelSize(DFontSizeManager::T4, 22);

// 修改基准大小（所有级别等比缩放）
mgr->setFontGenericPixelSize(16);
```

## 5. DFontManager (dtkgui) 用法

### 5.1 基本操作

```cpp
#include <DFontManager>

auto *fm = DGuiApplicationHelper::instance()->fontManager();

// 获取字体
QFont title = fm->get(DFontManager::T3);
QFont body = fm->get(DFontManager::T6);

// 便捷方法
QFont t1 = fm->t1();
QFont t6 = fm->t6();

// 基准字体
QFont base = fm->baseFont();
fm->setBaseFont(QFont("Noto Sans CJK SC", 14));
fm->resetBaseFont(); // 恢复默认
```

### 5.2 像素大小查询

```cpp
int px = fm->fontPixelSize(DFontManager::T6); // 14
int pxFromFont = DFontManager::fontPixelSize(someFont); // 从 QFont 获取
```

### 5.3 监听字体变化

```cpp
connect(DGuiApplicationHelper::instance()->fontManager(),
        &DFontManager::fontChanged,
        this, &MyWidget::onFontChanged);
```

## 6. QML 用法

```qml
import org.deepin.dtk 1.0

Text {
    // 使用 fontManager 获取字体
    font: D.DTK.fontManager.t4
}

Text {
    font: D.DTK.fontManager.t6
}
```

## 7. 选择决策

```
需要设置字体大小？
    │
    ├─ QWidget 应用？
    │   └─ 使用 DFontSizeManager::bind() 自动跟随系统
    │
    ├─ v25 DTK QML 应用？
    │   └─ 使用 D.DTK.fontManager.tN
    ├─ v20 QML 应用？
    │   └─ 使用 Qt font 属性或应用自建桥接
    │
    ├─ 需要自定义基准字体？
    │   └─ DFontManager::setBaseFont() 或 DFontSizeManager::setFontGenericPixelSize()
    │
    └─ 只需获取一次字体？
        └─ DFontSizeManager::instance()->get(T6)
```

## 8. 常见错误与避坑

### 错误 1：手动 setFont 而不 bind

```cpp
// ❌ 错误：手动设置字体，系统字体变化时不会自动更新
label->setFont(QFont("", 14));

// ✅ 正确：使用 bind 自动跟随系统
DFontSizeManager::instance()->bind(label, DFontSizeManager::T6);
```

### 错误 2：在 QML 中硬编码像素大小

```qml
// ❌ 错误：硬编码像素大小
font.pixelSize: 14

// ✅ 正确：使用 fontManager
font: D.DTK.fontManager.t6
```

## 9. 相关文档

- [gui-helper.md](gui-helper.md) - DGuiApplicationHelper
- [palette.md](../theme/palette.md) - 调色板规范
