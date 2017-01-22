from sprite.mysprite import MySprite
import pygame


class TestSprite(MySprite):
    """Fake class used for testing purposes"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill((255, 0, 0))

    def draw(self, _screen, _positionx, _positiony):
        _screen.blit(self.image, (_positionx, _positiony))

    def update(self, _delta):
        MySprite.update(self, _delta)
