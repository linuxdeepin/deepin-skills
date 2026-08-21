# 快捷面板插件开发指南

本文档说明如何开发带快捷面板的托盘插件。**纯托盘插件无需阅读此文档**。

## 概述

快捷面板是任务栏展开后的区域，用于显示常用功能的快捷控件（如音量、亮度、蓝牙等）。快捷面板插件同时显示：
- 托盘图标：显示在托盘区的小图标
- 快捷面板控件：显示在快捷面板展开区域的大控件

## flags 设置

快捷面板插件必须使用 `Type_Quick` 类型，搭配布局标志：

| flags 组合 | 布局尺寸 | 适用场景 |
|------------|----------|----------|
| `Type_Quick \| Quick_Panel_Single` | 70x60 | 简单开关（如蓝牙） |
| `Type_Quick \| Quick_Panel_Multi` | 150x60 | 双列控件 |
| `Type_Quick \| Quick_Panel_Full` | 310x60 | 复杂控件（如音量滑块） |

> **重要**：`Type_Tray` 和 `Type_Quick` 是互斥的，不应同时使用。

## 控件尺寸规范

| 控件类型 | 尺寸 | 设置方式 |
|----------|------|----------|
| 快捷面板-单列 | 70x60 | `setFixedHeight(Dock::QUICK_ITEM_HEIGHT)` |
| 快捷面板-双列 | 150x60 | `setFixedHeight(Dock::QUICK_ITEM_HEIGHT)` |
| 快捷面板-四列 | 310x60 | `setFixedHeight(Dock::QUICK_ITEM_HEIGHT)` |
| 快捷面板图标 | 24x24 | `setFixedSize(Dock::QUICK_PANEL_ICON_SIZE)` |

> **关键**：快捷面板控件只使用 `setFixedHeight(Dock::QUICK_ITEM_HEIGHT)`，**不要使用 `setFixedSize()` 锁定宽度**，框架会根据 `Quick_Panel_*` 标志自动设置宽度。

## itemWidget 实现

快捷面板控件通过 `itemWidget(Dock::QUICK_ITEM_KEY)` 返回：

```cpp
#define MYPLUGIN_KEY "myplugin-item-key"

QWidget *MyPlugin::itemWidget(const QString &itemKey)
{
    // 快捷面板控件（使用 Dock::QUICK_ITEM_KEY）
    if (itemKey == Dock::QUICK_ITEM_KEY) {
        return m_quickPanel.data();
    }
    // 托盘图标控件（使用自定义 key）
    if (itemKey == MYPLUGIN_KEY) {
        return m_trayIcon.data();
    }
    return nullptr;
}
```

> **关键点**：
> - 注册时使用自定义 key：`m_proxyInter->itemAdded(this, MYPLUGIN_KEY)`
> - `itemWidget` 必须处理 `Dock::QUICK_ITEM_KEY`，返回快捷面板控件
> - `itemWidget` 必须处理自定义 key，返回托盘图标控件

## itemPopupApplet 与 Tooltip

**框架逻辑**：当鼠标 hover 托盘图标时，框架检查 `itemPopupApplet` 返回的控件是否存在且可见。如果存在，则认为有弹出面板，**不显示 tooltip**。

### 正确用法

| 场景 | `itemPopupApplet` 返回值 | 说明 |
|------|---------------------------|------|
| 有弹出面板（如音量滑块） | 返回弹出面板控件 | 点击托盘图标显示弹窗 |
| 无弹出面板 | 返回 `nullptr` | 点击托盘图标执行命令或无操作 |
| 有快捷面板 | 返回 `nullptr` | 快捷面板通过 `itemWidget(QUICK_ITEM_KEY)` 提供 |

### 错误示例

```cpp
// 错误！返回快捷面板控件会导致 tooltip 不显示
QWidget *MyPlugin::itemPopupApplet(const QString &itemKey)
{
    if (itemKey == MYPLUGIN_KEY) {
        return m_quickPanel.data();  // ❌ 错误：快捷面板不应从这里返回
    }
    return nullptr;
}
```

### 正确示例

```cpp
// 正确：快捷面板通过 itemWidget(QUICK_ITEM_KEY) 提供
QWidget *MyPlugin::itemWidget(const QString &itemKey)
{
    if (itemKey == Dock::QUICK_ITEM_KEY) {
        return m_quickPanel.data();  // ✓ 快捷面板从这里返回
    }
    if (itemKey == MYPLUGIN_KEY) {
        return m_trayIcon.data();
    }
    return nullptr;
}

QWidget *MyPlugin::itemPopupApplet(const QString &itemKey)
{
    Q_UNUSED(itemKey)
    return nullptr;  // ✓ 无弹出面板，返回 nullptr
}
```

> **注意**：快捷面板控件和弹出面板控件是不同的概念：
> - **快捷面板**：显示在快捷面板区域，通过 `itemWidget(QUICK_ITEM_KEY)` 返回
> - **弹出面板**：点击托盘图标后弹出的控件，通过 `itemPopupApplet(MYPLUGIN_KEY)` 返回

## 快捷面板子页面实现

当快捷面板插件需要点击后显示详情页面（子页面）时，使用 `requestSetAppletVisible()` 主动请求显示。

> **与托盘弹出面板的区别**：托盘弹出面板由 `itemPopupApplet` 返回，点击托盘图标时框架自动显示；快捷面板子页面需要插件主动调用 `requestSetAppletVisible` 请求显示。

### 1. 实现 itemPopupApplet

```cpp
QWidget *MyPlugin::itemPopupApplet(const QString &itemKey)
{
    if (itemKey == Dock::QUICK_ITEM_KEY || itemKey == "myplugin") {
        if (!m_detailWidget) {
            m_detailWidget.reset(new MyDetailWidget);
        }
        return m_detailWidget.data();
    }
    return nullptr;
}
```

### 2. 快捷面板控件发出点击信号

```cpp
class MyQuickPanel : public QWidget
{
    Q_OBJECT

signals:
    void requestShowDetail();

protected:
    void mousePressEvent(QMouseEvent *event) override
    {
        if (event->button() == Qt::LeftButton) {
            emit requestShowDetail();
        }
        QWidget::mousePressEvent(event);
    }
};
```

### 3. 插件连接信号并请求显示子页面

```cpp
void MyPlugin::init(PluginProxyInterface *proxyInter)
{
    m_proxyInter = proxyInter;
    m_quickPanel.reset(new MyQuickPanel);
    
    connect(m_quickPanel.data(), &MyQuickPanel::requestShowDetail, this, [this]() {
        if (m_detailWidget) {
            m_detailWidget->updateData();
        }
        // 关键：请求显示子页面
        m_proxyInter->requestSetAppletVisible(this, "myplugin", true);
    });
    
    m_proxyInter->itemAdded(this, "myplugin");
}
```

### 4. 子页面控件实现

```cpp
class MyDetailWidget : public QWidget
{
    Q_OBJECT

public:
    explicit MyDetailWidget(QWidget *parent = nullptr)
        : QWidget(parent)
    {
        setAttribute(Qt::WA_TranslucentBackground);
        setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Expanding);
        setFixedWidth(Dock::QUICK_ITEM_FULL_WIDTH);
    }

    QSize sizeHint() const override
    {
        return QSize(Dock::QUICK_ITEM_FULL_WIDTH, 400);
    }
};
```

> **关键点**：
> 1. `itemPopupApplet` 返回子页面控件，但 Dock 不会自动显示
> 2. 必须通过 `requestSetAppletVisible(this, itemKey, true)` 主动请求显示
> 3. 快捷面板控件需要发出信号，插件连接信号后调用 `requestSetAppletVisible`

## 配置注册

快捷面板插件必须在 `quickPlugins` 中注册才能显示。注册值使用
`pluginName()` 的返回值；未注册时，即使插件已经成功加载，任务栏快捷面板也不会展示它。

### 配置文件

配置元数据路径：

`/usr/share/dsg/configs/org.deepin.dde.shell/org.deepin.ds.dock.tray.json`

对应的 DConfig 参数：

- App ID：`org.deepin.dde.shell`
- Resource：`org.deepin.ds.dock.tray`
- Key：`quickPlugins`

不要直接修改 `/usr/share/dsg/configs` 下的元数据文件。添加自定义插件时，使用
`dde-dconfig` 读取并更新 `quickPlugins`。

### 使用 dde-dconfig 注册

先读取现有插件列表：

```bash
dde-dconfig get \
    -a org.deepin.dde.shell \
    -r org.deepin.ds.dock.tray \
    -k quickPlugins
```

将自定义插件的 `pluginName()` 追加到现有数组后，写回完整数组：

```bash
dde-dconfig set \
    -a org.deepin.dde.shell \
    -r org.deepin.ds.dock.tray \
    -k quickPlugins \
    -v '["network", "bluetooth", "my-plugin"]'
```

上面的数组仅为示例。`dde-dconfig set` 会替换整个 `quickPlugins` 值，因此必须保留
查询结果中的已有插件，只追加自定义插件名。数组顺序决定快捷面板中的显示顺序。

写入后再次执行 `dde-dconfig get` 验证结果；如任务栏未立即刷新，重启任务栏或重新
登录后再检查。

### 配置值示例

```json
{
    "quickPlugins": ["brightness", "volume", "weather"]
}
```

值为 `pluginName()` 返回值的数组，顺序决定显示顺序。

## 常见问题

### 快捷面板不显示

排查步骤：
1. 确认 `flags()` 返回 `Type_Quick | Quick_Panel_Full`（或其他 `Quick_Panel_*`）
2. 确认 `itemWidget(Dock::QUICK_ITEM_KEY)` 返回了有效控件
3. 使用 `dde-dconfig get -a org.deepin.dde.shell -r org.deepin.ds.dock.tray -k quickPlugins`
   确认插件名称已注册
4. 确认快捷面板控件只使用了 `setFixedHeight()`，没有使用 `setFixedSize()`

### Tooltip 不显示

- 检查 `itemPopupApplet` 返回值：如果返回了控件，框架会认为有弹出面板存在，从而不显示 tooltip
- 无弹出面板的插件应返回 `nullptr`
- 快捷面板通过 `itemWidget(QUICK_ITEM_KEY)` 提供，不应从 `itemPopupApplet` 返回

## 参考实现

参考 dde-tray-loader 源码中的 sound 插件（`Quick_Panel_Full` 示例）。
