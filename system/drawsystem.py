from artifact.spriteartifact import SpriteArtifact
from myevents import SCREEN_EFFECT_EVENT, ScreenEffectEvent, EventType, startTimer,\
    GAME_STATE_CHANGE_EVENT, MENU_EVENT, MenuEventType
import pygame
from system.gamesystem import GameState

class DrawSystem:
    NAME = "DrawSystem"
    screen = None
    observing = []
    currentEffect = None
    currentGameState = GameState.INIT
    def __init__(self):
        self.createDisplay()
           
    def createDisplay(self, _resolution=(1024,768), _maximized=False): 
        if _maximized:    
            self.screen = pygame.display.set_mode(_resolution, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF, 32)
        else:
            self.screen = pygame.display.set_mode(_resolution, 0, 32)
        pygame.display.set_caption('KomesMan')
        
    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts:   
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")
        
    def remove(self, _entity):
        self.observing[:] = [entity for entity in self.observing if entity != _entity]
        
    def draw(self):
        self.screen.fill(pygame.Color('black'))
        for entity in self.observing:
            spriteArtifact = entity.artifacts[SpriteArtifact.NAME]
            if spriteArtifact.drawStage & int(self.currentGameState):
                spriteArtifact.sprite.draw(self.screen, spriteArtifact.positionX, spriteArtifact.positionY)
        if self.currentEffect is not None:
            if self.currentEffect.dict['type'] == ScreenEffectEvent.BLUR:#czemu nie mog� dac .type
                scale = 1.0/float(10.0)
                surf_size = self.screen.get_size()
                scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
                surf = pygame.transform.smoothscale(self.screen, scale_size)
                surf = pygame.transform.smoothscale(surf, surf_size)
                self.screen.blit(surf, (0, 0))
            elif self.currentEffect.dict['type'] == ScreenEffectEvent.COLOR_EXPLOSION:#czemu nie mog� dac .type
                surf = self.screen
                array = pygame.surfarray.pixels3d(surf)
                array[:,:,1:] = 0
                del array
                self.screen.blit(surf, (0, 0))
        pygame.display.flip()
    def update(self, _timeDelta, _systems):
        for entity in self.observing:
            entity.artifacts[SpriteArtifact.NAME].sprite.update(_timeDelta)
    def input(self, _event):
        if _event.type == GAME_STATE_CHANGE_EVENT:
            self.currentGameState = _event.state
        elif _event.type == SCREEN_EFFECT_EVENT:#dodac obsluge wielu efektow na raz
            if _event.reason == EventType.START:
                self.currentEffect = _event
                startTimer(_event.time, lambda : pygame.event.post(pygame.event.Event(SCREEN_EFFECT_EVENT, reason=EventType.STOP)))
            elif _event.reason == EventType.STOP:
                self.currentEffect = None
        elif _event.type == MENU_EVENT:
            if _event.action == MenuEventType.MAXIMIZE:
                self.createDisplay(_maximized=True)
