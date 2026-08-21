// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: LGPL-3.0-or-later

#ifndef TRAY_ITEM_WIDGET_H
#define TRAY_ITEM_WIDGET_H

#include <QWidget>

class QLabel;

// 托盘图标控件：单击切换"合并应用图标"开关。
class TrayItemWidget : public QWidget
{
    Q_OBJECT

public:
    explicit TrayItemWidget(QWidget *parent = nullptr);

    void setMergeApps(bool enabled);

signals:
    // 用户单击托盘图标
    void clicked();

protected:
    void mouseReleaseEvent(QMouseEvent *event) override;

private:
    QLabel *m_iconLabel = nullptr;
};

#endif // TRAY_ITEM_WIDGET_H
