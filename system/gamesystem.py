from myevents import GAME_EVENT, GAME_STATE_CHANGE_EVENT, MENU_EVENT, MenuEventType, starttimer, GameEventType, \
    ENTITY_EFFECT_EVENT, EntityEffect, SCREEN_EFFECT_EVENT, ScreenEffectEvent, EventType
from enum import IntEnum
import pygame


class GameState(IntEnum):
    """
    Enum representing game state
    """
    MENU = 1
    END = 2
    GAME = 4
    INIT = 8
    LOST_GAME = 16
    WON_GAME = 32
    LOST_LIFE = 64
    NEW_HIGHSCORE = 128
    SHOW_HIGHSCORES = 256
    PAUSED = 512

class GameSystem:
    """
    System responsible for maintaining game state.
    """
    NAME = "GameSystem"
    gameState = GameState.GAME

    def __init__(self):
        """
        Constructor
        """
        self.gameState = GameState.MENU
        self.activeTimer = None

    def remove(self, _entity):
        """
        Stub method
        :param _entity: unused
        :return: nothing
        """
        pass

    def input(self, _event):
        """
        Processes events connected with game state.
        Porcesses GAME_EVENT such as: NEW_HIGHSCORE, PAUSE_GAME, LOST_GAME, LOST_LIFE, WON_GAME
        Processes breaking game by pressing ESC
        :param _event: event to be processed
        :return: nothing
        """
        if _event.type == GAME_EVENT:
            if _event.reason == GameEventType.NEW_HIGHSCORE:
                self.gameState = GameState.LOST_GAME
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.LOST_GAME))
                if self.activeTimer is not None:
                    self.activeTimer.cancel()
                self.activeTimer = starttimer(1000, lambda: pygame.event.post(
                    pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.NEW_HIGHSCORE)))
            elif _event.reason == GameEventType.PAUSE_GAME:
                if self.gameState == GameState.GAME:
                    self.gameState = GameState.PAUSED
                    pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.GAME | GameState.PAUSED))
                    pygame.event.post(pygame.event.Event(SCREEN_EFFECT_EVENT, type=ScreenEffectEvent.PAUSE_EFFECT,
                                                         time = None, reason=EventType.START))
                elif self.gameState == GameState.PAUSED or self.gameState == GameState.PAUSED | GameState.GAME:
                    self.gameState = GameState.GAME
                    pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.GAME))
                    pygame.event.post(pygame.event.Event(SCREEN_EFFECT_EVENT, reason=EventType.STOP))
            elif _event.reason == GameEventType.LOST_GAME:
                self.gameState = GameState.LOST_GAME
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.LOST_GAME))
                if self.activeTimer is not None:
                    self.activeTimer.cancel()
                self.activeTimer = starttimer(1000, lambda: pygame.event.post(
                    pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.MENU)))
            elif _event.reason == GameEventType.LOST_LIFE:
                self.gameState = GameState.LOST_LIFE
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.LOST_LIFE))
                pygame.event.post(pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.PLAY_SOUND,
                                                     path="res/sound/youlose.wav"))
                if self.activeTimer is not None:
                    self.activeTimer.cancel()
                self.activeTimer = starttimer(1000, lambda: pygame.event.post(
                    pygame.event.Event(MENU_EVENT, action=MenuEventType.RESTART_GAME)))
            elif _event.reason == GameEventType.WON_GAME:
                self.gameState = GameState.WON_GAME
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.WON_GAME))
                if self.activeTimer is not None:
                    self.activeTimer.cancel()
                self.activeTimer = starttimer(1000, lambda: pygame.event.post(
                    pygame.event.Event(MENU_EVENT, action=MenuEventType.CONTINUE_GAME)))
        elif _event.type == pygame.QUIT:
            self.gameState = GameState.END
            pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.END))
        elif _event.type == GAME_STATE_CHANGE_EVENT:
            if _event.state == GameState.GAME | GameState.PAUSED:
                self.gameState = GameState.GAME | GameState.PAUSED
            if _event.state == GameState.GAME:
                self.gameState = GameState.GAME
                #to tylko na probe!!
        elif _event.type == MENU_EVENT:
#            if _event.action == MenuEventType.START_NEW_GAME or _event.action == MenuEventType.RESTART_GAME or _event.action == MenuEventType.CONTINUE_GAME:
#                self.gameState = GameState.GAME
#                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.GAME))
            if _event.action == MenuEventType.QUIT:
                self.gameState = GameState.END
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.END))
        elif _event.type == pygame.KEYUP:
            if _event.key == pygame.K_ESCAPE:
                if self.gameState == GameState.GAME:
                    self.gameState = GameState.MENU
                    pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.MENU))

    def update(self, _timedelta, _systems):
        """
        Stub method for updating systems.
        :param _timedelta: time delta of game loop
        :param _systems: all systems
        :return: nothing
        """
        pass

    def quit(self):
        """
        Ends game.
        :return: nothing
        """
        return self.gameState == GameState.END

    def getcurrentgamestate(self):
        """
        Game state getter
        :return: game state
        """
        return self.gameState

    def endinit(self):
        """
        Finishes initialization of system.
        :return: nothing
        """
        self.gameState = GameState.MENU
        pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.MENU))
