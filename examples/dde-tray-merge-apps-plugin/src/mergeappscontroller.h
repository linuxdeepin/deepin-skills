// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: LGPL-3.0-or-later

#ifndef MERGE_APPS_CONTROLLER_H
#define MERGE_APPS_CONTROLLER_H

#include <QObject>

namespace Dtk { namespace Core { class DConfig; } }

// 合并应用图标功能的开关控制器。
// 控制中心通过 DConfig 的 noTaskGrouping 键控制"合并应用图标"：
//   noTaskGrouping == false  => 合并应用图标(开启)
//   noTaskGrouping == true   => 不合并应用图标(关闭)
// 本类对该键做一层封装，对外统一提供 mergeApps()/setMergeApps() 语义。
class MergeAppsController : public QObject
{
    Q_OBJECT

public:
    explicit MergeAppsController(QObject *parent = nullptr);

    // 是否开启"合并应用图标"（默认开启）
    bool mergeApps() const;

public slots:
    // 设置"合并应用图标"开关，enabled 为 true 表示开启合并
    void setMergeApps(bool enabled);

signals:
    // 开关状态变化（含外部如控制中心改动导致的同步变化）
    void mergeAppsChanged(bool enabled);

private:
    Dtk::Core::DConfig *m_config = nullptr;
};

#endif // MERGE_APPS_CONTROLLER_H
