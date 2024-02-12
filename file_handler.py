import pygame
import csv
from text_box import TextBox
from button import Button
from utils import LABEL_COLOR, BLUE_LABEL

class FileHandler:
    
    def __init__(self, file_name):
        path = 'C:/Users/HP/python projects/Final/resources/'
        path += file_name
        self.file_name = path
        self.file = None
        
    def open_file(self):
        self.file = open(self.file_name)
        self.reader = csv.reader(self.file)
    
    def close_file(self):
        self.file.close()
        
    def _get_rows(self):
        rows = []
        for row in self.reader:
            rows.append(row)
        return rows
    
    def _draw_borders(self, screen, color):
        for i in range(3):
            for j in range(3):
                rect = pygame.Rect(52+j*132, 52+i*132, 132, 132)
                top_width = 5 if not i else 4
                bottom_width = 5 if i == 2 else 4
                left_width = 5 if not j else 4
                right_width = 5 if j == 2 else 4
                pygame.draw.line(screen, color, (rect.left, rect.top), (rect.right, rect.top), top_width)
                pygame.draw.line(screen, color, (rect.right, rect.top), (rect.right, rect.bottom), right_width)
                pygame.draw.line(screen, color, (rect.left, rect.bottom), (rect.right, rect.bottom), bottom_width)
                pygame.draw.line(screen, color, (rect.left, rect.top), (rect.left, rect.bottom), left_width)
        pygame.display.update()
    
    def draw_rows(self, screen, theme):
        rows = self._get_rows()
        color = LABEL_COLOR if theme == "pink" else BLUE_LABEL
        
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                element = rows[i][j]
                coordinates = (52 + (j*44), 52 + (i*44))
                if element == "x":
                    #draw a text box
                    t_box = TextBox(coordinates)
                    t_box.draw(screen, theme)
                else:
                    #draw a button
                    b_box = Button(element, "Oswald", 40, (15, 10), coordinates, (44, 44))
                    b_box.change_theme(theme)
                    b_box.display_button(screen)
                    rect = pygame.Rect(coordinates[0], coordinates[1], 44, 44)
                    pygame.draw.rect(screen, color , rect, 1)
                    pygame.display.update()
                    
        self._draw_borders(screen, color)
                    
        