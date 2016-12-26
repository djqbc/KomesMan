from sprite.mysprite import MySprite, AnimationState
from math import floor
import pygame

class KomesManSprite(MySprite):
    '''KomesMan!!!!'''
    def __init__(self):
        super(KomesManSprite, self).__init__()
        self.animations = {
                AnimationState.MOVE_UP : [
                        pygame.image.load('res/img/PacU_001.png'),
                        pygame.image.load('res/img/PacU_002.png'),
                        pygame.image.load('res/img/PacU_003.png')
                    ],
                AnimationState.MOVE_LEFT : [
                        pygame.image.load('res/img/PacL_001.png'),
                        pygame.image.load('res/img/PacL_002.png'),
                        pygame.image.load('res/img/PacL_003.png')
                    ],
                AnimationState.MOVE_RIGHT : [
                        pygame.image.load('res/img/PacR_001.png'),
                        pygame.image.load('res/img/PacR_002.png'),
                        pygame.image.load('res/img/PacR_003.png')
                    ],
                AnimationState.MOVE_DOWN : [
                        pygame.image.load('res/img/PacD_001.png'),
                        pygame.image.load('res/img/PacD_002.png'),
                        pygame.image.load('res/img/PacD_003.png')
                    ]
            }
    def draw(self, _screen, _positionX, _positionY):
        diff = self.timeElapsed - floor(self.timeElapsed) 
        if diff < 0.33:
            _screen.blit(self.animations[self.currentAnimation][0], (_positionX, _positionY))
        elif diff < 0.66:
            _screen.blit(self.animations[self.currentAnimation][1], (_positionX, _positionY))
        else:
            _screen.blit(self.animations[self.currentAnimation][2], (_positionX, _positionY))
    def update(self, _delta):
        MySprite.update(self, _delta)