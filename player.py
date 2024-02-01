import pygame

player1Keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE]
player2Keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN]

class Player:

    """A class for representing a player
        
        Fields:
            _points (int): The amount of the points the player has won (private)
            _name (str): The name of the player (private)
            _isComputer (bool): Stores if the player is a bot (private)
            _playerNum (int): Stores the number of the player (valid values: 1, 2) (private)
            selectedCards (list): Stores the indexes of the tables on the card that the player has selected
            hoveredOverCardIndex (int): Stores the index of the card which the player currently is hovering above
            _currentKeys (list): Stores the keybinds for the current players
            _color (str): Stores the color of the player, used for things like filenames
            """

    def __init__(self, name: str, isComputer, playerNum: int, input: str):
        self._points = 0
        self._name = name
        self._isComputer = isComputer
        self._playerNum = playerNum
        
        self.selectedCards = []
        self.hoveredOverCardIndex = playerNum + 7
        if playerNum == 1:
            self._currentKeys = player1Keys
        elif playerNum == 2:
            self._currentKeys = player2Keys
        
        #Sets the color of the player
        if playerNum == 1:
            self._color = "yellow"
        elif playerNum == 2:
            self._color = "cyan"

    def addPoint(self):
        """Gives a point to the player"""
        self._points += 1

    def removePoint(self):
        """Removes a point from the player"""
        self._points = max(self._points - 1, 0)

    def getPoints(self):
        """Returns the points of the player"""
        return self._points
    
    def isComputer(self):
        """Returns if the player is a computer"""
        return self._isComputer

    def getName(self):
        """Returs the name of the player"""
        if self.isComputer(): return "computer"
        return self._name
    
    def getColor(self):
        """Returns the color of the player"""
        return self._color
    
    def getRGBValue(self):
        """Returns the RGBValue of the color of the player"""
        if self._playerNum == 1:
            return (255, 216, 0)
        elif self._playerNum == 2:
            return (33, 182, 196)

    def selectCard(self, cardIndex: int):
        """Selects a card as this player"""
        if cardIndex in self.selectedCards:
            self.selectedCards.remove(cardIndex)
            return
        self.selectedCards.append(cardIndex)

    def handleKeyboardInput(self, key):
        """Handles keyboard input"""
        if key == self._currentKeys[0] and (self.hoveredOverCardIndex != 11 and self.hoveredOverCardIndex != 5):
            self.hoveredOverCardIndex += 1 
        if key == self._currentKeys[1] and (self.hoveredOverCardIndex != 6 and self.hoveredOverCardIndex != 0):
            self.hoveredOverCardIndex -=1
        if key == self._currentKeys[2] and self.hoveredOverCardIndex <= 5:
            self.hoveredOverCardIndex += 6
        if key == self._currentKeys[3] and self.hoveredOverCardIndex > 5:
            self.hoveredOverCardIndex -=6
        if key == self._currentKeys[4]:
            self.selectCard(self.hoveredOverCardIndex)
        
    def handleControllerDPadInput(self, axis):
        """Handles controller D-Pad input"""
        if axis == (-1, 0) and (self.hoveredOverCardIndex != 11 and self.hoveredOverCardIndex != 5):
            self.hoveredOverCardIndex += 1 
        if axis == (1, 0) and (self.hoveredOverCardIndex != 6 and self.hoveredOverCardIndex != 0):
            self.hoveredOverCardIndex -=1
        if axis == (0, 1) and self.hoveredOverCardIndex <= 5:
            self.hoveredOverCardIndex += 6
        if axis == (0, -1) and self.hoveredOverCardIndex > 5:
            self.hoveredOverCardIndex -=6
    
    def handleControllerButtonInput(self, button):
        """Handles controller button input"""
        if button == 0:
            self.selectCard(self.hoveredOverCardIndex)

