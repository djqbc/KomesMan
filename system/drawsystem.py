"""DrawSystem module."""
from artifact.spriteartifact import SpriteArtifact
from myevents import SCREEN_EFFECT_EVENT, ScreenEffectEvent, EventType, starttimer, \
    GAME_STATE_CHANGE_EVENT, MENU_EVENT, MenuEventType
import pygame
from system.gamesystem import GameState


class DrawSystem:
    """System rsponsible for drawing items on screen."""

    NAME = "DrawSystem"
    screen = None
    observing = []
    current_effect = None
    current_game_state = GameState.INIT
    col = 0

    def __init__(self):
        """Constructor."""
        self.createdisplay()

    def createdisplay(self, _resolution=(1024, 768), _maximized=False):
        """
        Function responsible for creating display.

        :param _resolution: Screen resolution dimensions tuple.
        :param _maximized: Boolean value determining maximalization.
        :return: nothing
        """
        if _maximized:
            self.screen = pygame.display.set_mode(_resolution, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF,
                                                  32)
        else:
            self.screen = pygame.display.set_mode(_resolution, 0, 32)
        pygame.display.set_caption('KomesMan')

    def register(self, _object):
        """
        Add object for observing.

        :param _object: object to be added
        :return: nothing
        """
        if SpriteArtifact.NAME in _object.artifacts:
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")

    def remove(self, _entity):
        """
        Remove entity from system.

        :param _entity: entity to be removed.
        :return:
        """
        self.observing[:] = [entity for entity in self.observing if entity != _entity]

    def draw(self):
        """
        Function responsible for drawing all observed items on screen, and for special effects.

        :return: nothing
        """
        self.screen.fill(pygame.Color('black'))
        for entity in self.observing:
            sprite_artifact = entity.artifacts[SpriteArtifact.NAME]
            if sprite_artifact.drawstage & int(self.current_game_state):
                sprite_artifact.sprite.draw(self.screen, sprite_artifact.positionx, sprite_artifact.positiony)
        if self.current_effect is not None:
            if self.current_effect.dict['type'] == ScreenEffectEvent.BLUR:  # czemu nie mog� dac .type
                scale = 1.0 / float(20.0)
                surf_size = self.screen.get_size()
                scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
                surf = pygame.transform.smoothscale(self.screen, scale_size)
                surf = pygame.transform.smoothscale(surf, surf_size)
                self.screen.blit(surf, (0, 0))
            elif self.current_effect.dict['type'] == ScreenEffectEvent.COLOR_EXPLOSION:  # czemu nie mog� dac .type
                surf = self.screen
                array = pygame.surfarray.pixels3d(surf)
                array[:, :, self.col:] = 0
                del array
                self.col+=1
                if self.col == 3:
                    self.col = 0
                self.screen.blit(surf, (0, 0))
            elif self.current_effect.dict['type'] == ScreenEffectEvent.PAUSE_EFFECT:
                surf = self.screen
                array = pygame.surfarray.pixels3d(surf)
                array[:, :, 1:] = 0
                del array
                self.screen.blit(surf, (0, 0))
        pygame.display.flip()

    def update(self, _timedelta, _systems):
        """
        Update all sprites.

        :param _timedelta: game loop delta
        :param _systems: all game systems.
        :return:
        """
        for entity in self.observing:
            entity.artifacts[SpriteArtifact.NAME].sprite.update(_timedelta)

    def input(self, _event):
        """
        Responsible for processing events connected with drawing.

        :param _event: event for processing
        :return: nothing
        """
        if _event.type == GAME_STATE_CHANGE_EVENT:
            self.current_game_state = _event.state
            self.current_effect = None
        elif _event.type == SCREEN_EFFECT_EVENT:  # dodac obsluge wielu efektow na raz
            if _event.reason == EventType.START:
                self.current_effect = _event
                if _event.time is not None:
                    starttimer(_event.time,
                           lambda: pygame.event.post(pygame.event.Event(SCREEN_EFFECT_EVENT, reason=EventType.STOP)))
            elif _event.reason == EventType.STOP:
                self.current_effect = None
        elif _event.type == MENU_EVENT:
            if _event.action == MenuEventType.MAXIMIZE:
                self.createdisplay(_maximized=True)
