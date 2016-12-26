from enum import Enum
import sys, pygame

from board import Board
from predefinedboard import PredefinedBoard
from sprite.komesmansprite import KomesManSprite
from sprite.copsprite import CopSprite
from map import Map

from system.drawsystem import DrawSystem
from system.usermovementsystem import UserMovementSystem
from system.aimovementsystem import AiMovementSystem
from entity import Entity
from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
from artifact.tagartifact import TagArtifact

class GameState(Enum):
    '''Enum representing game state'''
    INIT = 0
    END = 1

class GameManager:
    '''Class managing game state''' 
    gameState = GameState.INIT  
    screen = None
    drawSystem = DrawSystem()
    userMoveSystem = UserMovementSystem()
    aiMoveSystem = AiMovementSystem()
    allSystems = [userMoveSystem, aiMoveSystem, drawSystem]#kolejnosc moze byc wazna
    
    def __init__(self):
        pygame.init()
        self.gameState = GameState.INIT
        self.screen = pygame.display.set_mode((1024, 768), 0, 32)
        pygame.display.set_caption('KomesMan')        
        self.init()
    
    def update(self, _timeDelta):
        '''Updates current game state'''
        for system in self.allSystems:
            system.update(_timeDelta)
    
    def init(self):
        self.helperCreateKomesMan()
        self.helperCreateCop(200, 0)
        self.helperCreateCop(400, 0)
        self.helperCreateBoard(PredefinedBoard().get_board())
        self.m = Map()
        self.m.generate()
    
    def render(self, _updateMidstep):
        '''Renders currect scene'''
        self.screen.fill(pygame.Color('black'))
#         self.m.draw(self.screen)
        self.drawSystem.draw(self.screen)
        pygame.display.flip()
    
    def input(self, _event):
        if _event.type == pygame.QUIT:
            self.gameState = GameState.END
        else:
            self.userMoveSystem.input(_event)
            self.aiMoveSystem.input(_event)
    
    def quit(self):
        return (self.gameState == GameState.END)
    
    def helperCreateKomesMan(self):
        komesMan = Entity()
        komesMan.addArtifact(SpriteArtifact(KomesManSprite(), 0, 0))
        komesMan.addArtifact(MovementArtifact())
        self.userMoveSystem.register(komesMan)
        self.drawSystem.register(komesMan)
        
    def helperCreateCop(self, _x, _y):
        cop = Entity()
        cop.addArtifact(SpriteArtifact(CopSprite(), _x, _y))
        cop.addArtifact(MovementArtifact())
        self.aiMoveSystem.register(cop)
        self.drawSystem.register(cop)

    def helperCreateBoard(self, predefinedboard):
        board = Board(predefinedboard, self.drawSystem)

