import QtQuick 2.11
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3


Rectangle {
                border.color: "black"
                color: "#DCDCDC"
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.row: 1
                Layout.column: 1
                             ListView {
                                        id: listproject
                                        anchors {
                                            top: parent.top
                                            left: parent.left
                                            right: parent.right
                                            bottom: parent.verticalCenter
                                            margins: 10
                                        }


                                        delegate: CheckBox
                                        {
                                                id: checkBoxDelegate
                                                checked: true

                                                Text{
                                                   text: name[0]
                                                   font.pixelSize: 16
                                                   anchors { left: parent.left; margins: 30 }
//                                                   color: "black"
                                                }

//                                                        text: name
                                                indicator: Rectangle
                                                {
                                                     implicitHeight:16
                                                     implicitWidth:16
                                                     radius: 3
                                                     border.color: activeFocus ? "darkblue" : "grey"
                                                     border.width: 1
                                                     Rectangle
                                                     {
                                                         visible: checked
                                                         color: "red"
                                                         border.color: "black"
                                                         radius: 1
                                                         anchors.margins: 4
                                                         anchors.fill: parent
                                                     }
                                                }



                                            onClicked: {
                                                // При изменении состояния чекбокса производим установку его состояния в модель данных
                                                store.sum(name, checked)
                                            }

                                        }
                                    model: store.channels

                             }
                }