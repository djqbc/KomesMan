from sprite.mysprite import MySprite
import pygame

class TextSprite(MySprite):
    text = None
    timeElapsed = 0.0
    lastColor = (255,255,255)
    textContent = ""
    def __init__(self, _text):
        super().__init__()
        basicFont = pygame.font.SysFont(None, 48)
        self.textContent = _text
        self.text = basicFont.render(_text, True, (255,255,255), (0,0,0))
    def draw(self, _screen):
        textRect = self.text.get_rect()
        textRect.centerx = _screen.get_rect().centerx
        textRect.centery = _screen.get_rect().centery
        _screen.blit(self.text, textRect)
    def update(self, _delta):
        self.timeElapsed += _delta
        if self.timeElapsed > 5.0:
            self.timeElapsed = 0.0
            basicFont = pygame.font.SysFont(None, 48)
            if self.lastColor == (255, 255, 255):
                self.text = basicFont.render(self.textContent, True, (127,127,127), (0,0,0))
                self.lastColor = (127, 127, 127)
            else:
                self.text = basicFont.render(self.textContent, True, (255, 255, 255), (0,0,0))
                self.lastColor = (255, 255, 255)