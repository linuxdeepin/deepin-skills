// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: LGPL-3.0-or-later

#ifndef MERGE_APPS_PLUGIN_H
#define MERGE_APPS_PLUGIN_H

#include "pluginsiteminterface_v2.h"

#include <QObject>
#include <QScopedPointer>

class MergeAppsController;
class QLabel;
class QuickPanelWidget;
class TrayItemWidget;

// 合并应用图标快捷开关插件示例。
// 同时提供托盘图标与快捷面板控件，单击任意一处即可切换
// 控制中心"个性化 -> 桌面和任务栏"下的"合并应用图标"开关。
class MergeAppsPlugin : public QObject, public PluginsItemInterfaceV2
{
    Q_OBJECT
    Q_INTERFACES(PluginsItemInterfaceV2)
    Q_PLUGIN_METADATA(IID ModuleInterface_iid_V2 FILE "dde-tray-merge-apps-plugin.json")

public:
    explicit MergeAppsPlugin(QObject *parent = nullptr);
    ~MergeAppsPlugin() override;

    const QString pluginName() const override;
    const QString pluginDisplayName() const override;
    void init(PluginProxyInterface *proxyInter) override;

    Dock::PluginFlags flags() const override
    {
        // 快捷面板插件：使用 Type_Quick + 布局标志（这里用整行 Full 以便显示更多信息）
        return Dock::Type_Quick | Dock::Quick_Panel_Full
                | Dock::Attribute_CanDrag | Dock::Attribute_CanInsert;
    }

    QWidget *itemWidget(const QString &itemKey) override;
    QWidget *itemTipsWidget(const QString &itemKey) override;
    const QString itemContextMenu(const QString &itemKey) override;
    void invokedMenuItem(const QString &itemKey, const QString &menuId, const bool checked) override;

    bool pluginIsAllowDisable() override { return true; }
    bool pluginIsDisable() override;
    void pluginStateSwitched() override;
    void refreshIcon(const QString &itemKey) override;

private:
    void initTranslator();
    void toggleMergeApps();
    void openControlCenterDock();

private:
    QScopedPointer<MergeAppsController> m_controller;
    QScopedPointer<TrayItemWidget> m_trayItem;
    QScopedPointer<QuickPanelWidget> m_quickPanel;
    QScopedPointer<QLabel> m_tipsLabel;
};

#endif // MERGE_APPS_PLUGIN_H
