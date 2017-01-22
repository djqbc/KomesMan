from myevents import GAME_EVENT, GameEventType, ENTITY_EFFECT_EVENT,\
    EntityEffect, MENU_EVENT, MenuEventType
import pygame
from artifact.tagartifact import TagType, TagSubType
from system.tagsystem import TagSystem
from artifact.spriteartifact import SpriteArtifact

class PlayerProgressSystem:
    NAME = "PlayerProgressSystem"
    def __init__(self):
        self.currentLevel = 1
        self.currentCaps = 0
        self.overallPoints = 0
        self.currentMaxCaps = 0
        self.currentLifes = 3
        self.systems = None
    def register(self, _object):
        pass
    def remove(self, _entity):
        pass
    def update(self, _timeDelta, _systems):
        self.systems = _systems
    def input(self, _event):
        if _event.type == GAME_EVENT:
            if _event.reason == GameEventType.WON_GAME:
                self.currentLevel += 1
                self.overallPoints += 100#bonus
                self.currentCaps = 0
                self.updateHUD()
            if _event.reason == GameEventType.LOST_LIFE:
                self.currentLifes -= 1
                self.currentCaps = 0
                if self.currentLifes == 0:
                    self.currentLevel = 1
                    pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.LOST_GAME))
            elif _event.reason == GameEventType.SET_MAX_POINTS:
                self.currentMaxCaps = _event.maxPoints
                self.updateHUD()
        elif _event.type == ENTITY_EFFECT_EVENT:
            if _event.effect == EntityEffect.PICK_UP_CAP:
                self.currentCaps += 1
                self.overallPoints += 10
                self.updateHUD()
                if self.currentCaps >= self.currentMaxCaps:
                    pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.WON_GAME))
        elif _event.type == MENU_EVENT:
            if _event.action == MenuEventType.START_NEW_GAME:
                self.currentCaps = 0
                self.currentLifes = 3
                self.currentLevel = 1
                self.overallPoints = 0
                self.updateHUD()
            elif _event.action == MenuEventType.CONTINUE_GAME:
                self.currentCaps = 0
                self.updateHUD()
        elif _event.type == pygame.KEYUP:
            if _event.key == pygame.K_b:
                if self.overallPoints > 100:
                    self.overallPoints -= 100
                    self.updateHUD()
                    tagSystem = self.systems[TagSystem.NAME]
                    komesman = tagSystem.getEntities(TagType.KOMESMAN)[0]
                    spriteArtifact = komesman.artifacts[SpriteArtifact.NAME]
                    pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.SPAWN_OBJECT, spawntype=TagType.ITEM, 
                                          spawnsubtype=TagSubType.BAIT, x=spriteArtifact.positionX, y=spriteArtifact.positionY))
                    
    def updateHUD(self):
        currentCapsString = str(self.currentCaps) + "/" + str(self.currentMaxCaps)
        currentLifesString = str(self.currentLifes)
        currentPointsString = str(self.overallPoints)
        pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.HUD_UPDATE, caps=currentCapsString, lifes=currentLifesString, points=currentPointsString))