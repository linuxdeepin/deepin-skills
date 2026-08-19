// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: GPL-3.0-or-later

#include "sysmonpanel.h"
#include "cpumonitor.h"
#include "memorymonitor.h"
#include "sysmonadaptor.h"

#include "pluginfactory.h"

#include <QTimer>
#include <QFile>
#include <QTextStream>
#include <QDebug>
#include <QDateTime>
#include <QHostInfo>
#include <QDBusConnection>
#include <QQuickWindow>

#include <sys/sysinfo.h>
#include <sys/statvfs.h>

#include <DConfig>

SysmonPanel::SysmonPanel(QObject *parent)
    : DPanel(parent)
{
}

SysmonPanel::~SysmonPanel() = default;

int SysmonPanel::cpuUsage() const { return m_cpuMonitor ? m_cpuMonitor->cpuUsage() : 0; }
int SysmonPanel::memoryUsage() const { return m_memoryMonitor ? m_memoryMonitor->memoryUsage() : 0; }
qint64 SysmonPanel::memoryUsed() const { return m_memoryMonitor ? m_memoryMonitor->memoryUsed() : 0; }
qint64 SysmonPanel::memoryTotal() const { return m_memoryMonitor ? m_memoryMonitor->memoryTotal() : 0; }
int SysmonPanel::diskUsage() const { return m_diskUsage; }
qint64 SysmonPanel::diskUsed() const { return m_diskUsed; }
qint64 SysmonPanel::diskTotal() const { return m_diskTotal; }
QString SysmonPanel::hostname() const { return m_hostname; }
QString SysmonPanel::osVersion() const { return m_osVersion; }
QString SysmonPanel::kernelVersion() const { return m_kernelVersion; }
QString SysmonPanel::cpuModel() const { return m_cpuModel; }
QString SysmonPanel::uptimeStr() const { return m_uptimeStr; }
bool SysmonPanel::isVisible() const { return m_visible; }

bool SysmonPanel::load()
{
    return DPanel::load();
}

bool SysmonPanel::init()
{
    DPanel::init();

    DCORE_USE_NAMESPACE;
    auto config = DConfig::create("org.deepin.dde.shell", "org.deepin.ds.sysmon");
    int interval = config ? config->value("refreshInterval", 2000).toInt() : 2000;

    gatherSystemInfo();

    m_cpuMonitor = new CpuMonitor(this);
    m_cpuMonitor->setInterval(interval);
    connect(m_cpuMonitor, &CpuMonitor::cpuUsageChanged, this, &SysmonPanel::cpuUsageChanged);

    m_memoryMonitor = new MemoryMonitor(this);
    m_memoryMonitor->setInterval(interval);
    connect(m_memoryMonitor, &MemoryMonitor::memoryUsageChanged, this, &SysmonPanel::memoryUsageChanged);
    connect(m_memoryMonitor, &MemoryMonitor::memoryUsedChanged, this, &SysmonPanel::memoryUsedChanged);
    connect(m_memoryMonitor, &MemoryMonitor::memoryTotalChanged, this, &SysmonPanel::memoryTotalChanged);

    m_uptimeTimer = new QTimer(this);
    m_uptimeTimer->setInterval(10000);
    connect(m_uptimeTimer, &QTimer::timeout, this, &SysmonPanel::refreshUptime);

    refreshDisk();
    refreshUptime();

    connect(this, &DApplet::rootObjectChanged, this, [this]() {
        if (!rootObject() || !window()) {
            qWarning() << "SysmonPanel: rootObject or window is null, deferring D-Bus registration";
            return;
        }
        qInfo() << "SysmonPanel: root object ready";
        registerDBus();
    });

    m_cpuMonitor->start();
    m_memoryMonitor->start();
    m_uptimeTimer->start();

    return true;
}

void SysmonPanel::gatherSystemInfo()
{
    m_hostname = QHostInfo::localHostName();

    QFile osRelease("/etc/os-release");
    if (osRelease.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QTextStream in(&osRelease);
        while (!in.atEnd()) {
            QString line = in.readLine();
            if (line.startsWith("PRETTY_NAME=")) {
                m_osVersion = line.mid(12).remove('"');
                break;
            }
        }
        osRelease.close();
    }
    if (m_osVersion.isEmpty())
        m_osVersion = "Deepin/UOS";

    m_kernelVersion = QSysInfo::kernelVersion();

    QFile cpuinfo("/proc/cpuinfo");
    if (cpuinfo.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QTextStream in(&cpuinfo);
        while (!in.atEnd()) {
            QString line = in.readLine();
            if (line.startsWith("model name")) {
                m_cpuModel = line.section(':', 1).trimmed();
                break;
            }
        }
        cpuinfo.close();
    }
    if (m_cpuModel.isEmpty())
        m_cpuModel = "Unknown CPU";
}

void SysmonPanel::registerDBus()
{
    new SysmonAdaptor(this);

    QDBusConnection bus = QDBusConnection::sessionBus();
    if (!bus.registerService("org.deepin.ds.sysmon")) {
        qWarning() << "SysmonPanel: failed to register D-Bus service:" << bus.lastError().message();
        return;
    }
    if (!bus.registerObject("/org/deepin/ds/sysmon", this)) {
        qWarning() << "SysmonPanel: failed to register D-Bus object:" << bus.lastError().message();
        return;
    }
    qInfo() << "SysmonPanel: D-Bus service registered at org.deepin.ds.sysmon";
}

void SysmonPanel::toggleVisible()
{
    setVisible(!m_visible);
}

void SysmonPanel::setVisible(bool v)
{
    if (m_visible == v)
        return;

    m_visible = v;
    if (auto *win = window()) {
        win->setVisible(v);
    }
    Q_EMIT visibleChanged(m_visible);
}

void SysmonPanel::refreshDisk()
{
    struct statvfs stat;
    if (statvfs("/", &stat) == 0) {
        qint64 total = static_cast<qint64>(stat.f_blocks) * stat.f_frsize;
        qint64 available = static_cast<qint64>(stat.f_bavail) * stat.f_frsize;
        qint64 used = total - available;
        int usage = total > 0 ? static_cast<int>(100 * used / total) : 0;

        if (usage != m_diskUsage) {
            m_diskUsage = usage;
            Q_EMIT diskUsageChanged(usage);
        }
        if (used != m_diskUsed) {
            m_diskUsed = used;
            Q_EMIT diskUsedChanged(used);
        }
        if (total != m_diskTotal) {
            m_diskTotal = total;
            Q_EMIT diskTotalChanged(total);
        }
    }
}

void SysmonPanel::refreshUptime()
{
    struct sysinfo info;
    if (sysinfo(&info) == 0) {
        qint64 uptimeSecs = info.uptime;
        int days = static_cast<int>(uptimeSecs / 86400);
        int hours = static_cast<int>((uptimeSecs % 86400) / 3600);
        int mins = static_cast<int>((uptimeSecs % 3600) / 60);

        QString str;
        if (days > 0)
            str = QString("%1d %2h %3m").arg(days).arg(hours).arg(mins);
        else if (hours > 0)
            str = QString("%1h %2m").arg(hours).arg(mins);
        else
            str = QString("%1m").arg(mins);

        if (str != m_uptimeStr) {
            m_uptimeStr = str;
            Q_EMIT uptimeStrChanged();
        }
    }

    refreshDisk();
}

D_APPLET_CLASS(SysmonPanel)

#include "sysmonpanel.moc"
