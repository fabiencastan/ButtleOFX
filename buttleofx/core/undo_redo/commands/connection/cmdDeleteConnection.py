# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand


class CmdDeleteConnection(UndoableCommand):
    """
        Command that deletes a connection between 2 clips.
        Attributes :
        - graphTarget
        - connection : we save the buttle connection because we will need it for the redo
    """

    def __init__(self, graphTarget, connection):
        self._graphTarget = graphTarget
        self._connection = connection

    def undoCmd(self):
        """
            Undoes the delete of the connection <=> recreates the connection.
        """
        tuttleNodeSource = self._graphTarget.getNode(self._connection.getClipOut().getNodeName()).getTuttleNode()
        tuttleNodeOutput = self._graphTarget.getNode(self._connection.getClipIn().getNodeName()).getTuttleNode()
        self._graphTarget.getGraphTuttle().connect(tuttleNodeSource, tuttleNodeOutput)
        self._graphTarget.getConnections().append(self._connection)

        # emit signal
        self._graphTarget.connectionsChanged()

    def redoCmd(self):
        """
            Redoes the delete of the connection.
            Just calls the doCmd() function.
        """
        self.doCmd()

    def doCmd(self):
        """
            Deletes a connection.
        """
        # Get the output clip and the source clip of the tuttle connection
        tuttleNodeSource = self._graphTarget.getNode(str(self._connection.getClipOut().getNodeName())).getTuttleNode()
        tuttleNodeOutput = self._graphTarget.getNode(str(self._connection.getClipIn().getNodeName())).getTuttleNode()
        outputClip = tuttleNodeSource.getClip("Output")
        inputClip = tuttleNodeOutput.getClip(str(self._connection.getClipIn().getClipName()))

        # Delete the tuttle connection
        self._graphTarget.getGraphTuttle().unconnect(outputClip, inputClip)

        # Delete the buttle connection
        self._graphTarget.getConnections().remove(self._connection)

        # emit signal
        self._graphTarget.connectionsChanged()
