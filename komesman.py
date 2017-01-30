"""
main module
"""
import time
import pygame

from gamemanager import GameManager

GAME = GameManager()

FPS_TIME = 0.0
TIME_DELTA = 0.01

CURRENT_TIME = time.clock()
ACCUMULATOR = 0.0
NEW_TIME = 0

while not GAME.quit():
    NEW_TIME = time.clock()
    FRAME_TIME = NEW_TIME - CURRENT_TIME
    CURRENT_TIME = NEW_TIME

    ACCUMULATOR += FRAME_TIME
    while ACCUMULATOR >= TIME_DELTA:
        for event in pygame.event.get():
            GAME.input(event)
        GAME.update(TIME_DELTA)
        ACCUMULATOR -= TIME_DELTA
        FPS_TIME += TIME_DELTA
    GAME.render()
    NEW_TIME += 1
    if FPS_TIME > 1.0:
        print(NEW_TIME)
        NEW_TIME = FPS_TIME = 0
