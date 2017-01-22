from myevents import COLLISION_EVENT, ENTITY_EFFECT_EVENT, EntityEffect
from artifact.tagartifact import TagArtifact, TagType
from artifact.spriteartifact import SpriteArtifact
import math
import pygame


class TeleportBehavior:
    @staticmethod
    def input(_event, _posteventcallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            tag_artifact = entity.artifacts[TagArtifact.NAME]
            if tag_artifact.type == TagType.ENEMY or tag_artifact.type == TagType.KOMESMAN:
                my_sprite_artifact = _event.me.artifacts[SpriteArtifact.NAME]
                entity_sprite_artifact = entity.artifacts[SpriteArtifact.NAME]
                if math.hypot(my_sprite_artifact.positionX - entity_sprite_artifact.positionX,
                              my_sprite_artifact.positionY - entity_sprite_artifact.positionY) < 3:
                    _posteventcallback(
                        pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.TELEPORT, teleport=_event.me,
                                           reference=entity))
