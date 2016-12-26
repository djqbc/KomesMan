from artifact.tagartifact import TagArtifact

class TagSystem:
    NAME = "TagSystem"
    def __init__(self):
        self.tags = {}
    def register(self, _object):
        if TagArtifact.NAME in _object.artifacts:   
            tag = _object.artifacts[TagArtifact.NAME].tag
            if tag in self.tags:
                self.tags[tag].append(_object)
            else:
                self.tags[tag] = [_object]
        else:
            raise NameError("ERROR!!!")
    def getEntities(self, _tag):
        return self.tags.get(_tag, None)
    def update(self, _timeDelta, _systems):
        pass