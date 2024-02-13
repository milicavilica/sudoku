import pygame
import csv
from utils import LABEL_COLOR, SEL_SQUARE, BLUE_LABEL

class GameLogic:
    
    def __init__(self, text_boxes, f_handler, current_game_path):
        self.text_boxes = text_boxes
        self.f_handler = f_handler
        self.notes_on = False
        self.current_game_path = current_game_path
        
    def _select_text_box(self, box, screen, color):
        box.activate()
        pygame.draw.rect(screen, color, box.box, 1)
        
    def _deselect_text_box(self, box, screen, color):
        box.deactivate()
        pygame.draw.rect(screen, color, box.box, 1)
        
    def notes_switch(self, notes):
        self.notes_on = notes
    
    def activate_box(self, position, theme, screen):
        color_selected = SEL_SQUARE
        color_normal = LABEL_COLOR if theme == "pink" else BLUE_LABEL
        for box in self.text_boxes:
            if box.collide_point(position):
                self._select_text_box(box, screen, color_selected)
            else:
                self._deselect_text_box(box, screen, color_normal)
                
    def update_current_game_file(self, digit, position):
        with open(self.current_game_path, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)
            
        rows[position[0]][position[1]] = digit
        with open(self.current_game_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)
                
    def handle_input(self, event, screen, theme):
        for box in self.text_boxes:
            if event.type == pygame.KEYDOWN and box.is_active():
                if not self.notes_on:
                    if event.key == pygame.K_BACKSPACE:
                        # Handle backspace key
                        box.text = box.text[:-1]
                    elif event.unicode.isdigit() and (int(event.unicode) != 0) and not box.text:
                        # Append the pressed key to the text #####################################check game logic
                        box.text += event.unicode
                    box.draw(screen, theme)
                    self.update_current_game_file(box.text, box.grid_coordinates)
                    self.f_handler.draw_borders(screen, theme)
                    box.deactivate()
                else:
                    if event.key == pygame.K_BACKSPACE:
                        # Handle backspace key
                        box.notes = []
                        box.draw(screen, theme)
                        self.f_handler.draw_borders(screen, theme)
                        box.deactivate()
                    elif event.unicode.isdigit() and (int(event.unicode) != 0):
                        # Append the pressed key to the text
                        box.notes.append(event.unicode)
                        box.draw_notes(screen, theme)