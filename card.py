import pygame
import os

from pygame.locals import RLEACCEL

colors= ["red", "green", "purple"]
shapes= ["squiggle", "oval", "diamond"]
fills= ["empty", "filled", "shaded"]
numbers= ["1", "2", "3"]

class Card:

    """A class for representing a Set card with a color, shape, fill and number
    
        Fields:
            _color (str): Color of the card (valid values: "red", "green", "purple") (private)
            _shape (str): Shape of the card (valid values: "squiggle", "oval", "diamond") (private)
            _fill (str): Fill of the card (valid values: "empty", "filled", "shaded") (private)
            _number (str): Number of the card (valid values: "1", "2", "3") (private)"""

    def __init__(self, color, shape, fill, number):
        self.color(color)
        self.shape(shape)
        self.fill(fill)
        self.number(number) 

    def __repr__(self):
        # The class is represented as a string so Python can easily print it out
        return self._color + self._shape + self._fill + self._number 
    
    def color(self, color):
        """Changes the color of the card"""
        if color in colors:
            self._color=color
        else: return False

    def shape(self, shape):
        """Changes the shape of the card"""
        if shape in shapes:
            self._shape=shape
        else: return False

    def fill(self, fill):
        """Changes the fill of the card"""
        if fill in fills:
            self._fill=fill
        else: return False

    def number(self, number):
        """Changes the number of the card"""
        if number in numbers:
            self._number=number
        else: return False
    
    def toVector(self):
        """Returns the card as an array of numbers a.k.a. a vector"""
        return [colors.index(self._color) + 1, shapes.index(self._shape) + 1, fills.index(self._fill) + 1, numbers.index(self._number) + 1]

class CardSprite(pygame.sprite.Sprite):
    
    """A class for representing a renderable object that holds a card"""

    def __init__(self, screenSize):
        super(CardSprite, self).__init__()
        self._screenSize = screenSize
    
    def replaceCard(self, card: Card):
        """Replace the currently rendered card with another card"""

        # Scales the card with the resolution of your screen
        widthMultiplier = (self._screenSize[0] / 1920)
        heightMultiplier = (self._screenSize[1] / 1080)

        installPath = os.path.dirname(os.path.realpath(__file__))
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join(installPath, "assets", "cards", str(card._color + card._shape + card._fill + card._number + ".png"))), (130 * widthMultiplier, 240 * heightMultiplier))
        self.rect = self.surf.get_rect()
        self.card = card