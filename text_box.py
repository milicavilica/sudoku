import pygame
from utils import BUTTON_BG_COLOR, BLUE_BUTTON_BG_COLOR, LABEL_COLOR, BLUE_LABEL

class TextBox:
    
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.box = pygame.Rect(self.coordinates[0], self.coordinates[1], 44, 44)
        self.active = False
        self.text = ""
    
    def collide_point(self, position):
        return (self.coordinates[0] + 44 >= position[0] >= self.coordinates[0] and
                self.coordinates[1] + 44 >= position[1] >= self.coordinates[1])
    
    def draw(self, screen, theme):
        if theme == "pink":
            color = BUTTON_BG_COLOR
        else:
            color = BLUE_BUTTON_BG_COLOR
        
        label_color = (0,0,0)
        pygame.draw.rect(screen, color, self.box)
        if self.text:
            font = pygame.font.SysFont("Oswald", 40)
            text_surface = font.render(self.text, True, label_color)
            text_rect = text_surface.get_rect(center=self.box.center)
            screen.blit(text_surface, text_rect)
        pygame.draw.rect(screen, LABEL_COLOR, self.box, 1)
        pygame.display.update()
        
    def is_active(self):
        return self.active
    
    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False