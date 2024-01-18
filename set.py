import pygame
from pygame import (
    Surface
)
from card import Card

pygame.init()

screenInfo = pygame.display.Info()
screenSize = (screenInfo.current_w, screenInfo.current_h)
screen=pygame.display.set_mode(screenSize)
pygame.display.toggle_fullscreen()

card = Card("red", "squiggle", "empty", "1") 

margin = 20

selectedCards = [False]*12

#Returns card positions for cards on the table
def getCardsPos(index: int):
    cardWidth = card.surf.get_width()
    cardHeight = card.surf.get_height()
    cardXPos = screenSize[0]/2 - (cardWidth+margin)*(index%6-2)
    cardYPos = screenSize[1]/2 - (cardHeight+margin)*((index-index%6)/6+1)
    return (cardXPos, cardYPos, cardWidth, cardHeight)

def getCardIndexFromPos(x: int, y: int):
    for index in range(0,12):
        cardXPos, cardYPos, cardWidth, cardHeight  = getCardsPos(index)
        if x >= cardXPos and x <= (cardXPos + cardWidth) and y >= cardYPos and y <= (cardYPos + cardHeight):
            return index
    return -1
        


def displayCards(screen: Surface, cards: list, selectedCards: list):
    for i in range(0,12):
        
        cardXPos, cardYPos, cardWidth, cardHeight  = getCardsPos(i)

        #Draw card
        screen.blit(card.surf, (cardXPos, cardYPos))

        #Draw selection
        if (selectedCards[i]): pygame.draw.rect(screen, (239,170,32), pygame.Rect(cardXPos, cardYPos, cardWidth, cardHeight), 5, border_radius=7)

running = True

def handleEvents(event):
    if event.type == pygame.QUIT:
        global running 
        running = False
    if event.type == pygame.MOUSEBUTTONUP:
        x, y = pygame.mouse.get_pos()
        cardIndex = getCardIndexFromPos(x, y)
        if cardIndex != -1: 
            selectedCards[cardIndex] = not selectedCards[cardIndex]
        


while running:
    for event in pygame.event.get():
        handleEvents(event)
    
    screen.fill((32,134,29))
    displayCards(screen, [card]*12, selectedCards)
    pygame.display.flip()

pygame.quit()