from sprite.mysprite import MySprite
import pygame

class TextSprite(MySprite):
    def __init__(self, _text):
        super(TextSprite, self).__init__()
        self.basicFont = pygame.font.SysFont(None, 48)
        self.textContent = _text
        self.color = (127,127,127)
        self.text = self.basicFont.render(_text, True, self.color)
    def draw(self, _screen, _positionX, _positionY):
        _screen.blit(self.text, (_positionX, _positionY))
    def update(self, _delta):
        MySprite.update(self, _delta)
    def addHighlight(self):
        self.color = (255,255,255)
        self.text = self.basicFont.render(self.textContent, True, self.color)
    def removeHighlight(self):
        self.color = (127,127,127)
        self.text = self.basicFont.render(self.textContent, True, self.color)