import set_algorithms
from deck import Deck
import time
import matplotlib.pyplot as plt

deck = Deck()

def drawNCards(n: int):
    """same as drawcards function, but allows drawing more 81 cards"""
    visibleCards=[]
    while 1:
        if deck.getCardAmount() >= n:
            visibleCards = visibleCards + deck.drawCards(n)
            return visibleCards
        else:
            n-=deck.getCardAmount()
            visibleCards = visibleCards + deck.drawCards(deck.getCardAmount())
            deck.populate()
            deck.shuffle()
        

def timeFunction(k: int,function,visibleCards: list):
    """runs the function on the same visble cards k times and returns the evarage"""
    starttime = time.time()
    for i in range(k):
        function(visibleCards)
    endtime = time.time()
    return (endtime-starttime)/k

def averageTime(n: int,m: int,k: int,function):
    """runs timeFunction() on different decks m times and returns the evarage"""
    average=0
    for i in range(m):
        deck.populate()
        deck.shuffle()
        visibleCards=drawNCards(n)
        average+=timeFunction(k,function,visibleCards)/m
    return average
    

timingPrecision=1
sampleSize=1

cardamount=[]
timegraph1=[]
timegraph2=[]
comparison=[]
for i in range(3,400):
    """takes the averagetime for each cardamount (i) and plots it against the function:t=(n-2)**3/16700000"""
    print(i)
    cardamount.append(i)
    #timegraph1.append(averageTime(i,sampleSize,timingPrecision,set_algorithms.findOneSet))
    timegraph2.append(averageTime(i,sampleSize,timingPrecision,set_algorithms.findSets))
    comparison.append((i-2)**3/1680000)
#plt.plot(cardamount,timegraph1,label="time find one set function")
plt.plot(cardamount,timegraph2,label="time find set function")
plt.plot(cardamount,comparison,label="(n-2)**3/16800000")
plt.title("time complexity")
plt.xlabel("card amounts")
plt.ylabel("time(s)")
plt.show()