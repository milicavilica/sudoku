import pygame
import csv
from text_box import TextBox
from button import Button
from utils import LABEL_COLOR, BLUE_LABEL, def_font

class FileHandler:
    
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = None
        self.file_contents = None
        
    def open_file(self):
        self.file = open(self.file_name)
        self.file_contents = self.file.read()
        self.file.seek(0)
        self.reader = csv.reader(self.file)
    
    def close_file(self):
        self.file.close()
        
    def get_rows(self):
        rows = []
        for row in self.reader:
            rows.append(row)
        return rows
    
    def draw_borders(self, screen, theme):
        color = LABEL_COLOR if theme == "pink" else BLUE_LABEL
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
        rows = self.get_rows()
        color = LABEL_COLOR if theme == "pink" else BLUE_LABEL
        text_boxes = []
        
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                element = rows[i][j]
                coordinates = (52 + (j*44), 52 + (i*44))
                if element == "x":
                    #draw a text box
                    t_box = TextBox(coordinates, (i, j))
                    t_box.draw(screen, theme)
                    text_boxes.append(t_box)
                else:
                    #draw a button
                    b_box = Button(element, def_font, 40, coordinates, (44, 44))
                    b_box.change_theme(theme)
                    b_box.display_button(screen)
                    rect = pygame.Rect(coordinates[0], coordinates[1], 44, 44)
                    pygame.draw.rect(screen, color , rect, 1)
                    pygame.display.update()
                    
        self.draw_borders(screen, theme)
        return text_boxes
                    
        