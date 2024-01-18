from card import Card


colors= ["red", "green", "purple"]
shapes= ["squiggle", "oval", "diamond"]
fills= ["empty", "filled", "shaded"]
numbers= ["1", "2", "3"]

class Deck:
    def __init__(self):
        self._cards = [ Card(c, s, f, n) for c in colors for s in shapes for f in fills for n in numbers] 



