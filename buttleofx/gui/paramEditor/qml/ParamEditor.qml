import QtQuick 1.1
import QtDesktop 0.1

//parent of the ParamEditor is the Row of the ButtleAp
Rectangle {
    id: paramEditor

    property variant params 
    property variant currentParamNode

    property color background: "#212121"
    property color backgroundInput: "#141414"
    property color gradian1: background
    property color gradian2: "#111111"
    property color borderInput: "#333"

    property color textColor : "white"
    property color activeFocusOn : "white"
    property color activeFocusOff : "grey"

    implicitWidth: 300
    implicitHeight: 500

    color: background

    Rectangle{
        id: paramEditorTittle
        width: parent.width
        height: 40
        color: paramEditor.background

        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            color: textColor
            font.weight: Font.DemiBold
            horizontalAlignment: Text.AlignHCenter
            font.pointSize: 12
            text: "Parameters"
        }

        gradient: Gradient {
            GradientStop { position: 0.65; color: paramEditor.gradian1 }
            GradientStop { position: 1; color: paramEditor.gradian2 }
        }
    }
    
    
    /* Tuttle for the parameters from Tuttle */
    Rectangle{
        id: tuttleParamTittle
        width: paramEditor.width
        height: 40
        color: paramEditor.background
        y: paramEditorTittle.height

        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            color: textColor
            font.underline: true
            font.pointSize: 12
            text: "Node properties from Tuttle"
        }

        gradient: Gradient {
            GradientStop { position: 0.95; color: paramEditor.gradian1 }
            GradientStop { position: 1; color: paramEditor.gradian2 }
        }
    }

    /* Params depend on the node type (Tuttle data)*/
    ListView {
        id: tuttleParam
        interactive: false
        anchors.fill: parent
        anchors.margins: 20
        anchors.topMargin: 50 + tuttleParamTittle.height

        model: params
        
        delegate: Component {
            Loader {
                id: param
                source : model.object.paramType + ".qml"
                height: 30
                width: parent.width
            }
        }
    }

    Rectangle{
        id: buttleParamTittle
        width: paramEditor.width
        height: 40
        color: paramEditor.background
        y: tuttleParam.y + tuttleParam.contentHeight + 20

        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            color: textColor
            font.underline: true
            font.pointSize: 12
            text: "Node properties from Buttle"
        }

        gradient: Gradient {
            GradientStop { position: 0.95; color: paramEditor.gradian1 }
            GradientStop { position: 1; color: paramEditor.gradian2 }
        }
    }

    Loader {
        sourceComponent: currentParamNode ? nodeParamComponent : undefined
        anchors.fill: parent
        anchors.topMargin: 10
        Component {
            id: nodeParamComponent
            Column {
                spacing: 10
                y: buttleParamTittle.y + buttleParamTittle.height

                /*Name of the node (Buttle data)*/
                Item {
                    id: nodeNameUserItem
                    implicitWidth: 300
                    implicitHeight: 30
                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    Row {
                        id: nodeNameUserContainer
                        spacing: 10

                        /* Title */
                        Text {
                            id: nodeNameUserText
                            width: 80
                            anchors.top: parent.top
                            anchors.verticalCenter: parent.verticalCenter
                            color: textColor
                            text: "Name : "
                        }

                        /* Input field limited to 50 characters */
                        Rectangle {
                            height: 20
                            implicitWidth: 200
                            color: paramEditor.backgroundInput
                            border.width: 1
                            border.color: paramEditor.borderInput
                            radius: 3
                            TextInput {
                                id: nodeNameUserInput
                                text: currentParamNode.nameUser
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.leftMargin: 5
                                maximumLength: 100
                                selectByMouse : true
                                color: activeFocus ? activeFocusOn : activeFocusOff

                                onAccepted: currentParamNode.nameUser = nodeNameUserInput.text
                                onActiveFocusChanged: currentParamNode.nameUser = nodeNameUserInput.text

                                KeyNavigation.backtab: nodeColorRGBInput
                                KeyNavigation.tab: nodeCoordXInput


                            }
                        }
                    }
                }
            
                /* Type of the node (Buttle data) */
                Item {
                    id: nodeTypeItem
                    implicitWidth: 300
                    implicitHeight: 30
                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    Row {
                        id: nodeTypeContainer
                        spacing: 10

                        /* Title */
                        Text {
                            id: nodeTypeText
                            width: 80
                            text: "Type : "
                            color: textColor
                            anchors.top: parent.top
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        /* Input field limited to 50 characters */
                        Rectangle{
                            height: 20
                            implicitWidth: 200
                            color: "transparent"
                            Text{
                                id: nodeTypeInput
                                text: currentParamNode.nodeType
                                anchors.left: parent.left
                                anchors.leftMargin: 5
                                color: "grey"
                            }
                        }
                    }
                }

                /* Coord of the node (Buttle data) */
                Item {
                    id: nodecoordItem
                    implicitWidth: 300
                    implicitHeight: 30
                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    Row {
                        id: nodeCoordContainer
                        spacing: 10

                        /* Title */
                        Text {
                            id: nodeCoordText
                            width: 80
                            text: "Coord : "
                            color: textColor
                            anchors.top: parent.top
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        /* Input label : "x : " */
                        Rectangle {
                            height: 20
                            implicitWidth: 15
                            color: "transparent"
                            Text{
                                id: nodeCoordXLabel
                                text: "x :"
                                anchors.left: parent.left
                                anchors.leftMargin: 5
                                color: textColor
                            }
                        }
                        /* Input field limited : x */
                        Rectangle {
                            height: 20
                            implicitWidth: 35
                            color: paramEditor.backgroundInput
                            border.width: 1
                            border.color: paramEditor.borderInput
                            radius: 3
                            TextInput {
                                id: nodeCoordXInput
                                text: currentParamNode.coord.x
                                anchors.left: parent.left
                                anchors.leftMargin: 5
                                color: activeFocus ? activeFocusOn : activeFocusOff
                                selectByMouse : true

                                onAccepted: currentParamNode.coord.x = nodeCoordXInput.text
                                onActiveFocusChanged: currentParamNode.coord.x = nodeCoordXInput.text

                                KeyNavigation.backtab: nodeNameUserInput
                                KeyNavigation.tab: nodeCoordYInput

                            }
                        }

                        /* Input label : "y : " */
                        Rectangle {
                            height: 20
                            implicitWidth: 15
                            color: "transparent"
                            Text{
                                id: nodeCoordYLabel
                                text: "y :"
                                anchors.left: parent.left
                                anchors.leftMargin: 5
                                color: textColor
                            }
                        }
                        /* Input field limited : y */
                        Rectangle {
                            height: 20
                            implicitWidth: 35
                            color: paramEditor.backgroundInput
                            border.width: 1
                            border.color: paramEditor.borderInput
                            radius: 3
                            TextInput {
                                id: nodeCoordYInput
                                text: currentParamNode.coord.y
                                anchors.left: parent.left
                                anchors.leftMargin: 5
                                color: activeFocus ? activeFocusOn : activeFocusOff
                                selectByMouse : true

                                onAccepted: currentParamNode.coord.y = nodeCoordYInput.text
                                onActiveFocusChanged: currentParamNode.coord.y = nodeCoordYInput.text

                                KeyNavigation.backtab: nodeCoordXInput
                                KeyNavigation.tab: nodeColorRGBInput
                            }
                        }
                    }
                }

                /* Color of the node (Buttle data) */
                Item {
                    id: nodecolorItem
                    implicitWidth: 300
                    implicitHeight: 30
                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    Row {
                        id: nodeColorContainer
                        spacing: 10

                        /* Title */
                        Text {
                            id: nodeColorText
                            width: 80
                            text: "Color (Hex) : "
                            color: textColor
                            anchors.top: parent.top
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        /* Input field limited : rgb */
                        Rectangle {
                            height: 20
                            implicitWidth: 80
                            color: paramEditor.backgroundInput
                            border.width: 1
                            border.color: paramEditor.borderInput
                            radius: 3
                            TextInput {
                                id: nodeColorRGBInput
                                text: currentParamNode.color
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.leftMargin: 5
                                maximumLength: 50
                                selectByMouse : true
                                color: activeFocus ? activeFocusOn : activeFocusOff

                                onAccepted: currentParamNode.color = nodeColorRGBInput.text
                                onActiveFocusChanged: currentParamNode.color = nodeColorRGBInput.text

                                KeyNavigation.backtab: nodeCoordYInput
                                KeyNavigation.tab: nodeNameUserInput
                            }
                        }
                    }
                }
            }
        }
    }
}
