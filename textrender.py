from pygame import Surface
import pygame
import os
import math
pygame.font.init()
pygame.init()
screenInfo = pygame.display.Info()
screenSize = (screenInfo.current_w,screenInfo.current_h)
widthMultiplier = (screenSize[0] / 1920)
heightMultiplier = (screenSize[1] / 1080)
installPath = os.path.dirname(os.path.realpath(__file__))
font = pygame.font.Font(os.path.join(installPath, "assets", "fonts", "PixelEmulator-xq08.ttf"), int(48 * math.sqrt(widthMultiplier * heightMultiplier)))

def drawText(screen: Surface, text: str, rgbColor, XPos: int, YPos: int):
    """Renders text on the center of the given position"""
    img = font.render(text, True,  rgbColor)
    rect = img.get_rect()
    screen.blit(img, (XPos - rect.width / 2, YPos - rect.height / 2))