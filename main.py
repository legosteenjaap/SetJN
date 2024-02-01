import pygame
from game import Game
from menu import Menu

running = True

pygame.init()
pygame.joystick.init()
screenInfo = pygame.display.Info()
screenSize = (screenInfo.current_w, screenInfo.current_h)
screen=pygame.display.set_mode(screenSize)
pygame.display.toggle_fullscreen()
menu = Menu(screen, screenSize)

#Loop which runs the game untill you quit the game
while running:

    while not menu.isFinished:
        menu.tick()

    if menu.shouldCloseWindow:
        running = False
        break

    game = Game(screen, screenSize, menu.isMultiplayer, menu.input, menu.timeOutTime)
    while not game.isFinished:
        game.tick()

    if game.shouldCloseWindow: 
        running = False
    else:
        menu.isFinished = False

pygame.quit()