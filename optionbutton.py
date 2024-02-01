from button import Button
from pygame import Surface
class OptionButton(Button):

    """A class for representing a button with multiple option which you can scroll trough (child of Button)
        Fields:
            options (list): Holds the options through which you can scroll
            optionIndex (int): Stores the index of the option that is selected
            updateAction (callable): The function that is called when an option is changed
            """

    def __init__(self, screen: Surface, options: list, XPos: int, YPos: int, updateAction):
        super(OptionButton, self).__init__(screen, options[0], XPos, YPos, updateAction)
        self.options = options
        self.optionIndex = 0

    def scrollLeft(self):
        """Goes to the option on the left"""
        self.optionIndex = self.optionIndex - 1
        if self.optionIndex < 0:
            self.optionIndex = 0
        self.action(self.options[self.optionIndex])
        self.replaceText(self.options[self.optionIndex])


    def scrollRight(self):
        """Goes to the option on the right"""
        self.optionIndex = self.optionIndex + 1
        if self.optionIndex >= len(self.options) - 1:
            self.optionIndex = len(self.options) - 1
        self.action(self.options[self.optionIndex])
        self.replaceText(self.options[self.optionIndex])
    
    def scroll(self):
        """Scrolls through all the options"""
        self.optionIndex = self.optionIndex + 1
        if self.optionIndex >= len(self.options):
            self.optionIndex = 0
        self.replaceText(self.options[self.optionIndex])

    def setOptionIndex(self, index: int):
        """Changes and updates the button when a new option is selected"""
        self.optionIndex = index
        self.text = self.options[self.optionIndex]
        self.replaceText(self.options[self.optionIndex])

    def doAction(self):
        """Updates the contents of the button"""
        self.scroll()
        self.action(self.options[self.optionIndex])
        self.replaceText(self.options[self.optionIndex])

