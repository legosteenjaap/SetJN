import pygame
from pygame import (
    Surface
)
from table import Table
from deck import Deck
from player import Player
import os
import textrender
import set_algorithms

class Game:

    """A class for representing a game of SET.
    
        Fields:
            screen (Surface): The screen on which the game is drawn
            screenSize (Surface): The size of the screen on which the game is drawn
            _isMultiplayer (bool): (valid values: Is not True if _input equals "mouse") (private)
            _input (str): The input device used for this game (valid values: "mouse" or "keyboard") (private)
            _timeOutTime (int): The time a round takes for this game (changes with difficulty) (private)
            player1, player2 (Player): The 2 player objects, player2 can be real or the computer
            players (List[Player]): Holds the player objects
            _deck (Deck): The card deck for this game
            _table (Table): The table on which this game is played
            isFinished (bool): Stores if this game is finished and if we can return to the startmenu
            shouldCloseWindow (bool): Stores if the program window should close, for example when alt + f4 is pressed
            _lastPressedButtons: Stores the last pressed buttons
            _state (str): Stores the current game state, game states are mostly used for special events like finding a set or winning the game
            _blinkingCards (List): Stores a list of integer indexes for the cards that are blinking during a game state
            _announcementPlayer (Player): If an announcement about the game is broadcast this variable can be used to store the player which it is about
            """

    def __init__(self, screen: Surface, screenSize : tuple, isMultiplayer: bool, input: str, timeOutTime: int):
        self.screen = screen
        self.screenSize = screenSize
        self._isMultiplayer = isMultiplayer
        self._input = input
        
        if not isMultiplayer :
            self._timeOutTime = timeOutTime
        else:
            self._timeOutTime = 30

        self.player1 = Player("player1", False, 1, self._input)
        self.player2 = Player("player2", not isMultiplayer, 2, self._input)
        self.players = [self.player1, self.player2]

        self._deck = Deck()
        self._table = Table(self._deck, screenSize) 

        self.isFinished = False
        self.shouldCloseWindow = False
        self._lastPressedButtons = pygame.mouse.get_pressed()

        self._state = "playing"
        self._blinkingCards = []
        self._announcementPlayer = self.player1

        self.startRound()
        
    def startRound(self):
        """Starts a new round of set"""
        self.startTime = pygame.time.get_ticks()
        self.stateStartTime = self.startTime
        for player in self.players:
            player.selectedCards.clear()

    def tick(self):

        # Reloads all the connected controllers
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        self.tickState()

        if self._state == "playing":
            if (self._input == "mouse"): 
                self.updateHoveredOverCardMouse(self.players[0])
            
            for player in self.players:
                self.playerCheckIfSet(player)

            if pygame.time.get_ticks() >= self.startTime + self._timeOutTime * 1000:
                self.timeOut()

        for event in pygame.event.get():
            self.handleEvent(event)
        
        self.tickRender()

    def tickRender(self):
        """Renders the game"""

        # Fills the screen with a greenish color
        self.screen.fill((32,134,29))
        
        self._table.displayCards(self.screen, self.players, self._blinkingCards, self.stateStartTime)

        timer = str(self._timeOutTime - int((pygame.time.get_ticks() - self.startTime) / 1000))
        if self._state != "playing":
            # If a special game state is active we don't want the timer decreasing
            timer = str(self._timeOutTime)

            self.renderSpecialState()

        # Renders timer
        textrender.drawText(self.screen, timer, (255, 216, 0), self.screenSize[0] / 10 * 9, self.screenSize[1] / 10)

        # Renders remaining card amount
        textrender.drawText(self.screen, str(self._deck.getCardAmount()), (255, 216, 0), self.screenSize[0] / 10, self.screenSize[1] / 10)
        
        # Renders player scores
        textrender.drawText(self.screen, self.player1.getName() + ": " + str(self.player1.getPoints()), (255, 216, 0), self.screenSize[0] / 20 * 3, self.screenSize[1] / 10 * 9)
        textrender.drawText(self.screen, self.player2.getName() + ": " + str(self.player2.getPoints()), (33, 182, 196), self.screenSize[0] / 20 * 17, self.screenSize[1] / 10 * 9)
        
        pygame.display.flip()

    def renderSpecialState(self):
        """Renders objects for special game states"""
        installPath = os.path.dirname(os.path.realpath(__file__))
        if self._state == "draw":
            # Renders draw announcement
            textrender.drawText(self.screen, "Game is draw.", (79, 205, 104), self.screenSize[0] / 2, self.screenSize[1] / 10 * 8)

        elif self._state == "playerwin":
            
            # Creates win animation image and scales it to the screen resolution
            widthMultiplier = (self.screenSize[0] / 1920)
            heightMultiplier = (self.screenSize[1] / 1080)
            winAnimValue = str(int((pygame.time.get_ticks() / 200) % 4 + 1))
            winAnim = pygame.transform.scale(pygame.image.load(os.path.join(installPath, "assets", "win", self._announcementPlayer.getColor() + "SetWon" + winAnimValue + ".png")), (820 * widthMultiplier, 320 * heightMultiplier))
            rect = winAnim.get_rect()
            
            # Renders win animation
            self.screen.blit(winAnim, (self.screenSize[0] / 2 - rect.width / 2, self.screenSize[1] / 2))
            
            # Renders win announcement
            textrender.drawText(self.screen, self._announcementPlayer.getName() + " won!", self._announcementPlayer.getRGBValue(), self.screenSize[0] / 2, self.screenSize[1] / 10 * 9)

        elif self._state != "newcards":
            announcementText = ""
            if self._state == "foundset":
                announcementText = " has found a set!"
            elif self._state == "wrongset":
                announcementText = " selected a wrong set."

            # Renders announcement after selecting card
            textrender.drawText(self.screen, self._announcementPlayer.getName() + announcementText, self._announcementPlayer.getRGBValue(), self.screenSize[0] / 2, self.screenSize[1] / 10 * 8)

        else:

            # Renders announcement if there is a timeout which causes the game to grab 3 new cards
            textrender.drawText(self.screen, "Placing new cards.", (79, 205, 104), self.screenSize[0] / 2, self.screenSize[1] / 10 * 8)

    def handleEvent(self, event):
        """Handles all pygame events."""
        if event.type == pygame.QUIT:
            self.isFinished = True
            self.shouldCloseWindow = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.isFinished = True
        elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:
                    self.isFinished = True
        # Stops the player from interacting with the game if the game state is not playing            
        if self._state != "playing":
            return
        
        if self._input == "mouse":
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._lastPressedButtons = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONUP and self._lastPressedButtons[0]:
                x, y = pygame.mouse.get_pos()
                cardIndex = self._table.getCardIndexFromPos(x, y)
                if cardIndex != -1: 
                    self.players[0].selectCard(cardIndex)

        elif self._input == "keyboard":
            if event.type == pygame.KEYDOWN:
                for player in self.players:
                    if not player.isComputer(): player.handleKeyboardInput(event.key)

        elif self._input == "controller":
            if event.type == pygame.JOYHATMOTION:
                for player in self.players:
                    if not player.isComputer() and len(self.joysticks) >= player._playerNum: player.handleControllerDPadInput(self.joysticks[player._playerNum - 1].get_hat(0))
            elif event.type == pygame.JOYBUTTONDOWN:
                for player in self.players:
                    if not player.isComputer() and len(self.joysticks) >= player._playerNum and event.instance_id == player._playerNum - 1: player.handleControllerButtonInput(event.button)

    
    def playerCheckIfSet(self, player: Player):
        """Checks if a player has selected 3 cards"""
        if len(player.selectedCards) >= 3:
            if self._table.isSet(player.selectedCards):
                self.playerSet(player, player.selectedCards.copy())
                if self._deck.getCardAmount() <= 3:
                    self.gameEnd()
            else:
                self.wrongSet(player, player.selectedCards.copy())
            
            player.selectedCards.clear()

    def updateHoveredOverCardMouse(self, player: Player):
        """Updates the card that is hovered over with the mouse"""
        x, y = pygame.mouse.get_pos()
        player.hoveredOverCardIndex = self._table.getCardIndexFromPos(x, y)

    def switchState(self, state: str):
        """Switches game state"""
        self._state = state
        self.stateStartTime = pygame.time.get_ticks()
        
    def tickState(self):
        """Stops state if state timer is done and handles finished game state"""
        if self._state != "playing" and (pygame.time.get_ticks() - self.stateStartTime) >= 3000:
            if self._state == "foundset":
                self._table.replaceCards(self._deck, self._blinkingCards)

            elif self._state == "newcards":
                self._table.insertThreeNewCards(self._deck)

            # If a player has won or if the game has ended we want to return to the start menu
            elif self._state == "playerwin" or self._state == "draw":
                self.isFinished = True

            self._blinkingCards.clear()   
            if self._state != "wrongset":
                self.startRound()
            self._state = "playing"

    def timeOut(self):
        """Handles a timeout"""
        if not self._isMultiplayer:
            # Tries to grab a set of cards as the computer if time has run out
            solution = set_algorithms.findOneSet(self._table.getCardList())
            if len(solution) == 3: self.playerSet(self.players[1], solution)
        if self._deck.getCardAmount() >= 3:
            # We handle timeouts differently between singe- and multiplayer
            # In singleplayer the computer can grab cards, in multiplayer 3 cards are always replaced
            if self._isMultiplayer:
                self.threeNewCards()
            else:
                if len(solution) != 3:
                    self.threeNewCards()
            for player in self.players:
                player.selectedCards.clear()
        else:
            self.gameEnd()

    def threeNewCards(self):
        """Adds three new cards to the table"""
        self._blinkingCards = [11, 10, 9]
        self.switchState("newcards")

    def playerSet(self, player: Player, setCards: list):
        """Sets the game state when a player has a set"""
        player.addPoint()
        if self._state == "playerwin":
            return
        self._announcementPlayer = player
        self._blinkingCards = setCards
        self.switchState("foundset")

    def wrongSet(self, player: Player, setCards: list):
        """Sets the game state when a player has chosen a wrong set"""
        self._announcementPlayer = player
        player.removePoint()
        self._blinkingCards = setCards
        self.switchState("wrongset")

    def playerWin(self, player: Player):
        """Sets game state when a player has won"""
        self._announcementPlayer = player
        self.switchState("playerwin")
    
    def gameIsDraw(self):
        """Sets game state when the game is draw"""
        self.switchState("draw")

    def gameEnd(self):
        """Ends game and determines outcome"""
        if self.player1.getPoints() == self.player2.getPoints():
            self.gameIsDraw()
        elif self.player1.getPoints() > self.player2.getPoints():
            self.playerWin(self.player1)
        else:
            self.playerWin(self.player2)