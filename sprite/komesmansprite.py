"""Komes man sprite package."""
from math import floor
import pygame
from sprite.mysprite import MySprite, AnimationState


class KomesManSprite(MySprite):
    """KomesMan."""

    def __init__(self, tilesize):
        """
        Constructor.

        :param tilesize: desired width and height of tile in pixels.
        """
        super(KomesManSprite, self).__init__()
        self.animations = {
            AnimationState.MOVE_UP: [
                pygame.image.load('res/img/PacU_001.png'),
                pygame.image.load('res/img/PacU_002.png'),
                pygame.image.load('res/img/PacU_003.png')
            ],
            AnimationState.MOVE_LEFT: [
                pygame.image.load('res/img/PacL_001.png'),
                pygame.image.load('res/img/PacL_002.png'),
                pygame.image.load('res/img/PacL_003.png')
            ],
            AnimationState.MOVE_RIGHT: [
                pygame.image.load('res/img/PacR_001.png'),
                pygame.image.load('res/img/PacR_002.png'),
                pygame.image.load('res/img/PacR_003.png')
            ],
            AnimationState.MOVE_DOWN: [
                pygame.image.load('res/img/PacD_001.png'),
                pygame.image.load('res/img/PacD_002.png'),
                pygame.image.load('res/img/PacD_003.png')
            ]
        }
        for k, value in self.animations.items():
            tmp = []
            for image in value:
                tmp.append(pygame.transform.scale(image, (tilesize, tilesize)))
            self.animations[k] = tmp
        self.image = self.animations[self.currentanimation][0]
        self.rect = self.image.get_rect()

    def draw(self, _screen, _positionx, _positiony):
        """
        Draw KomesMan (animated).

        :param _screen: screen surface
        :param _positionx: X position to draw item
        :param _positiony: Y position to draw item
        :return: nothing
        """
        diff = self.timeelapsed - floor(self.timeelapsed)
        if diff < 0.33:
            _screen.blit(self.animations[self.currentanimation][0], (_positionx, _positiony))
        elif diff < 0.66:
            _screen.blit(self.animations[self.currentanimation][1], (_positionx, _positiony))
        else:
            _screen.blit(self.animations[self.currentanimation][2], (_positionx, _positiony))

    def update(self, _delta):
        """
        Update sprite.

        :param _delta:
        :return: nothing
        """
        MySprite.update(self, _delta)
