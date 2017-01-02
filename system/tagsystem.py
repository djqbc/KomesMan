from artifact.tagartifact import TagArtifact, TagType

class TagSystem:
    NAME = "TagSystem"
    def __init__(self):
        self.tags = {}
    def register(self, _object):
        if TagArtifact.NAME in _object.artifacts:   
            tagArtifact = _object.artifacts[TagArtifact.NAME]
            if tagArtifact.type in self.tags:
                if tagArtifact.subtype in self.tags[tagArtifact.type]:
                    self.tags[tagArtifact.type][tagArtifact.subtype].append(_object)
                else:
                    self.tags[tagArtifact.type][tagArtifact.subtype] = [_object]
            else:
                self.tags[tagArtifact.type] = {tagArtifact.subtype : [_object]}
        else:
            raise NameError("ERROR!!!")
    def remove(self, _entity):
        for _, subtypeDict in self.tags.items():
            for _, entityList in subtypeDict.items():
                entityList[:] = [entity for entity in entityList if entity != _entity]
    def getEntities(self, _type=TagType.KOMESMAN, _subtype=None):
        typeDict = self.tags.get(_type, None)
        if typeDict != None:
            if _subtype != None:
                return typeDict.get(_subtype, None)
            else:
                result = []
                for _, entityList in typeDict.items():
                    result += entityList
                return result
        return None
    def update(self, _timeDelta, _systems):
        pass
    def input(self, _event):
        pass