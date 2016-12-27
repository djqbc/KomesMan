import pygame
from enum import Enum

COLLISION_EVENT = pygame.USEREVENT + 1
LOST_GAME_EVENT = pygame.USEREVENT + 2
REMOVE_OBJECT_EVENT = pygame.USEREVENT + 3
SCREEN_EFFECT_EVENT = pygame.USEREVENT + 4

class ScreenEffectEvent(Enum):
    BLUR = 0
