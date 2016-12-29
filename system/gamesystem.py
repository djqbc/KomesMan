from myevents import LOST_GAME_EVENT, GAME_STATE_CHANGE_EVENT, MENU_EVENT,\
    MenuEventType, WON_GAME_EVENT
from enum import IntEnum
import pygame

class GameState(IntEnum):
    '''Enum representing game state'''
    MENU = 1
    END = 2
    GAME = 4
    INIT = 8

class GameSystem:
    NAME = "GameSystem"
    gameState = GameState.GAME  
    def __init__(self):
        self.gameState = GameState.GAME
    def remove(self, _entity):
        pass
    def input(self, _event):
        if _event.type == LOST_GAME_EVENT:
            self.gameState = GameState.END
            pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.END))
        elif _event.type == WON_GAME_EVENT:
            self.gameState = GameState.END
            pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.END))
        elif _event.type == pygame.QUIT:
            self.gameState = GameState.END
            pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.END))
        elif _event.type == MENU_EVENT:
            if _event.action == MenuEventType.START_NEW_GAME:
                self.gameState = GameState.GAME
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.GAME))
            if _event.action == MenuEventType.QUIT:
                self.gameState = GameState.END
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.END))
        elif _event.type == pygame.KEYUP:
            if _event.key == pygame.K_ESCAPE:
                if self.gameState == GameState.GAME:
                    self.gameState = GameState.MENU
                    pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.MENU))
    def update(self, _timeDelta, _systems):
        pass
    def quit(self):
        return (self.gameState == GameState.END)
    def getCurrentGameState(self):
        return self.gameState
    def endInit(self):
        self.gameState = GameState.MENU
        pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.MENU))