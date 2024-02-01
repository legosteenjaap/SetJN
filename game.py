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

    def __init__(self, screen: Surface, screenSize, isMultiplayer: bool, input: str, timeOutTime: int):
        self.screen = screen
        self.screenSize = screenSize
        self._isMultiplayer = isMultiplayer
        self._input = input
        if not isMultiplayer :
            self.timeOutTime = timeOutTime
        else:
            self.timeOutTime = 30
        self.currentRounds = 0
        self.player1 = Player("player1", False, 1)
        self.player2 = Player("player2", not isMultiplayer, 2)
        self.players = [self.player1, self.player2]
        self.deck = Deck()
        self.table = Table(self.deck, screenSize)    
        self.isFinished = False
        self.shouldCloseWindow = False
        self.lastPressedButtons = pygame.mouse.get_pressed()
        self.startRound()
        
    def startRound(self):
        self.currentRounds += 1
        self.startTime = pygame.time.get_ticks()

    def tick(self):
        if (self._input == "mouse"): 
            self.updateHoveredOverCardMouse(self.players[0])
        
        for player in self.players:
            self.playerCheckIfSet(player)
        for event in pygame.event.get():
            self.handleEvent(event)

        if pygame.time.get_ticks() >= self.startTime + self.timeOutTime * 1000:
            self.timeOut()

        self.tickRender()

    def tickRender(self):
        #Fills the screen with a greenish color
        self.screen.fill((32,134,29))
        
        self.table.displayCards(self.screen, self.players)

        textrender.drawText(self.screen, str(self.timeOutTime - int((pygame.time.get_ticks() - self.startTime) / 1000)), (255, 216, 0), self.screenSize[0] / 10 * 9, self.screenSize[1] / 10)

        textrender.drawText(self.screen, self.player1.getName() + ": " + str(self.player1.getPoints()), (255, 216, 0), self.screenSize[0] / 20 * 3, self.screenSize[1] / 10 * 9)
        textrender.drawText(self.screen, self.player2.getName() + ": " + str(self.player2.getPoints()), (33, 182, 196), self.screenSize[0] / 20 * 17, self.screenSize[1] / 10 * 9)
        pygame.display.flip()

    def handleEvent(self, event):
        """Handles all pygame events."""
        if event.type == pygame.QUIT:
            self.isFinished = True
            self.shouldCloseWindow = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.isFinished = True
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
                player.addPoint()
                if self.deck.getCardAmount() >= 3:
                    self.table.replaceThreeCards(self.deck, player.selectedCards)
                    self.startRound()
                else :
                    self.gameEnd()
            else:
                player.removePoint()
            
            player.selectedCards.clear()

    def updateHoveredOverCardMouse(self, player: Player):
        x, y = pygame.mouse.get_pos()
        player.hoveredOverCardIndex = self.table.getCardIndexFromPos(x, y)




    def timeOut(self):
        if not self._isMultiplayer:
            self.players[1].addPoint()
        if self.deck.getCardAmount() >= 3:
            if self._isMultiplayer:
                self.table.insertThreeNewCards(self.deck)
            else:
                solution = set_algorithms.findOneSet(self.table.getCardList())
                if len(solution) == 3:
                    self.table.replaceThreeCards(self.deck, solution)
                else:
                    self.table.insertThreeNewCards(self.deck)
            for player in self.players:
                player.selectedCards.clear()
            self.startRound()
        else:
            self.gameEnd()

    def playerWin(self, player: Player):
        print(player.getName() + " has won")
    
    def gameIsDraw(self):
        print("Draw")

    def gameEnd(self):
        pointList = []
        print("game end")
        if self.player1.getPoints() == self.player2.getPoints():
            self.gameIsDraw()
        elif self.player1.getPoints() > self.player2.getPoints():
            self.playerWin(self.player1)
        else:
            self.playerWin(self.player2)
        self.isFinished = True