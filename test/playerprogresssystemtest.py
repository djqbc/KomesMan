import unittest
import pygame
from system.playerprogresssystem import PlayerProgressSystem
from myevents import GAME_EVENT, GameEventType, ENTITY_EFFECT_EVENT,\
    EntityEffect

class TestPlayerProgressSystem(unittest.TestCase):
    def setUp(self):
        pygame.init()
    def test_advance_level(self):
        system = PlayerProgressSystem()
        self.assertEqual(system.current_level, 1)
        system.input(pygame.event.Event(GAME_EVENT, reason=GameEventType.WON_GAME))
        self.assertEqual(system.current_level, 2)
        system.input(pygame.event.Event(GAME_EVENT, reason=GameEventType.WON_GAME))
        self.assertEqual(system.current_level, 3)
    def test_lost_game(self):
        system = PlayerProgressSystem()
        self.assertEqual(system.current_level, 1)
        system.input(pygame.event.Event(GAME_EVENT, reason=GameEventType.WON_GAME))
        self.assertEqual(system.current_level, 2)
        self.assertEqual(system.current_lifes, 3)
        system.input(pygame.event.Event(GAME_EVENT, reason=GameEventType.LOST_LIFE))
        self.assertEqual(system.current_level, 2)
        self.assertEqual(system.current_lifes, 2)
        system.input(pygame.event.Event(GAME_EVENT, reason=GameEventType.LOST_LIFE))
        self.assertEqual(system.current_lifes, 1)
        self.assertEqual(system.current_level, 2)
        system.input(pygame.event.Event(GAME_EVENT, reason=GameEventType.LOST_LIFE))
        self.assertEqual(system.current_lifes, 0)
        self.assertEqual(system.current_level, 1)
    def test_add_points(self):
        system = PlayerProgressSystem()
        self.assertEqual(system.overall_points, 0)
        system.input(pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.PICK_UP_CAP))
        self.assertEqual(system.overall_points, 10)
        system.input(pygame.event.Event(GAME_EVENT, reason=GameEventType.WON_GAME))
        self.assertEqual(system.overall_points, 110)
    
    