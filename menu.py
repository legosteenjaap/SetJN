import pygame
from button import Button
from optionbutton import OptionButton
from pygame import (
    Surface
)
import os
class Menu():

    def __init__(self, screen: Surface, screenSize):
        self.screen = screen
        self.screenSize = screenSize
        self.isFinished = False
        self.shouldCloseWindow = False
        self.startButton = Button(screen, "start", screenSize[0] / 2, screenSize[1] / 2, self.startGame)
        self.numPlayerButton = OptionButton(screen, ["singleplayer", "multiplayer"], screenSize[0] / 2, screenSize[1] / 2 + self.startButton.rect.height, self.switchMultiplayer)
        self.inputButton = OptionButton(screen, ["mouse", "keyboard"], screenSize[0] / 2, screenSize[1] / 2 + self.startButton.rect.height, self.switchInput)

        self.buttons = [self.startButton, self.numPlayerButton]
        self.isMultiplayer = False
        self.input = "mouse"
        self.lastPressedButtons = pygame.mouse.get_pressed()
        self.state = "playing"

    def tick(self): 
        self.updateHoveredOverButtonMouse()

        for event in pygame.event.get():
            self.handleEvent(event)
        self.tickRender()

    def tickRender(self):
        #Fills the screen with a greenish color
        self.screen.fill((32,134,29))

        installPath = os.path.dirname(os.path.realpath(__file__))
        logo = pygame.transform.scale(pygame.image.load(os.path.join(installPath, "assets", "logo.png")), (820, 480))
        rect = logo.get_rect()
        self.screen.blit(logo, (self.screenSize[0] / 2 - rect.width / 2, 0))

        self.startButton.render()
        self.numPlayerButton.render()

        pygame.display.flip()

    def handleEvent(self, event):
        """Handles all pygame events."""
        if event.type == pygame.QUIT:
            self.isFinished = True
            self.shouldCloseWindow = True
        if event.type == pygame.MOUSEBUTTONDOWN:
                self.lastPressedButtons = pygame.mouse.get_pressed()
        if event.type == pygame.MOUSEBUTTONUP and self.lastPressedButtons[0]:
            for button in self.buttons:
                if button.isSelected:
                    button.doAction()
    
    def startGame(self):
        self.isFinished = True
    
    def switchInput(self, inputType: str):
        if inputType == "mouse":
            self.numPlayerButton.setIndex(0)


    def switchMultiplayer(self, mode: str):
        if mode == "singleplayer":
            self.isMultiplayer = False
        elif mode == "multiplayer":
            self.isMultiplayer = True
        
    
    def updateHoveredOverButtonMouse(self):
        for button in self.buttons:
            button.isSelected = button.hasCollision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])