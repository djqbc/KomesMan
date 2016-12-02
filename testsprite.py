from mysprite import MySprite
import pygame

class TestSprite(MySprite):
    '''Fake class used for testing purposes'''
    def __init__(self, _controller=None):
        super().__init__(_controller)
        self.image = pygame.Surface([20, 20])
        self.image.fill((255, 0, 0))
    def draw(self, _screen):
        _screen.blit(self.image, (self.x, self.y))
    def update(self, _delta):
        MySprite.update(self, _delta)