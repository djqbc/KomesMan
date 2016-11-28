import pygame, sys

pygame.init()
windowSurface = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('KomesMan')
basicFont = pygame.font.SysFont(None, 48)

text = basicFont.render('KomesMan', True, (255,255,255), (0,0,0))
textRect = text.get_rect()
textRect.centerx = windowSurface.get_rect().centerx
textRect.centery = windowSurface.get_rect().centery

windowSurface.fill((0,0,0))

windowSurface.blit(text, textRect)

pygame.display.update()

while True:
    for event in pygame.event.get():
        continue
