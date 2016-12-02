import pygame

class MySprite(pygame.sprite.Sprite):
    controller = None
    x = 0
    y = 0
    def __init__(self, _controller = None, _x = 0, _y = 0):
        super().__init__()
        self.controller = _controller
        self.x = _x
        self.y = _y
    def draw(self, _screen):
        pass
    def input(self, _event):
        if self.controller != None:
            self.controller.input(self, _event)
    def moveBy(self, _dX, _dY):
        self.x += _dX #
        self.y += _dY
    def update(self, _delta):
        #move
        pass