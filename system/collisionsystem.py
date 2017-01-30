"""
Collision system module
"""
import random
import pygame
from artifact.spriteartifact import SpriteArtifact
from artifact.behaviorartifact import BehaviorArtifact
from artifact.movementartifact import MovementArtifact
from artifact.tagartifact import TagType, TagSubType
from myevents import COLLISION_EVENT, ENTITY_EFFECT_EVENT, EntityEffect
from system.gamesystem import GameSystem, GameState
from system.tagsystem import TagSystem


class CollisionSystem:
    """
    System responsible for handling collisions
    """
    NAME = "CollisionSystem"
    all = []
    moveableIndexes = []
    observing = []

    sprites = []
    behaviors = []

    def __init__(self):
        """
        Constructor
        """
        self.systems = None
        self.tile_size = 64

    def register(self, _object):
        """
        Registers objects for collision detection system. Holds positions, sprites and behaviours.
        :param _object: Object to be added to collision processing system
        :return: nothing
        """
        if SpriteArtifact.NAME in _object.artifacts and BehaviorArtifact.NAME in _object.artifacts:
            self.observing.append(_object)
            e1_sprite_artifact = _object.artifacts[SpriteArtifact.NAME]
            e1_behavior_artifact = _object.artifacts[BehaviorArtifact.NAME]
            e1_sprite_artifact.sprite.rect.x = e1_sprite_artifact.positionX
            e1_sprite_artifact.sprite.rect.y = e1_sprite_artifact.positionY
            self.all.append(e1_sprite_artifact.sprite.rect)
            self.sprites.append(e1_sprite_artifact)
            self.behaviors.append(e1_behavior_artifact)
            if MovementArtifact.NAME in _object.artifacts:
                self.moveableIndexes.append(len(self.all) - 1)
        else:
            raise NameError("ERROR!!!")

    def remove(self, _entity):
        """
        Removes entity from system
        :param _entity: entity to remove
        :return: nothing
        """
        try:
            index = self.observing.index(_entity)
        except:
            return

        del self.all[index]
        del self.behaviors[index]
        del self.sprites[index]
        if index in self.moveableIndexes:
            self.moveableIndexes.remove(index)
        for ind in range(len(self.moveableIndexes)):
            if self.moveableIndexes[ind] > index:
                self.moveableIndexes[ind] = self.moveableIndexes[ind] - 1
        self.observing.remove(_entity)

    def input(self, _event):
        """
        Processing of player's teleporation when reached border of screen.
        :param _event: event to process
        :return: nothing
        """
        if _event.type == ENTITY_EFFECT_EVENT and _event.effect == EntityEffect.TELEPORT:
            teleports = self.systems[TagSystem.NAME].getentities(TagType.FIXED, TagSubType.TELEPORT)
            teleports = [FPS_TIME for FPS_TIME in teleports if FPS_TIME != _event.teleport]
            if len(teleports) > 0:
                board = self.systems[TagSystem.NAME].getentities(TagType.FIXED, TagSubType.BOARD)[0]
                target_teleport = random.choice(teleports)
                target_teleport_sprite_artifact = target_teleport.artifacts[SpriteArtifact.NAME]
                entity_sprite_artifact = _event.reference.artifacts[SpriteArtifact.NAME]
                entity_sprite_artifact.positionX = target_teleport_sprite_artifact.positionX
                entity_sprite_artifact.positionY = target_teleport_sprite_artifact.positionY
                # poprawic tile size sztywny
                if board.checkmove(entity_sprite_artifact.positionX, entity_sprite_artifact.positionY, 0, -self.tile_size):
                    entity_sprite_artifact.positionY -= self.tile_size
                elif board.checkmove(entity_sprite_artifact.positionX, entity_sprite_artifact.positionY, 0, self.tile_size):
                    entity_sprite_artifact.positionY += self.tile_size
                elif board.checkmove(entity_sprite_artifact.positionX, entity_sprite_artifact.positionY, -self.tile_size, 0):
                    entity_sprite_artifact.positionX -= self.tile_size
                elif board.checkmove(entity_sprite_artifact.positionX, entity_sprite_artifact.positionY, self.tile_size, 0):
                    entity_sprite_artifact.positionX += self.tile_size
                else:
                    print("Couldn'FPS_TIME find teleport output cell")

    def update(self, _timedelta, _systems):
        """
        Verifies if items are colliding, and creates collision events, for both entities.
        :param _timedelta: game loop delta
        :param _systems: all system collection
        :return: nothing
        """
        if _systems[GameSystem.NAME].getcurrentgamestate() != GameState.GAME:
            return
        self.systems = _systems
        for entity_ind in self.moveableIndexes:
            self.all[entity_ind].x = self.sprites[entity_ind].positionX
            self.all[entity_ind].y = self.sprites[entity_ind].positionY

        for entity_ind in self.moveableIndexes:
            colliding = self.all[entity_ind].collidelistall(self.all)
            for index in colliding:
                if index != entity_ind:
                    entity = self.observing[entity_ind]
                    entity2 = self.observing[index]

                    self.behaviors[entity_ind].behavior.input(
                        pygame.event.Event(COLLISION_EVENT, me=entity, colliding=entity2), pygame.event.post)

                    if index not in self.moveableIndexes:
                        self.behaviors[index].behavior.input(
                            pygame.event.Event(COLLISION_EVENT, me=entity2, colliding=entity), pygame.event.post)