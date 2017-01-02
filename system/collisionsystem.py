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
    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts and BehaviorArtifact.NAME in _object.artifacts:   
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")
    def remove(self, _entity):
        self.observing[:] = [entity for entity in self.observing if entity != _entity]
    def input(self, _event):
        #obsluga nie powinna byc w tym systemie ale nie mialem pomyslu gdzie to wrzucic zeby bylo globalnie
        if _event.type == ENTITY_EFFECT_EVENT and _event.effect == EntityEffect.TELEPORT:
            teleports = self.systems[TagSystem.NAME].getEntities(TagType.FIXED, TagSubType.TELEPORT)
            teleports = [t for t in teleports if t != _event.teleport]
            if len(teleports) > 0:
                board = self.systems[TagSystem.NAME].getEntities(TagType.FIXED, TagSubType.BOARD)[0]
                targetTeleport = random.choice(teleports)
                targetTeleportSpriteArtifact = targetTeleport.artifacts[SpriteArtifact.NAME]
                entitySpriteArtifact = _event.reference.artifacts[SpriteArtifact.NAME]
                entitySpriteArtifact.positionX = targetTeleportSpriteArtifact.positionX
                entitySpriteArtifact.positionY = targetTeleportSpriteArtifact.positionY
                #poprawic tile size sztywny
                if board.checkMove(entitySpriteArtifact.positionX, entitySpriteArtifact.positionY, 0, -64):
                    entitySpriteArtifact.positionY -= 64
                elif board.checkMove(entitySpriteArtifact.positionX, entitySpriteArtifact.positionY, 0, 64):
                    entitySpriteArtifact.positionY += 64
                elif board.checkMove(entitySpriteArtifact.positionX, entitySpriteArtifact.positionY, -64, 0):
                    entitySpriteArtifact.positionX -= 64
                elif board.checkMove(entitySpriteArtifact.positionX, entitySpriteArtifact.positionY, 64, 0):
                    entitySpriteArtifact.positionX += 64
                else:
                    print("Couldn't find teleport output cell")
    def update(self, _timeDelta, _systems):
        if _systems[GameSystem.NAME].getCurrentGameState() != GameState.GAME:
            return
        self.systems = _systems
        x = 0
        for entity in self.observing:
            x += 1
            for index in range(x, len(self.observing)):
                entity2 = self.observing[index]
#             for entity2 in self.observing:
                if entity != entity2:
                    e1SpriteArtifact = entity.artifacts[SpriteArtifact.NAME]
                    e2SpriteArtifact = entity2.artifacts[SpriteArtifact.NAME]
                    e1SpriteArtifact.sprite.rect.x = e1SpriteArtifact.positionX
                    e1SpriteArtifact.sprite.rect.y = e1SpriteArtifact.positionY
                    e2SpriteArtifact.sprite.rect.x = e2SpriteArtifact.positionX
                    e2SpriteArtifact.sprite.rect.y = e2SpriteArtifact.positionY
                    if pygame.sprite.collide_rect(e1SpriteArtifact.sprite, e2SpriteArtifact.sprite) == True:
                        entity.artifacts[BehaviorArtifact.NAME].behavior.input(pygame.event.Event(COLLISION_EVENT, me=entity, colliding=entity2), pygame.event.post)
                        entity2.artifacts[BehaviorArtifact.NAME].behavior.input(pygame.event.Event(COLLISION_EVENT, me=entity2, colliding=entity), pygame.event.post)
