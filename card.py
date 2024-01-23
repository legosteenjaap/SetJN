import pygame
import os

from pygame.locals import RLEACCEL

colors= ["red", "green", "purple"]
shapes= ["squiggle", "oval", "diamond"]
fills= ["empty", "filled", "shaded"]
numbers= ["1", "2", "3"]

class Card(pygame.sprite.Sprite):
    def __init__(self, color, shape, fill, number):
        super(Card, self).__init__()
        self.surf = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + "/kaarten/" + color + shape + fill + number + ".gif")
        self.rect = self.surf.get_rect()
        self._color=color
        self._shape=shape
        self._fill=fill
        self._number=number

    def __repr__(self):
        return self._color, self._shape, self._fill, self._number 
    
    def color(self, color):
        if color in colors:
            self._color=color
        else: return False

    def shape(self, shape):
        if shape in shapes:
            self._shape=shape
        else: return False

    def fill(self, fill):
        if fill in fills:
            self._fill=fill
        else: return False

    def number(self, number):
        if number in numbers:
            self._number=number
        else: return False
    
    def toVector(self):
        return [colors.index(self._color)+1, shapes.index(self._shape)+1, fills.index(self._fill)+1, numbers.index(self._number)+1]


