from sprite.mysprite import MySprite, Modifiers
import pygame


class TextSprite(MySprite):
    def __init__(self, _text, _modifiers=Modifiers.NONE):
        super(TextSprite, self).__init__()
        self.modifiers = _modifiers
        self.basicFont = pygame.font.SysFont(None, 48)
        self.textContent = _text
        self.color = (127, 127, 127)
        self.text = self.basicFont.render(_text, True, self.color)

    def draw(self, _screen, _positionX, _positionY):
        if self.modifiers is not None:
            x = _positionX
            y = _positionY
            textWidth, textHeight = self.basicFont.size(self.textContent)
            if self.modifiers & Modifiers.CENTER_H:
                width = _screen.get_width() / 2
                x = width - textWidth / 2
            if self.modifiers & Modifiers.CENTER_V:
                height = _screen.get_height() / 2
                y = height - textHeight / 2
            _screen.blit(self.text, (x, y))
        else:
            _screen.blit(self.text, (_positionX, _positionY))

    def update(self, _delta):
        MySprite.update(self, _delta)

    def size(self):
        return self.basicFont.size(self.textContent)

    def addHighlight(self):
        self.color = (255, 255, 255)
        self.text = self.basicFont.render(self.textContent, True, self.color)

    def removeHighlight(self):
        self.color = (127, 127, 127)
        self.text = self.basicFont.render(self.textContent, True, self.color)
