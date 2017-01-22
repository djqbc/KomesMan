DRAW_ALWAYS = 0xFFFFFFFF
DRAW_NEVER = 0x00000000


class SpriteArtifact:
    NAME = "SpriteArtifact"

    def __init__(self, _sprite, _positionx=0, _positiony=0, _drawstage=DRAW_ALWAYS):
        self.sprite = _sprite
        self.positionX = _positionx
        self.positionY = _positiony
        self.drawStage = _drawstage
