from artifact.tagartifact import TagArtifact, TagType


class TagSystem:
    NAME = "TagSystem"

    def __init__(self):
        self.tags = {}

    def register(self, _object):
        if TagArtifact.NAME in _object.artifacts:
            tag_artifact = _object.artifacts[TagArtifact.NAME]
            if tag_artifact.type in self.tags:
                if tag_artifact.subtype in self.tags[tag_artifact.type]:
                    self.tags[tag_artifact.type][tag_artifact.subtype].append(_object)
                else:
                    self.tags[tag_artifact.type][tag_artifact.subtype] = [_object]
            else:
                self.tags[tag_artifact.type] = {tag_artifact.subtype: [_object]}
        else:
            raise NameError("ERROR!!!")

    def remove(self, _entity):
        for _, subtypeDict in self.tags.items():
            for _, entityList in subtypeDict.items():
                entityList[:] = [entity for entity in entityList if entity != _entity]

    def getentities(self, _type=TagType.KOMESMAN, _subtype=None):
        type_dict = self.tags.get(_type, None)
        if type_dict is not None:
            if _subtype is not None:
                return type_dict.get(_subtype, [])
            else:
                result = []
                for _, entityList in type_dict.items():
                    result += entityList
                return result
        return []

    def update(self, _timedelta, _systems):
        pass

    def input(self, _event):
        pass
