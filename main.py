import pygame, sys
from pygame.locals import *

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((1024, 768), 0, 32)
pygame.display.set_caption('Komesman')


myimage = pygame.image.load("res/logo.png")
imagerect = myimage.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
#     windowSurface.fill(black)
    windowSurface.blit(myimage, imagerect)
    pygame.display.flip()


    