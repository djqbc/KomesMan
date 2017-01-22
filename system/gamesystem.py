from myevents import GAME_EVENT, GAME_STATE_CHANGE_EVENT, MENU_EVENT, MenuEventType, starttimer, GameEventType, \
    ENTITY_EFFECT_EVENT, EntityEffect
from enum import IntEnum
import pygame


class GameState(IntEnum):
    """Enum representing game state"""
    MENU = 1
    END = 2
    GAME = 4
    INIT = 8
    LOST_GAME = 16
    WON_GAME = 32
    LOST_LIFE = 64


class GameSystem:
    NAME = "GameSystem"
    gameState = GameState.GAME

    def __init__(self):
        self.gameState = GameState.GAME
        self.activeTimer = None

    def remove(self, _entity):
        pass

    def input(self, _event):
        if _event.type == GAME_EVENT:
            if _event.reason == GameEventType.LOST_GAME:
                self.gameState = GameState.LOST_GAME
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.LOST_GAME))
                if self.activeTimer is not None:
                    self.activeTimer.cancel()
                self.activeTimer = starttimer(2000, lambda: pygame.event.post(
                    pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.MENU)))
            elif _event.reason == GameEventType.LOST_LIFE:
                self.gameState = GameState.LOST_LIFE
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.LOST_LIFE))
                pygame.event.post(pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.PLAY_SOUND,
                                                     path="res/sound/youlose.wav"))
                if self.activeTimer is not None:
                    self.activeTimer.cancel()
                self.activeTimer = starttimer(2000, lambda: pygame.event.post(
                    pygame.event.Event(MENU_EVENT, action=MenuEventType.RESTART_GAME)))
            elif _event.reason == GameEventType.WON_GAME:
                self.gameState = GameState.WON_GAME
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.WON_GAME))
                if self.activeTimer is not None:
                    self.activeTimer.cancel()
                self.activeTimer = starttimer(2000, lambda: pygame.event.post(
                    pygame.event.Event(MENU_EVENT, action=MenuEventType.CONTINUE_GAME)))
        elif _event.type == pygame.QUIT:
            self.gameState = GameState.END
            pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.END))
        elif _event.type == MENU_EVENT:
            if _event.action == MenuEventType.START_NEW_GAME or _event.action == MenuEventType.RESTART_GAME or _event.action == MenuEventType.CONTINUE_GAME:
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

    def update(self, _timedelta, _systems):
        pass

    def quit(self):
        return self.gameState == GameState.END

    def getcurrentgamestate(self):
        return self.gameState

    def endinit(self):
        self.gameState = GameState.MENU
        pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.MENU))
