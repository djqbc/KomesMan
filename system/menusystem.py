from artifact.spriteartifact import SpriteArtifact
from system.gamesystem import GameState
from myevents import GAME_STATE_CHANGE_EVENT, MENU_EVENT, MenuEventType
import pygame

class MenuSystem:
    NAME = "MenuSystem"
    menu = {}
    currentNode = None
    currentIndex = 0
    currentGameState = GameState.INIT
    def __init__(self):
        pass
    def remove(self, _entity):
        pass
    def register(self, _object, _parent=None):
        if SpriteArtifact.NAME in _object.artifacts: 
            tmp = self.menu.get(_parent, None)
            if tmp != None:
                self.menu[_parent].append(_object)
            else:
                self.menu[_parent] = [_object]
        else:
            raise NameError("ERROR!!!")
    def update(self, _timeDelta, _systems):
        pass
    def input(self, _event):
        if _event.type == GAME_STATE_CHANGE_EVENT:
            self.currentGameState = _event.state
            if _event.state == GameState.MENU:
                self.currentNode = None
#                 for element in self.menu[self.currentNode]:
#                     element.artifacts[SpriteArtifact.NAME].drawStage = True
            else:
                self.currentNode = None
#                 for element in self.menu[self.currentNode]:
#                     element.artifacts[SpriteArtifact.NAME].draw = False
        elif _event.type == pygame.KEYUP:
            if _event.key == pygame.K_DOWN and self.currentGameState == GameState.MENU:
                self.menu[self.currentNode][self.currentIndex].artifacts[SpriteArtifact.NAME].sprite.removeHighlight()
                self.currentIndex = (self.currentIndex + 1) % len(self.menu[self.currentNode])
                self.menu[self.currentNode][self.currentIndex].artifacts[SpriteArtifact.NAME].sprite.addHighlight()
            elif _event.key == pygame.K_UP and self.currentGameState == GameState.MENU:
                self.menu[self.currentNode][self.currentIndex].artifacts[SpriteArtifact.NAME].sprite.removeHighlight()
                self.currentIndex = self.currentIndex - 1
                if self.currentIndex < 0:
                    self.currentIndex = len(self.menu[self.currentNode]) + self.currentIndex
                self.menu[self.currentNode][self.currentIndex].artifacts[SpriteArtifact.NAME].sprite.addHighlight()
            elif _event.key == pygame.K_RETURN and self.currentGameState == GameState.MENU:
                #narazie kazda opcja zaczyna gre
                pygame.event.post(pygame.event.Event(MENU_EVENT, action=MenuEventType.START_NEW_GAME))