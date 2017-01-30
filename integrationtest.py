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
        GAME = GameManager()
        GAME.input(pygame.event.Event(pygame.QUIT, state=GameState.END))
        self.assertEqual(GAME.gameSystem.getcurrentgamestate(), GameState.END)
        del GAME
        
    def test_change_tile_size(self):
        GAME = GameManager()
        GAME.gameSystem.endinit()
        for event in pygame.event.get():
            GAME.input(event)
        self.assertEqual(GAME.builders[0].tile_size, 32)
        GAME.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        GAME.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        GAME.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        GAME.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        for event in pygame.event.get():
            GAME.input(event)
        self.assertEqual(GAME.builders[0].tile_size, 64)
        del GAME
    
    def test_changing_highscores(self):
        with open("highscores.txt", "w") as file:
            file.write("Mateusz III Wielki|0\n")
            file.write("JBK|1000\n")
            file.write("real|9999\n")
            file.write("pepe|-1\n")
        GAME = GameManager()
        GAME.gameSystem.endinit()
        for event in pygame.event.get():
            GAME.input(event)
        GAME.menuSystem.current_index = 0
        GAME.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        GAME.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        GAME.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        for event in pygame.event.get():
            GAME.input(event)
        names = [e.artifacts[SpriteArtifact.NAME].sprite.textcontent for e in GAME.builders[1].highscorenames]
        values = [e.artifacts[SpriteArtifact.NAME].sprite.textcontent for e in GAME.builders[1].highscorevalues]
        xN = len([s for s in names if s != 'x'])
        names = names[:xN]
        values = values[:xN]
        expected = {"1 Mateusz III Wielki" : '0', 
                    "2 JBK" : '1000',
                    "3 real" : '9999',
                    "4 pepe" : '-1'}
        self.assertDictEqual(dict(zip(names, values)), expected)
        del GAME
        
    def test_lost_game(self):
        GAME = GameManager()
        GAME.gameSystem.endinit()
        for event in pygame.event.get():
            GAME.input(event)
        GAME.menuSystem.current_index = 0
        GAME.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        for event in pygame.event.get():
            GAME.input(event)
        GAME.input(pygame.event.Event(pygame.KEYUP, key=pygame.K_p))
        i = 0
        while True:
            for event in pygame.event.get():
                GAME.input(event)
            GAME.update(0.01)
#             GAME.render()
            if GAME.gameSystem.getcurrentgamestate() & GameState.PAUSED:
                GAME.input(pygame.event.Event(pygame.KEYUP, key=pygame.K_p))
            if len(GAME.tagSystem.getentities(TagType.ENEMY)) == 0 or i > 10000:
                print("Reload")
                pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.WON_GAME))
            if GAME.playerProgressSystem.current_lifes == 0:
                break
            i += 1
        self.assertEqual(GAME.playerProgressSystem.current_lifes, 0)
        del GAME
        
    def test_pause(self):
        GAME = GameManager()
        GAME.gameSystem.endinit()
        for event in pygame.event.get():
            GAME.input(event)
        GAME.menuSystem.current_index = 0
        GAME.input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        for event in pygame.event.get():
            GAME.input(event)
        GAME.input(pygame.event.Event(pygame.KEYUP, key=pygame.K_p))
        for event in pygame.event.get():
            GAME.input(event)
        GAME.input(pygame.event.Event(pygame.KEYUP, key=pygame.K_p))
        for event in pygame.event.get():
            GAME.input(event)
        self.assertIsNot(GAME.gameSystem.getcurrentgamestate() & GameState.PAUSED, 0)
        del GAME
        
if __name__ == '__main__':
    unittest.main()