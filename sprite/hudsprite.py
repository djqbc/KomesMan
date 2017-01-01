from sprite.mysprite import MySprite, Modifiers
from sprite.textsprite import TextSprite
from sprite.simpleimagesprite import SimpleImageSprite

class HUDSprite(MySprite):
    '''HUDSprite'''
    def __init__(self, _modifiers=Modifiers.NONE):
        super(HUDSprite, self).__init__()
        self.modifiers = _modifiers
        self.textPoints = TextSprite("")
        self.imageLifes = SimpleImageSprite("res/img/life.png")
        self.imageLifes.scale(self.textPoints.size()[1], self.textPoints.size()[1])
        self.textLifes = TextSprite("")
    def draw(self, _screen, _positionX, _positionY):        
        textPointsWidth, _ = self.textPoints.size()
        imageLifesWidth, _ = self.imageLifes.size()
        textLifesWidth, _ = self.textLifes.size()
        
        if self.modifiers & Modifiers.CENTER_H:
            width = _screen.get_width() / 2
            x = width - (textPointsWidth + imageLifesWidth + textLifesWidth + 20) / 2
            self.textPoints.draw(_screen, x, _positionY)
            self.imageLifes.draw(_screen, x + textPointsWidth + 10, _positionY)
            self.textLifes.draw(_screen, x + textPointsWidth + imageLifesWidth + 20, _positionY)
        else:
            self.textPoints.draw(_screen, _positionX, _positionY)
            self.imageLifes.draw(_screen, _positionX + textPointsWidth + 10, _positionY)
            self.textLifes.draw(_screen, _positionX + textPointsWidth + imageLifesWidth + 20, _positionY)
    def update(self, _delta):
        MySprite.update(self, _delta)
    def updateHUD(self, _points, _lifes):
        self.textPoints = TextSprite(_points)
        self.imageLifes.scale(self.textPoints.size()[1], self.textPoints.size()[1])
        self.textLifes = TextSprite(_lifes)