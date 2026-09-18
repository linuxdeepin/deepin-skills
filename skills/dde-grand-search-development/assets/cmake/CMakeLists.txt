# DDE Grand Search 扩展搜索插件 —— 工程模板
#
# 用法：复制到新插件工程根目录，按需修改 PROJECT_NAME / 源文件列表 / 依赖。
# 关键点：
#   1. 可执行文件与 .conf 必须安装到同一个 searcher 插件目录
#   2. .conf 中的 Exec 由 configure_file 注入绝对路径，避免硬编码架构目录
#   3. CMAKE_INSTALL_FULL_LIBDIR 会自动展开为 /usr/lib/<arch>

cmake_minimum_required(VERSION 3.10)
project(my-search-plugin VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

# ── Qt 版本自动检测（优先 Qt6，回退 Qt5）──────────────────────────────
# 仅用到 Core 与 DBus；若插件需要访问剪贴板等 GUI 能力再加入 Gui
if (NOT DEFINED QT_VERSION_MAJOR)
    find_package(Qt6 QUIET COMPONENTS Core Gui DBus)
    if (Qt6_FOUND)
        set(QT_VERSION_MAJOR 6)
        message("   >>> Auto detected Qt version: 6")
    else()
        find_package(Qt5 QUIET COMPONENTS Core Gui DBus)
        if (Qt5_FOUND)
            set(QT_VERSION_MAJOR 5)
            message("   >>> Auto detected Qt version: 5")
        else()
            message(FATAL_ERROR "Neither Qt6 nor Qt5 found!")
        endif()
    endif()
else()
    message("   >>> Using specified Qt version: ${QT_VERSION_MAJOR}")
endif()

set(QT_NS Qt${QT_VERSION_MAJOR})
find_package(${QT_NS} REQUIRED COMPONENTS Core Gui DBus)

# ── 源文件 ───────────────────────────────────────────────────────────
set(PLUGIN_SOURCES
    ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/searcher.h
    ${CMAKE_CURRENT_SOURCE_DIR}/searcher.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/searchpluginadaptor.h
    ${CMAKE_CURRENT_SOURCE_DIR}/searchpluginadaptor.cpp
)

add_executable(${PROJECT_NAME} ${PLUGIN_SOURCES})

target_link_libraries(${PROJECT_NAME}
    PRIVATE
        ${QT_NS}::Core
        ${QT_NS}::Gui
        ${QT_NS}::DBus
)

# ── 安装 ─────────────────────────────────────────────────────────────
include(GNUInstallDirs)

# 扩展搜索插件目录：/usr/lib/<arch>/dde-grand-search-daemon/plugins/searcher
if (NOT DEFINED PLUGIN_INSTALL_DIR)
    set(PLUGIN_INSTALL_DIR
        ${CMAKE_INSTALL_FULL_LIBDIR}/dde-grand-search-daemon/plugins/searcher
    )
endif()
message("   >>> Plugin install dir: ${PLUGIN_INSTALL_DIR}")

install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION ${PLUGIN_INSTALL_DIR}
)

# 由 .conf.in 生成 .conf，注入可执行文件绝对路径
set(PLUGIN_EXEC_PATH "${PLUGIN_INSTALL_DIR}/${PROJECT_NAME}")
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/plugin.conf.in
    ${CMAKE_CURRENT_BINARY_DIR}/my-search.conf
    @ONLY
)

install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/my-search.conf
    DESTINATION ${PLUGIN_INSTALL_DIR}
)

# ── Trigger 模式可选：安装 D-Bus service 文件 ────────────────────────
# Trigger 模式下 DBus 依据该文件自动拉起插件进程。
# 若插件使用 Auto 或 Manual 模式，删除下面这段。
# install(
#     FILES ${CMAKE_CURRENT_BINARY_DIR}/my-search.service
#     DESTINATION ${CMAKE_INSTALL_FULL_DATADIR}/dbus-1/services
# )
