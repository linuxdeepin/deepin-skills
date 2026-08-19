# SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-3.0-or-later
#
# 控制中心插件示例 —— 专注模式 (Focus Mode)
#
# 该文件演示开发一个独立控制中心插件的完整构建流程：
#   1. find_package(DdeControlCenter) 引入插件开发所需的头文件、CMake 宏
#   2. add_library(... MODULE ...)     构建插件动态库（含 DCC_FACTORY_CLASS 注册）
#   3. dcc_install_plugin              安装 QML 资源与插件动态库到正确目录
#   4. dcc_handle_plugin_translation   处理 20 种 locale 的翻译
#   5. install(FILES ...)              安装 DConfig 元数据文件

cmake_minimum_required(VERSION 3.23) # qt_add_qml_module 建议 3.23+

# 插件名：只允许字母和数字，必须与 qml/Focusmode.qml 中 DccObject 的 name 完全一致，
# 用于控制中心的模块隐藏/禁用等操作。
set(PLUGIN_NAME "focusmode")

project(${PLUGIN_NAME}
    VERSION 1.0.0
    DESCRIPTION "Focus Mode plugin for DDE Control Center"
    LANGUAGES CXX
)

# 自动 MOC：处理 Q_OBJECT / DCC_FACTORY_CLASS，生成对应的 .moc
set(CMAKE_AUTOMOC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# 自动 RCC：把内置 DCI 图标 .qrc 编译进插件资源
set(CMAKE_AUTORCC ON)


# DdeControlCenter 提供 dcc_install_plugin / dcc_handle_plugin_translation 等宏
find_package(DdeControlCenter REQUIRED)
# LinguistTools 被 dcc_handle_plugin_translation 使用
find_package(Qt6 COMPONENTS Core LinguistTools DBus REQUIRED)
# Dtk6Core 提供 DConfig / DDBusSender
find_package(Dtk6Core REQUIRED)

# 收集 C++ 源码与内置资源
file(GLOB_RECURSE PLUGIN_SRCS
    "src/*.cpp"
    "src/*.h"
)
list(APPEND PLUGIN_SRCS
    "data/icons/icons.qrc"   # 内置 DCI 图标资源（/dsg/built-in-icons/）
)

# 构建插件动态库（非可执行文件）
add_library(${PLUGIN_NAME} MODULE ${PLUGIN_SRCS})

target_link_libraries(${PLUGIN_NAME} PRIVATE
    Dde::Control-Center
    Qt6::Core
    Qt6::DBus
    Dtk6::Core
)

# 安装插件（QML 资源 + 动态库）到控制中心插件目录
dcc_install_plugin(NAME ${PLUGIN_NAME} TARGET ${PLUGIN_NAME})

# 处理并安装翻译
dcc_handle_plugin_translation(NAME ${PLUGIN_NAME})

# 安装 DConfig 元数据文件
#   路径：/usr/share/dsg/configs/{appId}/
#   appId 必须是宿主应用（dde-control-center）的应用标识，插件不能单独构造 appId
install(FILES
    configs/org.deepin.dde.control-center.focusmode.json
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/dsg/configs/org.deepin.dde.control-center
)
