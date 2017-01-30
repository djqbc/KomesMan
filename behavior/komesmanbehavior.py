"""Komes man behaviour package."""
from myevents import COLLISION_EVENT, GAME_EVENT, GameEventType
from artifact.tagartifact import TagArtifact, TagType
import pygame


class KomesManBehavior:
    """Class defining behaviour of KomesMan on incoming events."""

    @staticmethod
    def input(_event, _posteventcallback):
        """
        Reaction on incoming event (Death if colliding with enemy.

        :param _event: event to process
        :param _posteventcallback: function to evaluate after processing input
        :return: nothing
        """
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            tag_artifact = entity.artifacts[TagArtifact.NAME]
            if tag_artifact.type == TagType.ENEMY:
                _posteventcallback(pygame.event.Event(GAME_EVENT
                                                      , reason=GameEventType.LOST_LIFE))
