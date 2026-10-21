# QML 窗口

提供 DTK 窗口及其附加属性，用于在 QML 场景中控制窗口外观与行为。

## DQuickWindow

### 定位

DTK QML 窗口类型。

### 功能能力总结

提供 DTK 窗口特有的属性和行为，包括窗口圆角、模糊效果、窗口阴影在内的平台视觉属性的 QML 接口。

### 使用场景

QML 中需要使用 DTK 扩展窗口属性（圆角、模糊、阴影）时。


---

## DQuickWindowAttached

### 定位

DTK 窗口附加属性提供者。

### 功能能力总结

为任意 QML Item 提供 DTK 窗口附加属性。使普通 QML Item 能够访问其所属 DTK 窗口的平台属性。

### 使用场景

需要在普通 QML Item 中访问所属 DTK 窗口的平台属性时。


---

## 最小使用示例

链接 `Dtk6::Declarative` 及示例使用的 GUI 依赖，使用 Qt6/DTK6。为 Qt Quick 窗口设置附加装饰属性；实际圆角效果取决于当前平台插件和窗口管理器。

```cpp
#include <DQuickWindow>
#include <QQuickWindow>

void setWindowDecoration(QQuickWindow *window)
{
    auto *settings = Dtk::Quick::DQuickWindow::qmlAttachedProperties(window);
    settings->setEnabled(true);
    settings->setWindowRadius(12);
}
```
