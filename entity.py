class Entity:
    """
    Class representing single in-game Entity
    """
    def __init__(self):
        """
        Constructor
        """
        self.artifacts = {}

    def addartifact(self, _artifact):
        """
        Add artifact to entity
        :param _artifact: Artifact to add
        :return: nothing
        """
        self.artifacts[_artifact.NAME] = _artifact
