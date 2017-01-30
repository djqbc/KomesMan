"""
Board builder package
"""
import time
import pygame

from binaryboarditemsgetter import BinaryBoardItemsGetter
from binaryboardtospritesconverter import BinaryBoardToSpritesConverter
from board import Board
from pathfinder import Pathfinder
from predefinedboard import PredefinedBoard
from entity import Entity
from myevents import GAME_EVENT, GameEventType, GAME_STATE_CHANGE_EVENT
from myevents import MENU_EVENT, MenuEventType
from generatedboard import GeneratedBoard

from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
from artifact.tagartifact import TagArtifact, TagType, TagSubType
from artifact.behaviorartifact import BehaviorArtifact

from behavior.simplecopbehavior import SimpleCopBehavior
from behavior.komesmanbehavior import KomesManBehavior
from behavior.beerbehavior import BeerBehavior
from behavior.drugbehavior import DrugBehavior
from behavior.capbehavior import CapBehavior
from behavior.pillbehavior import PillBehavior
from behavior.teleportbehavior import TeleportBehavior
from behavior.baitbehavior import BaitBehavior

from sprite.komesmansprite import KomesManSprite
from sprite.copsprite import CopSprite
from sprite.capsprite import CapSprite
from sprite.drugsprite import DrugSprite
from sprite.beersprite import BeerSprite
from sprite.pillsprite import PillSprite
from sprite.dummysprite import DummySprite
from sprite.baitsprite import BaitSprite

from system.playerprogresssystem import PlayerProgressSystem
from system.gamesystem import GameState
from system.aimovementsystem import AiMovementSystem
from system.collisionsystem import CollisionSystem
from system.tagsystem import TagSystem
from system.usermovementsystem import UserMovementSystem
from system.drawsystem import DrawSystem

class BoardBuilder:
    """
    Class responsible for preparing game board for play.
    """

    def __init__(self, _systems):
        """
        Constructor
        :param _systems: Reference to systems collection
        """
        self.systems = _systems
        self.elements = []
        self.binaryboard = None
        self.tile_size = 32
        self.last_data = None

    def build(self, _restart=False):
        """
        Function responsible for building board for game:
         - Generate board
         - Convert board to sprites
         - Insert items.
        After finishing sends event starting game.
        :param _restart: Defines whether board should be
        generated again (f.e. after continuing game)
        :return:
        """
        print("Build")
        resolution_x, resolution_y = (1024, 768)
        self.systems[CollisionSystem.NAME].tile_size = self.tile_size

        if not _restart:
            if self.systems[PlayerProgressSystem.NAME].currentLevel == 0:
                self.binaryboard = PredefinedBoard().get_board_binary()
            else:
                self.binaryboard = GeneratedBoard().get_board_binary(resolution_x // self.tile_size,
                                                                     resolution_y // self.tile_size)
            self.createboard(BinaryBoardToSpritesConverter().convert(self.binaryboard), False)
        else:
            self.createboard(BinaryBoardToSpritesConverter().convert(self.binaryboard), True)
        print("Board created")
        itemsgetter = BinaryBoardItemsGetter()
        itemsgetter.load_items(self.binaryboard)

        pygame.event.post(
            pygame.event.Event(GAME_EVENT, reason=GameEventType.SET_MAX_POINTS
                               , maxPoints=len(itemsgetter.caps)))

        print("Creating items")
        for pill in itemsgetter.pills:
            self.createpill(pill[0] * self.tile_size, pill[1] * self.tile_size)
        for cap in itemsgetter.caps:
            self.createcap(cap[0] * self.tile_size, cap[1] * self.tile_size)
        for amph in itemsgetter.amphs:
            self.createdrug(amph[0] * self.tile_size, amph[1] * self.tile_size)
        for beer in itemsgetter.beers:
            self.createbeer(beer[0] * self.tile_size, beer[1] * self.tile_size)
        for enemy in itemsgetter.enemies:
            self.createcop(enemy[0] * self.tile_size, enemy[1] * self.tile_size)
        self.createkomesman(itemsgetter.komesman[0] * self.tile_size
                            , itemsgetter.komesman[1] * self.tile_size)
        for teleport in itemsgetter.teleports:
            self.createteleport(teleport[0] * self.tile_size
                                , teleport[1] * self.tile_size)

        print("Starting")
        pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT
                                             , state=GameState.GAME | GameState.PAUSED))

    def clear(self):
        """
        Clears board elements from other systems.
        :return: nothing
        """
        for entity in self.elements:
            for _, system in self.systems.items():
                system.remove(entity)
        self.elements.clear()

    def process_menu_event(self, _event):
        """
        Processes input events for MENU_EVENT
        :param _event: event to process
        :return: nothing
        """
        if _event.action == MenuEventType.START_NEW_GAME \
                or _event.action == MenuEventType.CONTINUE_GAME:
            self.clear()
            self.build()
        elif _event.action == MenuEventType.RESTART_GAME:
            self.clear()
            self.build(True)
        elif _event.action == MenuEventType.CHANGE_TILE_SIZE:
            if self.tile_size == 128:
                self.tile_size = 16
            else:
                self.tile_size *= 2

    def input(self, _event):
        """
        Processes input events for:
         - recreating the board (MENU_EVENT)
         - removing and adding objects (GAME_EVENT)
        :param _event: event to process
        :return: nothing
        """
        if _event.type == MENU_EVENT:
            self.process_menu_event(_event)
        elif _event.type == GAME_EVENT:
            if _event.reason == GameEventType.REMOVE_OBJECT:
                try:
                    self.elements.remove(_event.reference)
                    for _, system in self.systems.items():
                        system.remove(_event.reference)
                except:
                    pass
            elif _event.reason == GameEventType.SPAWN_OBJECT:
                if _event.spawntype == TagType.ENEMY \
                        and _event.spawnsubtype == TagSubType.SUPER_COP:
                    self.createsupercop(_event.x, _event.y)
                elif _event.spawntype == TagType.ITEM \
                        and _event.spawnsubtype == TagSubType.BAIT:
                    self.createbait(_event.x, _event.y)

    def createkomesman(self, komesx, komesy):
        """
        Creates our hero - KomesMan
        :param komesx: integer X position
        :param komesy: integer Y position
        :return: nothing
        """
        komes_man = Entity()
        komes_man.addartifact(SpriteArtifact(KomesManSprite(self.tile_size)
                                             , komesx, komesy, GameState.GAME))
        komes_man.addartifact(MovementArtifact())
        komes_man.addartifact(TagArtifact(TagType.KOMESMAN))
        komes_man.addartifact(BehaviorArtifact(KomesManBehavior()))
        self.systems[TagSystem.NAME].register(komes_man)
        self.systems[UserMovementSystem.NAME].register(komes_man)
        self.systems[DrawSystem.NAME].register(komes_man)
        self.systems[CollisionSystem.NAME].register(komes_man)
        self.elements.append(komes_man)

    def createcop(self, copx, copy):
        """
        Creates cop.
        :param copx: integer X position
        :param copy: integer Y position
        :return: nothing
        """
        cop = Entity()
        cop.addartifact(SpriteArtifact(CopSprite(self.tile_size), copx, copy, GameState.GAME))
        cop.addartifact(MovementArtifact(1))
        cop.addartifact(TagArtifact(TagType.ENEMY, TagSubType.SIMPLE_COP))
        cop.addartifact(BehaviorArtifact(SimpleCopBehavior()))
        self.systems[AiMovementSystem.NAME].register(cop)
        self.systems[DrawSystem.NAME].register(cop)
        self.systems[TagSystem.NAME].register(cop)
        self.systems[CollisionSystem.NAME].register(cop)
        self.elements.append(cop)

    def createsupercop(self, supercopx, supercopy):
        """
        Creates super cop.
        :param supercopx: integer X position
        :param supercopy: integer Y position
        :return:
        """
        cop = Entity()
        cop.addartifact(SpriteArtifact(CopSprite(self.tile_size)
                                       , supercopx, supercopy, GameState.GAME))
        cop.addartifact(MovementArtifact(1.25))
        cop.addartifact(TagArtifact(TagType.ENEMY, TagSubType.SUPER_COP))
        cop.addartifact(BehaviorArtifact(SimpleCopBehavior()))
        self.systems[AiMovementSystem.NAME].register(cop)
        self.systems[DrawSystem.NAME].register(cop)
        self.systems[TagSystem.NAME].register(cop)
        self.systems[CollisionSystem.NAME].register(cop)
        self.elements.append(cop)

    def createbeer(self, beerx, beery):
        """
        Creates bottle of beer
        :param beerx: integer X position
        :param beery: integer Y position
        :return: nothing
        """
        beer = Entity()
        beer.addartifact(SpriteArtifact(BeerSprite(self.tile_size), beerx, beery, GameState.GAME))
        beer.addartifact(TagArtifact(TagType.ITEM, TagSubType.BEER))
        beer.addartifact(BehaviorArtifact(BeerBehavior()))
        self.systems[DrawSystem.NAME].register(beer)
        self.systems[TagSystem.NAME].register(beer)
        self.systems[CollisionSystem.NAME].register(beer)
        self.elements.append(beer)

    def createbait(self, baitx, baity):
        """
        Creates bait for cops
        :param baitx: integer X position
        :param baity: integer Y position
        :return: nothing
        """
        bait = Entity()
        bait.addartifact(SpriteArtifact(BaitSprite(self.tile_size), baitx, baity, GameState.GAME))
        bait.addartifact(TagArtifact(TagType.ITEM, TagSubType.BAIT))
        bait.addartifact(BehaviorArtifact(BaitBehavior()))
        self.systems[DrawSystem.NAME].register(bait)
        self.systems[TagSystem.NAME].register(bait)
        self.systems[CollisionSystem.NAME].register(bait)
        self.elements.append(bait)

    def createdrug(self, drugx, drugy):
        """
        Creates drug (powder)
        :param drugx: integer X position
        :param drugy: integer Y position
        :return:
        """
        drug = Entity()
        drug.addartifact(SpriteArtifact(DrugSprite(self.tile_size), drugx, drugy, GameState.GAME))
        drug.addartifact(TagArtifact(TagType.ITEM, TagSubType.DRUG))
        drug.addartifact(BehaviorArtifact(DrugBehavior()))
        self.systems[DrawSystem.NAME].register(drug)
        self.systems[TagSystem.NAME].register(drug)
        self.systems[CollisionSystem.NAME].register(drug)
        self.elements.append(drug)

    def createcap(self, capx, capy):
        """
        Creates beer cap
        :param capx: integer X position
        :param capy: integer Y position
        :return:
        """
        cap = Entity()
        cap.addartifact(SpriteArtifact(CapSprite(self.tile_size), capx, capy, GameState.GAME))
        cap.addartifact(TagArtifact(TagType.ITEM, TagSubType.CAP))
        cap.addartifact(BehaviorArtifact(CapBehavior()))
        self.systems[DrawSystem.NAME].register(cap)
        self.systems[TagSystem.NAME].register(cap)
        self.systems[CollisionSystem.NAME].register(cap)
        self.elements.append(cap)

    def createteleport(self, teleportx, teleporty):
        """
        Creates teleport
        :param teleportx: integer X position
        :param teleporty: integer Y position
        :return:
        """
        teleport = Entity()
        teleport.addartifact(SpriteArtifact(DummySprite(self.tile_size)
                                            , teleportx, teleporty, GameState.GAME))
        teleport.addartifact(TagArtifact(TagType.FIXED, TagSubType.TELEPORT))
        teleport.addartifact(BehaviorArtifact(TeleportBehavior()))
        self.systems[DrawSystem.NAME].register(teleport)
        self.systems[TagSystem.NAME].register(teleport)
        self.systems[CollisionSystem.NAME].register(teleport)
        self.elements.append(teleport)

    def createpill(self, pillx, pilly):
        """
        Creates pill
        :param pillx: integer X position
        :param pilly: integer Y position
        :return:
        """
        pill = Entity()
        pill.addartifact(SpriteArtifact(PillSprite(self.tile_size), pillx, pilly, GameState.GAME))
        pill.addartifact(TagArtifact(TagType.ITEM, TagSubType.PILL))
        pill.addartifact(BehaviorArtifact(PillBehavior()))
        self.systems[DrawSystem.NAME].register(pill)
        self.systems[TagSystem.NAME].register(pill)
        self.systems[CollisionSystem.NAME].register(pill)
        self.elements.append(pill)

    def createboard(self, predefinedboard, uselastdata):
        """
        Creates board and prepares paths if not prepared.
        :param predefinedboard: Array of sprites
        :param uselastdata: Bool value determining if paths have already been calculated.
        :return: nothing
        """
        Board(predefinedboard, self.systems, self.elements, self.tile_size)
        start = int(round(time.time() * 1000))
        if not uselastdata:
            self.last_data = Pathfinder(predefinedboard)
            self.last_data.prepareallstepsforshortestpaths()
            print("Pathfinder time: ", int(round(time.time() * 1000)) - start)
        self.systems[AiMovementSystem.NAME].register(self.last_data)
        self.elements.append(self.last_data)
