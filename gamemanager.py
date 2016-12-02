from enum import Enum
import sys, pygame
from drawmanager import SpriteManager
from textsprite import TextSprite

class GameState(Enum):
    '''Enum representing game state'''
    INIT = 0
    END = 1

class GameManager:
    '''Class managing game state''' 
    gameState = GameState.INIT  
    screen = None
    drawManager = None
    def __init__(self):
        pygame.init()
        self.gameState = GameState.INIT
        self.screen = pygame.display.set_mode((800, 600), 0, 32)
        pygame.display.set_caption('KomesMan')
        self.drawManager = SpriteManager()
        
        self.init()
    
    def update(self, _timeDelta):
        '''Updates current game state'''
        pass
    
    def init(self):
        self.drawManager.add(TextSprite('KomesMan'))
    
    def render(self, _updateMidstep):
        '''Renders currect scene'''
        self.screen.fill(pygame.Color('black'))
        self.drawManager.drawAll(self.screen)
        pygame.display.flip()
    
    def input(self, _event):
        if _event.type == pygame.QUIT:
            self.gameState = GameState.END
    
    def quit(self):
        return (self.gameState == GameState.END)