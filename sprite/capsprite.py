from sprite.mysprite import MySprite
import pygame


class CapSprite(MySprite):
    """Cap item - catch them all!!!"""

    def __init__(self, tilesize):
        super(CapSprite, self).__init__()
        self.image = pygame.image.load('res/img/cap.png')
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect()

    def draw(self, _screen, _positionx, _positiony):
        _screen.blit(self.image, (_positionx, _positiony))

    def update(self, _delta):
        MySprite.update(self, _delta)
