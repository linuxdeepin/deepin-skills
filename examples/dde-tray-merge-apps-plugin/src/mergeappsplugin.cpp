// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: LGPL-3.0-or-later

#include "mergeappsplugin.h"

#include "mergeappscontroller.h"
#include "quickpanelwidget.h"
#include "trayitemwidget.h"

#include <DGuiApplicationHelper>

DGUI_USE_NAMESPACE

#include <QLabel>
#include <QLocale>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QProcess>
#include <QtGlobal>

namespace {

constexpr char kTrayKey[] = "dde-tray-merge-apps";

// 打开控制中心并跳转到"个性化 -> 桌面和任务栏"模块
constexpr char kControlCenterPage[] = "personalization/dock";

} // namespace

MergeAppsPlugin::MergeAppsPlugin(QObject *parent)
    : QObject(parent)
    , m_controller(new MergeAppsController(this))
    , m_trayItem(new TrayItemWidget)
    , m_quickPanel(new QuickPanelWidget)
{
}

MergeAppsPlugin::~MergeAppsPlugin() = default;

const QString MergeAppsPlugin::pluginName() const
{
    return QStringLiteral("dde-tray-merge-apps");
}

const QString MergeAppsPlugin::pluginDisplayName() const
{
    return tr("Merge application icons");
}

void MergeAppsPlugin::init(PluginProxyInterface *proxyInter)
{
    m_proxyInter = proxyInter;

    initTranslator();

    m_trayItem->setMergeApps(m_controller->mergeApps());
    m_quickPanel->setMergeApps(m_controller->mergeApps());

    // 托盘单击切换
    connect(m_trayItem.data(), &TrayItemWidget::clicked, this, &MergeAppsPlugin::toggleMergeApps);
    // 快捷面板单击切换
    connect(m_quickPanel.data(), &QuickPanelWidget::clicked, this, &MergeAppsPlugin::toggleMergeApps);
    // 配置变化（含控制中心侧改动）时同步刷新显示
    connect(m_controller.data(), &MergeAppsController::mergeAppsChanged, this, [this](bool enabled) {
        m_trayItem->setMergeApps(enabled);
        m_quickPanel->setMergeApps(enabled);
        if (m_proxyInter)
            m_proxyInter->itemUpdate(this, kTrayKey);
    });

    // 托盘图标注册（快捷面板通过 quickPlugins 注册后由 itemWidget(QUICK_ITEM_KEY) 提供）
    m_proxyInter->itemAdded(this, kTrayKey);
}

QWidget *MergeAppsPlugin::itemWidget(const QString &itemKey)
{
    if (itemKey == Dock::QUICK_ITEM_KEY)
        return m_quickPanel.data();

    if (itemKey == QLatin1String(kTrayKey))
        return m_trayItem.data();

    return nullptr;
}

QWidget *MergeAppsPlugin::itemTipsWidget(const QString &itemKey)
{
    if (itemKey != QLatin1String(kTrayKey))
        return nullptr;

    // 提示控件建议缓存复用，避免每次调用都新建
    if (!m_tipsLabel)
        m_tipsLabel.reset(new QLabel());
    m_tipsLabel->setObjectName("dde-tray-merge-apps-tips");
    m_tipsLabel->setText(m_controller->mergeApps()
                             ? tr("Merge application icons: on")
                             : tr("Merge application icons: off"));
    return m_tipsLabel.data();
}

const QString MergeAppsPlugin::itemContextMenu(const QString &itemKey)
{
    if (itemKey != QLatin1String(kTrayKey))
        return QString();

    QJsonArray items;

    QJsonObject toggle;
    toggle["itemId"] = "toggle";
    toggle["itemText"] = m_controller->mergeApps() ? tr("Turn off merge") : tr("Turn on merge");
    toggle["isCheckable"] = false;
    toggle["isActive"] = true;
    items.append(toggle);

    QJsonObject openCc;
    openCc["itemId"] = "open-control-center";
    openCc["itemText"] = tr("Open control center settings");
    openCc["isCheckable"] = false;
    openCc["isActive"] = true;
    items.append(openCc);

    QJsonObject menu;
    menu["items"] = items;
    menu["checkableMenu"] = false;
    menu["singleCheck"] = false;

    return QString::fromUtf8(QJsonDocument(menu).toJson());
}

void MergeAppsPlugin::invokedMenuItem(const QString &itemKey, const QString &menuId, const bool checked)
{
    Q_UNUSED(itemKey)
    Q_UNUSED(checked)

    if (menuId == QLatin1String("toggle")) {
        toggleMergeApps();
    } else if (menuId == QLatin1String("open-control-center")) {
        openControlCenterDock();
    }
}

void MergeAppsPlugin::toggleMergeApps()
{
    m_controller->setMergeApps(!m_controller->mergeApps());
}

bool MergeAppsPlugin::pluginIsDisable()
{
    // 禁用状态通过代理接口持久化到 dde-dock.conf，重启任务栏后仍生效
    return m_proxyInter && m_proxyInter->getValue(this, "disabled", false).toBool();
}

void MergeAppsPlugin::pluginStateSwitched()
{
    const bool disabled = !pluginIsDisable();
    m_proxyInter->saveValue(this, "disabled", disabled);

    // 禁用时移除托盘项，重新启用时加回；快捷面板控件由 loader 依据
    // flags() 与 quickPlugins 注册状态管理，无需在此手动增删。
    if (disabled)
        m_proxyInter->itemRemoved(this, kTrayKey);
    else
        m_proxyInter->itemAdded(this, kTrayKey);
}

void MergeAppsPlugin::refreshIcon(const QString &itemKey)
{
    Q_UNUSED(itemKey)

    // 图标主题或亮暗主题变化时，按当前状态重新渲染两处图标
    const bool enabled = m_controller->mergeApps();
    m_trayItem->setMergeApps(enabled);
    m_quickPanel->setMergeApps(enabled);
}

void MergeAppsPlugin::openControlCenterDock()
{
    // 推荐使用 dde-am 打开控制中心：Wayland 下 dde-am 会正确处理 xdg-activation token
    QStringList args{
        "--by-user",
        "org.deepin.dde.control-center",
        "--",
        "-p",
        kControlCenterPage,
    };
    QProcess::startDetached(QStringLiteral("dde-am"), args);
}

void MergeAppsPlugin::initTranslator()
{
    // 遵循 dtk-development 的翻译加载规则：
    // DGuiApplicationHelper::loadTranslator 会从标准数据目录
    // (/usr/share/<name>/translations/ 等) 加载 <name>_<locale>.qm，
    // 并自动处理 zh_CN -> zh 的语言回退；加载成功即安装 translator。
    // 必须在创建可翻译文本(快捷面板/菜单文本)之前调用。
    DGuiApplicationHelper::loadTranslator(pluginName(), pluginName(),
                                          { QLocale::system() });
}
