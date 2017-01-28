from sprite.mysprite import MySprite, AnimationState
from math import floor
import pygame


class CopSprite(MySprite):
    """Bad cop"""

    def __init__(self, tilesize):
        """
        Constructor. Creates animation for each direction of movement.
        :param tilesize: desired width and height of tile in pixels.
        """
        super(CopSprite, self).__init__()
        self.animations = {
            AnimationState.MOVE_UP: [
                pygame.image.load('res/img/EneU_001.png'),
                pygame.image.load('res/img/EneU_002.png'),
                pygame.image.load('res/img/EneU_003.png')
            ],
            AnimationState.MOVE_LEFT: [
                pygame.image.load('res/img/EneL_001.png'),
                pygame.image.load('res/img/EneL_002.png'),
                pygame.image.load('res/img/EneL_003.png')
            ],
            AnimationState.MOVE_RIGHT: [
                pygame.image.load('res/img/EneR_001.png'),
                pygame.image.load('res/img/EneR_002.png'),
                pygame.image.load('res/img/EneR_003.png')
            ],
            AnimationState.MOVE_DOWN: [
                pygame.image.load('res/img/EneD_001.png'),
                pygame.image.load('res/img/EneD_002.png'),
                pygame.image.load('res/img/EneD_003.png')
            ]
        }
        for k, v in self.animations.items():
            tmp = []
            for image in v:
                tmp.append(pygame.transform.scale(image, (tilesize, tilesize)))
            self.animations[k] = tmp
        self.image = self.animations[self.currentAnimation][0]
        self.rect = self.image.get_rect()

    def draw(self, _screen, _positionx, _positiony):
        """
        Draw item
        :param _screen: screen surface
        :param _positionx: X position to draw item
        :param _positiony: Y position to draw item
        :return: nothing
        """
        diff = self.timeElapsed - floor(self.timeElapsed)
        if diff < 0.33:
            _screen.blit(self.animations[self.currentAnimation][0], (_positionx, _positiony))
        elif diff < 0.66:
            _screen.blit(self.animations[self.currentAnimation][1], (_positionx, _positiony))
        else:
            _screen.blit(self.animations[self.currentAnimation][2], (_positionx, _positiony))

    def update(self, _delta):
        """
        Update sprite
        :param _delta:
        :return: nothing
        """
        MySprite.update(self, _delta)
