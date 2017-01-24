from entity import Entity
from artifact.spriteartifact import SpriteArtifact
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
    def __init__(self, _systems):
        self.dirty = True
        self.systems = _systems
        self.elements = []

    def build(self):
        # TODO wyrzucic bezwzgledne pozycjonowanie
        self.createmenubackground(0, 0)
        self.createmenuelement(490, 550, "Play", MenuEventType.START_NEW_GAME, None)
        option_settings = self.createmenuelement(490, 600, "Settings", MenuEventType.MENU_IN, None)
        self.createmenuelement(490, 550, "Maximize window", MenuEventType.MAXIMIZE, option_settings)
        self.createmenuelement(490, 600, "Change tile size", MenuEventType.CHANGE_TILE_SIZE, option_settings)
        self.createmenuelement(490, 660, "Back", MenuEventType.MENU_OUT, option_settings)
        self.createmenuelement(490, 650, "Exit", MenuEventType.QUIT, None)
        self.createhud(950, 10)
        self.createresult("You win!!!", GameState.WON_GAME)
        self.createresult("You lost - restarting...!!!", GameState.LOST_LIFE)
        self.createresult("You lost!!!", GameState.LOST_GAME)
        self.createHighscores()

    def clear(self):
        for e in self.elements:
            for _, system in self.systems.items():
                system.remove(e)
        self.elements.clear()
        self.systems[HUDSystem.NAME].currentCaps = 0  # poprawic

    def input(self, _event):
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

    def createmenuelement(self, _x, _y, _text, _type, _parent):
        menu = Entity()
        menu.addartifact(SpriteArtifact(TextSprite(_text, Modifiers.CENTER_H), _x, _y, GameState.MENU))
        menu.addartifact(MenuArtifact(_type))
        self.systems[DrawSystem.NAME].register(menu)
        self.systems[MenuSystem.NAME].register(menu, _parent)
        self.elements.append(menu)
        return menu

    def createmenubackground(self, _x, _y):
        bg = Entity()
        bg.addartifact(SpriteArtifact(SimpleImageSprite('res/img/logo.png'), _x, _y, GameState.MENU))
        self.systems[DrawSystem.NAME].register(bg)
        self.elements.append(bg)

    def createhud(self, _x, _y):
        hud = Entity()
        hud.addartifact(SpriteArtifact(HUDSprite(Modifiers.CENTER_H), _x, _y, GameState.GAME))
        self.systems[DrawSystem.NAME].register(hud)
        self.systems[HUDSystem.NAME].register(hud)
        self.elements.append(hud)

    def createresult(self, _text, _type):
        result = Entity()
        result.addartifact(SpriteArtifact(TextSprite(_text, Modifiers.CENTER_H | Modifiers.CENTER_V), 0, 0, _type))
        self.systems[DrawSystem.NAME].register(result)
        self.elements.append(result)

    def createHighscores(self):
        new_highscore = Entity()
        new_highscore.addartifact(SpriteArtifact(TextSprite("New highscore!", Modifiers.CENTER_H), 100, 100, GameState.NEW_HIGHSCORE))
        self.systems[DrawSystem.NAME].register(new_highscore)
        self.elements.append(new_highscore)

        enter_your_name = Entity()
        enter_your_name.addartifact(SpriteArtifact(TextSprite("Enter your name:", Modifiers.CENTER_H), 100, 200, GameState.NEW_HIGHSCORE))
        self.systems[DrawSystem.NAME].register(enter_your_name)
        self.elements.append(enter_your_name)

        player_name = Entity()
        player_name.addartifact(SpriteArtifact(TextSprite("", Modifiers.CENTER_H), 100, 300, GameState.NEW_HIGHSCORE))
        self.systems[DrawSystem.NAME].register(player_name)
        self.elements.append(player_name)
