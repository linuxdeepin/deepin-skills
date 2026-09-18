// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: GPL-3.0-or-later
//
// DDE Grand Search 扩展搜索插件入口模板。
//
// 职责：注册 DBus 服务与对象，进入事件循环。
// 三个必须与 .conf 保持一致的点：服务名、对象路径、接口名。

#include "searcher.h"
#include "searchpluginadaptor.h"

#include <QCoreApplication>
#include <QDBusConnection>
#include <QLoggingCategory>

// 必须与 my-search.conf 中的 DBusService / DBusAddress 完全一致
#define DBUS_SERVICE_NAME   "com.example.MySearch"
#define DBUS_OBJECT_PATH    "/com/example/MySearch"

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    app.setApplicationName("my-search-plugin");

    // 开发期开启插件日志；生产环境建议由环境变量控制
    QLoggingCategory::setFilterRules("myplugin.search.debug=true");

    MySearcher searcher;

    // Adaptor 必须是导出对象的子对象，否则对象导出后不带 Adaptor 接口
    SearchPluginAdaptor adaptor(&searcher);

    // 全局搜索只监听会话总线，插件也必须注册到会话总线
    QDBusConnection connection = QDBusConnection::sessionBus();

    if (!connection.registerService(DBUS_SERVICE_NAME)) {
        // 常见原因：已有同名服务在运行（上一个实例未退出）
        qCritical("Failed to register DBus service: %s", DBUS_SERVICE_NAME);
        return 1;
    }

    if (!connection.registerObject(DBUS_OBJECT_PATH, &searcher)) {
        qCritical("Failed to register DBus object: %s", DBUS_OBJECT_PATH);
        return 1;
    }

    qInfo("Search plugin started - Service: %s, Path: %s",
          DBUS_SERVICE_NAME, DBUS_OBJECT_PATH);

    return app.exec();
}
