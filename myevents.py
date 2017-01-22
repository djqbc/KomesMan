from enum import Enum
from threading import Timer

import pygame

# fajnie byoby to pozamieniac na enum ale mi sie nie chce
# czemu mnie to nie dziwi?
# widze ze nie tylko mi sie nie chce ;)
# ogolnie odkrylem ze mozna miec tylko 8 eventow wlasnych - trzeba bedzie kompresowac
COLLISION_EVENT = pygame.USEREVENT + 0
GAME_EVENT = pygame.USEREVENT + 1
SCREEN_EFFECT_EVENT = pygame.USEREVENT + 2
GAME_STATE_CHANGE_EVENT = pygame.USEREVENT + 3
ENTITY_EFFECT_EVENT = pygame.USEREVENT + 4
MENU_EVENT = pygame.USEREVENT + 5


class ScreenEffectEvent(Enum):
    BLUR = 0
    COLOR_EXPLOSION = 1


class EventType(Enum):
    START = 0
    STOP = 1
    DELAYED = 2


class EntityEffect(Enum):
    SPEED_CHANGE = 0
    PICK_UP_CAP = 1
    PLAY_SOUND = 2
    TELEPORT = 3


class MenuEventType(Enum):
    START_NEW_GAME = 0  # start whole new game
    QUIT = 1
    MENU_IN = 2
    MENU_OUT = 3
    MAXIMIZE = 4
    RESTART_GAME = 5  # after loss of life
    CONTINUE_GAME = 6  # next level


class GameEventType(Enum):
    LOST_GAME = 0
    WON_GAME = 1
    REMOVE_OBJECT = 2
    REMOVE_ALL_OBJECTS = 3
    SET_MAX_POINTS = 4
    HUD_UPDATE = 5
    LOST_LIFE = 6
    SPAWN_OBJECT = 7


def starttimer(_timeoutms, _timeoutcallback):
    t = Timer(_timeoutms / 1000, _timeoutcallback)
    t.start()
    return t


def copyevent(_event):
    # todo: tu nie powinno byc dalej deepcopy ale na konkretnym elemencie ?

    tmp = {}
    for k, v in _event.dict.items():
        tmp[k] = v

    return pygame.event.Event(_event.type, tmp)
