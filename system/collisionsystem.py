from artifact.spriteartifact import SpriteArtifact
import pygame
from artifact.behaviorartifact import BehaviorArtifact
from myevents import COLLISION_EVENT

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
        x = 0
        for entity in self.observing:
            x += 1
            for index in range(x, len(self.observing)):
                entity2 = self.observing[index]
                if entity != entity2:
                    entity.artifacts[SpriteArtifact.NAME].sprite.rect.x = entity.artifacts[SpriteArtifact.NAME].positionX
                    entity.artifacts[SpriteArtifact.NAME].sprite.rect.y = entity.artifacts[SpriteArtifact.NAME].positionY
                    entity2.artifacts[SpriteArtifact.NAME].sprite.rect.x = entity2.artifacts[SpriteArtifact.NAME].positionX
                    entity2.artifacts[SpriteArtifact.NAME].sprite.rect.y = entity2.artifacts[SpriteArtifact.NAME].positionY
                    if pygame.sprite.collide_rect(entity.artifacts[SpriteArtifact.NAME].sprite, entity2.artifacts[SpriteArtifact.NAME].sprite) == True:
                        entity.artifacts[BehaviorArtifact.NAME].behavior.input(pygame.event.Event(COLLISION_EVENT, me=entity, colliding=entity2), pygame.event.post)
                        entity2.artifacts[BehaviorArtifact.NAME].behavior.input(pygame.event.Event(COLLISION_EVENT, me=entity2, colliding=entity), pygame.event.post)
