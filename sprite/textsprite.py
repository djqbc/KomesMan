from sprite.mysprite import MySprite
import pygame
from enum import IntEnum

class TextPosition(IntEnum):
    CENTER_H = 1
    CENTER_V = 2

class TextSprite(MySprite):
    def __init__(self, _text, _positioning=None):
        super(TextSprite, self).__init__()
        self.positioning = _positioning
        self.basicFont = pygame.font.SysFont(None, 48)
        self.textContent = _text
        self.color = (127,127,127)
        self.text = self.basicFont.render(_text, True, self.color)
    def draw(self, _screen, _positionX, _positionY):
        if self.positioning != None:
            x = _positionX
            y = _positionY
            textWidth, textHeight = self.basicFont.size(self.textContent)
            if self.positioning & TextPosition.CENTER_H:
                width = _screen.get_width() / 2
                x = width - textWidth / 2
            if self.positioning & TextPosition.CENTER_V:
                height = _screen.get_height() / 2
                y = height - textHeight / 2
            _screen.blit(self.text, (x, y))
        else:
            _screen.blit(self.text, (_positionX, _positionY))
    def update(self, _delta):
        MySprite.update(self, _delta)
    def addHighlight(self):
        self.color = (255,255,255)
        self.text = self.basicFont.render(self.textContent, True, self.color)
    def removeHighlight(self):
        self.color = (127,127,127)
        self.text = self.basicFont.render(self.textContent, True, self.color)