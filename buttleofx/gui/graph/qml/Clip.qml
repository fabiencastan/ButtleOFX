import QtQuick 1.1

Rectangle {
    property string port : parent.port

    height: clipSize
    width: clipSize
    color: "#bbbbbb"
    radius: 4

    MouseArea {
        anchors.fill: parent
        anchors.margins: -8
        hoverEnabled: true
        onPressed: {
            color = "red"
            _buttleData.clipPressed(m.nodeModel.name, port, index) // we send all information needed to identify the clip : nodename, port and clip number
        }
        onReleased: {
            color = "#bbbbbb"
             _buttleData.clipReleased(m.nodeModel.name, port, index)
        }
        onEntered: {
            color = "blue"
        }
        onExited: {
            color = "#bbbbbb"
        }
    }
}
