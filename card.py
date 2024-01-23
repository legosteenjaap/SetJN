import pygame
import os

from pygame.locals import RLEACCEL


class Card:

    def __init__(self):
        self

    def __init__(self, color, shape, fill, number):
        self._color=color
        self._shape=shape
        self._fill=fill
        self._number=number

    def __repr__(self):
        return self._color, self._shape, self._fill, self._number 
    
    def color(self, color):
        if color in ["red", "green", "purple"]:
            self._color=color
        else: return False

    def shape(self, shape):
        if shape in ["squiggle", "oval", "diamond"]:
            self._shape=shape
        else: return False

    def fill(self, fill):
        if fill in ["empty", "filled", "shaded"]:
            self._fill=fill
        else: return False

    def number(self, number):
        if number in ["1", "2", "3"]:
            self._number=number
        else: return False

class CardSprite(pygame.sprite.Sprite):

    def __init__(self):
        super(CardSprite, self).__init__()
    
    def replaceCard(self, card: Card):
        self.surf = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + "\\kaarten\\" + card._color + card._shape + card._fill + card._number + ".gif")
        #installPath = str(os.path.dirname(os.path.realpath(__file__)))
        #print(type(installPath))
        #self.surf = pygame.image.load(installPath+ card.color + card.shape + card.fill + card.number + ".gif")
        self.rect = self.surf.get_rect()
        self.card = card