from enum import Enum


class TagType(Enum):
    KOMESMAN = 0
    ENEMY = 1
    ITEM = 2
    FIXED = 3
    OTHER = 4


class TagSubType(Enum):
    NO_TYPE = 0
    # KOMESMAN
    # ---
    # ENEMY
    SIMPLE_COP = 5
    SUPER_COP = 6
    # ITEM
    CAP = 20
    PILL = 21
    DRUG = 22
    BEER = 23
    BAIT = 24
    # FIXED
    BOARD = 40
    TELEPORT = 41
    # OTHER
    PATHFINDER = 60


class TagArtifact:
    NAME = "TagArtifact"

    def __init__(self, _type=TagType.FIXED, _subtype=TagSubType.NO_TYPE):
        self.subtype = _subtype
        self.type = _type
