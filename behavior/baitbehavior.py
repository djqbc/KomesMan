"""Bait behaviour module."""
from myevents import COLLISION_EVENT, GAME_EVENT, GameEventType
from artifact.tagartifact import TagArtifact, TagType
import pygame


class BaitBehavior:
    """Class defining behaviour of bait on incoming events."""

    @staticmethod
    def input(_event, _posteventcallback):
        """
        Reaction on incoming event.

        Currently handles only collision (deletes object from map)
        :param _event: event to process
        :param _posteventcallback: function to evaluate after processing input
        :return: nothingS
        """
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            if entity.artifacts[TagArtifact.NAME].type == TagType.ENEMY:
                _posteventcallback(
                    pygame.event.Event(GAME_EVENT, reason=GameEventType.REMOVE_OBJECT
                                       , reference=_event.me))
