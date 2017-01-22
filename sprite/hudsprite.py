from sprite.mysprite import MySprite, Modifiers
from sprite.textsprite import TextSprite
from sprite.simpleimagesprite import SimpleImageSprite


class HUDSprite(MySprite):
    """HUDSprite"""

    def __init__(self, _modifiers=Modifiers.NONE):
        super(HUDSprite, self).__init__()
        self.modifiers = _modifiers
        self.SEPARATOR_WIDTH = 10
        self.textCaps = TextSprite("")
        self.imageLifes = SimpleImageSprite("res/img/life.png")
        self.imageLifes.scale(self.textCaps.size()[1], self.textCaps.size()[1])
        self.textLifes = TextSprite("")
        self.imagePoints = SimpleImageSprite("res/img/points.png")
        self.imagePoints.scale(self.textCaps.size()[1], self.textCaps.size()[1])
        self.textPoints = TextSprite("")

    def draw(self, _screen, _positionX, _positionY):
        textCapsWidth, _ = self.textCaps.size()
        imageLifesWidth, _ = self.imageLifes.size()
        textLifesWidth, _ = self.textLifes.size()
        imagePointsWidth, _ = self.imagePoints.size()
        textPointsWidth, _ = self.textPoints.size()

        shift = 0
        if self.modifiers & Modifiers.CENTER_H:
            width = _screen.get_width() / 2
            x = width - (
                        textCapsWidth + imageLifesWidth + textLifesWidth + imagePointsWidth + textPointsWidth + self.SEPARATOR_WIDTH * 4) / 2
            self.textCaps.draw(_screen, x + shift, _positionY)
            shift += textCapsWidth + self.SEPARATOR_WIDTH
            self.imageLifes.draw(_screen, x + shift, _positionY)
            shift += imageLifesWidth + self.SEPARATOR_WIDTH
            self.textLifes.draw(_screen, x + shift, _positionY)
            shift += textLifesWidth + self.SEPARATOR_WIDTH
            self.imagePoints.draw(_screen, x + shift, _positionY)
            shift += imagePointsWidth + self.SEPARATOR_WIDTH
            self.textPoints.draw(_screen, x + shift, _positionY)
        else:
            self.textCaps.draw(_screen, _positionX + shift, _positionY)
            shift += textCapsWidth + self.SEPARATOR_WIDTH
            self.imageLifes.draw(_screen, _positionX + shift, _positionY)
            shift += imageLifesWidth + self.SEPARATOR_WIDTH
            self.textLifes.draw(_screen, _positionX + shift, _positionY)
            shift += textLifesWidth + self.SEPARATOR_WIDTH
            self.imagePoints.draw(_screen, _positionX + shift, _positionY)
            shift += imagePointsWidth + self.SEPARATOR_WIDTH
            self.textPoints.draw(_screen, _positionX + shift, _positionY)

    def update(self, _delta):
        MySprite.update(self, _delta)

    def updateHUD(self, _caps, _lifes, _points):
        self.textCaps = TextSprite(_caps)
        self.imageLifes.scale(self.textCaps.size()[1], self.textCaps.size()[1])
        self.textLifes = TextSprite(_lifes)
        self.imagePoints.scale(self.textCaps.size()[1], self.textCaps.size()[1])
        self.textPoints = TextSprite(_points)
