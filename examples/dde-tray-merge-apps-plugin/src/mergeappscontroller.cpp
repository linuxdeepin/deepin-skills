// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: LGPL-3.0-or-later

#include "mergeappscontroller.h"

#include <DConfig>

#include <QDebug>

DCORE_USE_NAMESPACE

namespace {

// DConfig 的 AppId 与配置 ID，与 dde-shell taskmanager 保持一致
constexpr char kConfigAppId[] = "org.deepin.dde.shell";
constexpr char kConfigId[] = "org.deepin.ds.dock.taskmanager";
constexpr char kKeyNoTaskGrouping[] = "noTaskGrouping";

} // namespace

MergeAppsController::MergeAppsController(QObject *parent)
    : QObject(parent)
    , m_config(DConfig::create(kConfigAppId, kConfigId, QString(), this))
{
    if (!m_config || !m_config->isValid()) {
        qWarning() << "MergeAppsController: DConfig is unavailable, fall back to default (merged)";
    }

    // 监听配置变化：控制中心或其他入口改动后，插件能同步刷新显示
    connect(m_config, &DConfig::valueChanged, this, [this](const QString &key) {
        if (key == QLatin1String(kKeyNoTaskGrouping)) {
            Q_EMIT mergeAppsChanged(mergeApps());
        }
    });
}

bool MergeAppsController::mergeApps() const
{
    if (!m_config || !m_config->isValid())
        return true; // 配置不可用时按默认"合并"处理

    const bool noTaskGrouping = m_config->value(kKeyNoTaskGrouping, false).toBool();
    return !noTaskGrouping;
}

void MergeAppsController::setMergeApps(bool enabled)
{
    if (!m_config || !m_config->isValid())
        return;

    if (mergeApps() == enabled)
        return;

    m_config->setValue(kKeyNoTaskGrouping, !enabled);
    // valueChanged 信号会触发 mergeAppsChanged
}
