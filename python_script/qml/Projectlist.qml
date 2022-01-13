import QtQuick 2.11
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
 import QtQuick.Window 2.2
 import QtQuick 2.10
import QtQuick.Window 2.10
import QtQuick.Controls 2.3




Rectangle {
property bool dialogview

Dialogwin{
id: dialogAndroid
}
Highlightcomp{id: highlight}

        property var internalModel
        property int column
        property string objectName
        property int pixelSize

                border.color: "black"
                color: "Gainsboro"
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.row: 1
                Layout.column: column
                                ListView {
                                    id:lv
                                    objectName : parent.objectName
                                    model: internalModel.channels
                                    anchors.fill: parent

                                    delegate: Item {
                                    id: item
                                    property var view: ListView.view
                                    property var isCurrent: ListView.isCurrentItem
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    height: 45

                                        GridLayout{
                                            anchors.fill: parent
                                            anchors.margins: 10
                                            columns: 2

                                                    Rectangle {
                                                        border.color: "DarkGrey"
                                                        border.width: 1
                                                        Text{
                                                            id: com
                                                            width: parent.width
                                                            horizontalAlignment: Text.AlignLeft
                                                            anchors.centerIn: parent
                                                            font.pixelSize: pixelSize
                                                            color: "black"
                                                            text: name
//                                                            verticalAlignment: Text.AlignVCenter
//                                                            horizontalAlignment: Text.AlignHCenter
                                                            elide: Text.ElideRight
                                                        }


                                                        MouseArea {
                                                            property int mouseButtonClicked: Qt.NoButton

                                                            acceptedButtons: Qt.RightButton | Qt.LeftButton

                                                            anchors.fill: parent

                                                            onPressed: {
                                                                if (pressedButtons & Qt.LeftButton) {
                                                                    mouseButtonClicked = Qt.LeftButton
                                                                } else if (pressedButtons & Qt.RightButton) {
                                                                    mouseButtonClicked = Qt.RightButton
                                                                }
                                                            }

                                                            onClicked: {
                                                                if (mouseButtonClicked === Qt.LeftButton) {
                                                                    internalModel.sum(lv.objectName, name),
                                                                    view.currentIndex = index
                                                                } else if (mouseButtonClicked === Qt.RightButton) {
//                                                                    firstContextMenu.open(),view.currentIndex = index
                                                                }
                                                            }

                                                            onDoubleClicked: {
                                                                if(lv.objectName=="station"){
                                                                dialogAndroid.name=name,
                                                                dialogAndroid.objectName1=lv.objectName,
                                                                dialogAndroid.internalModel=internalModel,
                                                                dialogAndroid.open(),view.currentIndex = index;}
//
//
                                                            }


                                                                                                                }

                                                        color: "#DCDCDC"
                                                        Layout.fillHeight: true
                                                        Layout.fillWidth: true
                                                        Layout.row: 1
                                                        Layout.column: 1
                                                    }


//                                                    Buttoncreate{visible: buttoncheck}
                                        }
                                    }
                                highlight: highlight
                                highlightFollowsCurrentItem: true
                                highlightMoveDuration : 10
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                ScrollBar.vertical: ScrollBar {}
                                }

                }