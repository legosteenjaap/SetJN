from card import Card
from deck import Deck
import random

validprimes=[1,6,8,27]
def isSet(cardlist: list):
    """returns if the imputed cards make a set"""
    for property in range(0,4):
        primefactors=1
        for card in cardlist:
            card=card.toVector()
            primefactors=primefactors*card[property]
        if not primefactors in validprimes:
            return False
    return True

def findSet(visibleCards: list):
    """voert isSet() uit op alle mogelijke card combinaties"""
    solutions=[]
    for i in range(0,len(visibleCards)-2):
        for j in range(i+1,len(visibleCards)-1):
            for k in range(j+1,len(visibleCards)):
                if isSet([visibleCards[i],visibleCards[j],visibleCards[k]]):
                    solutions.append([i,j,k])
    return solutions


deck=Deck()
visibleCards=deck.drawCards(12)
solutions=findSet(visibleCards)

print(visibleCards)
print(solutions)

if len(solutions)>0: #print 1 oplossing
    print(solutions[random.randint(0,len(solutions)-1)])
else:
    print("no solutions")



