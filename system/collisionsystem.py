from artifact.spriteartifact import SpriteArtifact
import pygame
from artifact.behaviorartifact import BehaviorArtifact
from myevents import COLLISION_EVENT, ENTITY_EFFECT_EVENT, EntityEffect
from system.gamesystem import GameSystem, GameState
from system.tagsystem import TagSystem
from artifact.tagartifact import TagType, TagSubType
import random


class CollisionSystem:
    NAME = "CollisionSystem"
    observing = []

    def __init__(self):
        self.systems = None
        self.tile_size = 64

    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts and BehaviorArtifact.NAME in _object.artifacts:
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")

    def remove(self, _entity):
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
        x = 0
        for entity in self.observing:
            x += 1
            for index in range(x, len(self.observing)):
                entity2 = self.observing[index]
                #             for entity2 in self.observing:
                if entity != entity2:
                    e1_sprite_artifact = entity.artifacts[SpriteArtifact.NAME]
                    e2_sprite_artifact = entity2.artifacts[SpriteArtifact.NAME]
                    e1_sprite_artifact.sprite.rect.x = e1_sprite_artifact.positionX
                    e1_sprite_artifact.sprite.rect.y = e1_sprite_artifact.positionY
                    e2_sprite_artifact.sprite.rect.x = e2_sprite_artifact.positionX
                    e2_sprite_artifact.sprite.rect.y = e2_sprite_artifact.positionY
                    if pygame.sprite.collide_rect(e1_sprite_artifact.sprite, e2_sprite_artifact.sprite):
                        entity.artifacts[BehaviorArtifact.NAME].behavior.input(
                            pygame.event.Event(COLLISION_EVENT, me=entity, colliding=entity2), pygame.event.post)
                        entity2.artifacts[BehaviorArtifact.NAME].behavior.input(
                            pygame.event.Event(COLLISION_EVENT, me=entity2, colliding=entity), pygame.event.post)
