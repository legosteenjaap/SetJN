from pygame import (
    Surface
)
import textrender as textrender

class Button:

    """A class for representing a renderable button
        
        Fields:
            screen (Surface): The screen on which the game is drawn
            text (str): The text displayed on the button
            xPos, yPos (int) Stores the position of the button
            action (function) Stores the function which is executed when the button is activated"""

    def __init__(self, screen: Surface, text: str, xPos: int, yPos: int, action: callable):
        self.screen = screen
        self.text = text
        self.xPos = xPos
        self.yPos = yPos
        self.isSelected = False
        self.replaceText(text)
        self.action = action
    

    def replaceText(self, text: str):
        """Replaces the text on the button"""
        self.img = textrender.font.render(text, True,  (0,0,0))
        self.rect = self.img.get_rect()

        #If the button is selected the text becomes a greenish color
        self.imgSelect = textrender.font.render(text, True,  (79, 205, 104))

    def render(self):
        """Renders the button"""
        if not self.isSelected:
            self.screen.blit(self.img, (self.xPos - self.rect.width / 2, self.yPos - self.rect.height / 2))
        else:
            self.screen.blit(self.imgSelect, (self.xPos - self.rect.width / 2, self.yPos - self.rect.height / 2))
    
    def hasCollision(self, collisionXPos: int, collisionYPos: int):
        """Checks if a point collides with the button"""
        return self.rect.collidepoint(collisionXPos - (self.xPos - self.rect.width / 2), collisionYPos - (self.yPos - self.rect.height / 2))

    def doAction(self):
        """Executes the action saved with the button"""
        self.action()
