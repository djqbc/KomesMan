from enum import Enum
import sys, pygame
from spritemanager import SpriteManager
from textsprite import TextSprite
from testsprite import TestSprite
from usercontroller import UserController

class GameState(Enum):
    '''Enum representing game state'''
    INIT = 0
    END = 1

class GameManager:
    '''Class managing game state''' 
    gameState = GameState.INIT  
    screen = None
    spriteManager = None
    def __init__(self):
        pygame.init()
        self.gameState = GameState.INIT
        self.screen = pygame.display.set_mode((800, 600), 0, 32)
        pygame.display.set_caption('KomesMan')
        self.spriteManager = SpriteManager()
        
        self.init()
    
    def update(self, _timeDelta):
        '''Updates current game state'''
        # update state of sprites
        self.spriteManager.update(_timeDelta)
        # check game rules and do something with them
        # checkRules()
    
    def init(self):
        self.spriteManager.add(TextSprite('KomesMan'))
        self.spriteManager.add(TestSprite(_controller=UserController()))
    
    def render(self, _updateMidstep):
        '''Renders currect scene'''
        self.screen.fill(pygame.Color('black'))
        self.spriteManager.drawAll(self.screen)
        pygame.display.flip()
    
    def input(self, _event):
        if _event.type == pygame.QUIT:
            self.gameState = GameState.END
        else:
            self.spriteManager.inputAll(_event)
    
    def quit(self):
        return (self.gameState == GameState.END)