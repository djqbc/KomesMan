from artifact.spriteartifact import SpriteArtifact
from artifact.tagartifact import TagArtifact
from entity import Entity
from sprite.wallsprite import WallSprite, WallKind, WallKindTrueTable, Direction, WallKindDirection

from system.drawsystem import DrawSystem
from system.tagsystem import TagSystem

class Board(Entity):
    def __init__(self, board, systems, tilesize=64):
        super(Board, self).__init__()
        self.map = [[Entity() for x in range(len(board))] for y in range(len(board[0]))] 
        self.tileSize = tilesize
        iX = 0
        for row in board:
            iY = 0
            for cell in row:
                if cell != 0:
                    tileSprite = WallSprite(cell)
                    self.map[iY][iX].addArtifact(SpriteArtifact(tileSprite, iY*tilesize, iX*tilesize))                    
                    systems[DrawSystem.NAME].register(self.map[iY][iX])
                iY += 1
            iX += 1
        self.addArtifact(TagArtifact("Board"))
        systems[TagSystem.NAME].register(self)
    
    def getWallkinds(self, _x, _y, _d):
        x1 = int((_x) // self.tileSize)
        y1 = int((_y) // self.tileSize)
        x = _x
        y = _y
        if _d == Direction.LEFT:
            x -= 3
        elif _d == Direction.RIGHT:
            x += 3
        elif _d == Direction.UP:
            y -= 3
        else:
            y += 3
        x = int((x) // self.tileSize)
        y = int((y) // self.tileSize)
        wallkind = nextWallkind = None
        if x1 == x and y1 == y:
            return [WallKind.NONE, WallKind.NONE]
        try:
            wallkind = self.map[x1][y1].artifacts[SpriteArtifact.NAME].sprite.wallkind
        except:
            wallkind = WallKind.NONE
        try:
            nextWallkind = self.map[x][y].artifacts[SpriteArtifact.NAME].sprite.wallkind
        except:
            nextWallkind = WallKind.NONE
        return [wallkind, nextWallkind]
        
    def checkMove(self, _posX, _posY, _dX, _dY):
        size = 10
        if _dX < 0:#try to go left
            wallkinds = self.getWallkinds(_posX + size, _posY + 32, Direction.LEFT)
            if not((wallkinds[0] in WallKindTrueTable.table[Direction.LEFT][WallKindDirection.OUT]) and (wallkinds[1] in WallKindTrueTable.table[Direction.LEFT][WallKindDirection.IN])):
                return False
        elif _dX > 0:#try to go right
            wallkinds = self.getWallkinds(_posX + 64 - size, _posY + 32, Direction.RIGHT)
            if not((wallkinds[0] in WallKindTrueTable.table[Direction.RIGHT][WallKindDirection.OUT]) and (wallkinds[1] in WallKindTrueTable.table[Direction.RIGHT][WallKindDirection.IN])):
                return False
        
        if _dY < 0:#try to go up
            wallkinds = self.getWallkinds(_posX + 32, _posY + size, Direction.UP)
            if not((wallkinds[0] in WallKindTrueTable.table[Direction.UP][WallKindDirection.OUT]) and (wallkinds[1] in WallKindTrueTable.table[Direction.UP][WallKindDirection.IN])):
                return False
        elif _dY > 0:#try to go down
            wallkinds = self.getWallkinds(_posX + 32, _posY + 64 - size, Direction.DOWN)
            if not((wallkinds[0] in WallKindTrueTable.table[Direction.DOWN][WallKindDirection.OUT]) and (wallkinds[1] in WallKindTrueTable.table[Direction.DOWN][WallKindDirection.IN])):
                return False
        
        return True