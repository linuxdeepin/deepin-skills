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

`org.kde.StatusNotifierWatcher` 用于标准 StatusNotifierItem 注册与状态通知；DDE 的 `org.deepin.dde.TrayManager1` 提供桌面托盘管理能力，两者并非同一协议的可互换名称。面向标准 SNI 客户端时仍使用本协议，不能只替换服务名或方法名。

## 注册与查询

### RegisterStatusNotifierItem

注册已存在的 StatusNotifierItem。参数 `serviceOrPath` 为提供该对象的服务名或对象路径；调用进程需保持其托盘对象及总线连接存活。

```bash
gdbus call --session \
  --dest org.kde.StatusNotifierWatcher \
  --object-path /StatusNotifierWatcher \
  --method org.kde.StatusNotifierWatcher.RegisterStatusNotifierItem \
  "${sni_service:?请提供实际的 StatusNotifierItem 服务名}"
```

返回值为空；失败时返回 D-Bus 错误。使用对象路径注册时，调用者自身必须导出该对象，不能用一次性命令代替实际托盘客户端。

### 状态属性

`RegisteredStatusNotifierItems`（`as`）、`IsStatusNotifierHostRegistered`（`b`）和 `ProtocolVersion`（`i`）为只读状态：

```bash
gdbus call --session \
  --dest org.kde.StatusNotifierWatcher \
  --object-path /StatusNotifierWatcher \
  --method org.freedesktop.DBus.Properties.GetAll org.kde.StatusNotifierWatcher
```

### 状态变化信号

条目注册或注销时发出 `StatusNotifierItemRegistered` / `StatusNotifierItemUnregistered`，参数为条目标识；宿主注册时发出 `StatusNotifierHostRegistered`。

```bash
gdbus monitor --session \
  --dest org.kde.StatusNotifierWatcher \
  --object-path /StatusNotifierWatcher
```
