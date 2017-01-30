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
    """
    System responsible for humant movement.
    """
    NAME = "UserMovementSystem"
    observing = []
    activeKeys = {}

    def __init__(self):
        """
        Constructor
        """
        self.previousdX = 0
        self.previousdY = 0
        self.paused = False

    def register(self, _object):
        """
        Register movable object for system
        :param _object: Movable entity
        :return: nothing
        """
        if SpriteArtifact.NAME in _object.artifacts and MovementArtifact.NAME in _object.artifacts:
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")

    def remove(self, _entity):
        """
        Remove entity from system
        :param _entity: Entity to be removed
        :return: Nothing
        """
        self.observing[:] = [entity for entity in self.observing if entity != _entity]

    def update(self, _delta, _systems):
        """
        Update observed entities based on received events. Works only when unpaused
        :param _delta: game loop delta
        :param _systems: all systems collection
        :return: nothing
        """
        if _systems[GameSystem.NAME].getcurrentgamestate() != GameState.GAME:
            self.paused = True
            return
        self.paused = False
        tag_system = _systems[TagSystem.NAME]
        board = tag_system.getentities(TagType.FIXED, TagSubType.BOARD)[0]
        for entity in self.observing:
            movement_artifact = entity.artifacts[MovementArtifact.NAME]
            if movement_artifact.movementvector != [0, 0]:
                d_x = movement_artifact.movementvector[0] * movement_artifact.speedmodifier * _delta
                d_y = movement_artifact.movementvector[1] * movement_artifact.speedmodifier * _delta
                sprite_artifact = entity.artifacts[SpriteArtifact.NAME]
                if board.checkmove(sprite_artifact.positionx, sprite_artifact.positiony, d_x, d_y):
                    sprite_artifact.positionx += d_x
                    sprite_artifact.positiony += d_y
                    self.previousdX = d_x
                    self.previousdY = d_y
                else:
                    if d_x != 0:  # left
                        if board.checkmove(sprite_artifact.positionx, sprite_artifact.positiony, 0, self.previousdY):
                            sprite_artifact.positiony += self.previousdY
                            sprite_artifact.positiony = int(sprite_artifact.positiony)
                    if d_y != 0:  # up
                        if board.checkmove(sprite_artifact.positionx, sprite_artifact.positiony, self.previousdX, 0):
                            sprite_artifact.positionx += self.previousdX
                            sprite_artifact.positionx = int(sprite_artifact.positionx)


    def input(self, _event):
        """
        Process input events (create movement vectors for events based on input keystrokes)
        :param _event: event to be processed
        :return: nothing
        """
        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_DOWN:
                if not self.activeKeys.get(pygame.K_DOWN, False):
                    self.activeKeys[pygame.K_DOWN] = True
                    for entity in self.observing:
                        entity.artifacts[SpriteArtifact.NAME].sprite.currentanimation = AnimationState.MOVE_DOWN
                        entity.artifacts[MovementArtifact.NAME].movementvector[1] = 1
            elif _event.key == pygame.K_UP:
                if not self.activeKeys.get(pygame.K_UP, False):
                    self.activeKeys[pygame.K_UP] = True
                    for entity in self.observing:
                        entity.artifacts[SpriteArtifact.NAME].sprite.currentanimation = AnimationState.MOVE_UP
                        entity.artifacts[MovementArtifact.NAME].movementvector[1] = -1
            elif _event.key == pygame.K_LEFT:
                if not self.activeKeys.get(pygame.K_LEFT, False):
                    self.activeKeys[pygame.K_LEFT] = True
                    for entity in self.observing:
                        entity.artifacts[SpriteArtifact.NAME].sprite.currentanimation = AnimationState.MOVE_LEFT
                        entity.artifacts[MovementArtifact.NAME].movementvector[0] = -1
            elif _event.key == pygame.K_RIGHT:
                if not self.activeKeys.get(pygame.K_RIGHT, False):
                    self.activeKeys[pygame.K_RIGHT] = True
                    for entity in self.observing:
                        entity.artifacts[SpriteArtifact.NAME].sprite.currentanimation = AnimationState.MOVE_RIGHT
                        entity.artifacts[MovementArtifact.NAME].movementvector[0] = 1
        elif _event.type == pygame.KEYUP:
            if _event.key == pygame.K_DOWN:
                if self.activeKeys[pygame.K_DOWN]:
                    self.activeKeys[pygame.K_DOWN] = False
                    for entity in self.observing:
                        entity.artifacts[MovementArtifact.NAME].movementvector[1] = 0
            elif _event.key == pygame.K_UP:
                if self.activeKeys[pygame.K_UP]:
                    self.activeKeys[pygame.K_UP] = False
                    for entity in self.observing:
                        entity.artifacts[MovementArtifact.NAME].movementvector[1] = 0
            elif _event.key == pygame.K_LEFT:
                if self.activeKeys[pygame.K_LEFT]:
                    self.activeKeys[pygame.K_LEFT] = False
                    for entity in self.observing:
                        entity.artifacts[MovementArtifact.NAME].movementvector[0] = 0
            elif _event.key == pygame.K_RIGHT:
                if self.activeKeys[pygame.K_RIGHT]:
                    self.activeKeys[pygame.K_RIGHT] = False
                    for entity in self.observing:
                        entity.artifacts[MovementArtifact.NAME].movementvector[0] = 0
        elif _event.type == ENTITY_EFFECT_EVENT:
            if _event.effect == EntityEffect.SPEED_CHANGE:
                if _event.reason == EventType.START:
                    for entity in self.observing:
                        if entity == _event.reference:
                            entity.artifacts[MovementArtifact.NAME].speedmodifier *= _event.modifier
                            starttimer(_event.time, lambda:
                            pygame.event.post(pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.SPEED_CHANGE,
                                                                 reason=EventType.STOP, modifier=1.0 / _event.modifier,
                                                                 reference=_event.reference)))
                elif _event.reason == EventType.STOP:
                    for entity in self.observing:
                        if entity == _event.reference:
                            entity.artifacts[MovementArtifact.NAME].speedmodifier *= _event.modifier
                elif _event.reason == EventType.DELAYED:
                    tmp = copyevent(_event)
                    tmp.reason = EventType.START
                    # czemu kopiowanie referencji nie dzia�a poprawnie w copyEvent?
                    tmp.reference = _event.reference
                    starttimer(_event.delay, lambda: pygame.event.post(tmp))
