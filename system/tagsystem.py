"""
TagSystem module
"""
from artifact.tagartifact import TagArtifact, TagType


class TagSystem:
    """
    System responsible for getting objects tags
    """
    NAME = "TagSystem"

    def __init__(self):
        """
        Constructor
        """
        self.tags = {}

    def register(self, _object):
        """
        Register object for system
        :param _object: Object to be registered
        :return: nothing
        """
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
        """
        Remove object from system
        :param _entity: Entity to be removed
        :return: nothing
        """
        for _, subtype_dict in self.tags.items():
            for _, entity_list in subtype_dict.items():
                entity_list[:] = [entity for entity in entity_list if entity != _entity]

    def getentities(self, _type=TagType.KOMESMAN, _subtype=None):
        """
        Method responsible for getting entities of certain type
        :param _type: Type of entity to get
        :param _subtype: Subtype of entity to get
        :return: Entities list
        """
        type_dict = self.tags.get(_type, None)
        if type_dict is not None:
            if _subtype is not None:
                return type_dict.get(_subtype, [])
            else:
                result = []
                for _, entity_list in type_dict.items():
                    result += entity_list
                return result
        return []

    def update(self, _timedelta, _systems):
        """
        Update method stub
        :param _timedelta: game loop time delta
        :param _systems: all systems collection
        :return: nothing
        """
        pass

    def input(self, _event):
        """
        Input method stub
        :param _event: event to be processed
        :return: nothing
        """
        pass
