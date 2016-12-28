from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
from sprite.mysprite import AnimationState
from system.tagsystem import TagSystem
import pygame
from myevents import ENTITY_EFFECT_EVENT, EventType, EntityEffect, startTimer

class UserMovementSystem:
    NAME = "UserMovementSystem"
    observing = []
    activeKeys = {}
    
    def __init__(self):
        pass
    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts and MovementArtifact.NAME in _object.artifacts:   
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")
    def remove(self, _entity):
        self.observing[:] = [entity for entity in self.observing if entity != _entity]
    def update(self, _delta, _systems):
        tagSystem = _systems[TagSystem.NAME]
        board = tagSystem.getEntities("Board")[0]
        for entity in self.observing:
            if entity.artifacts[MovementArtifact.NAME].movementVector != [0, 0]:
                dX = entity.artifacts[MovementArtifact.NAME].movementVector[0] * entity.artifacts[MovementArtifact.NAME].speedModifier
                dY = entity.artifacts[MovementArtifact.NAME].movementVector[1] * entity.artifacts[MovementArtifact.NAME].speedModifier
                if board.checkMove(entity.artifacts[SpriteArtifact.NAME].positionX, entity.artifacts[SpriteArtifact.NAME].positionY, dX, dY):
                    entity.artifacts[SpriteArtifact.NAME].positionX += dX
                    entity.artifacts[SpriteArtifact.NAME].positionY += dY
    def input(self, _event):
        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_DOWN:
                if self.activeKeys.get(pygame.K_DOWN, False) == False:
                    self.activeKeys[pygame.K_DOWN] = True
                    for entity in self.observing:
                        entity.artifacts[SpriteArtifact.NAME].sprite.currentAnimation = AnimationState.MOVE_DOWN
                        entity.artifacts[MovementArtifact.NAME].movementVector[1] = 1
            elif _event.key == pygame.K_UP:
                if self.activeKeys.get(pygame.K_UP, False) == False:
                    self.activeKeys[pygame.K_UP] = True
                    for entity in self.observing:
                        entity.artifacts[SpriteArtifact.NAME].sprite.currentAnimation = AnimationState.MOVE_UP
                        entity.artifacts[MovementArtifact.NAME].movementVector[1] = -1
            elif _event.key == pygame.K_LEFT:
                if self.activeKeys.get(pygame.K_LEFT, False) == False:
                    self.activeKeys[pygame.K_LEFT] = True
                    for entity in self.observing:
                        entity.artifacts[SpriteArtifact.NAME].sprite.currentAnimation = AnimationState.MOVE_LEFT
                        entity.artifacts[MovementArtifact.NAME].movementVector[0] = -1
            elif _event.key == pygame.K_RIGHT:
                if self.activeKeys.get(pygame.K_RIGHT, False) == False:
                    self.activeKeys[pygame.K_RIGHT] = True
                    for entity in self.observing:
                        entity.artifacts[SpriteArtifact.NAME].sprite.currentAnimation = AnimationState.MOVE_RIGHT
                        entity.artifacts[MovementArtifact.NAME].movementVector[0] = 1
        elif _event.type == pygame.KEYUP:
            if _event.key == pygame.K_DOWN:
                if self.activeKeys[pygame.K_DOWN] == True:
                    self.activeKeys[pygame.K_DOWN] = False
                    for entity in self.observing:
                        entity.artifacts[MovementArtifact.NAME].movementVector[1] = 0
            elif _event.key == pygame.K_UP:
                if self.activeKeys[pygame.K_UP] == True:
                    self.activeKeys[pygame.K_UP] = False
                    for entity in self.observing:
                        entity.artifacts[MovementArtifact.NAME].movementVector[1] = 0
            elif _event.key == pygame.K_LEFT:
                if self.activeKeys[pygame.K_LEFT] == True:
                    self.activeKeys[pygame.K_LEFT] = False
                    for entity in self.observing:
                        entity.artifacts[MovementArtifact.NAME].movementVector[0] = 0
            elif _event.key == pygame.K_RIGHT:
                if self.activeKeys[pygame.K_RIGHT] == True:
                    self.activeKeys[pygame.K_RIGHT] = False
                    for entity in self.observing:
                        entity.artifacts[MovementArtifact.NAME].movementVector[0] = 0
        elif _event.type == ENTITY_EFFECT_EVENT:
            if _event.reason == EventType.START:
                for entity in self.observing:
                    if entity == _event.reference:
                        if _event.effect == EntityEffect.SPEED_CHANGE:
                            entity.artifacts[MovementArtifact.NAME].speedModifier *= _event.modifier
                            startTimer(_event.time, lambda : 
                                       pygame.event.post(pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.SPEED_CHANGE, 
                                                                            reason=EventType.STOP, modifier=1.0/_event.modifier, reference=_event.reference)))
            elif _event.reason == EventType.STOP:
                for entity in self.observing:
                    if entity == _event.reference:
                        if _event.effect == EntityEffect.SPEED_CHANGE:
                            entity.artifacts[MovementArtifact.NAME].speedModifier *= _event.modifier