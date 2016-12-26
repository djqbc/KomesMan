from artifact.spriteartifact import SpriteArtifact
from entity import Entity
from sprite.wallsprite import WallSprite

class Board(Entity):
    def __init__(self, board, drawSystem, tilesize=64):
        super(Board, self).__init__()
        x = 0
        for row in board:
            y=0
            for cell in row:
                y+=tilesize
                if cell != 0:
                    tileSprite = WallSprite(cell)
                    self.addArtifact(SpriteArtifact(tileSprite, x, y))
                    drawSystem.register(self)
            x+=tilesize

