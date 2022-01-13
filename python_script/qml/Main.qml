import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.4
import QtQuick 2.11

ApplicationWindow {

    color: "#C0C0C0"
    visible: true
    x: 400
    y: 200
    width: 1000
    height: 550
    title: "Create report"
    GridLayout{
            anchors.fill: parent
            columns: 4
                Projectlist{
                pixelSize:15
                internalModel: store
                column:1
                objectName : "project"
                dialogview: false
                }

                Projectlist{
                pixelSize:15
                internalModel: station
                column:2
                objectName : "station"
                dialogview: true
                }

                Projectlist{
                pixelSize:15
                internalModel: report
                column:3
                objectName : "report"
                dialogview: false
                }
    }

}