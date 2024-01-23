from deck import Deck
from card import (
    Card,
    CardSprite
)
class Table:

    def __init__(self):
        self._cards = [CardSprite() for i in range(0, 12)]

    def replaceAllCards(self, deck: Deck):
        drawnCards = deck.drawCards(12)
        for i in range(0, 12):
            self.replaceCard(i, drawnCards[i])


    def replaceCard(self, index: int, card: Card):
        self._cards[index].replaceCard(card)

