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
        buttonYDiff = self.startButton.rect.height
        self.numPlayerButton = OptionButton(screen, ["singleplayer", "multiplayer"], screenSize[0] / 2, screenSize[1] / 2 + buttonYDiff, self.switchMultiplayer)
        self.inputButton = OptionButton(screen, ["mouse", "keyboard"], screenSize[0] / 2, screenSize[1] / 2 + buttonYDiff * 2, self.switchInput)
        self.quitButton = Button(screen, "quit", screenSize[0] / 2, screenSize[1] / 2 + buttonYDiff * 3, self.quitGame)
        self.buttons = [self.startButton, self.numPlayerButton, self.inputButton, self.quitButton]
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

        for button in self.buttons:
            button.render()
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
    
    def quitGame(self):
        self.isFinished = True
        self.shouldCloseWindow = True

    def switchInput(self, inputType: str):
        if inputType == "mouse":
            self.numPlayerButton.setIndex(0)
            self.isMultiplayer = False
            self.input = "mouse"
        elif inputType == "keyboard":
            self.input = "keyboard"

    def switchMultiplayer(self, mode: str):
        if mode == "singleplayer":
            self.isMultiplayer = False
        elif mode == "multiplayer":
            if self.inputButton.optionIndex == 0:
                self.inputButton.setIndex(1)
                self.switchInput("keyboard")
            self.isMultiplayer = True
        
    
    def updateHoveredOverButtonMouse(self):
        for button in self.buttons:
            button.isSelected = button.hasCollision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])