import pygame
from utils import BUTTON_BG_COLOR, BLUE_BUTTON_BG_COLOR, LABEL_COLOR, BLUE_LABEL

class TextBox:
    
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.box = pygame.Rect(self.coordinates[0], self.coordinates[1], 44, 44)
        self.active = False
        
    def draw(self, screen, theme):
        if theme == "pink":
            color = BUTTON_BG_COLOR
        else:
            color = BLUE_BUTTON_BG_COLOR
        pygame.draw.rect(screen, color, self.box)
        pygame.draw.rect(screen, LABEL_COLOR, self.box, 1)
        pygame.display.update()
        
    def is_active(self):
        return self.active
    
    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False