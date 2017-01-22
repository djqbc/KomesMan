from sprite.mysprite import MySprite
import pygame


class BeerSprite(MySprite):
    """Beer item - good, old Komes"""

    def __init__(self):
        super(BeerSprite, self).__init__()
        self.image = pygame.image.load('res/img/bottle.png')
        self.rect = self.image.get_rect()

    def draw(self, _screen, _positionX, _positionY):
        _screen.blit(self.image, (_positionX, _positionY))

    def update(self, _delta):
        MySprite.update(self, _delta)
