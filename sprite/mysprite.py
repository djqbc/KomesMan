from enum import Enum
from enum import IntEnum
import pygame

class AnimationState(Enum):
    '''Enum representing animation state'''
    MOVE_UP = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    
class Modifiers(IntEnum):
    NONE = 0
    CENTER_H = 1
    CENTER_V = 2

class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        super(MySprite, self).__init__()
        self.timeElapsed = 0.0
        self.currentAnimation = AnimationState.MOVE_UP
        self.animations = {}
        self.modifiers = Modifiers.NONE
    def draw(self, _screen, _positionX, _positionY):
        pass
    def changeAnimation(self, _newAnimation):
        if _newAnimation != self.currentAnimation:
            self.currentAnimation = _newAnimation
            self.timeElapsed = 0.0
    def update(self, _delta):
        self.timeElapsed += _delta