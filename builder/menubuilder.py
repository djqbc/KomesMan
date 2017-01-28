from copy import copy

from entity import Entity
from artifact.spriteartifact import SpriteArtifact
from highscoresmanager import HighscoresManager
from sprite.textsprite import TextSprite, Modifiers
from sprite.simpleimagesprite import SimpleImageSprite
from sprite.hudsprite import HUDSprite
from system.gamesystem import GameState
from system.drawsystem import DrawSystem
from system.menusystem import MenuSystem
from system.hudsystem import HUDSystem
from artifact.menuartifact import MenuArtifact
from myevents import MenuEventType, GAME_STATE_CHANGE_EVENT, MENU_EVENT


class MenuBuilder:
    """
    Class handling building of menu
    """
    def __init__(self, _systems):
        """
        Constructor
        :param _systems: Reference to other systems collection.
        """
        self.dirty = True
        self.systems = _systems
        self.elements = []
        self.highscorenames = []
        self.highscorevalues = []
        self.player_name = None
        self.highscoresManager = HighscoresManager()
        self.screen_height = 768 #todo: gdzies wyciagnac.
        self.margin = 10

    def build(self):
        """
        Creates menu items, and large messages (f.e. after deatH)
        :return: nothing
        """
        # TODO wyrzucic bezwzgledne pozycjonowanie
        self.createmenubackground(0, 0)
        self.createmenuelement(490, 550, "Play", MenuEventType.START_NEW_GAME, None)
        option_settings = self.createmenuelement(490, 600, "Settings", MenuEventType.MENU_IN, None)
        self.createmenuelement(490, 650, "Hall of fame", MenuEventType.SHOW_HIGHSCORES, None)
        self.createmenuelement(490, 550, "Maximize window", MenuEventType.MAXIMIZE, option_settings)
        self.createmenuelement(490, 600, "Change tile size", MenuEventType.CHANGE_TILE_SIZE, option_settings)
        self.createmenuelement(490, 660, "Back", MenuEventType.MENU_OUT, option_settings)
        self.createmenuelement(490, 700, "Exit", MenuEventType.QUIT, None)
        self.createhud(950, 10)
        self.createresult("You win!!!", GameState.WON_GAME)
        self.createresult("You lost - restarting...!!!", GameState.LOST_LIFE)
        self.createresult("You lost!!!", GameState.LOST_GAME)
        self.createresult("Press 'P' to play!", GameState.PAUSED)
        self.createHighscores()
        self.createhalloffame()

    def clear(self):
        """
        Cleanup of menu items in other systems.
        :return: nothing
        """
        for e in self.elements:
            for _, system in self.systems.items():
                system.remove(e)
        self.elements.clear()
        self.systems[HUDSystem.NAME].currentCaps = 0  # poprawic

    def input(self, _event):
        """
        Handles rebuilding menu elements on ceratin events
        Handles entering of name for highscores.
        :param _event: event to process
        :return: nothing
        """
        if _event.type == GAME_STATE_CHANGE_EVENT:
            if _event.state == GameState.MENU and self.dirty:
                self.dirty = False
                self.build()
        elif _event.type == MENU_EVENT:
            if _event.action == MenuEventType.START_NEW_GAME or _event.action == MenuEventType.CONTINUE_GAME:
                self.clear()
                self.build()
            elif _event.action == MenuEventType.RESTART_GAME:
                self.clear()
                self.build()
            elif _event.action == MenuEventType.UPDATE_NAME:
                nick = copy(_event.nick)
                if(len(_event.nick) < _event.maxnick):
                    underscores = "_" * (_event.maxnick - len(_event.nick))
                    nick += underscores

                self.player_name.artifacts[SpriteArtifact.NAME].sprite.changetext(''.join(nick))
            elif _event.action == MenuEventType.SHOW_HIGHSCORES:
                self.reloadhighscores()


    def createmenuelement(self, _x, _y, _text, _type, _parent):
        """
        Creates single menu element
        :param _x: X position of text
        :param _y: Y position of text
        :param _text: Text of element
        :param _type: Type of menu event
        :param _parent: Parent menu element.
        :return: menu entity
        """
        menu = Entity()
        menu.addartifact(SpriteArtifact(TextSprite(_text, Modifiers.CENTER_H), _x, _y, GameState.MENU))
        menu.addartifact(MenuArtifact(_type))
        self.systems[DrawSystem.NAME].register(menu)
        self.systems[MenuSystem.NAME].register(menu, _parent)
        self.elements.append(menu)
        return menu

    def createmenubackground(self, _x, _y):
        """
        Creates large KomesMan logo
        :param _x: X position of logo
        :param _y: Y position of logo
        :return: nothing
        """
        bg = Entity()
        bg.addartifact(SpriteArtifact(SimpleImageSprite('res/img/logo.png'), _x, _y, GameState.MENU))
        self.systems[DrawSystem.NAME].register(bg)
        self.elements.append(bg)

    def createhud(self, _x, _y):
        """
        Creates HUD (points, lives, cap status)
        :param _x: X position in pixels
        :param _y: Y position in pixels
        :return: nothing
        """
        hud = Entity()
        hud.addartifact(SpriteArtifact(HUDSprite(Modifiers.CENTER_H), _x, _y, GameState.GAME))
        self.systems[DrawSystem.NAME].register(hud)
        self.systems[HUDSystem.NAME].register(hud)
        self.elements.append(hud)

    def createresult(self, _text, _type):
        """
        Creates black board with specified text
        :param _text: text to display
        :param _type: GameState in which board should be displayed.
        :return: nothing
        """
        result = Entity()
        result.addartifact(SpriteArtifact(TextSprite(_text, Modifiers.CENTER_H | Modifiers.CENTER_V), 0, 0, _type))
        self.systems[DrawSystem.NAME].register(result)
        self.elements.append(result)

    def createHighscores(self):
        """
        Creates labels for highscore entering, and placeholder for entering player name.
        :return: nothing
        """
        new_highscore = Entity()
        new_highscore.addartifact(SpriteArtifact(TextSprite("New highscore!", Modifiers.CENTER_H), 100, 100, GameState.NEW_HIGHSCORE))
        self.systems[DrawSystem.NAME].register(new_highscore)
        self.elements.append(new_highscore)

        enter_your_name = Entity()
        enter_your_name.addartifact(SpriteArtifact(TextSprite("Enter your name:", Modifiers.CENTER_H), 100, 200, GameState.NEW_HIGHSCORE))
        self.systems[DrawSystem.NAME].register(enter_your_name)
        self.elements.append(enter_your_name)

        self.player_name = Entity()
        self.player_name.addartifact(SpriteArtifact(TextSprite('_'*30, Modifiers.CENTER_H), 100, 300, GameState.NEW_HIGHSCORE))
        self.systems[DrawSystem.NAME].register(self.player_name)
        self.elements.append(self.player_name)

    def createhalloffame(self):
        """
        Creates labels and placeholders for loading highscore values.
        :return: nothing
        """
        potential_size_of_one_line = (self.screen_height - 2*self.margin ) / (HighscoresManager.topscorescount) + 1
        hall_of_fame = Entity()
        hall_of_fame.addartifact(SpriteArtifact(TextSprite("HALL OF FAME!", Modifiers.CENTER_H), 0, self.margin, GameState.SHOW_HIGHSCORES))
        self.systems[DrawSystem.NAME].register(hall_of_fame)
        self.elements.append(hall_of_fame)

        self.highscorevalues.clear()
        self.highscorenames.clear()

        for i in range(HighscoresManager.topscorescount):
            highscore_player = Entity()
            highscore_player.addartifact(SpriteArtifact(TextSprite("x"), self.margin, self.margin + (i+1) * potential_size_of_one_line, GameState.SHOW_HIGHSCORES))
            self.systems[DrawSystem.NAME].register(highscore_player)
            self.elements.append(highscore_player)
            self.highscorenames.append(highscore_player)

        for i in range(HighscoresManager.topscorescount):
            highscore_value = Entity()
            highscore_value.addartifact(SpriteArtifact(TextSprite("1"), 900, self.margin + (i+1) * potential_size_of_one_line, GameState.SHOW_HIGHSCORES))
            self.systems[DrawSystem.NAME].register(highscore_value)
            self.elements.append(highscore_value)
            self.highscorevalues.append(highscore_value)

    def reloadhighscores(self):
        """
        Loads highscores using highscoresManager into menu entities.
        :return: nothing
        """
        self.highscoresManager.load()
        i = 0
        for highscore in self.highscoresManager.highscores:
            self.highscorenames[i].artifacts[SpriteArtifact.NAME].sprite.changetext(
                str(i + 1) + " " + highscore.name)
            self.highscorevalues[i].artifacts[SpriteArtifact.NAME].sprite.changetext(str(highscore.score))
            i += 1


