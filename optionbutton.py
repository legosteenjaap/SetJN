from button import Button
from pygame import Surface
class OptionButton(Button):

    def __init__(self, screen: Surface, options: list, XPos: int, YPos: int, action):
        super(OptionButton, self).__init__(screen, options[0], XPos, YPos, action)
        self.options = options
        self.optionIndex = 0

    def scrollLeft(self):
        self.optionIndex = self.optionIndex - 1
        if self.optionIndex < 0:
            self.optionIndex = 0
        
        self.text = self.options[self.optionIndex]

    def scrollRight(self):
        self.optionIndex = self.optionIndex + 1
        if self.optionIndex > len(self.options) - 1:
            self.optionIndex = len(self.options) - 1
    
    def scroll(self):
        self.optionIndex = self.optionIndex + 1
        if self.optionIndex > len(self.options) - 1:
            self.optionIndex = 0

    def setIndex(self, index: int):
        self.optionIndex = index

    def doAction(self):
        self.scroll()
        self.action(self.options[self.optionIndex])
        self.buildTextRender(self.options[self.optionIndex])

