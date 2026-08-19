// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.15

import org.deepin.dcc 1.0

// 主页面：设置直接挂在模块（focusmode）下，处于第二级，无需额外的中间页面层。
// 此处可以使用 dccData（C++ 数据对象已加载）。
DccObject {
    DccObject {
        name: "focusModeGroup"
        parentName: "focusmode"
        displayName: qsTr("Focus Mode")
        pageType: DccObject.Item
        page: DccGroupView {}

        DccObject {
            name: "focusModeSwitch"
            parentName: "focusmode/focusModeGroup"
            displayName: qsTr("Enable Focus Mode")
            description: qsTr("Block distractions and stay focused")
            backgroundType: DccObject.Normal
            pageType: DccObject.Editor
            page: Switch {
                checked: dccData.enabled
                onToggled: dccData.setEnabled(checked)
            }
        }
    }
}
