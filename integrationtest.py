import unittest
import pygame
from gamemanager import GameManager
from system.gamesystem import GameState
from artifact.spriteartifact import SpriteArtifact
from artifact.tagartifact import TagType
from myevents import GAME_STATE_CHANGE_EVENT

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_quit(self):
        game = GameManager()
        game.input(pygame.event.Event(pygame.QUIT, state=GameState.END))
        self.assertEqual(game.gameSystem.getcurrentgamestate(), GameState.END)
        del game
        
    def test_change_tile_size(self):
        game = GameManager()
        game.gameSystem.endinit()
        for event in pygame.event.get():
            game.input(event)
        self.assertEqual(game.builders[0].tile_size, 32)
        game.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        game.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        game.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        game.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        for event in pygame.event.get():
            game.input(event)
        self.assertEqual(game.builders[0].tile_size, 64)
        del game
    
    def test_changing_highscores(self):
        with open("highscores.txt", "w") as file:
            file.write("Mateusz III Wielki|0\n")
            file.write("JBK|1000\n")
            file.write("real|9999\n")
            file.write("pepe|-1\n")
        game = GameManager()
        game.gameSystem.endinit()
        for event in pygame.event.get():
            game.input(event)
        game.menuSystem.currentIndex = 0
        game.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        game.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        game.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        for event in pygame.event.get():
            game.input(event)
        names = [e.artifacts[SpriteArtifact.NAME].sprite.textContent for e in game.builders[1].highscorenames]
        values = [e.artifacts[SpriteArtifact.NAME].sprite.textContent for e in game.builders[1].highscorevalues]
        xN = len([s for s in names if s != 'x'])
        names = names[:xN]
        values = values[:xN]
        expected = {"1 Mateusz III Wielki" : '0', 
                    "2 JBK" : '1000',
                    "3 real" : '9999',
                    "4 pepe" : '-1'}
        self.assertDictEqual(dict(zip(names, values)), expected)
        del game
        
    def test_lost_game(self):
        game = GameManager()
        game.gameSystem.endinit()
        for event in pygame.event.get():
            game.input(event)
        game.menuSystem.currentIndex = 0
        game.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        for event in pygame.event.get():
            game.input(event)
        game.input(pygame.event.Event(pygame.KEYUP, key=pygame.K_p))
        i = 0
        while True:
            for event in pygame.event.get():
                game.input(event)
            game.update(0.01)
#             game.render()
            if game.gameSystem.getcurrentgamestate() & GameState.PAUSED:
                game.input(pygame.event.Event(pygame.KEYUP, key=pygame.K_p))
            if len(game.tagSystem.getentities(TagType.ENEMY)) == 0 or i > 1000000:
                print("Reload")
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.WON_GAME))
                i = 0
            if game.playerProgressSystem.currentLifes == 0:
                break
            i += 1
        self.assertEqual(game.playerProgressSystem.currentLifes, 0)
        del game
        
    def test_pause(self):
        game = GameManager()
        game.gameSystem.endinit()
        for event in pygame.event.get():
            game.input(event)
        game.menuSystem.currentIndex = 0
        game.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        for event in pygame.event.get():
            game.input(event)
        game.input(pygame.event.Event(pygame.KEYUP, key=pygame.K_p))
        for event in pygame.event.get():
            game.input(event)
        game.input(pygame.event.Event(pygame.KEYUP, key=pygame.K_p))
        for event in pygame.event.get():
            game.input(event)
        self.assertIsNot(game.gameSystem.getcurrentgamestate() & GameState.PAUSED, 0)
        del game
        
if __name__ == '__main__':
    unittest.main()