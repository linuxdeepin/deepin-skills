// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: GPL-3.0-or-later

#include "focusmode.h"
#include "focusmodeworker.h"

#include "dccfactory.h"

#include <QResource>

FocusModeModule::FocusModeModule(QObject *parent)
    : QObject(parent)
    , m_worker(new FocusModeWorker(this)) // 子对象必须纳入 QObject 树，随主线程移动
{
    // 注册内置 DCI 图标资源（/dsg/built-in-icons/），保证 DDciIcon::fromTheme("deepin-dde") 可解析。
    // 图标编译进插件自身，不安装到系统，避免与其它应用冲突。
    Q_INIT_RESOURCE(icons);
    // 把 Worker 的状态变化透传出去，供 QML 绑定
    connect(m_worker, &FocusModeWorker::enabledChanged, this,
            [this](bool enabled) { Q_EMIT enabledChanged(enabled); });
}

bool FocusModeModule::enabled() const
{
    return m_worker->enabled();
}

void FocusModeModule::setEnabled(bool enabled)
{
    m_worker->setEnabled(enabled);
}

FocusModeWorker *FocusModeModule::worker() const
{
    return m_worker;
}

// DCC_FACTORY_CLASS 生成 FocusModeModuleFactory 工厂类，注册插件数据对象；
// 调用后必须包含对应的 .moc 文件。
DCC_FACTORY_CLASS(FocusModeModule)
#include "focusmode.moc"
