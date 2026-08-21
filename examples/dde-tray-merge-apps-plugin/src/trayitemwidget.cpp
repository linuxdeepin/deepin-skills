// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: LGPL-3.0-or-later

#include "trayitemwidget.h"

#include "constants.h"

#include <DGuiApplicationHelper>

#include <QLabel>
#include <QMouseEvent>
#include <QVBoxLayout>

DGUI_USE_NAMESPACE

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

TrayItemWidget::TrayItemWidget(QWidget *parent)
    : QWidget(parent)
{
    setObjectName("MergeAppsTrayItem");
    setFixedSize(Dock::TRAY_PLUGIN_ITEM_FIXED_SIZE);

    m_iconLabel = new QLabel(this);
    m_iconLabel->setAlignment(Qt::AlignCenter);

    auto *layout = new QVBoxLayout(this);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->addWidget(m_iconLabel);
}

void TrayItemWidget::setMergeApps(bool enabled)
{
    m_iconLabel->setPixmap(QIcon::fromTheme(themeIconName(enabled))
                               .pixmap(Dock::TRAY_PLUGIN_ITEM_FIXED_SIZE));
    update();
}

void TrayItemWidget::mouseReleaseEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton && rect().contains(event->pos())) {
        Q_EMIT clicked();
        event->accept();
        return;
    }
    QWidget::mouseReleaseEvent(event);
}
