import set_algorithms
from deck import Deck
import time
import matplotlib.pyplot as plt

deck = Deck()

def drawNCards(cardAmount: int):
    """Same as drawcards function, but allows drawing more 81 cards"""
    visibleCards = []
    while True:
        if deck.getCardAmount() >= cardAmount:
            visibleCards = visibleCards + deck.drawCards(cardAmount)
            return visibleCards
        else:
            cardAmount -= deck.getCardAmount()
            visibleCards = visibleCards + deck.drawCards(deck.getCardAmount())
            deck.populate()
            deck.shuffle()
        

def timeFunction(timingPrecision: int, function, visibleCards: list):
    """Runs the function on the same visble cards k times and returns the average"""
    starttime = time.time()
    for i in range(timingPrecision):
        function(visibleCards)
    endtime = time.time()
    return (endtime-starttime) / timingPrecision

def averageTime(cardAmount: int ,sampleSize: int ,timingPrecision: int,function):
    """Runs timeFunction() on different decks m times and returns the average"""
    average = 0
    for i in range(sampleSize):
        deck.populate()
        deck.shuffle()
        visibleCards = drawNCards(cardAmount)
        average += timeFunction(timingPrecision,function,visibleCards) / sampleSize
    return average
    

timingPrecision=1
sampleSize=1

cardAmounts = []
timeGraph1 = []
timeGraph2 = []
comparison = []

c = 1680000

for cardAmount in range(3, 400):
    """Takes the averagetime for each cardAmount and plots it against the function: t = (cardAmount-2) ^ 3 / c"""
    print(cardAmount)
    cardAmounts.append(cardAmount)
    timeGraph2.append(averageTime(cardAmount,sampleSize,timingPrecision,set_algorithms.findSets))
    comparison.append((cardAmount - 2) ** 3 / c)

plt.plot(cardAmounts,timeGraph2,label = "time find set function")
plt.plot(cardAmounts,comparison,label = "(cardAmount-2)**3/c")

plt.title("time complexity")
plt.xlabel("card amounts")
plt.ylabel("time(s)")

plt.show()