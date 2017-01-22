from sprite.mysprite import MySprite
import pygame


class SimpleImageSprite(MySprite):
    """SimpleImageSprite"""

    def __init__(self, _path):
        super(SimpleImageSprite, self).__init__()
        self.image = pygame.image.load(_path)
        self.rect = self.image.get_rect()

    def draw(self, _screen, _positionX, _positionY):
        _screen.blit(self.image, (_positionX, _positionY))

    def update(self, _delta):
        MySprite.update(self, _delta)

    def size(self):
        return self.image.get_size()

    def scale(self, _x, _y):
        self.image = pygame.transform.scale(self.image, (_x, _y))
