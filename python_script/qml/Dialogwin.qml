import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.1
// Создаём объект диалогового окна
        Dialog {
            property string name
            property var internalModel
            property string objectName1
            /* Когда деплоите под Android-устройства,
             * обязательно закоментируйте эти две строки,
             * иначе словите глюки в работе устройства
             */
            width: 300  // Задаём ширину диалога, работает на десктопе, но на Android не сработает
            height: 100 // Задаём высоту диалога, работает на декстопе, но на Android не сработает

            // Создаём содержимое диалогового окна
            contentItem: Rectangle {
                width: 300          // Устанавливаем ширину, необходимо для Android-устройства
                height: 100         // Устанавливаем высоту, необходимо для Android-устройства
                color: "#f7f7f7"    // Задаём цвет

                // Область для сообщения диалогового окна
                Rectangle {
                    /* Прибиваем область к левой, правой и верхней частям диалога,
                     * а также снизу к разделителю, который отделяет область от кнопок
                     */
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: dividerHorizontal.top
                    color: "#f7f7f7"  // Задаём цвет области

                    // Задаём сообщение диалогового окна
                    Label {
                        id: textLabel
                        text: "Создать ведомость "+name
                        color: "black"
                        anchors.centerIn: parent // Помещаем сообщение в центре области для сообщения
                    }
                }

                // Создаём горизонтальный разделитель с помощью Rectangle
                Rectangle {
                    id: dividerHorizontal
                    color: "#d7d7d7"
                    height: 2 // Устанавливаем ширину в два пикселя
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: row.top
                }

                /* Создаём подложку для кнопок в виде объекта Строки
                 * В данном объекте для объектов детей не работают некоторые параметры
                 * anchors, кроме параметров anchors.top и anchors.bottom
                 */
                Row {
                    id: row
                    height: 50 // Задаём высоту
                    // А также прибиваем строку к низу диалогового окна
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    anchors.right: parent.right

                    Button {
                        id: dialogButtonCancel
                        // Растягиваем кнопку по высоте строки
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        // Задаём ширину кнопки на половину строки минус 1 пиксель
                        width: parent.width / 2 - 1

                        // Стилизуем кнопку
                        style: ButtonStyle {
                            background: Rectangle {
                                color: control.pressed ? "#d7d7d7" : "#f7f7f7"
                                border.width: 0
                            }

                            label: Text {
                                text: qsTr("Cancel")
                                color: "#34aadc"
                                // Устанавливаем текст в центр кнопки
                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                        // По нажатию кнопки закрываем диалог
                        onClicked: dialogAndroid.close()
                    }

                    // Создаём разделитель между кнопками шириной в 2 пикселя
                    Rectangle {
                        id: dividerVertical
                        width: 2
                        // Растягиваем разделитель по высоте объекта строки
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        color: "#d7d7d7" // Задаём цвет разделителя
                    }

                    Button {
                        id: dialogButtonOk
                        // Растягиваем кнопку по высоте строки
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        // Задаём ширину кнопки на половину строки минус 1 пиксель
                        width: parent.width / 2 - 1

                        // Стилизуем кнопку
                        style: ButtonStyle {
                            background: Rectangle {
                                color: control.pressed ? "#d7d7d7" : "#f7f7f7"
                                border.width: 0
                            }

                            label: Text {
                                text: qsTr("Ok")
                                color: "#34aadc"
                                // Устанавливаем текст в центр кнопки
                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                        // По нажатию кнопки закрываем диалог
                          onClicked: internalModel.openfile(objectName1, name),dialogAndroid.close()
                    }
                }
            }
        }
