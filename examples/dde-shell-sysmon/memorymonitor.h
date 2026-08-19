// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once

#include <QObject>
#include <QTimer>

class MemoryMonitor : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int memoryUsage READ memoryUsage NOTIFY memoryUsageChanged FINAL)
    Q_PROPERTY(qint64 memoryUsed READ memoryUsed NOTIFY memoryUsedChanged FINAL)
    Q_PROPERTY(qint64 memoryTotal READ memoryTotal NOTIFY memoryTotalChanged FINAL)

public:
    explicit MemoryMonitor(QObject *parent = nullptr);

    int memoryUsage() const;
    qint64 memoryUsed() const;
    qint64 memoryTotal() const;

    void setInterval(int msec);
    void start();
    void stop();

public Q_SLOTS:
    void refresh();

Q_SIGNALS:
    void memoryUsageChanged(int usage);
    void memoryUsedChanged(qint64 used);
    void memoryTotalChanged(qint64 total);

private:
    QTimer m_timer;
    int m_memoryUsage = 0;
    qint64 m_memoryUsed = 0;
    qint64 m_memoryTotal = 0;
};
