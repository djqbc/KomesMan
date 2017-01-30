import pygame
import time

from gamemanager import GameManager

game = GameManager()

t = 0.0
TIME_DELTA = 0.005

currentTime = time.clock()
accumulator = 0.0
fps = 0

while not game.quit():
    newTime = time.clock()
    frameTime = newTime - currentTime
    currentTime = newTime

    accumulator += frameTime
    while accumulator >= TIME_DELTA:
        for event in pygame.event.get():
            game.input(event)
        game.update(TIME_DELTA)
        accumulator -= TIME_DELTA
        t += TIME_DELTA
    game.render()
    fps += 1
    if t > 1.0:
        print(fps)
        fps = t = 0
