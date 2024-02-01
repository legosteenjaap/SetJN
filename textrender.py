from pygame import Surface
import pygame
import os

pygame.font.init()
installPath = os.path.dirname(os.path.realpath(__file__))
font = pygame.font.Font(os.path.join(installPath, "assets", "fonts", "PixelEmulator-xq08.ttf"), 48)

def drawText(screen: Surface, text: str, rgbColor, XPos: int, YPos: int):
    img = font.render(text, True,  rgbColor)
    rect = img.get_rect()
    screen.blit(img, (XPos - rect.width / 2, YPos - rect.height / 2))