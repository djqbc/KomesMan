import unittest
import pygame
from system.drawsystem import DrawSystem
from myevents import SCREEN_EFFECT_EVENT, EventType

class TestDrawSystem(unittest.TestCase):
    def setUp(self):
        pygame.init()
    def test_start_effect(self):
        system = DrawSystem()
        self.assertEqual(system.currentEffect, None)
        system.input(pygame.event.Event(SCREEN_EFFECT_EVENT, reason=EventType.START, time=None))
        self.assertNotEqual(system.currentEffect, None)
        
    def test_stop_effect(self):
        system = DrawSystem()
        self.assertEqual(system.currentEffect, None)
        system.input(pygame.event.Event(SCREEN_EFFECT_EVENT, reason=EventType.START, time=None))
        self.assertNotEqual(system.currentEffect, None)
        system.input(pygame.event.Event(SCREEN_EFFECT_EVENT, reason=EventType.STOP, time=None))
        self.assertEqual(system.currentEffect, None)