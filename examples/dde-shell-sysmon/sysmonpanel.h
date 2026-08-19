// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once

#include "panel.h"

#include <QTimer>
#include <QDBusContext>
#include <sys/statvfs.h>

DS_USE_NAMESPACE

class CpuMonitor;
class MemoryMonitor;
class QDBusServiceWatcher;

class SysmonPanel : public DPanel, protected QDBusContext
{
    Q_OBJECT
    Q_PROPERTY(int cpuUsage READ cpuUsage NOTIFY cpuUsageChanged FINAL)
    Q_PROPERTY(int memoryUsage READ memoryUsage NOTIFY memoryUsageChanged FINAL)
    Q_PROPERTY(qint64 memoryUsed READ memoryUsed NOTIFY memoryUsedChanged FINAL)
    Q_PROPERTY(qint64 memoryTotal READ memoryTotal NOTIFY memoryTotalChanged FINAL)
    Q_PROPERTY(int diskUsage READ diskUsage NOTIFY diskUsageChanged FINAL)
    Q_PROPERTY(qint64 diskUsed READ diskUsed NOTIFY diskUsedChanged FINAL)
    Q_PROPERTY(qint64 diskTotal READ diskTotal NOTIFY diskTotalChanged FINAL)
    Q_PROPERTY(QString hostname READ hostname CONSTANT FINAL)
    Q_PROPERTY(QString osVersion READ osVersion CONSTANT FINAL)
    Q_PROPERTY(QString kernelVersion READ kernelVersion CONSTANT FINAL)
    Q_PROPERTY(QString cpuModel READ cpuModel CONSTANT FINAL)
    Q_PROPERTY(QString uptimeStr READ uptimeStr NOTIFY uptimeStrChanged FINAL)
    Q_PROPERTY(bool visible READ isVisible NOTIFY visibleChanged FINAL)

public:
    explicit SysmonPanel(QObject *parent = nullptr);
    ~SysmonPanel() override;

    int cpuUsage() const;
    int memoryUsage() const;
    qint64 memoryUsed() const;
    qint64 memoryTotal() const;
    int diskUsage() const;
    qint64 diskUsed() const;
    qint64 diskTotal() const;
    QString hostname() const;
    QString osVersion() const;
    QString kernelVersion() const;
    QString cpuModel() const;
    QString uptimeStr() const;
    bool isVisible() const;

    bool load() override;
    bool init() override;

public Q_SLOTS:
    void toggleVisible();
    void setVisible(bool v);

Q_SIGNALS:
    void cpuUsageChanged(int usage);
    void memoryUsageChanged(int usage);
    void memoryUsedChanged(qint64 used);
    void memoryTotalChanged(qint64 total);
    void diskUsageChanged(int usage);
    void diskUsedChanged(qint64 used);
    void diskTotalChanged(qint64 total);
    void uptimeStrChanged();
    void visibleChanged(bool visible);

private:
    void gatherSystemInfo();
    void refreshDisk();
    void refreshUptime();
    void registerDBus();

    CpuMonitor *m_cpuMonitor = nullptr;
    MemoryMonitor *m_memoryMonitor = nullptr;
    QTimer *m_uptimeTimer = nullptr;

    int m_diskUsage = 0;
    qint64 m_diskUsed = 0;
    qint64 m_diskTotal = 0;
    QString m_hostname;
    QString m_osVersion;
    QString m_kernelVersion;
    QString m_cpuModel;
    QString m_uptimeStr;
    bool m_visible = true;
};
