from myevents import GAME_EVENT, GameEventType, ENTITY_EFFECT_EVENT,\
    EntityEffect, MENU_EVENT, MenuEventType
import pygame

class PlayerProgressSystem:
    NAME = "PlayerProgressSystem"
    def __init__(self):
        self.currentLevel = 1
        self.currentPoints = 0
        self.overallPoints = 0
        self.currentMaxPoints = 0
        self.currentLifes = 3
    def register(self, _object):
        pass
    def remove(self, _entity):
        pass
    def update(self, _timeDelta, _systems):
        pass
    def input(self, _event):
        if _event.type == GAME_EVENT:
            if _event.reason == GameEventType.WON_GAME:
                self.currentLevel += 1
                self.overallPoints += self.currentPoints
                self.currentPoints = 0
                self.updateHUD()
            if _event.reason == GameEventType.LOST_LIFE:
                self.currentLifes -= 1
                self.currentPoints = 0
                if self.currentLifes == 0:
                    pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.LOST_GAME))
            elif _event.reason == GameEventType.SET_MAX_POINTS:
                self.currentMaxPoints = _event.maxPoints
                self.updateHUD()
        elif _event.type == ENTITY_EFFECT_EVENT:
            if _event.effect == EntityEffect.PICK_UP_CAP:
                self.currentPoints += 1
                self.updateHUD()
                if self.currentPoints >= self.currentMaxPoints:
                    pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.WON_GAME))
        elif _event.type == MENU_EVENT:
            if _event.action == MenuEventType.START_NEW_GAME:
                self.currentPoints = 0
                self.currentLifes = 3
                self.currentLevel = 1
                self.updateHUD()
            elif _event.action == MenuEventType.CONTINUE_GAME:
                self.currentPoints = 0
                self.updateHUD()
    def updateHUD(self):
        currentPointString = str(self.currentPoints) + "/" + str(self.currentMaxPoints)
        currentLifesString = str(self.currentLifes)
        pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.HUD_UPDATE, points=currentPointString, lifes=currentLifesString))