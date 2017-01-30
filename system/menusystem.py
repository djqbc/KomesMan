"""MenuSystem module."""
from artifact.spriteartifact import SpriteArtifact, DRAW_NEVER
from artifact.menuartifact import MenuArtifact
from highscoresmanager import HighscoresManager
from system.gamesystem import GameState
from system.playerprogresssystem import PlayerProgressSystem
from myevents import GAME_STATE_CHANGE_EVENT, MENU_EVENT, MenuEventType, ENTITY_EFFECT_EVENT, EntityEffect
import pygame


class MenuSystem:
    """System repsonsible for managing all game menus and dialogs."""

    NAME = "MenuSystem"
    menu = {}
    current_node = None
    current_index = 0
    current_nick = []
    max_nick = 30
    save_request = False
    current_game_state = GameState.INIT
    focus_item = True

    def __init__(self):
        """Constructor. Creates Highscore Manager."""
        self.highscoresmanager = HighscoresManager()

    def remove(self, _entity):
        """
        Remove entity from system.

        :param _entity: Entity to be removed
        :return: nothing
        """
        if _entity in self.menu:
            if self.current_node == _entity:
                self.current_node = None
                self.current_index = 0
            del self.menu[_entity]
        for _, options in self.menu.items():
            if _entity in options:
                options.remove(_entity)

    def register(self, _object, _parent=None):
        """
        Register entity to the system.

        :param _object: object to be added
        :param _parent: parent of selected menu item, if applicable.
        :return:
        """
        if SpriteArtifact.NAME in _object.artifacts and MenuArtifact.NAME in _object.artifacts:
            tmp = self.menu.get(_parent, None)
            if tmp is not None:
                self.menu[_parent].append(_object)
            else:
                self.menu[_parent] = [_object]
        else:
            raise NameError("ERROR!!!")

    def update(self, _timedelta, _systems):
        """
        Update system. Responsible for saving highscore and focusing first item.

        :param _timedelta: game loop time delta
        :param _systems: collection of all systems.
        :return:
        """
        if self.focus_item:
            self.focus_item = False
            self.menu[self.current_node][self.current_index].artifacts[SpriteArtifact.NAME].sprite.addhighlight()
        if self.save_request:
            self.save_request = False
            self.highscoresmanager.load()
            score = _systems[PlayerProgressSystem.NAME].overall_points
            self.highscoresmanager.inserthighscore(''.join(self.current_nick), score)
            self.highscoresmanager.save()
            self.current_nick = []

    def input(self, _event):
        """
        Responsible for processing events connected with menu, highscores.

        Allows adding name to highscores, allows navigation through menu.
        :param _event: event to be processed
        :return: nothing
        """
        if _event.type == GAME_STATE_CHANGE_EVENT:
            self.current_game_state = _event.state
            if _event.state == GameState.MENU:
                self.focus_item = True
                self.current_node = None
                for node, options in self.menu.items():
                    for option in options:
                        if node == self.current_node:
                            option.artifacts[SpriteArtifact.NAME].drawstage = GameState.MENU
                        else:
                            option.artifacts[SpriteArtifact.NAME].drawstage = DRAW_NEVER
            else:
                self.current_node = None
            #                 for element in self.menu[self.current_node]:
            #                     element.artifacts[SpriteArtifact.NAME].draw = False
        elif _event.type == pygame.KEYDOWN:
            if self.current_game_state == GameState.NEW_HIGHSCORE:
                if _event.key == pygame.K_RETURN:
                    self.save_request = True
                    pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.MENU))
                    return
                else:
                    if len(self.current_nick) > self.max_nick and _event.key != pygame.K_BACKSPACE:
                        return
                    if len(_event.unicode) == 0:
                        return
                    if _event.key == pygame.K_BACKSPACE:
                        self.current_nick = self.current_nick[:-1]
                    else:
                        self.current_nick.append(_event.unicode)
                    pygame.event.post(pygame.event.Event(MENU_EVENT, action=MenuEventType.UPDATE_NAME, nick = self.current_nick, maxnick=self.max_nick))
                    pygame.event.post(pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.PLAY_SOUND, path="res/sound/menu.wav"))
            if self.current_game_state == GameState.SHOW_HIGHSCORES:
                if _event.key == pygame.K_RETURN:
                    pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.MENU))
                    return
            if self.current_game_state == GameState.MENU:
                pygame.event.post(
                    pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.PLAY_SOUND, path="res/sound/menu.wav"))
            if _event.key == pygame.K_DOWN and self.current_game_state == GameState.MENU:
                self.menu[self.current_node][self.current_index].artifacts[SpriteArtifact.NAME].sprite.removehighlight()
                self.current_index = (self.current_index + 1) % len(self.menu[self.current_node])
                self.menu[self.current_node][self.current_index].artifacts[SpriteArtifact.NAME].sprite.addhighlight()
            elif _event.key == pygame.K_UP and self.current_game_state == GameState.MENU:
                self.menu[self.current_node][self.current_index].artifacts[SpriteArtifact.NAME].sprite.removehighlight()
                self.current_index -= 1
                if self.current_index < 0:
                    self.current_index += len(self.menu[self.current_node])
                self.menu[self.current_node][self.current_index].artifacts[SpriteArtifact.NAME].sprite.addhighlight()
            elif _event.key == pygame.K_RETURN and self.current_game_state == GameState.MENU:
                current_action = self.menu[self.current_node][self.current_index].artifacts[MenuArtifact.NAME].action
                if current_action == MenuEventType.SHOW_HIGHSCORES:
                    pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.SHOW_HIGHSCORES))
                    pygame.event.post(pygame.event.Event(MENU_EVENT, action=MenuEventType.SHOW_HIGHSCORES))
                    return
                if current_action == MenuEventType.MENU_OUT:
                    self.focus_item = True
                    self.menu[self.current_node][self.current_index].artifacts[SpriteArtifact.NAME].sprite.removehighlight()
                    for node, options in self.menu.items():
                        if self.current_node in options:
                            self.current_node = node
                            break
                    self.current_index = 0
                    for node, options in self.menu.items():
                        for option in options:
                            if node == self.current_node:
                                option.artifacts[SpriteArtifact.NAME].drawStage = GameState.MENU
                            else:
                                option.artifacts[SpriteArtifact.NAME].drawStage = DRAW_NEVER
                elif current_action == MenuEventType.MENU_IN:
                    self.focus_item = True
                    self.menu[self.current_node][self.current_index].artifacts[SpriteArtifact.NAME].sprite.removehighlight()
                    self.current_node = self.menu[self.current_node][self.current_index]
                    self.current_index = 0
                    for node, options in self.menu.items():
                        for option in options:
                            if node == self.current_node:
                                option.artifacts[SpriteArtifact.NAME].drawStage = GameState.MENU
                            else:
                                option.artifacts[SpriteArtifact.NAME].drawStage = DRAW_NEVER
                else:
                    pygame.event.post(pygame.event.Event(MENU_EVENT, action=current_action))
