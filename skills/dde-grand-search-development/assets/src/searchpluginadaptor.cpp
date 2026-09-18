// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: GPL-3.0-or-later

#include "searchpluginadaptor.h"
#include "searcher.h"

SearchPluginAdaptor::SearchPluginAdaptor(QObject *parent)
    : QDBusAbstractAdaptor(parent), m_parent(parent)
{
    // 插件不需要向 daemon 转发信号
    setAutoRelaySignals(false);
}

SearchPluginAdaptor::~SearchPluginAdaptor()
{
}

QString SearchPluginAdaptor::Search(const QString &json)
{
    MySearcher *searcher = qobject_cast<MySearcher *>(m_parent);
    if (searcher)
        return searcher->search(json);

    return QString();
}

bool SearchPluginAdaptor::Stop(const QString &json)
{
    MySearcher *searcher = qobject_cast<MySearcher *>(m_parent);
    if (searcher)
        return searcher->stop(json);

    return false;
}

bool SearchPluginAdaptor::Action(const QString &json)
{
    MySearcher *searcher = qobject_cast<MySearcher *>(m_parent);
    if (searcher)
        return searcher->action(json);

    return false;
}
