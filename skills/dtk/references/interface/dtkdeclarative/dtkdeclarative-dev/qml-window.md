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
