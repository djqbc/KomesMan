from enum import Enum
from threading import Timer

import pygame

# Definition of custom events.
COLLISION_EVENT = pygame.USEREVENT + 0
GAME_EVENT = pygame.USEREVENT + 1
SCREEN_EFFECT_EVENT = pygame.USEREVENT + 2
GAME_STATE_CHANGE_EVENT = pygame.USEREVENT + 3
ENTITY_EFFECT_EVENT = pygame.USEREVENT + 4
MENU_EVENT = pygame.USEREVENT + 5


class ScreenEffectEvent(Enum):
    """
    Enum defining screen effects
    """
    BLUR = 0
    COLOR_EXPLOSION = 1
    PAUSE_EFFECT = 2

class EventType(Enum):
    """
    Enum defining types of events
    """
    START = 0
    STOP = 1
    DELAYED = 2


class EntityEffect(Enum):
    """
    Enum defining effects of entities.
    """
    SPEED_CHANGE = 0
    PICK_UP_CAP = 1
    PLAY_SOUND = 2
    TELEPORT = 3


class MenuEventType(Enum):
    """
    Enum defining menu events
    """
    START_NEW_GAME = 0  # start whole new game
    QUIT = 1
    MENU_IN = 2
    MENU_OUT = 3
    MAXIMIZE = 4
    RESTART_GAME = 5  # after loss of life
    CONTINUE_GAME = 6  # next level
    CHANGE_TILE_SIZE = 7
    UPDATE_NAME = 8
    SHOW_HIGHSCORES = 9


class GameEventType(Enum):
    """
    Enum defining types for game events.
    """
    LOST_GAME = 0
    WON_GAME = 1
    REMOVE_OBJECT = 2
    REMOVE_ALL_OBJECTS = 3
    SET_MAX_POINTS = 4
    HUD_UPDATE = 5
    LOST_LIFE = 6
    SPAWN_OBJECT = 7
    NEW_HIGHSCORE = 8
    PAUSE_GAME = 9


def starttimer(_timeoutms, _timeoutcallback):
    """
    Starts timer and executes action after time has finished
    :param _timeoutms: Milliseconds before event
    :param _timeoutcallback: Function to call after timeout
    :return:
    """
    t = Timer(_timeoutms / 1000, _timeoutcallback)
    t.start()
    return t


def copyevent(_event):
    """
    Copies event
    :param _event: Event to be copied
    :return: copy of event.
    """
    # todo: tu nie powinno byc dalej deepcopy ale na konkretnym elemencie ?

    tmp = {}
    for k, v in _event.dict.items():
        tmp[k] = v

    return pygame.event.Event(_event.type, tmp)
