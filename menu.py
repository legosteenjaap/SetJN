import pygame
from button import Button
from optionbutton import OptionButton
from pygame import (
    Surface
)
import os
import textrender
class Menu():

    def __init__(self, screen: Surface, screenSize):
        self.screen = screen
        self.screenSize = screenSize
        self.isFinished = False
        self.shouldCloseWindow = False
        self.startButton = Button(screen, "start", screenSize[0] / 2, screenSize[1] / 2, self.startGame)
        self.buttonYDiff = self.startButton.rect.height
        self.numPlayerButton = OptionButton(screen, ["singleplayer", "multiplayer"], screenSize[0] / 2, screenSize[1] / 2 + self.buttonYDiff, self.switchMultiplayer)
        self.inputButton = OptionButton(screen, ["mouse", "keyboard", "gamepad"], screenSize[0] / 2, screenSize[1] / 2 + self.buttonYDiff * 2, self.switchInput)
        self.difficultyButton = OptionButton(screen, ["easy", "medium", "hard"], screenSize[0] / 2, screenSize[1] / 2 + self.buttonYDiff * 3, self.switchDifficulty)
        self.quitButton = Button(screen, "quit", screenSize[0] / 2, screenSize[1] / 2 + self.buttonYDiff * 4, self.quitGame)
        self.buttons = [self.startButton, self.numPlayerButton, self.inputButton, self.quitButton]
        self.selectedButtonIndex = 0
        self.isMultiplayer = False
        self.input = "mouse"
        self.timeOutTime = 45
        self.lastPressedButtons = pygame.mouse.get_pressed()
        self.state = "playing"

    def tick(self): 

        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        self.updateHoveredOverButtonMouse()

        for event in pygame.event.get():
            self.handleEvent(event)
        self.tickRender()


    def tickRender(self):
        #Fills the screen with a greenish color
        self.screen.fill((32,134,29))

        widthMultiplier = (self.screenSize[0] / 1920)
        heightMultiplier = (self.screenSize[1] / 1080)
        installPath = os.path.dirname(os.path.realpath(__file__))
        logo = pygame.transform.scale(pygame.image.load(os.path.join(installPath, "assets", "logo.png")), (820 * widthMultiplier, 480 * heightMultiplier))
        rect = logo.get_rect()
        self.screen.blit(logo, (self.screenSize[0] / 2 - rect.width / 2, 0))

        if self.isMultiplayer and self.difficultyButton in self.buttons:
            self.buttons.remove(self.difficultyButton)
        elif not self.isMultiplayer and not self.difficultyButton in self.buttons:
            self.buttons.insert(3, self.difficultyButton)

        if self.isMultiplayer: textrender.drawText(self.screen, "locked", (0,0,0), self.screenSize[0] / 2, self.screenSize[1] / 2 + self.buttonYDiff * 3)

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
        if event.type == pygame.MOUSEMOTION:
            self.updateHoveredOverButtonMouse()
        if event.type == pygame.KEYDOWN:
            currentButton = self.buttons[self.selectedButtonIndex]
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                currentButton.doAction()
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.selectedButtonIndex = max(self.selectedButtonIndex - 1, 0)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.selectedButtonIndex = min(self.selectedButtonIndex + 1, len(self.buttons) - 1)
            if type(currentButton) == OptionButton:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    currentButton.scrollLeft()
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    currentButton.scrollRight()
        if event.type == pygame.JOYHATMOTION:
            for joystick in self.joysticks:
                hat_coords = joystick.get_hat(0)
                currentButton = self.buttons[self.selectedButtonIndex]
                if hat_coords[1] == 1:
                    self.selectedButtonIndex = max(self.selectedButtonIndex - 1, 0)
                elif hat_coords[1] == -1:
                    self.selectedButtonIndex = min(self.selectedButtonIndex + 1, len(self.buttons) - 1)
                if type(currentButton) == OptionButton:
                    if hat_coords[0] == -1:
                       currentButton.scrollLeft()
                    elif hat_coords[0] == 1:
                        currentButton.scrollRight()
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                self.buttons[self.selectedButtonIndex].doAction()
                

    
    def startGame(self):
        self.isFinished = True
    
    def quitGame(self):
        self.isFinished = True
        self.shouldCloseWindow = True

    def switchDifficulty(self, difficulty: str):
        if difficulty == "easy":
            self.timeOutTime = 45
        elif difficulty == "medium":
            self.timeOutTime = 30
        elif difficulty == "hard":
            self.timeOutTime = 15

    def switchInput(self, inputType: str):
        if inputType == "mouse":
            self.numPlayerButton.setIndex(0)
            self.isMultiplayer = False
            self.input = "mouse"
        elif inputType == "keyboard":
            self.input = "keyboard"
        elif inputType == "gamepad":
            self.input = "gamepad"

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
            if button.hasCollision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                self.selectedButtonIndex = self.buttons.index(button)
        self.updateSelectedButtons()

    def updateSelectedButtons(self):
        for buttonIndex in range(0, len(self.buttons)):
            self.buttons[buttonIndex].isSelected = buttonIndex == self.selectedButtonIndex