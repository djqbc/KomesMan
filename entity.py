class Entity:
    def __init__(self):
        self.artifacts = {}

    def addartifact(self, _artifact):
        self.artifacts[_artifact.NAME] = _artifact
