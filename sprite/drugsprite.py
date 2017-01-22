from sprite.mysprite import MySprite
import pygame

class DrugSprite(MySprite):
    """Drug item - one inhalation and everything is better ;)"""
    def __init__(self):
        super(DrugSprite, self).__init__()
        self.image = pygame.image.load('res/img/powderbag.png')
        self.rect = self.image.get_rect()
    def draw(self, _screen, _positionX, _positionY):
        _screen.blit(self.image, (_positionX, _positionY))
    def update(self, _delta):
        MySprite.update(self, _delta)