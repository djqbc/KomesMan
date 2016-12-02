import pygame

class SpriteManager:
    '''Class helping with drawing all subscribed objects''' 
    allSprites = []
    def __init__(self):
        self.allSprites = pygame.sprite.Group()
    
    def drawAll(self, _screen):
        it = iter(self.allSprites)
        for sprite in it:
            sprite.draw(_screen);  
            
    def add(self, _sprite):
        self.allSprites.add(_sprite)
        
    def update(self, _delta):
        self.allSprites.update(_delta)
    
    def inputAll(self, _event):
        it = iter(self.allSprites)
        for sprite in it:
            sprite.input(_event);