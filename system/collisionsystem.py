from artifact.spriteartifact import SpriteArtifact
import pygame
from artifact.behaviorartifact import BehaviorArtifact
from myevents import COLLISION_EVENT
from system.gamesystem import GameSystem, GameState

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
        pass
    def update(self, _timeDelta, _systems):
        if _systems[GameSystem.NAME].getCurrentGameState() != GameState.GAME:
            return
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
