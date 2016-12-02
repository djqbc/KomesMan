from controller import Controller
import pygame

class UserController(Controller):
    def __init__(self):
        super().__init__()
    def input(self, _sprite, _event):
        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_DOWN:
                # to tylko brzydki przyk�ad - tutaj raczej powinno byc oznaczenie �e wektor ruchu jako� jest zmieniony
                # reszta magii - czyli ruch, zderzenia, regu�y itp. powinnien zdarzyc sie w funkcji update sprita 
                _sprite.moveBy(0, 1) 