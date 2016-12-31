from binaryboardtospritesconverter import BinaryBoardToSpritesConverter
from board import Board
from pathfinder import Pathfinder
from predefinedboard import PredefinedBoard
from sprite.komesmansprite import KomesManSprite
from sprite.copsprite import CopSprite
from entity import Entity
from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
from artifact.tagartifact import TagArtifact, TagType
from artifact.behaviorartifact import BehaviorArtifact
from behavior.simplecopbehavior import SimpleCopBehavior
from behavior.komesmanbehavior import KomesManBehavior
from system.gamesystem import GameState
from sprite.beersprite import BeerSprite
from behavior.beerbehavior import BeerBehavior
from sprite.drugsprite import DrugSprite
from behavior.drugbehavior import DrugBehavior
from sprite.capsprite import CapSprite
from behavior.capbehavior import CapBehavior
from system.aimovementsystem import AiMovementSystem
from system.collisionsystem import CollisionSystem
from myevents import GAME_EVENT, GameEventType
from system.tagsystem import TagSystem
from system.usermovementsystem import UserMovementSystem
from system.drawsystem import DrawSystem
from myevents import MENU_EVENT, MenuEventType

class BoardBuilder:
    def __init__(self, _systems):
        self.systems = _systems
        self.elements = []
    def build(self):
        #TODO wyrzucic bezwzgledne pozycjonowanie
        self.createBoard(BinaryBoardToSpritesConverter().convert(PredefinedBoard().get_board_binary()))
        self.createKomesMan()
#        self.helperCreateCop(200, 64)
        self.createCop(800, 64)
        self.createBeer(0, 320)
        self.createDrug(448, 320)
        self.createCap(640, 320)
        self.createCap(640, 448)
    def clear(self):
        for e in self.elements:
            for _, system in self.systems.items():
                system.remove(e)
        self.elements.clear()
    def input(self, _event):
        if _event.type == MENU_EVENT:
            if _event.action == MenuEventType.START_NEW_GAME:
                self.clear()
                self.build()
        elif _event.type == GAME_EVENT and _event.reason == GameEventType.REMOVE_OBJECT:
            self.elements.remove(_event.reference)
            for _, system in self.systems.items():
                system.remove(_event.reference)
            
    def createKomesMan(self):
        komesMan = Entity()
        komesMan.addArtifact(SpriteArtifact(KomesManSprite(), 64, 64, GameState.GAME))
        komesMan.addArtifact(MovementArtifact())
        komesMan.addArtifact(TagArtifact("KomesMan", TagType.KOMESMAN))
        komesMan.addArtifact(BehaviorArtifact(KomesManBehavior()))
        self.systems[TagSystem.NAME].register(komesMan)
        self.systems[UserMovementSystem.NAME].register(komesMan)
        self.systems[DrawSystem.NAME].register(komesMan)
        self.systems[CollisionSystem.NAME].register(komesMan)
        self.elements.append(komesMan)
        
    def createCop(self, _x, _y):
        cop = Entity()
        cop.addArtifact(SpriteArtifact(CopSprite(), _x, _y, GameState.GAME))
        cop.addArtifact(MovementArtifact(1))
        cop.addArtifact(TagArtifact("Enemy", TagType.ENEMY))
        cop.addArtifact(BehaviorArtifact(SimpleCopBehavior()))
        self.systems[AiMovementSystem.NAME].register(cop)
        self.systems[DrawSystem.NAME].register(cop)
        self.systems[TagSystem.NAME].register(cop)
        self.systems[CollisionSystem.NAME].register(cop)
        self.elements.append(cop)
        
    def createBeer(self, _x, _y):
        beer = Entity()
        beer.addArtifact(SpriteArtifact(BeerSprite(), _x, _y, GameState.GAME))
        beer.addArtifact(TagArtifact("Item", TagType.ITEM))
        beer.addArtifact(BehaviorArtifact(BeerBehavior()))
        self.systems[DrawSystem.NAME].register(beer)
        self.systems[TagSystem.NAME].register(beer)
        self.systems[CollisionSystem.NAME].register(beer)
        self.elements.append(beer)
    
    def createDrug(self, _x, _y):
        drug = Entity()
        drug.addArtifact(SpriteArtifact(DrugSprite(), _x, _y, GameState.GAME))
        drug.addArtifact(TagArtifact("Item", TagType.ITEM))
        drug.addArtifact(BehaviorArtifact(DrugBehavior()))
        self.systems[DrawSystem.NAME].register(drug)
        self.systems[TagSystem.NAME].register(drug)
        self.systems[CollisionSystem.NAME].register(drug)
        self.elements.append(drug)
        
    def createCap(self, _x, _y):
        cap = Entity()
        cap.addArtifact(SpriteArtifact(CapSprite(), _x, _y, GameState.GAME))
        cap.addArtifact(TagArtifact("Item", TagType.ITEM))
        cap.addArtifact(BehaviorArtifact(CapBehavior()))
        self.systems[DrawSystem.NAME].register(cap)
        self.systems[TagSystem.NAME].register(cap)
        self.systems[CollisionSystem.NAME].register(cap)
        self.elements.append(cap)
        
    def createBoard(self, predefinedboard):
        #kijowe bezposrednie przekazanie elements - mozna olac jak nikomu sie nie bedzie chcialo poprawic
        board = Board(predefinedboard, self.systems, self.elements)
        pf = Pathfinder(predefinedboard)
        pf.prepareAllStepsForShortestPaths()
        self.systems[AiMovementSystem.NAME].register(pf)
        self.elements.append(pf)