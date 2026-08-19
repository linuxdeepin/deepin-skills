// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: GPL-3.0-or-later
import org.deepin.dcc 1.0

// 模块元数据（根 DccObject）。
// 注意：本文件中不能使用 dccData —— C++ 数据对象此时尚未加载。
DccObject {
    id: root
    name: "focusmode"           // 必须与 CMake 中 PLUGIN_NAME 完全一致
    parentName: "root"          // 挂载到控制中心根模块下
    displayName: qsTr("Focus Mode")
    description: qsTr("Manage focus mode state")
    icon: "deepin-dde"
    weight: 100

    visible: true               // 默认显示，可通过 DConfig hideModule 隐藏
}
