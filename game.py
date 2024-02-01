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
            _timeOutTime: TODO"""

    def __init__(self, screen: Surface, screenSize, isMultiplayer: bool, input: str, timeOutTime: int):
        self.screen = screen
        self.screenSize = screenSize
        self._isMultiplayer = isMultiplayer
        self._input = input
        
        if not isMultiplayer :
            self._timeOutTime = timeOutTime
        else:
            self._timeOutTime = 30

        self.player1 = Player("player1", False, 1)
        self.player2 = Player("player2", not isMultiplayer, 2)
        self.players = [self.player1, self.player2]

        self.deck = Deck()
        self.table = Table(self.deck, screenSize) 

        self.isFinished = False
        self.shouldCloseWindow = False
        self.lastPressedButtons = pygame.mouse.get_pressed()

        self.state = "playing"
        self.blinkingCards = []
        self.announcementPlayer = self.player1

        self.currentRounds = 0
        self.startRound()
        
    def startRound(self):
        self.currentRounds += 1
        self.startTime = pygame.time.get_ticks()
        self.stateStartTime = self.startTime

    def tick(self):
        if (self.currentRounds >= 5 and self.state == "playing"): self.gameEnd()

        self.tickState()        

        if self.state == "playing":
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
        #Fills the screen with a greenish color
        self.screen.fill((32,134,29))
        
        self.table.displayCards(self.screen, self.players, self.blinkingCards, self.stateStartTime)

        timer = str(self._timeOutTime - int((pygame.time.get_ticks() - self.startTime) / 1000))
        if self.state != "playing":
            timer = str(self._timeOutTime)
            self.renderSpecialState()

        textrender.drawText(self.screen, timer, (255, 216, 0), self.screenSize[0] / 10 * 9, self.screenSize[1] / 10)
        
        textrender.drawText(self.screen, self.player1.getName() + ": " + str(self.player1.getPoints()), (255, 216, 0), self.screenSize[0] / 20 * 3, self.screenSize[1] / 10 * 9)
        textrender.drawText(self.screen, self.player2.getName() + ": " + str(self.player2.getPoints()), (33, 182, 196), self.screenSize[0] / 20 * 17, self.screenSize[1] / 10 * 9)
        pygame.display.flip()

    def renderSpecialState(self):
        installPath = os.path.dirname(os.path.realpath(__file__))
        if self.state == "draw":
            textrender.drawText(self.screen, "Game is draw.", (79, 205, 104), self.screenSize[0] / 2, self.screenSize[1] / 10 * 8)
        elif self.state == "playerwin":
            winAnimValue = str(int((pygame.time.get_ticks() / 200) % 4 + 1))
            winAnim = pygame.transform.scale(pygame.image.load(os.path.join(installPath, "assets", "win", self.announcementPlayer.getColor() + "SetWon" + winAnimValue + ".png")), (820, 320))
            rect = winAnim.get_rect()
            self.screen.blit(winAnim, (self.screenSize[0] / 2 - rect.width / 2, self.screenSize[1] / 2))
            textrender.drawText(self.screen, self.announcementPlayer.getName() + " won!", self.announcementPlayer.getRGBValue(), self.screenSize[0] / 2, self.screenSize[1] / 10 * 9)
        elif self.state != "newcards":
            announcementText = ""
            if self.state == "foundset":
                announcementText = " has found a set!"
            elif self.state == "wrongset":
                announcementText = " selected a wrong set."
            textrender.drawText(self.screen, self.announcementPlayer.getName() + announcementText, self.announcementPlayer.getRGBValue(), self.screenSize[0] / 2, self.screenSize[1] / 10 * 8)
        else:
            textrender.drawText(self.screen, "Placing new cards.", self.announcementPlayer.getRGBValue(), self.screenSize[0] / 2, self.screenSize[1] / 10 * 8)

    def handleEvent(self, event):
        """Handles all pygame events."""
        if event.type == pygame.QUIT:
            self.isFinished = True
            self.shouldCloseWindow = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.isFinished = True
        if self.state != "playing":
            return
        if self._input == "mouse":
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.lastPressedButtons = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONUP and self.lastPressedButtons[0]:
                x, y = pygame.mouse.get_pos()
                cardIndex = self.table.getCardIndexFromPos(x, y)
                if cardIndex != -1: 
                    self.players[0].selectCard(cardIndex)
        elif self._input == "keyboard":
            if event.type == pygame.KEYDOWN:
                for player in self.players:
                    player.handleKeyboardInput(event.key)
    
    def playerCheckIfSet(self, player: Player):
        if len(player.selectedCards) >= 3:
            if self.table.isSet(player.selectedCards):
                self.playerSet(player, player.selectedCards.copy())
                if self.deck.getCardAmount() <= 3:
                    self.gameEnd()
            else:
                self.wrongSet(player, player.selectedCards)
            
            player.selectedCards.clear()

    def updateHoveredOverCardMouse(self, player: Player):
        x, y = pygame.mouse.get_pos()
        player.hoveredOverCardIndex = self.table.getCardIndexFromPos(x, y)

    def switchState(self, state: str):
        self.state = state
        self.stateStartTime = pygame.time.get_ticks()
        
    def tickState(self):
        #Stops state if state timer is done
        if self.state != "playing" and (pygame.time.get_ticks() - self.stateStartTime) >= 3000:
            print("state stopped")
            if self.state == "foundset":
                self.table.replaceThreeCards(self.deck, self.blinkingCards)
            elif self.state == "newcards":
                self.table.insertThreeNewCards(self.deck)
            elif self.state == "playerwin" or self.state == "draw":
                self.isFinished = True
            self.blinkingCards.clear()    
            if self.state != "wrongset":
                self.startRound()
            self.state = "playing"

    def timeOut(self):
        if not self._isMultiplayer:
            solution = set_algorithms.findOneSet(self.table.getCardList())
            if len(solution) == 3: self.playerSet(self.players[1], solution)
        if self.deck.getCardAmount() >= 3:
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
        self.blinkingCards = [11, 10, 9]
        self.switchState("newcards")

    def playerSet(self, player: Player, setCards: list):
        player.addPoint()
        print(self.state)
        if self.state == "playerwin":
            return
        self.announcementPlayer = player
        self.blinkingCards = setCards
        self.switchState("foundset")

    def wrongSet(self, player: Player, setCards: list):
        self.announcementPlayer = player
        player.removePoint()
        self.blinkingCards = setCards
        self.switchState("wrongset")

    def playerWin(self, player: Player):
        self.announcementPlayer = player
        self.switchState("playerwin")
    
    def gameIsDraw(self):
        self.switchState("draw")

    def gameEnd(self):
        if self.player1.getPoints() == self.player2.getPoints():
            self.gameIsDraw()
        elif self.player1.getPoints() > self.player2.getPoints():
            self.playerWin(self.player1)
        else:
            self.playerWin(self.player2)