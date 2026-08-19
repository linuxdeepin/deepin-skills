// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: GPL-3.0-or-later
#ifndef FOCUSMODE_H
#define FOCUSMODE_H

#include <QObject>

class FocusModeWorker;

/**
 * @brief 专注模式数据对象（插件入口）
 *
 * 通过 DCC_FACTORY_CLASS 注册，控制中心在加载插件时在线程池中调用
 * create() 创建本对象，随后移动到主线程，QML 中通过 dccData 访问。
 *
 * 本类只做「状态管理」：把开关状态透传给 FocusModeWorker 进行持久化，
 * 真正的专注业务由其它服务监听 DConfig 状态自行处理。
 */
class FocusModeModule : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool enabled READ enabled NOTIFY enabledChanged FINAL)
public:
    explicit FocusModeModule(QObject *parent = nullptr);

    bool enabled() const;
    Q_INVOKABLE void setEnabled(bool enabled);
    FocusModeWorker *worker() const;

Q_SIGNALS:
    void enabledChanged(bool enabled);

private:
    FocusModeWorker *m_worker = nullptr;
};

#endif // FOCUSMODE_H
