// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: GPL-3.0-or-later

#include "focusmodeworker.h"

#include <DConfig>
#include <DDBusSender>

#include <QDBusPendingCallWatcher>
#include <QLoggingCategory>

namespace {
Q_LOGGING_CATEGORY(focusLog, "dde.control.center.focusmode")

// appId 必须是宿主应用（dde-control-center）的应用标识，
// 插件自身的配置身份通过 configId（name）表达。
constexpr auto kAppId = "org.deepin.dde.control-center";
constexpr auto kConfigId = "org.deepin.dde.control-center.focusmode";
constexpr auto kEnabledKey = "enabled";
}

FocusModeWorker::FocusModeWorker(QObject *parent)
    : QObject(parent)
{
    m_config = Dtk::Core::DConfig::create(kAppId, kConfigId, QString(), this);
    if (!m_config || !m_config->isValid()) {
        qCWarning(focusLog) << "DConfig is unavailable, fall back to in-memory default state";
        m_enabled = false;
        return;
    }

    loadFromConfig();

    // 其它服务可能通过 DConfig 修改状态，这里监听外部变化以保持本插件 UI 同步。
    connect(m_config, &Dtk::Core::DConfig::valueChanged, this,
            [this](const QString &key) {
                if (key == QLatin1String(kEnabledKey)) {
                    syncFromConfig();
                }
            });
}

bool FocusModeWorker::enabled() const
{
    return m_enabled;
}

void FocusModeWorker::setEnabled(bool enabled)
{
    if (m_config && m_config->isValid()) {
        m_config->setValue(QLatin1String(kEnabledKey), enabled);
    } else {
        qCWarning(focusLog) << "DConfig unavailable, only update in-memory state";
    }

    // 立即更新本插件状态，保证 UI 响应；valueChanged 信号只负责同步外部修改，
    // 因此这里直接写内部状态。
    if (m_enabled != enabled) {
        m_enabled = enabled;
        Q_EMIT enabledChanged(m_enabled);
    }

    notifyFocusMode(enabled);
}

void FocusModeWorker::loadFromConfig()
{
    if (!m_config || !m_config->isValid()) {
        return;
    }
    syncFromConfig();
}

void FocusModeWorker::syncFromConfig()
{
    if (!m_config || !m_config->isValid()) {
        return;
    }
    const bool value = m_config->value(QLatin1String(kEnabledKey), false).toBool();
    if (m_enabled != value) {
        m_enabled = value;
        Q_EMIT enabledChanged(m_enabled);
    }
}

void FocusModeWorker::notifyFocusMode(bool enabled)
{
    const QString title = enabled ? tr("Focus Mode On") : tr("Focus Mode Off");
    const QString body = enabled
                             ? tr("Focus mode is enabled. Distractions are now blocked.")
                             : tr("Focus mode is disabled. Everything is back to normal.");

    // 通过 freedesktop 通知服务发送系统通知
    QDBusPendingCall call = DDBusSender()
        .service("org.freedesktop.Notifications")
        .path("/org/freedesktop/Notifications")
        .interface("org.freedesktop.Notifications")
        .method("Notify")
        .arg(QStringLiteral("focusmode"))        // app_name
        .arg(0U)                                  // replaces_id
        .arg(QStringLiteral("deepin-dde"))          // app_icon
        .arg(title)                               // summary
        .arg(body)                                // body
        .arg(QStringList())                       // actions
        .arg(QVariantMap())                       // hints
        .arg(5000)                                // expire_timeout (ms)
        .call();

    auto *watcher = new QDBusPendingCallWatcher(call, this);
    connect(watcher, &QDBusPendingCallWatcher::finished, this,
            [this](QDBusPendingCallWatcher *w) {
                if (w->isError()) {
                    qCWarning(focusLog) << "Failed to send notification:" << w->error().message();
                    Q_EMIT notificationFailed(w->error().message());
                }
                w->deleteLater();
            });
}
