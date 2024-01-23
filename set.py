import pygame
from pygame import (
    Surface
)
from card import (
    Card
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

standardCard = Card("red", "squiggle", "empty", "1")
cardWidth = standardCard.surf.get_width()
cardHeight = standardCard.surf.get_height()

#Returns card positions for cards on the table
def getCardHitBox(index: int):
    global cardWidth
    global cardHeight
    cardXPos = screenSize[0]/2 - (cardWidth+cardMargin)*(index%6-2)
    cardYPos = screenSize[1]/2 - (cardHeight+cardMargin)*((index-index%6)/6+1)
    return (cardXPos, cardYPos, cardWidth, cardHeight)

def getCardIndexFromPos(x: int, y: int):
    for index in range(0,12):
        cardXPos, cardYPos, cardWidth, cardHeight = getCardHitBox(index)
        if x >= cardXPos and x <= (cardXPos + cardWidth) and y >= cardYPos and y <= (cardYPos + cardHeight):
            return index
    return -1
        

def displayCards(screen: Surface, cards: list, selectedCards: list):
    for cardIndex in range(0,12):
        
        card = cards[cardIndex]

        cardXPos, cardYPos, cardWidth, cardHeight  = getCardHitBox(cardIndex)

        #Draw card
        screen.blit(card.surf, (cardXPos, cardYPos))

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
table = Table()        
deck = Deck()
table.replaceAllCards = deck.drawCards(12)
while running:
    for event in pygame.event.get():
        handleEvent(event)
    
    screen.fill((32,134,29))
    displayCards(screen, table.cards, selectedCards)
    pygame.display.flip()

pygame.quit()