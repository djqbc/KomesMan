from artifact.spriteartifact import SpriteArtifact
from myevents import ENTITY_EFFECT_EVENT, EntityEffect, GAME_EVENT, GameEventType
import pygame

class HUDSystem:#zmienic nazwe kiedys - nie chcialo mi sie myslec nad lepsza
    NAME = "HUDSystem"
    observing = []
    max_points = 2# do poprawy - pobierac to a nie na sztywno - moze z board, moze z buildera jak powstanie
    currentPoints = 0
    dirty = True
    def __init__(self):
        self.observing = []
    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts:  
            self.dirty = True 
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")
    def remove(self, _entity):
        self.observing[:] = [entity for entity in self.observing if entity != _entity]
    def update(self, _timeDelta, _systems):
        if self.dirty == True:
            self.dirty = False
            for entity in self.observing:
                entity.artifacts[SpriteArtifact.NAME].sprite.update(_timeDelta, str(self.currentPoints) + " / " + str(self.max_points))
    def input(self, _event):
        if _event.type == ENTITY_EFFECT_EVENT:
            if _event.effect == EntityEffect.PICK_UP_CAP:
                self.currentPoints += 1
                self.dirty = True
                if self.currentPoints >= self.max_points:
                    pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.WON_GAME))
                