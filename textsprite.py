from mysprite import MySprite
import pygame

class TextSprite(MySprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    text = None
    def __init__(self, _text):
        basicFont = pygame.font.SysFont(None, 48)
        self.text = basicFont.render(_text, True, (255,255,255), (0,0,0))
    def draw(self, _screen):
        textRect = self.text.get_rect()
        textRect.centerx = _screen.get_rect().centerx
        textRect.centery = _screen.get_rect().centery
        _screen.blit(self.text, textRect)
        