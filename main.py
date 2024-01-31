import pygame
from game import Game

running = True

pygame.init()
screenInfo = pygame.display.Info()
screenSize = (screenInfo.current_w, screenInfo.current_h)
screen=pygame.display.set_mode(screenSize)
pygame.display.toggle_fullscreen()

while running:

    game = Game(screen, screenSize, True, "keyboard", 5, 1)
    while not game.isFinished:
        game.tick()

    if game.shouldCloseWindow: running = False


pygame.quit()