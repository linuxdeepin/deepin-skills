// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: GPL-3.0-or-later
//
// 搜索器骨架：实现 Search / Stop / Action 与 V1.0 协议 JSON 构造。
//
// 需要按业务替换的部分：
//   - doSearch()     实际搜索逻辑
//   - doOpenItem()   点击结果时的操作
//   - 分组名与结果名的本地化文案

#ifndef SEARCHER_H
#define SEARCHER_H

#include <QObject>
#include <QHash>
#include <QMutex>
#include <QSet>

class MySearcher : public QObject
{
    Q_OBJECT
public:
    explicit MySearcher(QObject *parent = nullptr);
    ~MySearcher() override;

    // 对应 DBus 方法 Search(String json) -> String json
    QString search(const QString &json);
    // 对应 DBus 方法 Stop(String json) -> bool
    bool stop(const QString &json);
    // 对应 DBus 方法 Action(String json) -> bool
    bool action(const QString &json);

private:
    struct SearchInput {
        QString ver;
        QString mID;
        QString cont;
    };

    // ── 协议解析与构造 ────────────────────────────────────────────
    SearchInput parseSearchInput(const QString &json) const;
    QString buildEmptyResult(const QString &mID) const;
    QString buildResult(const QString &mID, const QList<QPair<QString, QString>> &items) const;

    // ── 业务逻辑（按需替换）────────────────────────────────────────
    // 返回 <item 标识, 界面显示名> 列表；结果为空表示无匹配
    QList<QPair<QString, QString>> doSearch(const QString &keyword) const;
    // 处理 openitem：根据 item 标识执行操作，返回是否成功
    bool doOpenItem(const QString &item);

    // ── 中断管理 ─────────────────────────────────────────────────
    // 记录被中断的任务号；Search 循环中周期检查
    bool isInterrupted(const QString &mID) const;
    void clearInterrupt(const QString &mID);

    mutable QMutex m_mutex;
    QSet<QString> m_interruptedIDs;
};

#endif // SEARCHER_H
