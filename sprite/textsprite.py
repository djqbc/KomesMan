"""
Text sprite package
"""
from sprite.mysprite import MySprite, Modifiers
import pygame


class TextSprite(MySprite):
    """
    Text sprite.
    """
    def __init__(self, _text, _modifiers=Modifiers.NONE):
        """
        Constructor
        :param _text: Text to show
        :param _modifiers: Position modifier (Modifiers.CENTER_H / Modifiers.CENTER_V)
        Used for text alignment.
        """
        super(TextSprite, self).__init__()
        self.modifiers = _modifiers
        self.basicfont = pygame.font.SysFont(None, 48)
        self.textcontent = _text
        self.color = (127, 127, 127)
        self.text = self.basicfont.render(_text, True, self.color)

    def draw(self, _screen, _positionx, _positiony):
        """
        Draw text. If self.modifiers contains Modifiers.CENTER_H, text is centered
        horizontally. In case of Modifiers.CENTER_V, text is centered vertically.
        :param _screen: screen surface
        :param _positionx: X position to draw item
        :param _positiony: Y position to draw item
        :return: nothing
        """
        if self.modifiers is not None:
            xpos = _positionx
            ypos = _positiony
            text_width, text_height = self.basicfont.size(self.textcontent)
            if self.modifiers & Modifiers.CENTER_H:
                width = _screen.get_width() / 2
                xpos = width - text_width / 2
            if self.modifiers & Modifiers.CENTER_V:
                height = _screen.get_height() / 2
                ypos = height - text_height / 2
            _screen.blit(self.text, (xpos, ypos))
        else:
            _screen.blit(self.text, (_positionx, _positiony))

    def update(self, _delta):
        """
        Update sprite
        :param _delta:
        :return: nothing
        """
        MySprite.update(self, _delta)

    def size(self):
        """
        Get size of font
        :return: size of font
        """
        return self.basicfont.size(self.textcontent)

    def changetext(self, _text):
        """
        Change text of text srpite
        :param _text: new text
        :return: nothing
        """
        self.textcontent = _text
        self.text = self.basicfont.render(_text, True, self.color)

    def addhighlight(self):
        """
        Add hihlight to text.
        :return: nothing
        """
        self.color = (255, 255, 255)
        self.text = self.basicfont.render(self.textcontent, True, self.color)

    def removehighlight(self):
        """
        Remove highlight from text.
        :return: nothing
        """
        self.color = (127, 127, 127)
        self.text = self.basicfont.render(self.textcontent, True, self.color)
