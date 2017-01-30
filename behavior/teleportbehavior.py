"""
Teleport behaviour package
"""
import math
import pygame
from myevents import COLLISION_EVENT, ENTITY_EFFECT_EVENT, EntityEffect
from artifact.tagartifact import TagArtifact, TagType
from artifact.spriteartifact import SpriteArtifact


class TeleportBehavior:
    """
    Class defining behaviour of teleport on incoming events
    """
    @staticmethod
    def input(_event, _posteventcallback):
        """
        Reaction on incoming event.
        Teleports player or enemy to the other side of screen.
        :param _event: event to process
        :param _posteventcallback: function to evaluate after processing input
        :return: nothing
        """
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            tag_artifact = entity.artifacts[TagArtifact.NAME]
            if tag_artifact.type == TagType.ENEMY or tag_artifact.type == TagType.KOMESMAN:
                my_sprite_artifact = _event.me.artifacts[SpriteArtifact.NAME]
                entity_sprite_artifact = entity.artifacts[SpriteArtifact.NAME]
                if math.hypot(my_sprite_artifact.positionX - entity_sprite_artifact.positionX,
                              my_sprite_artifact.positionY - entity_sprite_artifact.positionY) < 3:
                    _posteventcallback(
                        pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.TELEPORT
                                           , teleport=_event.me,
                                           reference=entity))
