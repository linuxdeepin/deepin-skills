# SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
#
# SPDX-License-Identifier: GPL-3.0-or-later

cmake_minimum_required(VERSION 3.16)
project(dde-shell-sysmon VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS LinguistTools DBus)
find_package(DDEShell REQUIRED)
find_package(Dtk6 REQUIRED COMPONENTS Core DConfig)

qt6_add_dbus_adaptor(DBUS_ADAPTOR_SOURCES
    org.deepin.ds.sysmon.xml
    sysmonpanel.h
    SysmonPanel
)

add_library(dde-sysmon SHARED
    sysmonpanel.h    sysmonpanel.cpp
    cpumonitor.h     cpumonitor.cpp
    memorymonitor.h  memorymonitor.cpp
    ${DBUS_ADAPTOR_SOURCES}
)

target_link_libraries(dde-sysmon PRIVATE
    Dde::Shell
    Dtk6::Core
    Qt6::DBus
)

target_include_directories(dde-sysmon PRIVATE ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR})

dtk_add_config_meta_files(
    APPID "org.deepin.dde.shell"
    FILES configs/org.deepin.ds.sysmon.json
)

ds_install_package(PACKAGE org.deepin.ds.sysmon TARGET dde-sysmon)
ds_handle_package_translation(PACKAGE org.deepin.ds.sysmon)

install(FILES misc/org.deepin.ds.sysmon.service
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/dbus-1/services
)
