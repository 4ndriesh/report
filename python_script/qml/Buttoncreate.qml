import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.4
import QtQuick 2.11
import QtQuick 2.10
import QtQuick.Window 2.10
import QtQuick.Controls 2.3

Rectangle {

                    Button {

                        id: control

                        text: qsTr(">>")
                        contentItem: Text {
                            text: control.text
                            font: control.font
                            opacity: enabled ? 1.0 : 0.3
                            color: control.down ? "red" : "black"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideRight
                        }
                            background: Rectangle {
                                implicitWidth: 30
                                implicitHeight: 30
                                opacity: enabled ? 1 : 0.3
                                border.color: control.down ? "red" : "black"
                                border.width: 2
                                radius: 10

                            // I want to change text color next
                            }
                        onClicked: {
                            store.sum(index, checked)
                        }
                    anchors.centerIn: parent
                    }
                    color: "grey"
                    width: 30;
                    Layout.fillHeight: true
//                    Layout.fillWidth: true
                    Layout.row: 1
                    Layout.column: 2
                }
