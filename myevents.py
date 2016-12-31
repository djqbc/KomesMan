import pygame
from enum import Enum
from threading import Timer
import copy

#fajnie byoby to pozamieniac na enum ale mi sie nie chce
#czemu mnie to nie dziwi?
#widze ze nie tylko mi sie nie chce ;)
#ogolnie odkrylem ze mozna miec tylko 8 eventow wlasnych - trzeba bedzie kompresowac 
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

class MenuEventType(Enum):
    START_NEW_GAME = 0
    QUIT = 1
    MENU_IN = 2
    MENU_OUT = 3
    
class GameEventType(Enum):
    LOST_GAME = 0
    WON_GAME = 1
    REMOVE_OBJECT = 2
    REMOVE_ALL_OBJECTS = 3
def startTimer(_timeoutMs, _timeoutCallback):
    t = Timer(_timeoutMs / 1000, _timeoutCallback)
    t.start()
    
def copyEvent(_event):
    tmp = copy.deepcopy(_event.dict)
    return pygame.event.Event(_event.type, tmp)