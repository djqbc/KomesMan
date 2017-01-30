"""
HUD sprite package
"""
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
        self.seperator_width = 10
        self.text_caps = TextSprite("")
        self.image_lifes = SimpleImageSprite("res/img/life.png")
        self.image_lifes.scale(self.text_caps.size()[1], self.text_caps.size()[1])
        self.text_lifes = TextSprite("")
        self.image_points = SimpleImageSprite("res/img/points.png")
        self.image_points.scale(self.text_caps.size()[1], self.text_caps.size()[1])
        self.text_points = TextSprite("")

    def draw(self, _screen, _positionx, _positiony):
        """
        Draw HUD (Points, caps status, lifes) - with images.
        :param _screen: screen surface
        :param _positionx: X position to draw item
        :param _positiony: Y position to draw item
        :return: nothing
        """
        text_caps_width, _ = self.text_caps.size()
        image_lifes_width, _ = self.image_lifes.size()
        text_lifes_width, _ = self.text_lifes.size()
        image_points_width, _ = self.image_points.size()
        text_points_width, _ = self.text_points.size()

        shift = 0
        if self.modifiers & Modifiers.CENTER_H:
            width = _screen.get_width() / 2
            xpos = width - (text_caps_width + image_lifes_width + text_lifes_width +
                            image_points_width + text_points_width + self.seperator_width * 4) / 2
            self.text_caps.draw(_screen, xpos + shift, _positiony)
            shift += text_caps_width + self.seperator_width
            self.image_lifes.draw(_screen, xpos + shift, _positiony)
            shift += image_lifes_width + self.seperator_width
            self.text_lifes.draw(_screen, xpos + shift, _positiony)
            shift += text_lifes_width + self.seperator_width
            self.image_points.draw(_screen, xpos + shift, _positiony)
            shift += image_points_width + self.seperator_width
            self.text_points.draw(_screen, xpos + shift, _positiony)
        else:
            self.text_caps.draw(_screen, _positionx + shift, _positiony)
            shift += text_caps_width + self.seperator_width
            self.image_lifes.draw(_screen, _positionx + shift, _positiony)
            shift += image_lifes_width + self.seperator_width
            self.text_lifes.draw(_screen, _positionx + shift, _positiony)
            shift += text_lifes_width + self.seperator_width
            self.image_points.draw(_screen, _positionx + shift, _positiony)
            shift += image_points_width + self.seperator_width
            self.text_points.draw(_screen, _positionx + shift, _positiony)

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
        self.text_caps = TextSprite(_caps)
        self.image_lifes.scale(self.text_caps.size()[1], self.text_caps.size()[1])
        self.text_lifes = TextSprite(_lifes)
        self.image_points.scale(self.text_caps.size()[1], self.text_caps.size()[1])
        self.text_points = TextSprite(_points)
