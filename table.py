from deck import Deck
from card import (
    Card,
    CardSprite
)
class Table:
    """A class for representing the table on which you play set.
    
    Doesnt hold Card objects but CardSprite objects because this is mostly an abstraction for rendering our table."""

    def __init__(self):
        self._cards = [CardSprite() for i in range(0, 12)]

    def replaceAllCards(self, deck: Deck):
        """Replaces all cards on the table with new cards from a deck."""
        drawnCards = deck.drawCards(12)
        for i in range(0, 12):
            self.replaceCard(i, drawnCards[i])


    def replaceCard(self, index: int, card: Card):
        """Replaces a card on the table on a specific position with another card."""
        self._cards[index].replaceCard(card)

