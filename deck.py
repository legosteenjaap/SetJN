from card import Card
import random

colors= ["red", "green", "purple"]
shapes= ["squiggle", "oval", "diamond"]
fills= ["empty", "filled", "shaded"]
numbers= ["1", "2", "3"]

class Deck:

    """A class for representing a deck of cards."""

    def __init__(self):
        self.populate()
        self.shuffle()

    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self._cards)

    def populate(self):
        """Empties the deck and fills it again with one of every possible unique Set card."""
        self._cards = [ Card(c, s, f, n) for c in colors for s in shapes for f in fills for n in numbers]

    def drawCards(self, amount: int):
        """Removes the top cards from the deck and returns these as a list."""
        if len(self._cards) < amount: return False
        drawnCards = []
        for i in range(0, amount):
            drawnCards.append(self._cards.pop())
        return drawnCards
