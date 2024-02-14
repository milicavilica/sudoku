import pygame
from utils import LABEL_COLOR, BLUE_LABEL

class Label:
    
    def __init__(self, name, font, font_size, coordinates):
        self.font = pygame.font.SysFont(font, font_size)
        self.name = self.font.render(name,True, LABEL_COLOR)
        self.name_text = name
        self.color = LABEL_COLOR
        self.coordinates = coordinates
        
    def set_text(self, new_text):
        self.name_text = new_text
        self.name = self.font.render(new_text,True, self.color)
        
    def display_label(self, screen):
        screen.blit(self.name, self.coordinates)
        pygame.display.update()
        
    def change_theme(self,color):
        if color == "blue":
            self.color = BLUE_LABEL
        elif color == "pink":
            self.color = LABEL_COLOR
        self.name = self.font.render(self.name_text, True, self.color)
