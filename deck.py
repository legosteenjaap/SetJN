from card import Card
import random

colors= ["red", "green", "purple"]
shapes= ["squiggle", "oval", "diamond"]
fills= ["empty", "filled", "shaded"]
numbers= ["1", "2", "3"]

class Deck:
    def __init__(self):
        self.populate()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self._cards)

    def populate(self):
        self._cards = [ Card(c, s, f, n) for c in colors for s in shapes for f in fills for n in numbers]

    def drawCards(self, amount: int):
        if len(self._cards) < amount: return False
        drawnCards = []
        for i in range(0, amount):
            drawnCards.append(self._cards.pop())
        return drawnCards
