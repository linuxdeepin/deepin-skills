// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: LGPL-3.0-or-later

#include "quickpanelwidget.h"

#include "constants.h"

#include <DGuiApplicationHelper>
#include <DLabel>

#include <QHBoxLayout>
#include <QLabel>
#include <QMouseEvent>

DGUI_USE_NAMESPACE
DWIDGET_USE_NAMESPACE

namespace {

constexpr char kIconOn[] = "merge-apps-on";
constexpr char kIconOff[] = "merge-apps-off";

// 亮/暗主题使用不同配色的两套图标，暗色主题取 -dark 后缀版本
QString themeIconName(bool enabled)
{
    const bool dark
            = DGuiApplicationHelper::instance()->themeType() == DGuiApplicationHelper::DarkType;
    QString name = QLatin1String(enabled ? kIconOn : kIconOff);
    if (dark)
        name += QLatin1String("-dark");
    return name;
}

} // namespace

QuickPanelWidget::QuickPanelWidget(QWidget *parent)
    : QWidget(parent)
{
    setObjectName("MergeAppsQuickPanel");

    // 快捷面板控件只固定高度，宽度由布局标志决定
    setFixedHeight(Dock::QUICK_ITEM_HEIGHT);

    m_iconLabel = new QLabel(this);
    m_iconLabel->setFixedSize(Dock::QUICK_PANEL_ICON_SIZE);

    m_nameLabel = new DLabel(this);

    m_stateLabel = new DLabel(this);
    m_stateLabel->setObjectName("stateLabel");

    auto *layout = new QHBoxLayout(this);
    layout->setContentsMargins(10, 0, 10, 0);
    layout->setSpacing(8);
    layout->addWidget(m_iconLabel);
    layout->addWidget(m_nameLabel);
    layout->addStretch();
    layout->addWidget(m_stateLabel);
}

void QuickPanelWidget::setMergeApps(bool enabled)
{
    m_enabled = enabled;
    // 名称与状态文本在此统一设置：插件在加载翻译后再调用本方法，
    // 从而保证显示的是翻译后的文本（不要在构造函数里用 tr() 固化文本）。
    m_nameLabel->setText(tr("Merge application icons"));
    m_iconLabel->setPixmap(QIcon::fromTheme(themeIconName(enabled))
                               .pixmap(Dock::QUICK_PANEL_ICON_SIZE));
    m_stateLabel->setText(enabled ? tr("Merged") : tr("Not merged"));
    update();
}

void QuickPanelWidget::mouseReleaseEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton && rect().contains(event->pos())) {
        Q_EMIT clicked();
        event->accept();
        return;
    }
    QWidget::mouseReleaseEvent(event);
}
