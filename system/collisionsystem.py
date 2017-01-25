from artifact.spriteartifact import SpriteArtifact
import pygame
from artifact.behaviorartifact import BehaviorArtifact
from myevents import COLLISION_EVENT, ENTITY_EFFECT_EVENT, EntityEffect
from system.gamesystem import GameSystem, GameState
from system.tagsystem import TagSystem
from artifact.tagartifact import TagType, TagSubType
import random
from artifact.movementartifact import MovementArtifact


class CollisionSystem:
    NAME = "CollisionSystem"
    all = []
    moveableIndexes = []
    observing = []
    
    sprites = []
    behaviors = []

    def __init__(self):
        self.systems = None
        self.tile_size = 64

    def register(self, _object):
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
        x = 0
        for e in self.observing:
            if e == _entity:
                del self.all[x]
                del self.behaviors[x]
                del self.sprites[x]
                if x in self.moveableIndexes:
                    self.moveableIndexes.remove(x)
                for ind in range(len(self.moveableIndexes)):
                    if self.moveableIndexes[ind] > x:
                        self.moveableIndexes[ind] = self.moveableIndexes[ind] - 1
                break
            x += 1
        self.observing[:] = [entity for entity in self.observing if entity != _entity]

    def input(self, _event):
        # obsluga nie powinna byc w tym systemie ale nie mialem pomyslu gdzie to wrzucic zeby bylo globalnie
        if _event.type == ENTITY_EFFECT_EVENT and _event.effect == EntityEffect.TELEPORT:
            teleports = self.systems[TagSystem.NAME].getentities(TagType.FIXED, TagSubType.TELEPORT)
            teleports = [t for t in teleports if t != _event.teleport]
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
                    print("Couldn't find teleport output cell")

    def update(self, _timedelta, _systems):
        if _systems[GameSystem.NAME].getcurrentgamestate() != GameState.GAME:
            return
        self.systems = _systems
        for entityInd in self.moveableIndexes:
            self.all[entityInd].x = self.sprites[entityInd].positionX
            self.all[entityInd].y = self.sprites[entityInd].positionY
            
        for entityInd in self.moveableIndexes:
            colliding = self.all[entityInd].collidelistall(self.all)
            for index in colliding:
                if index != entityInd:
                    entity = self.observing[entityInd]
                    entity2 = self.observing[index]
                    self.behaviors[entityInd].behavior.input(
                        pygame.event.Event(COLLISION_EVENT, me=entity, colliding=entity2), pygame.event.post)
                    self.behaviors[index].behavior.input(
                        pygame.event.Event(COLLISION_EVENT, me=entity2, colliding=entity), pygame.event.post)