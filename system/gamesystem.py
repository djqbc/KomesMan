from myevents import LOST_GAME_EVENT
from enum import Enum
import pygame

class GameState(Enum):
    '''Enum representing game state'''
    INIT = 0
    END = 1

class GameSystem:
    NAME = "GameSystem"
    gameState = GameState.INIT  
    def __init__(self):
        self.gameState = GameState.INIT
    def remove(self, _entity):
        pass
    def input(self, _event):
        if _event.type == LOST_GAME_EVENT:
            self.gameState = GameState.END
        elif _event.type == pygame.QUIT:
            self.gameState = GameState.END
    def update(self, _timeDelta, _systems):
        pass
    def quit(self):
        return (self.gameState == GameState.END)