from card import Card
from deck import Deck

validprimes=[1,6,8,27]
def isSet(cardlist: list):
    """Returns if the inputed cards make a set."""
    for property in range(0,4):
        primefactors=1
        for card in cardlist:
            card=card.toVector()
            primefactors=primefactors*card[property]
        if not primefactors in validprimes:
            return False
    return True

def findSets(visibleCards: list):
    """Executes isSet() on al possible card cominations and returns all solutions"""
    solutions=[]
    for i in range(0,len(visibleCards)-2):
        for j in range(i+1,len(visibleCards)-1):
            for k in range(j+1,len(visibleCards)):
                if isSet([visibleCards[i],visibleCards[j],visibleCards[k]]):
                    solutions.append([i,j,k])
    return solutions

def findOneSet(visibleCards: list):
    """Executes isSet() on al possible card cominations and returns the first solution it finds"""
    solutions=[]
    for i in range(0,len(visibleCards)-2):
        for j in range(i+1,len(visibleCards)-1):
            for k in range(j+1,len(visibleCards)):
                if isSet([visibleCards[i],visibleCards[j],visibleCards[k]]):
                    return [i,j,k]
    return solutions