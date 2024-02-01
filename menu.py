import pygame
from button import Button
from optionbutton import OptionButton
from pygame import (
    Surface
)
import os
import textrender
class Menu():
    """A class for representing the start menu
        Fields:
            screen (Surface): The screen on which the game is drawn
            screenSize (Surface): The size of the screen on which the game is drawn
            isDone (bool): Stores if the menu is done and if we can start the game
            shouldCloseWindow (bool): Stores if the program window should close, for example when alt + f4 is pressed
            startButton, numPlayerButton, inputButton, difficultyButton, quitButton (Button): Different buttons on the menu
            buttons (list[Button]): List of buttons on the menu
            selectedButtonIndex (int): The position in the buttons list of the button that is currently selected
            isMultiplayer (bool): (valid values: Is not True if _input equals "mouse")
            input (str): The input device used for this game (valid values: "mouse" or "keyboard")
            timeOutTime (int): The time a round takes for this game (changes with difficulty)
            """
    def __init__(self, screen: Surface, screenSize):
        self.screen = screen
        self.screenSize = screenSize

        self.isDone = False
        self.shouldCloseWindow = False
        

        self.startButton = Button(screen, "start", screenSize[0] / 2, screenSize[1] / 2, self.startGame)
        # Pixel difference between sorted buttons
        self.buttonYDiff = self.startButton.rect.height
        self.numPlayerButton = OptionButton(screen, ["singleplayer", "multiplayer"], screenSize[0] / 2, screenSize[1] / 2 + self.buttonYDiff, self.switchMultiplayer)
        self.inputButton = OptionButton(screen, ["mouse", "keyboard", "controller"], screenSize[0] / 2, screenSize[1] / 2 + self.buttonYDiff * 2, self.switchInput)
        self.difficultyButton = OptionButton(screen, ["easy", "medium", "hard"], screenSize[0] / 2, screenSize[1] / 2 + self.buttonYDiff * 3, self.switchDifficulty)
        self.quitButton = Button(screen, "quit", screenSize[0] / 2, screenSize[1] / 2 + self.buttonYDiff * 4, self.quitGame)
        
        self.buttons = [self.startButton, self.numPlayerButton, self.inputButton, self.quitButton]
        self.selectedButtonIndex = 0
        
        self.isMultiplayer = False
        self.input = "mouse"
        self.timeOutTime = 45

        self.lastPressedButtons = pygame.mouse.get_pressed()

    def tick(self):
        """Handles menu logic"""
        # Reloads all the connected controllers
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        self.updateSelectedButtons()

        for event in pygame.event.get():
            self.handleEvent(event)
        self.tickRender()


    def tickRender(self):
        """Renders the menu"""
        # Fills the screen with a greenish color
        self.screen.fill((32,134,29))

        # Scales logo to the screen resolution and renders it on the screen
        widthMultiplier = (self.screenSize[0] / 1920)
        heightMultiplier = (self.screenSize[1] / 1080)
        installPath = os.path.dirname(os.path.realpath(__file__))
        logo = pygame.transform.scale(pygame.image.load(os.path.join(installPath, "assets", "logo.png")), (820 * widthMultiplier, 480 * heightMultiplier))
        rect = logo.get_rect()
        self.screen.blit(logo, (self.screenSize[0] / 2 - rect.width / 2, 0))

        # Removes difficulty button if multiplayer is selected
        if self.isMultiplayer and self.difficultyButton in self.buttons:
            self.buttons.remove(self.difficultyButton)
        elif not self.isMultiplayer and not self.difficultyButton in self.buttons:
            self.buttons.insert(3, self.difficultyButton)

        # Renders the text locked in place of the difficulty button
        if self.isMultiplayer: textrender.drawText(self.screen, "locked", (0,0,0), self.screenSize[0] / 2, self.screenSize[1] / 2 + self.buttonYDiff * 3)

        for button in self.buttons:
            button.render()

        pygame.display.flip()

    def handleEvent(self, event):
        """Handles all pygame events."""
        if event.type == pygame.QUIT:
            self.isDone = True
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
        """Starts the game"""
        self.isDone = True
    
    def quitGame(self):
        """Quits the program"""
        self.isDone = True
        self.shouldCloseWindow = True

    def switchDifficulty(self, difficulty: str):
        """Switches difficulty"""
        if difficulty == "easy":
            self.timeOutTime = 45
        elif difficulty == "medium":
            self.timeOutTime = 30
        elif difficulty == "hard":
            self.timeOutTime = 15

    def switchInput(self, inputType: str):
        """Switches input"""
        if inputType == "mouse":
            self.numPlayerButton.setOptionIndex(0)
            self.isMultiplayer = False
            self.input = "mouse"
        elif inputType == "keyboard":
            self.input = "keyboard"
        elif inputType == "controller":
            self.input = "controller"

    def switchMultiplayer(self, mode: str):
        """Switches between single- and multiplayer"""
        if mode == "singleplayer":
            self.isMultiplayer = False
        elif mode == "multiplayer":
            if self.inputButton.optionIndex == 0:
                self.inputButton.setOptionIndex(1)
                self.switchInput("keyboard")
            self.isMultiplayer = True
        
    
    def updateHoveredOverButtonMouse(self):
        """Updates the selected button by the mouse"""
        for button in self.buttons:
            if button.hasCollision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                self.selectedButtonIndex = self.buttons.index(button)

    def updateSelectedButtons(self):
        """Tells the buttons that they are selected or not"""
        for buttonIndex in range(0, len(self.buttons)):
            self.buttons[buttonIndex].isSelected = buttonIndex == self.selectedButtonIndex