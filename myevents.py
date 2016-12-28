import pygame
from enum import Enum
from threading import Timer

#fajnie byoby to pozamieniac na enum ale mi sie nie chce 
COLLISION_EVENT = pygame.USEREVENT + 1
LOST_GAME_EVENT = pygame.USEREVENT + 2
REMOVE_OBJECT_EVENT = pygame.USEREVENT + 3
SCREEN_EFFECT_EVENT = pygame.USEREVENT + 4
GAME_STATE_CHANGE_EVENT = pygame.USEREVENT + 5
ENTITY_EFFECT_EVENT = pygame.USEREVENT + 6
MENU_EVENT = pygame.USEREVENT + 7

class ScreenEffectEvent(Enum):
    BLUR = 0
    COLOR_EXPLOSION = 1

class EventType(Enum):
    START = 0
    STOP = 1
    
class EntityEffect(Enum):
    SPEED_CHANGE = 0    

class MenuEventType(Enum):
    START_NEW_GAME = 0

def startTimer(_timeoutMs, _timeoutCallback):
    t = Timer(_timeoutMs / 1000, _timeoutCallback)
    t.start()