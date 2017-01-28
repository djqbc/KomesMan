from sprite.mysprite import MySprite, Modifiers
from sprite.textsprite import TextSprite
from sprite.simpleimagesprite import SimpleImageSprite


class HUDSprite(MySprite):
    """
    Sprite of on-screen display of points, caps and life
    """

    def __init__(self, _modifiers=Modifiers.NONE):
        """
        Constructor for HUD
        :param tilesize: desired width and height of tile in pixels.
        """
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

    def draw(self, _screen, _positionx, _positiony):
        """
        Draw HUD (Points, caps status, lifes) - with images.
        :param _screen: screen surface
        :param _positionx: X position to draw item
        :param _positiony: Y position to draw item
        :return: nothing
        """
        text_caps_width, _ = self.textCaps.size()
        image_lifes_width, _ = self.imageLifes.size()
        text_lifes_width, _ = self.textLifes.size()
        image_points_width, _ = self.imagePoints.size()
        text_points_width, _ = self.textPoints.size()

        shift = 0
        if self.modifiers & Modifiers.CENTER_H:
            width = _screen.get_width() / 2
            x = width - (
                        text_caps_width + image_lifes_width + text_lifes_width + image_points_width + text_points_width + self.SEPARATOR_WIDTH * 4) / 2
            self.textCaps.draw(_screen, x + shift, _positiony)
            shift += text_caps_width + self.SEPARATOR_WIDTH
            self.imageLifes.draw(_screen, x + shift, _positiony)
            shift += image_lifes_width + self.SEPARATOR_WIDTH
            self.textLifes.draw(_screen, x + shift, _positiony)
            shift += text_lifes_width + self.SEPARATOR_WIDTH
            self.imagePoints.draw(_screen, x + shift, _positiony)
            shift += image_points_width + self.SEPARATOR_WIDTH
            self.textPoints.draw(_screen, x + shift, _positiony)
        else:
            self.textCaps.draw(_screen, _positionx + shift, _positiony)
            shift += text_caps_width + self.SEPARATOR_WIDTH
            self.imageLifes.draw(_screen, _positionx + shift, _positiony)
            shift += image_lifes_width + self.SEPARATOR_WIDTH
            self.textLifes.draw(_screen, _positionx + shift, _positiony)
            shift += text_lifes_width + self.SEPARATOR_WIDTH
            self.imagePoints.draw(_screen, _positionx + shift, _positiony)
            shift += image_points_width + self.SEPARATOR_WIDTH
            self.textPoints.draw(_screen, _positionx + shift, _positiony)

    def update(self, _delta):
        """
        Update sprite
        :param _delta:
        :return: nothing
        """
        MySprite.update(self, _delta)

    def updatehud(self, _caps, _lifes, _points):
        """
        Updates HUD with specified number of caps, lifes, and points
        :param _caps: Collected caps
        :param _lifes: Lifes left
        :param _points: Collected points
        :return:
        """
        self.textCaps = TextSprite(_caps)
        self.imageLifes.scale(self.textCaps.size()[1], self.textCaps.size()[1])
        self.textLifes = TextSprite(_lifes)
        self.imagePoints.scale(self.textCaps.size()[1], self.textCaps.size()[1])
        self.textPoints = TextSprite(_points)
