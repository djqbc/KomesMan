from artifact.spriteartifact import SpriteArtifact, DRAW_NEVER
from highscoresmanager import HighscoresManager
from system.gamesystem import GameState
from myevents import GAME_STATE_CHANGE_EVENT, MENU_EVENT, MenuEventType, ENTITY_EFFECT_EVENT, EntityEffect
import pygame
from artifact.menuartifact import MenuArtifact
from system.playerprogresssystem import PlayerProgressSystem


class MenuSystem:
    NAME = "MenuSystem"
    menu = {}
    currentNode = None
    currentIndex = 0
    currentNick = []
    max_nick = 30
    saveRequest = False
    currentGameState = GameState.INIT

    def __init__(self):
        self.highscoresmanager = HighscoresManager()
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
        if self.currentGameState == GameState.NEW_HIGHSCORE:
            if self.saveRequest:
                self.saveRequest = False
                self.highscoresmanager.load()
                score = _systems[PlayerProgressSystem.NAME].overallPoints
                self.highscoresmanager.inserthighscore(''.join(self.currentNick), score)
                self.highscoresmanager.save()
                self.currentNick = []
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.MENU))
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
                    self.saveRequest = True
                    return
                else:
                    if len(self.currentNick) > self.max_nick and _event.key != pygame.K_BACKSPACE:
                        return
                    if len(_event.unicode) == 0:
                        return
                    if _event.key == pygame.K_BACKSPACE:
                        self.currentNick = self.currentNick[:-1]
                    else:
                        self.currentNick.append(_event.unicode)
                    pygame.event.post(pygame.event.Event(MENU_EVENT, action=MenuEventType.UPDATE_NAME, nick = self.currentNick, maxnick=self.max_nick))
                    pygame.event.post(pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.PLAY_SOUND, path="res/sound/menu.wav"))
        elif _event.type == pygame.KEYUP:
            if self.currentGameState == GameState.SHOW_HIGHSCORES:
                if _event.key == pygame.K_RETURN:
                    pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.MENU))
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
                if current_action == MenuEventType.SHOW_HIGHSCORES:
                    pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.SHOW_HIGHSCORES))
                    pygame.event.post(pygame.event.Event(MENU_EVENT, action=MenuEventType.SHOW_HIGHSCORES))
                    return
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
