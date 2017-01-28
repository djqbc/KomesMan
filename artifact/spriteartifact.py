DRAW_ALWAYS = 0xFFFFFFFF
DRAW_NEVER = 0x00000000


class SpriteArtifact:
    """
    Container class for sprite properties
    """
    NAME = "SpriteArtifact"

    def __init__(self, _sprite, _positionx=0, _positiony=0, _drawstage=DRAW_ALWAYS):
        """
        Constructor
        :param _sprite: Sprite object.
        :param _positionx: X position of sprite in pixels
        :param _positiony: Y position of sprite in pixels
        :param _drawstage: Stage in which sprite should be shown.
        """
        self.sprite = _sprite
        self.positionX = _positionx
        self.positionY = _positiony
        self.drawStage = _drawstage
