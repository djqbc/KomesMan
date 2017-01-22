from sprite.mysprite import MySprite
import pygame

class CapSprite(MySprite):
    """Cap item - catch them all!!!"""
    def __init__(self):
        super(CapSprite, self).__init__()
        self.image = pygame.image.load('res/img/cap.png')
        self.rect = self.image.get_rect()
    def draw(self, _screen, _positionX, _positionY):
        _screen.blit(self.image, (_positionX, _positionY))
    def update(self, _delta):
        MySprite.update(self, _delta)