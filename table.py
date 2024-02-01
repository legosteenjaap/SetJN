from deck import Deck
from card import (
    Card,
    CardSprite
)

import set_algorithms
from pygame import (
    Surface
)
from card import (
    Card,
    CardSprite
)
import pygame
import os
import math

class Table:
    """A class for representing the table on which you play set
    
    Doesnt hold Card objects but CardSprite objects because this is mostly an abstraction for rendering our table
    """

    def __init__(self, startDeck: Deck, screenSize):
        self._cards = [CardSprite(screenSize) for i in range(0, 12)]
        self.screenSize = screenSize
        self.widthMultiplier = (screenSize[0] / 1920)
        self.heightMultiplier = (screenSize[1] / 1080)
        self.cardMargin = int (20 * math.sqrt(self.widthMultiplier * self.heightMultiplier))
        self.replaceAllCards(startDeck)

    def replaceAllCards(self, deck: Deck):
        """Replaces all cards on the table with new cards from a deck"""
        drawnCards = deck.drawCards(12)
        for i in range(0, 12):
            self.replaceCard(i, drawnCards[i])
    
    def getCard(self, index: int):
        """Get card on a specific index"""
        return self._cards[index]
    
    def getCardList(self):
        """Returns a list of all the cards on the table"""
        cards = []
        for index in range(0,12):
            cards.append(self._cards[index].card)
        return cards

    def getCards(self, cardIndexes: list):
        """Returns the cards on specific positions on the table"""
        cards = []
        for index in cardIndexes:
            cards.append(self._cards[index].card)
        return cards

    def isSet(self, cardIndexes: list):
        """Returns if three cards on specific positions are a set"""
        return set_algorithms.isSet(self.getCards(cardIndexes))

    def insertThreeNewCards(self, deck: Deck):
        """Inserts three new cards on the bottom right of the table and removes three from the upper left"""
        for i in range(0, 3):
            self._cards.pop()
            self._cards.insert(0, CardSprite(self._screenSize))
            self._cards[0].replaceCard(deck.drawCards(1)[0])

    def replaceCards(self, deck: Deck, cardIndexes: list):
        """Replaces cards on the table on specific positions given by a list"""

        for index in cardIndexes:
            self.replaceCard(index, deck.drawCards(1)[0])

    def replaceCard(self, index: int, card: Card):
        """Replaces a card on the table on a specific position with another card."""
        self._cards[index].replaceCard(card)

    def getCardHitBox(self, cardSprite: CardSprite, index: int):
        """Returns the hitbox of the cardSprite on screen
        
            Parameters:
                cardSprite (CardSprite): A cardSprite
                index (int): The position of the card on the list which holds all the cards on the table

            Returns: 
                hitbox (tuple): Hitbox of a card defined by the x and y of the upperleft position plus the width and height 
        """
        cardWidth = cardSprite.surf.get_width()
        cardHeight = cardSprite.surf.get_height()
        cardXPos = self._screenSize[0]/2 - (cardWidth+self.cardMargin)*(index%6-2)
        cardYPos = self._screenSize[1]/2 - (cardHeight+self.cardMargin)*((index-index%6)/6+1)
        hitbox = (cardXPos, cardYPos, cardWidth, cardHeight)
        return hitbox

    def getCardIndexFromPos(self, x: int, y: int):
        """Takes a position on the screen and returns the current index of the cardSprite on the table."""
        for index in range(0, 12):
            cardXPos, cardYPos, cardWidth, cardHeight = self.getCardHitBox(self._cards[index], index)
            if x >= cardXPos and x <= (cardXPos + cardWidth) and y >= cardYPos and y <= (cardYPos + cardHeight):
                return index
        return -1
            

    def displayCards(self, screen: Surface, players: list, blinkingCards: list, blinkingStartTime):
        """Displays a list of cardSprites on the screen."""
        for cardIndex in range(0, 12):

            # Makes sure cards blink after a player found a set
            if not (cardIndex in blinkingCards and int((pygame.time.get_ticks()- blinkingStartTime) / 500) % 2 == 0):

                cardSprite = self._cards[cardIndex]
                cardXPos, cardYPos, cardWidth, cardHeight = self.getCardHitBox(cardSprite, cardIndex)

                # Draw card transparent if it is selected
                for player in players:
                    if (cardIndex in player.selectedCards): 
                        cardSprite.surf.set_alpha(128)
                    else:
                        cardSprite.surf.set_alpha(255)

                # Draw card
                screen.blit(cardSprite.surf, (cardXPos, cardYPos))

                # Draw selection image if card is selected
                installPath = os.path.dirname(os.path.realpath(__file__))
                for player in players:
                    if not player.isComputer():
                        if cardIndex in player.selectedCards:
                            selectVersion = str(int((pygame.time.get_ticks() / 200) % 4 + 1))
                            select = pygame.transform.scale(pygame.image.load(os.path.join(installPath, "assets", "select", player.getColor() + "Select" + selectVersion + ".png")), (130 * self.widthMultiplier, 240 * self.heightMultiplier))
                            screen.blit(select, (cardXPos, cardYPos))

                # Renders hover over image if card is hovered over for each player
                if not players[0].hoveredOverCardIndex == players[1].hoveredOverCardIndex or players[1].isComputer():
                    for player in players:
                        if not player.isComputer():
                            if cardIndex == player.hoveredOverCardIndex:
                                hover = pygame.transform.scale(pygame.image.load(os.path.join(installPath, "assets", "hover", player.getColor() + "Hover.png")), (130 * self.widthMultiplier, 240 * self.heightMultiplier))
                                screen.blit(hover, (cardXPos, cardYPos))

                # If both players select the same card the colors of both players are blended
                elif cardIndex == player.hoveredOverCardIndex and not players[1].isComputer():
                    hover = pygame.transform.scale(pygame.image.load(os.path.join(installPath, "assets", "hover", "secretHover.png")), (130 * self.widthMultiplier, 240 * self.heightMultiplier))
                    screen.blit(hover, (cardXPos, cardYPos))
                



