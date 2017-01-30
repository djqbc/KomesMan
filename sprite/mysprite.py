"""
My sprite package
"""
from enum import Enum
from enum import IntEnum
import pygame


class AnimationState(Enum):
    """
    Enum representing animation state
    """
    MOVE_UP = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3


class Modifiers(IntEnum):
    """
    Modifiers allowing to align text.
    """
    NONE = 0
    CENTER_H = 1
    CENTER_V = 2


class MySprite(pygame.sprite.Sprite):
    """
    Class defining my sprite.
    """
    def __init__(self):
        """
        Constructor
        """
        super(MySprite, self).__init__()
        self.timeelapsed = 0.0
        self.currentanimation = AnimationState.MOVE_UP
        self.animations = {}
        self.modifiers = Modifiers.NONE

    def draw(self, _screen, _positionx, _positiony):
        """
        Draw method stub
        :param _screen: unused
        :param _positionx: unused
        :param _positiony: unused
        :return: nothing
        """
        pass

    def changeanimation(self, _newanimation):
        """
        Change animation
        :param _newanimation: Animation for changing.
        :return:
        """
        if _newanimation != self.currentanimation:
            self.currentanimation = _newanimation
            self.timeelapsed = 0.0

    def update(self, _delta):
        """
        Update sprite
        :param _delta:
        :return: nothing
        """
        self.timeelapsed += _delta
