DRAW_ALWAYS = 0xFFFFFFFF

class SpriteArtifact:
    NAME = "SpriteArtifact"
    def __init__(self, _sprite, _positionX=0, _positionY=0, _drawStage=DRAW_ALWAYS):
        self.sprite = _sprite
        self.positionX = _positionX
        self.positionY = _positionY
        self.drawStage = _drawStage