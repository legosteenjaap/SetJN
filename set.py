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

table = Table()        
deck = Deck()

#Returns card positions for cards on the table
def getCardHitBox(cardSprite: CardSprite, index: int):
    cardWidth = cardSprite.surf.get_width()
    cardHeight = cardSprite.surf.get_height()
    cardXPos = screenSize[0]/2 - (cardWidth+cardMargin)*(index%6-2)
    cardYPos = screenSize[1]/2 - (cardHeight+cardMargin)*((index-index%6)/6+1)
    return (cardXPos, cardYPos, cardWidth, cardHeight)

def getCardIndexFromPos(x: int, y: int):
    global table
    for index in range(0, 12):
        cardXPos, cardYPos, cardWidth, cardHeight = getCardHitBox(table._cards[index], index)
        if x >= cardXPos and x <= (cardXPos + cardWidth) and y >= cardYPos and y <= (cardYPos + cardHeight):
            return index
    return -1
        

def displayCards(screen: Surface, cardSprites: list, selectedCards: list):
    for cardIndex in range(0, 12):
        cardSprite = cardSprites[cardIndex]
        cardXPos, cardYPos, cardWidth, cardHeight = getCardHitBox(cardSprite, cardIndex)

        #Draw card
        screen.blit(cardSprite.surf, (cardXPos, cardYPos))

        #Draw selection
        if (selectedCards[cardIndex]): pygame.draw.rect(screen, (239,170,32), pygame.Rect(cardXPos, cardYPos, cardWidth, cardHeight), 5, border_radius=7)

running = True

def handleEvent(event):
    if event.type == pygame.QUIT:
        global running 
        running = False
    if event.type == pygame.MOUSEBUTTONUP:
        x, y = pygame.mouse.get_pos()
        cardIndex = getCardIndexFromPos(x, y)
        if cardIndex != -1: 
            selectedCards[cardIndex] = not selectedCards[cardIndex]

table.replaceAllCards(deck)

while running:
    for event in pygame.event.get():
        handleEvent(event)
    
    screen.fill((32,134,29))
    displayCards(screen, table._cards, selectedCards)
    pygame.display.flip()

pygame.quit()