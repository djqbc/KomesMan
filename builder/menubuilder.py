from entity import Entity
from artifact.spriteartifact import SpriteArtifact
from sprite.textsprite import TextSprite, TextPosition
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
        #TODO wyrzucic bezwzgledne pozycjonowanie
        self.createMenuBackground(0, 0)
        self.createMenuElement(490, 550, "Play", MenuEventType.START_NEW_GAME, None)
        optionSettings = self.createMenuElement(490, 600, "Settings", MenuEventType.MENU_IN, None)
        self.createMenuElement(490, 550, "Maximize window", None, optionSettings)
        self.createMenuElement(490, 600, "Back", MenuEventType.MENU_OUT, optionSettings)
        self.createMenuElement(490, 650, "Exit", MenuEventType.QUIT, None)
        self.createHUD(950, 10)
        self.createResult("You win!!!", GameState.WON_GAME)
        self.createResult("You lost!!!", GameState.LOST_GAME)
    def clear(self):
        for e in self.elements:
            for _, system in self.systems.items():
                system.remove(e)
        self.elements.clear()
        self.systems[HUDSystem.NAME].currentPoints = 0#poprawic
    def input(self, _event):
        if _event.type == GAME_STATE_CHANGE_EVENT:
            if _event.state == GameState.MENU and self.dirty == True:
                self.dirty = False
                self.build()
        elif _event.type == MENU_EVENT:
            if _event.action == MenuEventType.START_NEW_GAME:
                self.clear()
                self.build()
    def createMenuElement(self, _x, _y, _text, _type, _parent):
        menu = Entity()
        menu.addArtifact(SpriteArtifact(TextSprite(_text, TextPosition.CENTER_H,), _x, _y, GameState.MENU))
        menu.addArtifact(MenuArtifact(_type))
        self.systems[DrawSystem.NAME].register(menu)
        self.systems[MenuSystem.NAME].register(menu, _parent)
        self.elements.append(menu)
        return menu
    
    def createMenuBackground(self, _x, _y):
        bg = Entity()
        bg.addArtifact(SpriteArtifact(SimpleImageSprite('res/img/logo.png'), _x, _y, GameState.MENU))
        self.systems[DrawSystem.NAME].register(bg)
        self.elements.append(bg)
        
    def createHUD(self, _x, _y):
        hud = Entity()
        hud.addArtifact(SpriteArtifact(HUDSprite(), _x, _y, GameState.GAME))
        self.systems[DrawSystem.NAME].register(hud)
        self.systems[HUDSystem.NAME].register(hud)
        self.elements.append(hud)
        
    def createResult(self, _text, _type):
        result = Entity()
        result.addArtifact(SpriteArtifact(TextSprite(_text, TextPosition.CENTER_H | TextPosition.CENTER_V), 0, 0, _type))
        self.systems[DrawSystem.NAME].register(result)
        self.elements.append(result)