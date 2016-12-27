from artifact.spriteartifact import SpriteArtifact
from myevents import SCREEN_EFFECT_EVENT, ScreenEffectEvent
import pygame

class DrawSystem:
    NAME = "DrawSystem"
    observing = []
    currentEffect = None
    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts:   
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")
    def remove(self, _entity):
        self.observing[:] = [entity for entity in self.observing if entity != _entity]
        
    def draw(self, _screen):
        for entity in self.observing:
            entity.artifacts[SpriteArtifact.NAME].sprite.draw(_screen, entity.artifacts[SpriteArtifact.NAME].positionX, 
                                                              entity.artifacts[SpriteArtifact.NAME].positionY)
        if self.currentEffect != None:
            if self.currentEffect.dict['type'] == ScreenEffectEvent.BLUR:#czemu nie mogê .type
                scale = 1.0/float(10.0)
                surf_size = _screen.get_size()
                scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
                surf = pygame.transform.smoothscale(_screen, scale_size)
                surf = pygame.transform.smoothscale(surf, surf_size)
                _screen.blit(surf, (0, 0))
    def update(self, _timeDelta, _systems):
        for entity in self.observing:
            entity.artifacts[SpriteArtifact.NAME].sprite.update(_timeDelta)
    def input(self, _event):
        if _event.type == SCREEN_EFFECT_EVENT:
            self.currentEffect = _event
