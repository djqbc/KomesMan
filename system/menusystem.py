from artifact.spriteartifact import SpriteArtifact, DRAW_NEVER
from system.gamesystem import GameState
from myevents import GAME_STATE_CHANGE_EVENT, MENU_EVENT, MenuEventType, ENTITY_EFFECT_EVENT, EntityEffect
import pygame
from artifact.menuartifact import MenuArtifact


class MenuSystem:
    NAME = "MenuSystem"
    menu = {}
    currentNode = None
    currentIndex = 0
    currentNick = []
    maxNick = 10
    currentGameState = GameState.INIT

    def __init__(self):
        pass

    def remove(self, _entity):
        if _entity in self.menu:
            if self.currentNode == _entity:
                self.currentNode = None
                self.currentIndex = 0
            del self.menu[_entity]
        for _, options in self.menu.items():
            if _entity in options:
                options.remove(_entity)

    def register(self, _object, _parent=None):
        if SpriteArtifact.NAME in _object.artifacts and MenuArtifact.NAME in _object.artifacts:
            tmp = self.menu.get(_parent, None)
            if tmp is not None:
                self.menu[_parent].append(_object)
            else:
                self.menu[_parent] = [_object]
        else:
            raise NameError("ERROR!!!")

    def update(self, _timedelta, _systems):
        pass

    def input(self, _event):
        if _event.type == GAME_STATE_CHANGE_EVENT:
            self.currentGameState = _event.state
            if _event.state == GameState.MENU:
                self.currentNode = None
                for node, options in self.menu.items():
                    for option in options:
                        if node == self.currentNode:
                            option.artifacts[SpriteArtifact.NAME].drawStage = GameState.MENU
                        else:
                            option.artifacts[SpriteArtifact.NAME].drawStage = DRAW_NEVER
            else:
                self.currentNode = None
            #                 for element in self.menu[self.currentNode]:
            #                     element.artifacts[SpriteArtifact.NAME].draw = False
        elif _event.type == pygame.KEYDOWN:
            if self.currentGameState == GameState.NEW_HIGHSCORE:
                if _event.key == pygame.K_RETURN:
                    pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.MENU))
                else:
                    if len(self.currentNick) > self.maxNick and _event.key != pygame.K_BACKSPACE:
                        return

                    #todo: input and show name
                    #if(_event.key == pygame.K_BACKSPACE)
                        
                    self.currentNick.append(_event.unicode)
                    print(self.currentNick)
                    pygame.event.post(pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.PLAY_SOUND, path="res/sound/menu.wav"))
        elif _event.type == pygame.KEYUP:
            if self.currentGameState == GameState.MENU:
                pygame.event.post(
                    pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.PLAY_SOUND, path="res/sound/menu.wav"))
            if _event.key == pygame.K_DOWN and self.currentGameState == GameState.MENU:
                self.menu[self.currentNode][self.currentIndex].artifacts[SpriteArtifact.NAME].sprite.removehighlight()
                self.currentIndex = (self.currentIndex + 1) % len(self.menu[self.currentNode])
                self.menu[self.currentNode][self.currentIndex].artifacts[SpriteArtifact.NAME].sprite.addhighlight()
            elif _event.key == pygame.K_UP and self.currentGameState == GameState.MENU:
                self.menu[self.currentNode][self.currentIndex].artifacts[SpriteArtifact.NAME].sprite.removehighlight()
                self.currentIndex -= 1
                if self.currentIndex < 0:
                    self.currentIndex += len(self.menu[self.currentNode])
                self.menu[self.currentNode][self.currentIndex].artifacts[SpriteArtifact.NAME].sprite.addhighlight()
            elif _event.key == pygame.K_RETURN and self.currentGameState == GameState.MENU:
                current_action = self.menu[self.currentNode][self.currentIndex].artifacts[MenuArtifact.NAME].action
                if current_action == MenuEventType.MENU_OUT:
                    for node, options in self.menu.items():
                        if self.currentNode in options:
                            self.currentNode = node
                            break
                    self.currentIndex = 0
                    for node, options in self.menu.items():
                        for option in options:
                            if node == self.currentNode:
                                option.artifacts[SpriteArtifact.NAME].drawStage = GameState.MENU
                            else:
                                option.artifacts[SpriteArtifact.NAME].drawStage = DRAW_NEVER
                elif current_action == MenuEventType.MENU_IN:
                    self.currentNode = self.menu[self.currentNode][self.currentIndex]
                    self.currentIndex = 0
                    for node, options in self.menu.items():
                        for option in options:
                            if node == self.currentNode:
                                option.artifacts[SpriteArtifact.NAME].drawStage = GameState.MENU
                            else:
                                option.artifacts[SpriteArtifact.NAME].drawStage = DRAW_NEVER
                else:
                    pygame.event.post(pygame.event.Event(MENU_EVENT, action=current_action))
