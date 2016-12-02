
class SpriteManager:
    '''Class helping with drawing all subscribed objects''' 
    toDraw = []
    def __init__(self):
        pass
    
    def drawAll(self, _screen):
        for sprite in self.toDraw:
            sprite.draw(_screen)
            
    def add(self, _drawable):
        self.toDraw.append(_drawable)