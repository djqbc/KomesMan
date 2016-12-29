from sprite.mysprite import MySprite
import pygame
from sprite.textsprite import TextSprite

class HUDSprite(MySprite):
    '''HUDSprite'''
    def __init__(self):
        super(HUDSprite, self).__init__()
#         self.image = pygame.image.load(_path)
#         self.rect = self.image.get_rect()
        self.text = TextSprite("")
    def draw(self, _screen, _positionX, _positionY):
        self.text.draw(_screen, _positionX, _positionY)
    def update(self, _delta, _text=None):
        MySprite.update(self, _delta)
        if _text != None:
            self.text = TextSprite(_text)