// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: LGPL-3.0-or-later

#ifndef QUICK_PANEL_WIDGET_H
#define QUICK_PANEL_WIDGET_H

#include <QWidget>

class QLabel;

// 快捷面板控件：显示图标、名称与当前状态，单击可切换"合并应用图标"开关。
// 注意：快捷面板控件的宽度由 Quick_Panel_* 布局标志决定，
// 这里只设置固定高度 Dock::QUICK_ITEM_HEIGHT，不要使用 setFixedSize()。
class QuickPanelWidget : public QWidget
{
    Q_OBJECT

public:
    explicit QuickPanelWidget(QWidget *parent = nullptr);

    // 刷新界面显示
    void setMergeApps(bool enabled);

signals:
    // 用户单击快捷面板控件
    void clicked();

protected:
    void mouseReleaseEvent(QMouseEvent *event) override;

private:
    QLabel *m_iconLabel = nullptr;
    QLabel *m_nameLabel = nullptr;
    QLabel *m_stateLabel = nullptr;
    bool m_enabled = true;
};

#endif // QUICK_PANEL_WIDGET_H
