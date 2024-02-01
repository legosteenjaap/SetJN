import pygame
from game import Game
from menu import Menu

running = True

pygame.init()
screenInfo = pygame.display.Info()
screenSize = (screenInfo.current_w, screenInfo.current_h)
screen=pygame.display.set_mode(screenSize)
pygame.display.toggle_fullscreen()

while running:

    menu = Menu(screen, screenSize)
    while not menu.isFinished:
        menu.tick()

    if menu.shouldCloseWindow:
        running = False
        break

    game = Game(screen, screenSize, menu.isMultiplayer, "keyboard", 30  )
    while not game.isFinished:
        game.tick()

    if game.shouldCloseWindow: running = False

pygame.quit()