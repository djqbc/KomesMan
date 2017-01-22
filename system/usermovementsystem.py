from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
from sprite.mysprite import AnimationState
from system.tagsystem import TagSystem
import pygame
from myevents import ENTITY_EFFECT_EVENT, EventType, EntityEffect, starttimer, \
    copyevent
from system.gamesystem import GameSystem, GameState
from artifact.tagartifact import TagType, TagSubType


class UserMovementSystem:
    NAME = "UserMovementSystem"
    observing = []
    activeKeys = {}

    def __init__(self):
        self.previousdX = 0
        self.previousdY = 0

    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts and MovementArtifact.NAME in _object.artifacts:
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")

    def remove(self, _entity):
        self.observing[:] = [entity for entity in self.observing if entity != _entity]

    def update(self, _delta, _systems):
        if _systems[GameSystem.NAME].getcurrentgamestate() != GameState.GAME:
            return
        tag_system = _systems[TagSystem.NAME]
        board = tag_system.getentities(TagType.FIXED, TagSubType.BOARD)[0]
        for entity in self.observing:
            movement_artifact = entity.artifacts[MovementArtifact.NAME]
            if movement_artifact.movementVector != [0, 0]:
                d_x = movement_artifact.movementVector[0] * movement_artifact.speedModifier * _delta
                d_y = movement_artifact.movementVector[1] * movement_artifact.speedModifier * _delta
                sprite_artifact = entity.artifacts[SpriteArtifact.NAME]
                if board.checkmove(sprite_artifact.positionX, sprite_artifact.positionY, d_x, d_y):
                    sprite_artifact.positionX += d_x
                    sprite_artifact.positionY += d_y
                    self.previousdX = d_x
                    self.previousdY = d_y
                else:
                    if d_x != 0:  # left
                        if board.checkmove(sprite_artifact.positionX, sprite_artifact.positionY, 0, self.previousdY):
                            sprite_artifact.positionY += self.previousdY
                    if d_y != 0:  # up
                        if board.checkmove(sprite_artifact.positionX, sprite_artifact.positionY, self.previousdX, 0):
                            sprite_artifact.positionX += self.previousdX

    def input(self, _event):
        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_DOWN:
                if not self.activeKeys.get(pygame.K_DOWN, False):
                    self.activeKeys[pygame.K_DOWN] = True
                    for entity in self.observing:
                        entity.artifacts[SpriteArtifact.NAME].sprite.currentAnimation = AnimationState.MOVE_DOWN
                        entity.artifacts[MovementArtifact.NAME].movementVector[1] = 1
            elif _event.key == pygame.K_UP:
                if not self.activeKeys.get(pygame.K_UP, False):
                    self.activeKeys[pygame.K_UP] = True
                    for entity in self.observing:
                        entity.artifacts[SpriteArtifact.NAME].sprite.currentAnimation = AnimationState.MOVE_UP
                        entity.artifacts[MovementArtifact.NAME].movementVector[1] = -1
            elif _event.key == pygame.K_LEFT:
                if not self.activeKeys.get(pygame.K_LEFT, False):
                    self.activeKeys[pygame.K_LEFT] = True
                    for entity in self.observing:
                        entity.artifacts[SpriteArtifact.NAME].sprite.currentAnimation = AnimationState.MOVE_LEFT
                        entity.artifacts[MovementArtifact.NAME].movementVector[0] = -1
            elif _event.key == pygame.K_RIGHT:
                if not self.activeKeys.get(pygame.K_RIGHT, False):
                    self.activeKeys[pygame.K_RIGHT] = True
                    for entity in self.observing:
                        entity.artifacts[SpriteArtifact.NAME].sprite.currentAnimation = AnimationState.MOVE_RIGHT
                        entity.artifacts[MovementArtifact.NAME].movementVector[0] = 1
        elif _event.type == pygame.KEYUP:
            if _event.key == pygame.K_DOWN:
                if self.activeKeys[pygame.K_DOWN]:
                    self.activeKeys[pygame.K_DOWN] = False
                    for entity in self.observing:
                        entity.artifacts[MovementArtifact.NAME].movementVector[1] = 0
            elif _event.key == pygame.K_UP:
                if self.activeKeys[pygame.K_UP]:
                    self.activeKeys[pygame.K_UP] = False
                    for entity in self.observing:
                        entity.artifacts[MovementArtifact.NAME].movementVector[1] = 0
            elif _event.key == pygame.K_LEFT:
                if self.activeKeys[pygame.K_LEFT]:
                    self.activeKeys[pygame.K_LEFT] = False
                    for entity in self.observing:
                        entity.artifacts[MovementArtifact.NAME].movementVector[0] = 0
            elif _event.key == pygame.K_RIGHT:
                if self.activeKeys[pygame.K_RIGHT]:
                    self.activeKeys[pygame.K_RIGHT] = False
                    for entity in self.observing:
                        entity.artifacts[MovementArtifact.NAME].movementVector[0] = 0
        elif _event.type == ENTITY_EFFECT_EVENT:
            if _event.effect == EntityEffect.SPEED_CHANGE:
                if _event.reason == EventType.START:
                    for entity in self.observing:
                        if entity == _event.reference:
                            entity.artifacts[MovementArtifact.NAME].speedModifier *= _event.modifier
                            starttimer(_event.time, lambda:
                            pygame.event.post(pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.SPEED_CHANGE,
                                                                 reason=EventType.STOP, modifier=1.0 / _event.modifier,
                                                                 reference=_event.reference)))
                elif _event.reason == EventType.STOP:
                    for entity in self.observing:
                        if entity == _event.reference:
                            entity.artifacts[MovementArtifact.NAME].speedModifier *= _event.modifier
                elif _event.reason == EventType.DELAYED:
                    tmp = copyevent(_event)
                    tmp.reason = EventType.START
                    # czemu kopiowanie referencji nie dzia�a poprawnie w copyEvent?
                    tmp.reference = _event.reference
                    starttimer(_event.delay, lambda: pygame.event.post(tmp))
