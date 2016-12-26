from artifact.spriteartifact import SpriteArtifact
from entity import Entity
from sprite.wallsprite import WallSprite

class Board:
    def __init__(self, board, drawSystem, tilesize=64):
        self.map = [[Entity() for x in range(len(board))] for y in range(len(board[0]))] 
        iX = 0
        for row in board:
            iY = 0
            for cell in row:
                if cell != 0:
                    tileSprite = WallSprite(cell)
                    self.map[iY][iX].addArtifact(SpriteArtifact(tileSprite, iY*tilesize, iX*tilesize))
                    drawSystem.register(self.map[iY][iX])
                iY += 1
            iX += 1
