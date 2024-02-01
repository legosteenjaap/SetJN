import pygame

player1Keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE]
player2Keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN]
gamepadKeys = [0, 1, 2, 3, 4]

class Player:

    def __init__(self, name: str, isComputer, playerNum: int, input: str):
        self._points = 0
        self._name = name
        self.selectedCards = []
        self._isComputer = isComputer
        self.playerNum = playerNum
        self.hoveredOverCardIndex = playerNum + 7
        if input == "keyboard":
            if playerNum == 1:
                self.currentKeys = player1Keys
            elif playerNum == 2:
                self.currentKeys = player2Keys
        elif input == "gamepad":
            self.currentKeys = gamepadKeys
        if playerNum == 1:
            self.color = "yellow"
        elif playerNum == 2:
            self.color = "cyan"

    def addPoint(self):
        self._points+=1

    def removePoint(self):
        self._points = max(self._points - 1, 0)

    def getPoints(self):
        return self._points
    
    def isComputer(self):
        return self._isComputer

    def getName(self):
        if self.isComputer(): return "computer"
        return self._name
    
    def getColor(self):
        return self.color
    
    def getRGBValue(self):
        if self.playerNum == 1:
            return (255, 216, 0)
        elif self.playerNum == 2:
            return (33, 182, 196)

    def selectCard(self, cardIndex: int):
        if cardIndex in self.selectedCards:
            self.selectedCards.remove(cardIndex)
            return
        self.selectedCards.append(cardIndex)

    def handleKeyboardOrGamepadInput(self, key):
        print(key)
        if key == self.currentKeys[0] and (self.hoveredOverCardIndex != 11 and self.hoveredOverCardIndex != 5):
            self.hoveredOverCardIndex += 1 
        if key == self.currentKeys[1] and (self.hoveredOverCardIndex != 6 and self.hoveredOverCardIndex != 0):
            self.hoveredOverCardIndex -=1
        if key == self.currentKeys[2] and self.hoveredOverCardIndex <= 5:
            self.hoveredOverCardIndex += 6
        if key == self.currentKeys[3] and self.hoveredOverCardIndex > 5:
            self.hoveredOverCardIndex -=6
        if key == self.currentKeys[4]:
            self.selectCard(self.hoveredOverCardIndex)
        

