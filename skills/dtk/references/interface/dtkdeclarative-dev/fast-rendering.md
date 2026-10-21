# 快速渲染

提供 QML 场景中的帧缓冲区位块传输渲染和视口裁剪渲染能力。

## DQuickBlitFramebuffer

### 定位

QML 场景中的帧缓冲区位块传输渲染项。

### 功能能力总结

将离屏帧缓冲区内容通过位块传输方式渲染到 QML 场景中。

### 使用场景

需要将离屏渲染的帧缓冲区内容高效地呈现到 QML 场景中时。


---

## DQuickItemViewport

### 定位

QML 场景中的视口裁剪渲染项。

### 功能能力总结

提供将指定源项的局部区域裁剪并渲染到视口的能力。

### 使用场景

需要在 QML 中实现视口裁剪或局部区域渲染时。


---

## 最小使用示例

链接 `Dtk6::Declarative` 及示例使用的 GUI 依赖，使用 Qt6/DTK6。为已有 QQuickItem 创建圆角视口；效果需要运行中的 Qt Quick 场景图。

```cpp
#include <DQuickItemViewport>
#include <QQuickItem>

void addViewport(QQuickItem *parent, QQuickItem *source)
{
    auto *viewport = new Dtk::Quick::DQuickItemViewport(parent);
    viewport->setSourceItem(source);
    viewport->setWidth(160);
    viewport->setHeight(100);
    viewport->setRadius(12);
}
```
