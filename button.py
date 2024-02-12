import pygame
from utils import (LABEL_COLOR, BUTTON_BG_COLOR, BUTTON_HOVERED,
                    BLUE_LABEL, BLUE_BUTTON_BG_COLOR, BLUE_HOVERED)

class Button:
    
    def __init__(self, name, font, font_size, button_coord, dimensions):
        self.background_color = BUTTON_BG_COLOR
        self.background_hovered = BUTTON_HOVERED
        self.name = name
        self.font = pygame.font.SysFont(font, font_size)
        self.text = self.font.render(name, True, LABEL_COLOR)
        self.button_coordinates = button_coord
        self.dimensions = dimensions
        self.button = pygame.Surface(dimensions)
        self.button.fill(self.background_color)
        
    def display_button(self, screen):
        text_rect = self.text.get_rect(center=self.button.get_rect().center)
        self.button.blit(self.text, text_rect)
        screen.blit(self.button, self.button_coordinates)
        pygame.display.update()

    def set_text(self, new_name):
        color = LABEL_COLOR if self.background_hovered == BUTTON_HOVERED else BLUE_LABEL
        self.text = self.font.render(new_name, True, color)
    
    def change_background(self, hovered):
        if hovered:
            self.button.fill(self.background_hovered)
        else:
            self.button.fill(self.background_color)
            
    def collide_point(self, position):
        return (self.button_coordinates[0] + self.dimensions[0] >= position[0] >= self.button_coordinates[0] and
                self.button_coordinates[1] + self.dimensions[1] >= position[1] >= self.button_coordinates[1])
        
    def change_theme(self, color):
        if color == "blue":
            self.text = self.font.render(self.name, True, BLUE_LABEL)
            self.background_color = BLUE_BUTTON_BG_COLOR
            self.background_hovered = BLUE_HOVERED
            self.button.fill(self.background_color)
        elif color == "pink":
            self.text = self.font.render(self.name, True, LABEL_COLOR)
            self.background_color = BUTTON_BG_COLOR
            self.background_hovered = BUTTON_HOVERED
            self.button.fill(self.background_color)
            
