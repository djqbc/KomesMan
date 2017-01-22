from sprite.mysprite import MySprite, AnimationState
from math import floor
import pygame


class CopSprite(MySprite):
    """Bad cop"""

    def __init__(self):
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
        self.image = self.animations[self.currentAnimation][0]
        self.rect = self.image.get_rect()

    def draw(self, _screen, _positionx, _positiony):
        diff = self.timeElapsed - floor(self.timeElapsed)
        if diff < 0.33:
            _screen.blit(self.animations[self.currentAnimation][0], (_positionx, _positiony))
        elif diff < 0.66:
            _screen.blit(self.animations[self.currentAnimation][1], (_positionx, _positiony))
        else:
            _screen.blit(self.animations[self.currentAnimation][2], (_positionx, _positiony))

    def update(self, _delta):
        MySprite.update(self, _delta)
