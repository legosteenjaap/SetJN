import pygame
from pygame import (
    Surface
)
from card import (
    Card,
    CardSprite
)
from table import Table
from deck import Deck

pygame.init()
screenInfo = pygame.display.Info()
screenSize = (screenInfo.current_w, screenInfo.current_h)
screen=pygame.display.set_mode(screenSize)
pygame.display.toggle_fullscreen()

cardMargin = 20

selectedCards = [False]*12

#Returns card positions for cards on the table
def getCardHitBox(cardSprite: CardSprite, index: int):
    """Returns the hitbox of the cardSprite on screen
    
        Parameters:
            cardSprite (CardSprite): A cardSprite
            index (int): The position of the card on the list which holds all the cards on the table

        Returns: 
            hitbox (tuple): Hitbox of a card defined by the x and y of the upperleft position plus the width and height 
    """
    cardWidth = cardSprite.surf.get_width()
    cardHeight = cardSprite.surf.get_height()
    cardXPos = screenSize[0]/2 - (cardWidth+cardMargin)*(index%6-2)
    cardYPos = screenSize[1]/2 - (cardHeight+cardMargin)*((index-index%6)/6+1)
    hitbox = (cardXPos, cardYPos, cardWidth, cardHeight)
    return hitbox

def getCardIndexFromPos(x: int, y: int):
    """Takes a position on the screen and returns the current index of the cardSprite on the table."""
    global table
    for index in range(0, 12):
        cardXPos, cardYPos, cardWidth, cardHeight = getCardHitBox(table._cards[index], index)
        if x >= cardXPos and x <= (cardXPos + cardWidth) and y >= cardYPos and y <= (cardYPos + cardHeight):
            return index
    return -1
        

def displayCards(screen: Surface, cardSprites: list, selectedCards: list):
    """Displays a list of cardSprites on the screen."""
    for cardIndex in range(0, 12):
        cardSprite = cardSprites[cardIndex]
        cardXPos, cardYPos, cardWidth, cardHeight = getCardHitBox(cardSprite, cardIndex)

        #Draw card
        screen.blit(cardSprite.surf, (cardXPos, cardYPos))

        #Draw selection
        if (selectedCards[cardIndex]): pygame.draw.rect(screen, (239,170,32), pygame.Rect(cardXPos, cardYPos, cardWidth, cardHeight), 5, border_radius=7)

running = True

def handleEvent(event):
    """Handles all pygame events."""
    if event.type == pygame.QUIT:
        global running 
        running = False
    if event.type == pygame.MOUSEBUTTONUP:
        x, y = pygame.mouse.get_pos()
        cardIndex = getCardIndexFromPos(x, y)
        if cardIndex != -1: 
            selectedCards[cardIndex] = not selectedCards[cardIndex]

table = Table()        
deck = Deck()

table.replaceAllCards(deck)

while running:
    for event in pygame.event.get():
        handleEvent(event)

    #Fills the screen with a greenish color
    screen.fill((32,134,29))
    
    displayCards(screen, table._cards, selectedCards)
    pygame.display.flip()

pygame.quit()