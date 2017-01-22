from myevents import COLLISION_EVENT, ENTITY_EFFECT_EVENT, EntityEffect
from artifact.tagartifact import TagArtifact, TagType
from artifact.spriteartifact import SpriteArtifact
import math
import pygame

class TeleportBehavior:
    @staticmethod
    def input(_event, _postEventCallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            tagArtifact = entity.artifacts[TagArtifact.NAME]
            if tagArtifact.type == TagType.ENEMY or tagArtifact.type == TagType.KOMESMAN:
                mySpriteArtifact = _event.me.artifacts[SpriteArtifact.NAME]
                entitySpriteArtifact = entity.artifacts[SpriteArtifact.NAME]
                if math.hypot(mySpriteArtifact.positionX - entitySpriteArtifact.positionX, mySpriteArtifact.positionY - entitySpriteArtifact.positionY) < 3:
                    _postEventCallback(pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.TELEPORT, teleport=_event.me, reference=entity))   
