from buttleofx.gui.graph import Graph
from buttleofx.gui.graph.node import NodeWrapper
from buttleofx.gui.graph.connection import ConnectionWrapper, IdClip
from buttleofx.core.undo_redo.manageTools import CommandManager

from quickmamba.models import QObjectListModel
from quickmamba.patterns import Signal
from quickmamba.patterns import Singleton

from PySide import QtDeclarative, QtCore


class GraphWrapper(QtCore.QObject, Singleton):
    """
        Class GraphWrapper defined by:
        - _engine : to have the view engine
        - _rootObject : to have the root object
        - _nodeWrappers : list of node wrappers (the python objects we use to communicate with the QML)
        - _connectionWrappers : list of connections wrappers (the python objects we use to communicate with the QML)
        - _currentNode : the current selected node (in QML). This is just the nodeName.
        - _tmpClipOut : the future connected output clip when a connection is beeing created. It correspounds of the output clip which was beeing clicked and not connected for the moment.
        - _tmpClipIn : the future connected input clip when a connection is beeing created. It correspounds of the input clip which was beeing clicked and not connected for the moment.
        - _zMax : to manage the depth of the graph (in QML)
        - _graph : the data of the graph (python objects, the core data : the nodes and the connections)

        Creates a QObject from a given python object Graph.
    """

    def __init__(self, graph, view):
        super(GraphWrapper, self).__init__(view)

        self._view = view
        self._engine = view.engine()
        self._rootObject = view.rootObject()

        self._nodeWrappers = QObjectListModel(self)
        self._connectionWrappers = QObjectListModel(self)

        self._currentNode = None
        self._currentImage = ""
        self._tmpClipIn = None
        self._tmpClipOut = None

        self._zMax = 2

        self._graph = graph

        # the links between the graph and this graphWrapper
        graph.nodeDeleted.connect(self.deleteNodeWrapper)
        graph.nodeDeleted.connect(self.deleteCurrentNode)

        graph.nodesChanged.connect(self.updateNodes)
        graph.connectionsChanged.connect(self.updateConnections)

    def __str__(self):
        """
            Displays on terminal some data.
            Usefull to debug the class.
        """
        print("---- all nodeWrappers ----")
        for nodeWrapper in self._nodeWrappers:
            print nodeWrapper.getName() + " " + str(nodeWrapper.getCoord())

        print("---- all nodes ----")
        for node in self._graph._nodes:
            print node._name + " " + str(node.getCoord())

        print("---- all connectionWrappers ----")
        for con in self._connectionWrappers:
            con.__str__()

        print("---- all connections ----")
        for con in self._graph._connections:
            con.__str__()

    @QtCore.Slot(result="QVariant")
    def getGraph(self):
        """
            Returns the graph (the node list and the connection list).
        """
        return self._graph

    @QtCore.Slot(result="QVariant")
    def getNodeWrappers(self):
        """
            Returns the nodeWrapper list.
        """
        return self._nodeWrappers

    def getNodeWrapper(self, nodeName):
        for node in self._nodeWrappers:
            if node.getName() == nodeName:
                return node

    @QtCore.Slot()
    def getConnectionWrappers(self):
        """
            Return the connectionWrapper list.
        """
        return self._connectionWrappers

    @QtCore.Slot(str, CommandManager)
    def creationProcess(self, nodeType, cmdManager):
        """
            Function called when we want to create a node from the QML.
        """
        self._graph.createNode(nodeType, cmdManager)
        # debug
        self.__str__()

    def getPositionClip(self, nodeName, port, clipNumber):
        """
            Function called when a new idClip is created.
            Returns the position of the clip.
            The calculation is the same as in the QML file (Node.qml).
        """
        nodeCoord = self._graph.getNode(nodeName).getCoord()
        widthNode = 110
        heightEmptyNode = 35
        clipSpacing = 7
        clipSize = 8
        nbInput = self._graph.getNode(nodeName).getNbInput()
        heightNode = heightEmptyNode + clipSpacing * nbInput
        inputTopMargin = (heightNode - clipSize * nbInput - clipSpacing * (nbInput - 1)) / 2

        if (port == "input"):
            xClip = nodeCoord[0] - clipSize / 2
            yClip = nodeCoord[1] + inputTopMargin + (clipNumber) * (clipSpacing + clipSize) + clipSize / 2
        elif (port == "output"):
            xClip = nodeCoord[0] + widthNode + clipSize / 2
            yClip = nodeCoord[1] + heightNode / 2 + clipSize / 2
        return (xClip, yClip)

    @QtCore.Slot(str, str, int)
    def clipPressed(self, nodeName, port, clipNumber):
        """
            Function called when a clip is pressed (but not released yet).
            The function replace the tmpClipIn or tmpClipOut.
        """
        position = self.getPositionClip(nodeName, port, clipNumber)
        #position = self._graph.getNode(nodeName).getCoord()
        idClip = IdClip(nodeName, port, clipNumber, position)
        if (port == "input"):
            print "inputPressed"
            self._tmpClipIn = idClip
            print "Add tmpNodeIn: " + nodeName + " " + port + " " + str(clipNumber)
        elif (port == "output"):
            print "outputPressed"
            self._tmpClipOut = idClip
            print "Add tmpNodeOut: " + nodeName + " " + port + " " + str(clipNumber)

    @QtCore.Slot(str, str, int)
    def clipReleased(self, nodeName, port, clipNumber):

        if (port == "input"):
            #if there is a tmpNodeOut we can connect the nodes
            print "inputReleased"
            if (self._tmpClipOut != None and self._tmpClipOut._nodeName != nodeName):
                position = self.getPositionClip(nodeName, port, clipNumber)
                #position = self._graph.getNode(nodeName).getCoord()
                idClip = IdClip(nodeName, port, clipNumber, position)
                self._graph.createConnection(self._tmpClipOut, idClip)
                self._tmpClipIn = None
                self._tmpClipOut = None
                self.__str__()

        elif (port == "output"):
            #if there is a tmpNodeIn we can connect the nodes
            print "inputReleased"
            if (self._tmpClipIn != None and self._tmpClipIn._nodeName != nodeName):
                position = self.getPositionClip(nodeName, port, clipNumber)
                #position = self._graph.getNode(nodeName).getCoord()
                idClip = IdClip(nodeName, port, clipNumber, position)
                self._graph.createConnection(idClip, self._tmpClipIn)
                self._tmpClipIn = None
                self._tmpClipOut = None
                self.__str__()

    def createNodeWrapper(self, nodeName):
        """
            Creates a node wrapper and add it to the nodeWrappers list.
        """
        print "createNodeWrapper"
        #wrapper = NodeWrapper(self._graph._nodes[nodeId])

        # search the right node in the node list
        for node in self._graph._nodes:
            if node.getName() == nodeName:
                nodeWrapper = NodeWrapper(node, self._view)
                self._nodeWrappers.append(nodeWrapper)
                #self.setCurrentNode(nodeWrapper.getName())
        # commandManager.doCmd( CmdCreateNodeWrapper(nodeId) )

    ############# CONNECTIONS #############

    def createConnectionWrapper(self, connection):
        """
            Creates a connection wrapper and add it to the connectionWrappers list.
        """
        print "begin creation of new ConnectionWrapper. (coordinates of corresponding Line should be displayed here in QML before end of the creation :"
        conWrapper = ConnectionWrapper(connection)
        self._connectionWrappers.append(conWrapper)
        print "end creation of new ConnectionWrapper.\n"
        # commandManager.doCmd( CmdCreateConnectionWrapper(clipOut, clipIn) )

    def updateConnections(self):
        """
            Updates the connectionWrappers when the signal connectionsChanged has been emited.
        """
        print "Begin update connectionWrappers."
        # we clear the list
        self._connectionWrappers.clear()
        # and we fill with the new data
        print " _connectionWrappers now empty. Begin of loop."
        for connection in self._graph.getConnections():
            print "Connection found."
            self.createConnectionWrapper(connection)
            print "ConnectionWrapper created."
        print "End update connectionWrappers.\n"

    def updateNodes(self):
        """
            Updates the nodeWrappers when the signal nodesChanged has been emited.
        """
        # we clear the list
        self._nodeWrappers.clear()
        # and we fill with the new data
        for node in self._graph.getNodes():
            self.createNodeWrapper(node.getName())

    @QtCore.Slot()
    def destructionProcess(self):
        """
            Function called when we want to delete a node from the QML.
        """
        # if at least one node in the graph
        if len(self._nodeWrappers) > 0 and len(self._graph._nodes) > 0:
            # if a node is selected
            if self._currentNode != None:
                self._graph.deleteNode(self._currentNode)
        # debug
        self.__str__()

    def deleteNodeWrapper(self, indiceW):
        print "deleteNodeWrapper"
        self._nodeWrappers.removeAt(indiceW)
        # commandManager.doCmd( CmdDeleteNodeWrapper(indiceW) )

    @QtCore.Slot(result="QVariant")
    def getCurrentNode(self):
        """
            Return the name of the current selected node.
        """
        return self._currentNode

    @QtCore.Slot(str)
    def setCurrentNode(self, nodeName):
        """
            Change the current selected node and emit the change.
        """
        print "setCurrentNode : " + str(nodeName)

        if self._currentNode == nodeName:
            return

        #we search the image of the selected node
        for nodeWrapper in self._nodeWrappers:
            if nodeWrapper.getName() == self._currentNode:
                self.setCurrentImage(nodeWrapper.getImage())
                self.currentImageChanged.emit()
                print(self._currentImage)

        self._currentNode = nodeName
        self.currentNodeChanged.emit()

    def getCurrentImage(self):
        """
            Return the url of the current image
        """
        return self._currentImage

    def setCurrentImage(self, urlImage):
        """
            Change the currentImage, displayed in the viewer
        """
        self._currentImage = urlImage

    def deleteCurrentNode(self, indiceW):
        """
            Delete the current selected node by calling the deleteNode() function.
        """
        print "deleteCurrentNode"
        self._currentNode = None

    @QtCore.Slot(result="double")
    def getZMax(self):
        return self._zMax

    @QtCore.Slot()
    def setZMax(self):
        self._zMax += 1

    nodesChanged = QtCore.Signal()
    nodes = QtCore.Property("QVariant", getNodeWrappers, notify=nodesChanged)
    connectionWrappersChanged = QtCore.Signal()
    connections = QtCore.Property("QVariant", getConnectionWrappers, notify=connectionWrappersChanged)
    currentNodeChanged = QtCore.Signal()
    currentNode = QtCore.Property(str, getCurrentNode, setCurrentNode, notify=currentNodeChanged)
    currentImageChanged = QtCore.Signal()
    currentImage = QtCore.Property(str, getCurrentImage, setCurrentImage, notify=currentImageChanged)