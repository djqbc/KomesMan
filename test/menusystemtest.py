import unittest
from system.menusystem import MenuSystem
from entity import Entity
from artifact.menuartifact import MenuArtifact
from system.gamesystem import GameState
from artifact.spriteartifact import SpriteArtifact
import pygame
from sprite.textsprite import TextSprite

class TestMenuSystem(unittest.TestCase):
    def setUp(self):
        pygame.init()
    def test_menu_up(self):
        system = MenuSystem()
        item = Entity()
        item.addartifact(SpriteArtifact(TextSprite("Sdasd"), 0, 0, GameState.MENU))
        item.addartifact(MenuArtifact())
        system.register(item)
        system.register(item)
        system.register(item)
        system.current_game_state = GameState.MENU
        
        self.assertEqual(system.current_index, 0)
        system.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
        self.assertEqual(system.current_index, 2)
        system.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
        self.assertEqual(system.current_index, 1)
        
        system.remove(item)
        system.remove(item)
        system.remove(item)
    
    def test_menu_down(self):
        system = MenuSystem()
        item = Entity()
        item.addartifact(SpriteArtifact(TextSprite("sdas"), 0, 0, GameState.MENU))
        item.addartifact(MenuArtifact())
        system.register(item)
        system.register(item)
        system.register(item)
        system.current_game_state = GameState.MENU
        
        self.assertEqual(system.current_index, 0)
        system.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        self.assertEqual(system.current_index, 1)
        system.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        self.assertEqual(system.current_index, 2)
        
        system.remove(item)
        system.remove(item)
        system.remove(item)
        