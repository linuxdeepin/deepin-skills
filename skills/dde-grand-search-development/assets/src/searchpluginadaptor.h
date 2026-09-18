// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: GPL-3.0-or-later
//
// DBus Adaptor 模板。
//
// 接口名必须与 .conf 的 DBusInterface 字段完全一致。
// 方法名必须是 Search / Stop / Action（首字母大写，DBus 方法名大小写敏感）。

#ifndef SEARCHPLUGINADAPTOR_H
#define SEARCHPLUGINADAPTOR_H

#include <QtDBus/QDBusAbstractAdaptor>

class SearchPluginAdaptor : public QDBusAbstractAdaptor
{
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "com.example.MySearch.SearchPlugin")
    Q_CLASSINFO("D-Bus Introspection", ""
        "  <interface name=\"com.example.MySearch.SearchPlugin\">\n"
        "    <method name=\"Search\">\n"
        "      <arg type=\"s\" direction=\"out\"/>\n"
        "      <arg name=\"json\" type=\"s\" direction=\"in\"/>\n"
        "    </method>\n"
        "    <method name=\"Action\">\n"
        "      <arg type=\"b\" direction=\"out\"/>\n"
        "      <arg name=\"json\" type=\"s\" direction=\"in\"/>\n"
        "    </method>\n"
        "    <method name=\"Stop\">\n"
        "      <arg type=\"b\" direction=\"out\"/>\n"
        "      <arg name=\"json\" type=\"s\" direction=\"in\"/>\n"
        "    </method>\n"
        "  </interface>\n"
        "")

public:
    explicit SearchPluginAdaptor(QObject *parent = nullptr);
    ~SearchPluginAdaptor() override;

public slots:
    // 签名：Search(s) -> s
    QString Search(const QString &json);
    // 签名：Stop(s) -> b
    bool Stop(const QString &json);
    // 签名：Action(s) -> b
    bool Action(const QString &json);

private:
    QObject *m_parent;
};

#endif // SEARCHPLUGINADAPTOR_H
