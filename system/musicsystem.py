"""
MusicSystem module
"""
from myevents import ENTITY_EFFECT_EVENT, EntityEffect
import pygame


class MusicSystem:
    """
    System responsible for playing sound.
    """
    NAME = "MusicSystem"

    def __init__(self):
        """
        Constructor
        """
        pass

    def register(self, _object):
        """
        Register object method stub
        :param _object: object to be registered
        :return: nothing
        """
        pass

    def remove(self, _entity):
        """
        Remove object method stub
        :param _entity: entity to be deleted
        :return: nothing
        """
        pass

    def update(self, _timedelta, _systems):
        """
        Update method stub
        :param _timedelta: game loop delta
        :param _systems: collection of all systems
        :return: nothing
        """
        pass

    @staticmethod
    def input(_event):
        """
        Function responsible for processing sound playing requests
        :param _event: event to be processed
        :return: nothing
        """
        if _event.type == ENTITY_EFFECT_EVENT and _event.effect == EntityEffect.PLAY_SOUND:
            pygame.mixer.music.load(_event.path)
            pygame.mixer.music.play()
