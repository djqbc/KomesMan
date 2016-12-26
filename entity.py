class Entity:
    def __init__(self):
        self.artifacts = {}
    def addArtifact(self, _artifact):
        self.artifacts[_artifact.NAME] = _artifact
    