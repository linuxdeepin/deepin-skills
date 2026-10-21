# 日志与通知

提供日志规则设置、日志文件定位和桌面通知发送能力。

## DLogManager

### 定位

日志输出通道的管理入口。

### 功能能力总结

注册控制台、滚动文件及条件可用的系统日志输出通道，设置日志格式与文件位置。还可依据配置项调整进程的日志过滤规则；文件通道按天滚动并限制保留数量。

### 使用场景

应用需要控制控制台、文件或系统日志输出时。


---

## DNotifySender

### 定位

桌面通知的构造和发送入口。

### 功能能力总结

逐步设置通知的摘要、应用名、图标、正文、替换标识、动作、提示数据和超时时间。完成后通过通知服务异步发送，并返回待完成调用对象。

### 使用场景

需要指定标题、正文、动作或超时时间并发送通知时。


---

## 最小使用示例

链接 `Dtk6::Core`，参考库入口的 CMake 集成说明。发送当前应用的桌面通知，需要会话通知服务及事件循环；调用结果返回通知 ID 或 D-Bus 错误。

```cpp
#include <DNotifySender>
#include <QDBusPendingCallWatcher>
#include <QDBusPendingReply>
#include <QDebug>

void notifyFinished(QObject *context)
{
    auto call = Dtk::Core::DUtil::DNotifySender("任务完成")
        .appName("Example").appBody("处理已完成").timeOut(3000).call();
    auto *watcher = new QDBusPendingCallWatcher(call, context);
    QObject::connect(watcher, &QDBusPendingCallWatcher::finished,
                     context, [watcher] {
        QDBusPendingReply<uint> reply = *watcher;
        if (reply.isError())
            qWarning() << reply.error().message();
        else
            qInfo() << "notification id:" << reply.value();
        watcher->deleteLater();
    });
}
```
