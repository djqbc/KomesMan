import sys, pygame

from binaryboardtospritesconverter import BinaryBoardToSpritesConverter
from board import Board
from predefinedboard import PredefinedBoard
from sprite.komesmansprite import KomesManSprite
from sprite.copsprite import CopSprite
from map import Map

from system.drawsystem import DrawSystem
from system.usermovementsystem import UserMovementSystem
from system.aimovementsystem import AiMovementSystem
from system.tagsystem import TagSystem
from entity import Entity
from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
from artifact.tagartifact import TagArtifact, TagType
from system.collisionsystem import CollisionSystem
from artifact.behaviorartifact import BehaviorArtifact
from behavior.simplecopbehavior import SimpleCopBehavior
from behavior.komesmanbehavior import KomesManBehavior
from system.gamesystem import GameSystem, GameState
from sprite.beersprite import BeerSprite
from behavior.beerbehavior import BeerBehavior
from myevents import REMOVE_OBJECT_EVENT
from sprite.drugsprite import DrugSprite
from behavior.drugbehavior import DrugBehavior
from sprite.capsprite import CapSprite
from behavior.capbehavior import CapBehavior
from sprite.textsprite import TextSprite
from system.menusystem import MenuSystem
from sprite.simpleimagesprite import SimpleImageSprite
from sprite.hudsprite import HUDSprite
from system.hudsystem import HUDSystem

class GameManager:
    '''Class managing game state''' 
    screen = None
    drawSystem = DrawSystem()
    userMoveSystem = UserMovementSystem()
    aiMoveSystem = AiMovementSystem()
    tagSystem = TagSystem()
    collisionSystem = CollisionSystem()
    gameSystem = GameSystem()
    menuSystem = MenuSystem()
    hudSystem = HUDSystem()
    allSystems = {
        hudSystem.NAME : hudSystem,
        tagSystem.NAME : tagSystem,
        collisionSystem.NAME : collisionSystem,
        userMoveSystem.NAME : userMoveSystem, 
        aiMoveSystem.NAME : aiMoveSystem, 
        drawSystem.NAME : drawSystem,
        gameSystem.NAME : gameSystem,
        menuSystem.NAME : menuSystem
        }#kolejnosc moze byc wazna
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768), 0, 32)
        pygame.display.set_caption('KomesMan')        
        self.init()
    
    def update(self, _timeDelta):
        '''Updates current game state'''
        for _, system in self.allSystems.items():
            system.update(_timeDelta, self.allSystems)
    
    def init(self):
        #TODO: usunac helpery - przeniesc je do osobnej klasy/klas builderow czy cos w tym stylu
        self.helperCreateBoard(BinaryBoardToSpritesConverter().convert(PredefinedBoard().get_board_binary()))
        self.helperCreateKomesMan()
        self.helperCreateCop(200, 64)
        self.helperCreateCop(400, 64)
        self.helperCreateBeer(0, 320)
        self.helperCreateDrug(448, 320)
        self.helperCreateCap(640, 320)
        self.helperCreateCap(640, 448)
        self.helperCreateMenuBackground(0, 0)
        self.helperCreateMenuElement(490, 550, "Play", None)
        self.helperCreateMenuElement(490, 600, "Exit", None)
        self.helperCreateHUD(950, 10)
        #self.helperCreateBoard(PredefinedBoard().get_board())
        self.m = Map()
        self.m.generate()
        
        self.gameSystem.endInit()
    
    def render(self, _updateMidstep):
        '''Renders currect scene'''
        self.screen.fill(pygame.Color('black'))
#         self.m.draw(self.screen)
        self.drawSystem.draw(self.screen)
        pygame.display.flip()
    
    def input(self, _event):
        if _event.type == REMOVE_OBJECT_EVENT:
            for _, system in self.allSystems.items():
                system.remove(_event.reference)
        else:
            for _, system in self.allSystems.items():
                system.input(_event)
    
    def quit(self):
        return self.gameSystem.quit()
    
    def helperCreateKomesMan(self):
        komesMan = Entity()
        komesMan.addArtifact(SpriteArtifact(KomesManSprite(), 64, 64, GameState.GAME))
        komesMan.addArtifact(MovementArtifact())
        komesMan.addArtifact(TagArtifact("KomesMan", TagType.KOMESMAN))
        komesMan.addArtifact(BehaviorArtifact(KomesManBehavior()))
        self.tagSystem.register(komesMan)
        self.userMoveSystem.register(komesMan)
        self.drawSystem.register(komesMan)
        self.collisionSystem.register(komesMan)
        
    def helperCreateCop(self, _x, _y):
        cop = Entity()
        cop.addArtifact(SpriteArtifact(CopSprite(), _x, _y, GameState.GAME))
        cop.addArtifact(MovementArtifact(0.3))
        cop.addArtifact(TagArtifact("Enemy", TagType.ENEMY))
        cop.addArtifact(BehaviorArtifact(SimpleCopBehavior()))
        self.aiMoveSystem.register(cop)
        self.drawSystem.register(cop)
        self.tagSystem.register(cop)
        self.collisionSystem.register(cop)
        
    def helperCreateBeer(self, _x, _y):
        beer = Entity()
        beer.addArtifact(SpriteArtifact(BeerSprite(), _x, _y, GameState.GAME))
        beer.addArtifact(TagArtifact("Item", TagType.ITEM))
        beer.addArtifact(BehaviorArtifact(BeerBehavior()))
        self.drawSystem.register(beer)
        self.tagSystem.register(beer)
        self.collisionSystem.register(beer)
    
    def helperCreateDrug(self, _x, _y):
        drug = Entity()
        drug.addArtifact(SpriteArtifact(DrugSprite(), _x, _y, GameState.GAME))
        drug.addArtifact(TagArtifact("Item", TagType.ITEM))
        drug.addArtifact(BehaviorArtifact(DrugBehavior()))
        self.drawSystem.register(drug)
        self.tagSystem.register(drug)
        self.collisionSystem.register(drug)
        
    def helperCreateCap(self, _x, _y):
        cap = Entity()
        cap.addArtifact(SpriteArtifact(CapSprite(), _x, _y, GameState.GAME))
        cap.addArtifact(TagArtifact("Item", TagType.ITEM))
        cap.addArtifact(BehaviorArtifact(CapBehavior()))
        self.drawSystem.register(cap)
        self.tagSystem.register(cap)
        self.collisionSystem.register(cap)
    
    def helperCreateMenuElement(self, _x, _y, _text, _parent):
        menu = Entity()
        menu.addArtifact(SpriteArtifact(TextSprite(_text), _x, _y, GameState.MENU))
        self.drawSystem.register(menu)
        self.menuSystem.register(menu, _parent)
        return menu
    
    def helperCreateMenuBackground(self, _x, _y):
        bg = Entity()
        bg.addArtifact(SpriteArtifact(SimpleImageSprite('res/img/logo.png'), _x, _y, GameState.MENU))
        self.drawSystem.register(bg)
        
    def helperCreateHUD(self, _x, _y):
        hud = Entity()
        hud.addArtifact(SpriteArtifact(HUDSprite(), _x, _y, GameState.GAME))
        self.drawSystem.register(hud)
        self.hudSystem.register(hud)

    def helperCreateBoard(self, predefinedboard):
        board = Board(predefinedboard, self.allSystems)

