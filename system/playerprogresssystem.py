from highscoresmanager import HighscoresManager
from myevents import GAME_EVENT, GameEventType, ENTITY_EFFECT_EVENT, \
    EntityEffect, MENU_EVENT, MenuEventType, SCREEN_EFFECT_EVENT, ScreenEffectEvent, EventType
import pygame
from artifact.tagartifact import TagType, TagSubType
from system.tagsystem import TagSystem
from artifact.spriteartifact import SpriteArtifact


class PlayerProgressSystem:
    """
    System responsible for maintaining player progress:
    points, lifes, levels, caps...
    """
    NAME = "PlayerProgressSystem"

    def __init__(self):
        """
        Constructor
        """
        self.highscoresmanager = HighscoresManager()
        self.highscoresmanager.load()
        self.currentLevel = 1
        self.currentCaps = 0
        self.overallPoints = 0
        self.currentMaxCaps = 0
        self.currentLifes = 3
        self.systems = None

    def register(self, _object):
        """
        Register method stub
        :param _object: object to be registered
        :return: nothing
        """
        pass

    def remove(self, _entity):
        """
        Remove method stub
        :param _entity: entity to be removed
        :return: nothing
        """
        pass

    def update(self, _timedelta, _systems):
        """
        Update method for system
        :param _timedelta: game loop time delta
        :param _systems: collection of all systems
        :return:
        """
        self.systems = _systems

    def input(self, _event):
        """
        Method responsibel for adding points for certain actions
        Continuing to next level, removing points for using bait, or pausing game.
        :param _event: event to be processed.
        :return: nothing
        """
        if _event.type == GAME_EVENT:
            if _event.reason == GameEventType.WON_GAME:
                self.currentLevel += 1
                self.overallPoints += 100  # bonus
                self.currentCaps = 0
                self.updatehud()
            if _event.reason == GameEventType.LOST_LIFE:
                self.currentLifes -= 1
                self.currentCaps = 0
                if self.currentLifes == 0:
                    self.currentLevel = 1
                    if self.highscoresmanager.ishighscore(self.overallPoints):
                        pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.NEW_HIGHSCORE))
                    else:
                        pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.LOST_GAME))
            elif _event.reason == GameEventType.SET_MAX_POINTS:
                self.currentMaxCaps = _event.maxPoints
                self.updatehud()
        elif _event.type == ENTITY_EFFECT_EVENT:
            if _event.effect == EntityEffect.PICK_UP_CAP:
                self.currentCaps += 1
                self.overallPoints += 10
                self.updatehud()
                if self.currentCaps >= self.currentMaxCaps:
                    pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.WON_GAME))
        elif _event.type == MENU_EVENT:
            if _event.action == MenuEventType.START_NEW_GAME:
                self.currentCaps = 0
                self.currentLifes = 3
                self.currentLevel = 1
                self.overallPoints = 0
                self.updatehud()
            elif _event.action == MenuEventType.CONTINUE_GAME:
                self.currentCaps = 0
                self.updatehud()
        elif _event.type == pygame.KEYUP:
            if _event.key == pygame.K_p:
                pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.PAUSE_GAME))
            elif _event.key == pygame.K_b:
                if self.overallPoints > 100:
                    self.overallPoints -= 100
                    self.updatehud()
                    tag_system = self.systems[TagSystem.NAME]
                    komesman = tag_system.getentities(TagType.KOMESMAN)[0]
                    sprite_artifact = komesman.artifacts[SpriteArtifact.NAME]
                    pygame.event.post(
                        pygame.event.Event(GAME_EVENT, reason=GameEventType.SPAWN_OBJECT, spawntype=TagType.ITEM,
                                           spawnsubtype=TagSubType.BAIT, x=sprite_artifact.positionX,
                                           y=sprite_artifact.positionY))

    def updatehud(self):
        """
        Method responsible for creating event for hud update
        :return: nothing
        """
        current_caps_string = str(self.currentCaps) + "/" + str(self.currentMaxCaps)
        current_lifes_string = str(self.currentLifes)
        current_points_string = str(self.overallPoints)
        pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.HUD_UPDATE, caps=current_caps_string,
                                             lifes=current_lifes_string, points=current_points_string))
