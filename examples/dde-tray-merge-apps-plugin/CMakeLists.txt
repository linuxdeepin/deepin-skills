# SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: CC0-1.0

cmake_minimum_required(VERSION 3.16)

set(PLUGIN_NAME "dde-tray-merge-apps")
project(${PLUGIN_NAME} VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 依赖：Qt6 + DTK6 + dde-tray-loader 开发头文件
find_package(Qt6 REQUIRED COMPONENTS Widgets Svg DBus LinguistTools)
find_package(Dtk6 REQUIRED COMPONENTS Widget Gui Core)
# 任务栏插件开发头文件由 dde-tray-loader-dev 提供，CMake 包名为 DdeTrayLoader，
# 头文件目录通过变量 DDE_TRAY_LOADER_INCLUDE_DIR 给出（指向 /usr/include/dde-dock）
find_package(DdeTrayLoader REQUIRED)

file(GLOB_RECURSE SRCS CONFIGURE_DEPENDS "src/*.h" "src/*.cpp")

add_library(${PLUGIN_NAME} SHARED ${SRCS})
target_include_directories(${PLUGIN_NAME} PRIVATE
    src
    ${DDE_TRAY_LOADER_INCLUDE_DIR}
)
target_link_libraries(${PLUGIN_NAME} PRIVATE
    Dtk6::Widget
    Dtk6::Gui
    Dtk6::Core
    Qt6::Widgets
    Qt6::Svg
    Qt6::DBus
)

# 编译 .ts 为 .qm：使用 Qt6 标准的 LinguistTools 写法 qt6_add_translations。
# 通过 QM_FILES_OUTPUT_VARIABLE 拿到生成的 .qm 路径，不内嵌进 .so，
# 以便 dtk-development 的 DGuiApplicationHelper::loadTranslator 从文件系统加载。
file(GLOB TS_FILES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/translations/*.ts")
set(QM_FILES "")
if(TS_FILES)
    qt6_add_translations(${PLUGIN_NAME}
        TS_FILES ${TS_FILES}
        QM_FILES_OUTPUT_VARIABLE QM_FILES
    )
endif()

# 安装到 dde-tray-loader 的插件目录（即 /usr/lib/dde-dock/plugins，该路径是
# dde-tray-loader 固定扫描的插件目录，并非依赖 dde-dock）
install(TARGETS ${PLUGIN_NAME} LIBRARY DESTINATION lib/dde-dock/plugins)

# 安装翻译文件到 /usr/share/<pluginName>/translations/（插件运行时从此处加载）
if(QM_FILES)
    install(FILES ${QM_FILES} DESTINATION share/${PLUGIN_NAME}/translations)
endif()

# 安装亮/暗两套图标到 hicolor 主题目录，供 QIcon::fromTheme 查找
install(FILES
    icons/merge-apps-on.svg
    icons/merge-apps-off.svg
    icons/merge-apps-on-dark.svg
    icons/merge-apps-off-dark.svg
    DESTINATION share/icons/hicolor/scalable/apps
)
