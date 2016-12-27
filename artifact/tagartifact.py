from enum import Enum
class TagType(Enum):
    KOMESMAN = 0
    ENEMY = 1
    ITEM = 2
    OTHER = 3

class TagArtifact:
    NAME = "TagArtifact"
    def __init__(self, _tag=None, _type=TagType.OTHER):
        self.tag = _tag
        self.type = _type