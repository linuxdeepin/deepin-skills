// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: GPL-3.0-or-later
#ifndef FOCUSMODEWORKER_H
#define FOCUSMODEWORKER_H

#include <QObject>
#include <QVariant>

namespace Dtk::Core {
class DConfig;
}

/**
 * @brief 专注模式后台工作类
 *
 * 负责两件事：
 *   1. 通过 DConfig 把开关状态持久化到系统配置，供其它服务跨进程监听；
 *   2. 状态变化时通过 DDBusSender 发送系统通知。
 *
 * 插件本身「只管理状态」—— 真正的专注业务（拦截通知、屏蔽打扰等）由其它
 * 服务订阅 DConfig 的 valueChanged 信号自行处理，不在此插件内实现。
 */
class FocusModeWorker : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool enabled READ enabled NOTIFY enabledChanged FINAL)
public:
    explicit FocusModeWorker(QObject *parent = nullptr);

    bool enabled() const;

    /**
     * @brief 设置专注模式开关
     *
     * 写入 DConfig 并立即同步内部状态；同时更新本插件（UI）状态。
     */
    void setEnabled(bool enabled);

Q_SIGNALS:
    void enabledChanged(bool enabled);
    void notificationFailed(const QString &errorMessage);

private:
    void loadFromConfig();
    void syncFromConfig();
    void notifyFocusMode(bool enabled);

    Dtk::Core::DConfig *m_config = nullptr;
    bool m_enabled = false;
};

#endif // FOCUSMODEWORKER_H
