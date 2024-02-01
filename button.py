from pygame import (
    Surface
)
import textrender as textrender

class Button:

    def __init__(self, screen: Surface, text: str, XPos: int, YPos: int, action):
        self.screen = screen
        self.text = text
        self.XPos = XPos
        self.YPos = YPos
        self.isSelected = False
        self.buildTextRender(text)
        self.action = action
    
    def buildTextRender(self, text: str):
        self.img = textrender.font.render(text, True,  (0,0,0))
        self.imgSelect = textrender.font.render(text, True,  (79, 205, 104))
        self.rect = self.img.get_rect()

    def render(self):
        if not self.isSelected:
            self.screen.blit(self.img, (self.XPos - self.rect.width / 2, self.YPos - self.rect.height / 2))
        else:
            self.screen.blit(self.imgSelect, (self.XPos - self.rect.width / 2, self.YPos - self.rect.height / 2))
    
    def hasCollision(self, collisionXPos: int, collisionYPos: int):
        return self.rect.collidepoint(collisionXPos - (self.XPos - self.rect.width / 2), collisionYPos - (self.YPos - self.rect.height / 2))

    def doAction(self):
        self.action()
