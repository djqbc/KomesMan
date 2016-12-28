from myevents import LOST_GAME_EVENT, GAME_STATE_CHANGE_EVENT
from enum import Enum
import pygame

class GameState(Enum):
    '''Enum representing game state'''
    MENU = 0
    END = 1
    GAME = 2

class GameSystem:
    NAME = "GameSystem"
    gameState = GameState.MENU  
    def __init__(self):
        self.gameState = GameState.MENU
    def remove(self, _entity):
        pass
    def input(self, _event):
        if _event.type == LOST_GAME_EVENT:
            self.gameState = GameState.END
            pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.END))
        elif _event.type == pygame.QUIT:
            self.gameState = GameState.END
            pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.END))
    def update(self, _timeDelta, _systems):
        pass
    def quit(self):
        return (self.gameState == GameState.END)