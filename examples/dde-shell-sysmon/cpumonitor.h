// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once

#include <QObject>
#include <QTimer>
#include <QFile>

class CpuMonitor : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int cpuUsage READ cpuUsage NOTIFY cpuUsageChanged FINAL)
public:
    explicit CpuMonitor(QObject *parent = nullptr);

    int cpuUsage() const;

    void setInterval(int msec);
    void start();
    void stop();

public Q_SLOTS:
    void refresh();

Q_SIGNALS:
    void cpuUsageChanged(int usage);

private:
    QTimer m_timer;
    qint64 m_prevIdle = 0;
    qint64 m_prevTotal = 0;
    int m_cpuUsage = 0;
};
