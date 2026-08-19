// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: GPL-3.0-or-later

#include "memorymonitor.h"

#include <QDebug>
#include <sys/sysinfo.h>

MemoryMonitor::MemoryMonitor(QObject *parent)
    : QObject(parent)
{
    connect(&m_timer, &QTimer::timeout, this, &MemoryMonitor::refresh);
    m_timer.setInterval(2000);
    // Defer first refresh via event loop
    QMetaObject::invokeMethod(this, "refresh", Qt::QueuedConnection);
}

int MemoryMonitor::memoryUsage() const
{
    return m_memoryUsage;
}

qint64 MemoryMonitor::memoryUsed() const
{
    return m_memoryUsed;
}

qint64 MemoryMonitor::memoryTotal() const
{
    return m_memoryTotal;
}

void MemoryMonitor::setInterval(int msec)
{
    m_timer.setInterval(msec);
}

void MemoryMonitor::start()
{
    m_timer.start();
}

void MemoryMonitor::stop()
{
    m_timer.stop();
}

void MemoryMonitor::refresh()
{
    struct sysinfo info;
    if (sysinfo(&info) != 0) {
        qWarning() << "MemoryMonitor: sysinfo() failed";
        return;
    }

    qint64 total = static_cast<qint64>(info.totalram) * info.mem_unit / 1024; // kB
    qint64 free = static_cast<qint64>(info.freeram) * info.mem_unit / 1024;
    qint64 used = total - free;

    if (total <= 0) {
        qWarning() << "MemoryMonitor: sysinfo returned zero totalram";
        return;
    }

    int usage = static_cast<int>(100 * used / total);

    if (usage != m_memoryUsage) {
        m_memoryUsage = usage;
        Q_EMIT memoryUsageChanged(usage);
    }
    if (used != m_memoryUsed) {
        m_memoryUsed = used;
        Q_EMIT memoryUsedChanged(used);
    }
    if (total != m_memoryTotal) {
        m_memoryTotal = total;
        Q_EMIT memoryTotalChanged(total);
    }
}
