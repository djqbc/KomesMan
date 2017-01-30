import unittest
from system.gamesystem import GameSystem, GameState
from myevents import GAME_STATE_CHANGE_EVENT
import pygame

class TestGameSystem(unittest.TestCase):
    def setUp(self):
        pygame.init()
    def test_game_state(self):
        system = GameSystem()
        self.assertEqual(system.game_state, GameState.MENU)
        system.endinit()
        self.assertEqual(system.game_state, GameState.MENU)
    
    def test_quit(self):
        system = GameSystem()
        self.assertFalse(system.quit())
        system.endinit()
        self.assertFalse(system.quit())
        system.input(pygame.event.Event(pygame.QUIT, state=GameState.END))
        self.assertTrue(system.quit())