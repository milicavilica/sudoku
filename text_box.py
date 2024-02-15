import pygame
from utils import BUTTON_BG_COLOR, BLUE_BUTTON_BG_COLOR, def_font

class TextBox:
    
    def __init__(self, coordinates, grid_coordinates):
        self.coordinates = coordinates
        self.grid_coordinates = grid_coordinates
        self.box = pygame.Rect(self.coordinates[0], self.coordinates[1], 44, 44)
        self.active = False
        self.text = ""
        self.notes = []
    
    def collide_point(self, position):
        return (self.coordinates[0] + 44 >= position[0] >= self.coordinates[0] and
                self.coordinates[1] + 44 >= position[1] >= self.coordinates[1])
    
    def draw(self, screen, theme):
        color = BUTTON_BG_COLOR if theme == "pink" else BLUE_BUTTON_BG_COLOR
        label_color = (0,0,0)
        pygame.draw.rect(screen, color, self.box)
        if self.text:
            font = pygame.font.SysFont(def_font, 40)
            text_surface = font.render(self.text, True, label_color)
            text_rect = text_surface.get_rect(center=self.box.center)
            screen.blit(text_surface, text_rect)
        pygame.draw.rect(screen, label_color, self.box, 1)
        pygame.display.update()
        
    def draw_notes(self, screen, theme):
        label_color = (105,105,105)
        font = pygame.font.SysFont(def_font, 20)
        color = BUTTON_BG_COLOR if theme == "pink" else BLUE_BUTTON_BG_COLOR
        new_x = self.coordinates[0] + 2
        new_y = self.coordinates[1] + 2
        screen.fill(color, pygame.Rect(new_x, new_y, 40, 40))
        for note in self.notes:
            text_surface = font.render(note, True, label_color)
            text_rect = (0,0)
            match note:
                case "1":
                    text_rect = (self.coordinates[0] + 5, self.coordinates[1]+ 3)
                case "2":
                    text_rect = (self.coordinates[0] + 20, self.coordinates[1]+ 3)
                case "3":
                    text_rect = (self.coordinates[0] + 35, self.coordinates[1]+ 3)
                case "4":
                    text_rect = (self.coordinates[0] + 5, self.coordinates[1]+ 15)
                case "5":
                    text_rect = (self.coordinates[0] + 20, self.coordinates[1]+ 15)
                case "6":
                    text_rect = (self.coordinates[0] + 35, self.coordinates[1]+ 15)
                case "7":
                    text_rect = (self.coordinates[0] + 5, self.coordinates[1]+ 30)
                case "8":
                    text_rect = (self.coordinates[0] + 20, self.coordinates[1]+ 30)
                case _:
                    text_rect = (self.coordinates[0] + 35, self.coordinates[1]+ 30)    
            screen.blit(text_surface, text_rect)        
    def is_active(self):
        return self.active
    
    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False