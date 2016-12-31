from myevents import ENTITY_EFFECT_EVENT, EntityEffect
import pygame

class MusicSystem:
    NAME = "MusicSystem"
    def __init__(self):
        pass
    def register(self, _object):
        pass
    def remove(self, _entity):
        pass
    def update(self, _timeDelta, _systems):
        pass
    def input(self, _event):
        if _event.type == ENTITY_EFFECT_EVENT and _event.effect == EntityEffect.PLAY_SOUND:
            pygame.mixer.music.load(_event.path)
            pygame.mixer.music.play()