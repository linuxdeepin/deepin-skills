// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: GPL-3.0-or-later

#include "cpumonitor.h"

#include <QTextStream>
#include <QDebug>

CpuMonitor::CpuMonitor(QObject *parent)
    : QObject(parent)
{
    connect(&m_timer, &QTimer::timeout, this, &CpuMonitor::refresh);
    m_timer.setInterval(2000);
    // Defer first refresh via event loop to avoid sandbox issues
    QMetaObject::invokeMethod(this, "refresh", Qt::QueuedConnection);
}

int CpuMonitor::cpuUsage() const
{
    return m_cpuUsage;
}

void CpuMonitor::setInterval(int msec)
{
    m_timer.setInterval(msec);
}

void CpuMonitor::start()
{
    m_timer.start();
}

void CpuMonitor::stop()
{
    m_timer.stop();
}

void CpuMonitor::refresh()
{
    QFile file("/proc/stat");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qWarning() << "CpuMonitor: cannot open /proc/stat:" << file.errorString();
        return;
    }

    QTextStream in(&file);
    QString line = in.readLine();
    file.close();

    if (!line.startsWith("cpu ")) {
        qWarning() << "CpuMonitor: unexpected /proc/stat format, first line:" << line.left(20);
        return;
    }

    // Format: cpu  user nice system idle iowait irq softirq steal guest guest_nice
    const QStringList parts = line.split(' ', Qt::SkipEmptyParts);
    if (parts.size() < 8) {
        qWarning() << "CpuMonitor: insufficient fields in /proc/stat, got:" << parts.size();
        return;
    }

    bool ok = false;
    qint64 user = parts[1].toLongLong(&ok); if (!ok) user = 0;
    qint64 nice = parts[2].toLongLong(&ok); if (!ok) nice = 0;
    qint64 system = parts[3].toLongLong(&ok); if (!ok) system = 0;
    qint64 idle = parts[4].toLongLong(&ok); if (!ok) idle = 0;
    qint64 iowait = parts[5].toLongLong(&ok); if (!ok) iowait = 0;
    qint64 irq = parts[6].toLongLong(&ok); if (!ok) irq = 0;
    qint64 softirq = parts[7].toLongLong(&ok); if (!ok) softirq = 0;
    qint64 steal = parts.size() > 8 ? parts[8].toLongLong() : 0;

    qint64 totalIdle = idle + iowait;
    qint64 total = user + nice + system + idle + iowait + irq + softirq + steal;

    if (m_prevTotal > 0) {
        qint64 deltaIdle = totalIdle - m_prevIdle;
        qint64 deltaTotal = total - m_prevTotal;
        if (deltaTotal > 0) {
            int usage = static_cast<int>(100 * (deltaTotal - deltaIdle) / deltaTotal);
            if (usage != m_cpuUsage) {
                m_cpuUsage = usage;
                Q_EMIT cpuUsageChanged(m_cpuUsage);
            }
        }
    }

    m_prevIdle = totalIdle;
    m_prevTotal = total;
}
