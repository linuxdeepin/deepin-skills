# org.kde.StatusNotifierWatcher 接口参考

该接口提供系统托盘状态通知管理能力，兼容 KDE StatusNotifierItem 协议。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.kde.StatusNotifierWatcher` |
| Object path | `/StatusNotifierWatcher` |
| Interface | `org.kde.StatusNotifierWatcher` |
| Bus | Session |

## 兼容性提示

`org.kde.StatusNotifierWatcher` 是 KDE 标准系统托盘状态通知接口，由 dde-daemon 提供兼容实现。新代码应推荐使用 `org.deepin.dde.TrayManager1`（service=`org.deepin.dde.TrayManager1`，path=`/org/deepin/dde/TrayManager1`）。
