// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: LGPL-3.0-or-later

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15

import org.deepin.ds 1.0

Window {
    id: root
    visible: true
    width: 200
    height: 200

    // LayerShell: top-right overlay
    DLayerShellWindow.anchors: DLayerShellWindow.AnchorTop
        | DLayerShellWindow.AnchorRight
    DLayerShellWindow.layer: DLayerShellWindow.LayerOverlay
    DLayerShellWindow.topMargin: 10
    DLayerShellWindow.rightMargin: 10
    DLayerShellWindow.keyboardInteractivity: DLayerShellWindow.KeyboardInteractivityNone

    color: "transparent"

    // Circular background
    Rectangle {
        id: circle
        anchors.centerIn: parent
        width: 190; height: 190
        radius: 95
        color: Qt.rgba(0, 0, 0, 0.82)
        border.color: Qt.rgba(255, 255, 255, 0.18)
        border.width: 1.5

        // Inner ring
        Rectangle {
            anchors { fill: parent; margins: 2 }
            radius: 93
            color: "transparent"
            border.color: Qt.rgba(255, 255, 255, 0.06)
            border.width: 1
        }

        Column {
            anchors.centerIn: parent
            width: 140
            spacing: 6

            // CPU
            Row {
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 8
                Text {
                    text: "CPU"; color: "#999"; font.pixelSize: 12
                    width: 28; anchors.verticalCenter: parent.verticalCenter
                }
                Rectangle {
                    width: 72; height: 6; radius: 3
                    color: Qt.rgba(255,255,255,0.1)
                    anchors.verticalCenter: parent.verticalCenter
                    Rectangle {
                        height: 6; radius: 3
                        width: parent.width * Applet.cpuUsage / 100
                        color: cpuColor()
                    }
                }
                Text {
                    text: Applet.cpuUsage + "%"; color: "#ddd"
                    font.pixelSize: 11; font.bold: true
                    width: 28; anchors.verticalCenter: parent.verticalCenter
                }
            }

            // Memory
            Row {
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 8
                Text {
                    text: "MEM"; color: "#999"; font.pixelSize: 12
                    width: 28; anchors.verticalCenter: parent.verticalCenter
                }
                Rectangle {
                    width: 72; height: 6; radius: 3
                    color: Qt.rgba(255,255,255,0.1)
                    anchors.verticalCenter: parent.verticalCenter
                    Rectangle {
                        height: 6; radius: 3
                        width: parent.width * Applet.memoryUsage / 100
                        color: memColor()
                    }
                }
                Text {
                    text: Applet.memoryUsage + "%"; color: "#ddd"
                    font.pixelSize: 11; font.bold: true
                    width: 28; anchors.verticalCenter: parent.verticalCenter
                }
            }

            // Disk
            Row {
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 8
                Text {
                    text: "DSK"; color: "#999"; font.pixelSize: 12
                    width: 28; anchors.verticalCenter: parent.verticalCenter
                }
                Rectangle {
                    width: 72; height: 6; radius: 3
                    color: Qt.rgba(255,255,255,0.1)
                    anchors.verticalCenter: parent.verticalCenter
                    Rectangle {
                        height: 6; radius: 3
                        width: parent.width * Applet.diskUsage / 100
                        color: diskColor()
                    }
                }
                Text {
                    text: Applet.diskUsage + "%"; color: "#ddd"
                    font.pixelSize: 11; font.bold: true
                    width: 28; anchors.verticalCenter: parent.verticalCenter
                }
            }

            // Divider
            Rectangle {
                width: 120; height: 1
                color: Qt.rgba(255,255,255,0.12)
                anchors.horizontalCenter: parent.horizontalCenter
            }

            // Hostname
            Text {
                text: Applet.hostname
                color: "#aaa"; font.pixelSize: 11
                anchors.horizontalCenter: parent.horizontalCenter
                elide: Text.ElideRight; width: 130
                horizontalAlignment: Text.AlignHCenter
            }

            // Uptime
            Text {
                text: "up " + Applet.uptimeStr
                color: "#777"; font.pixelSize: 10
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
    }

    function cpuColor() {
        var v = Applet.cpuUsage; if (v < 50) return "#4caf50"; if (v < 80) return "#ff9800"; return "#f44336"
    }
    function memColor() {
        var v = Applet.memoryUsage; if (v < 50) return "#4caf50"; if (v < 80) return "#ff9800"; return "#f44336"
    }
    function diskColor() {
        var v = Applet.diskUsage; if (v < 50) return "#4caf50"; if (v < 80) return "#ff9800"; return "#f44336"
    }
}
