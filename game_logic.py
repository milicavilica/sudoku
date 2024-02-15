import pygame
import csv
import random
from utils import LABEL_COLOR, SEL_SQUARE, BLUE_LABEL

class GameLogic:
    
    def __init__(self, text_boxes, f_handler, current_game_path):
        self.text_boxes = text_boxes
        self.f_handler = f_handler
        self.notes_on = False
        self.current_game_path = current_game_path
        self.hint_count = 0
        self.mistakes = 0
        self.completed = False
        self.rows = self.__extract_file()
        
        
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
                
    def __extract_file(self):
        with open(self.current_game_path, mode="r") as curr_file:
            reader = csv.reader(curr_file)
            rows = []
            for row in reader:
                rows.append(row)
        return rows
                
    def __valid_digit(self, digit, grid_coordinates, rows):
        digit_i = grid_coordinates[0]
        digit_j = grid_coordinates[1]
        for i in range(0, len(rows)):
            for j in range(0, len(rows[i])):
                if (i == digit_i and rows[i][j] == str(digit) or
                    j == digit_j and rows[i][j] == str(digit)):
                    return False
        
        startRow = digit_i - digit_i % 3
        startCol = digit_j - digit_j % 3
        for i in range(3):
            for j in range(3):
                if rows[i + startRow][j + startCol] == str(digit):
                    return False
                
        return True
           
    def back_track(self, temp_rows, i, j):
        if i == 8 and j == 9:
            return True
            
        if j == 9:
            i += 1
            j = 0
                
        if temp_rows[i][j] != 'x':
            return self.back_track(temp_rows,i,j+1)
            
        for num in range(1, 10):
            if self.__valid_digit(num,(i, j), temp_rows):
                temp_rows[i][j] = str(num)
                if self.back_track(temp_rows, i, j + 1):
                    return True
            temp_rows[i][j] = 'x'
        return False
                
    def give_hint(self, screen, theme):
        self.hint_count += 1
        temp_rows = [row[:] for row in self.rows]
        empty_boxes = [box for box in self.text_boxes if box.text == ""]
        if len(empty_boxes) == 0:
            self.completed = True
        else:
            box = random.choice(empty_boxes)
            i, j = box.grid_coordinates
            if self.back_track(temp_rows, 0, 0):
                new_value = temp_rows[i][j]
                self.rows[i][j] = new_value
                self.update_current_game_file(new_value, (i, j))
                box.text = str(new_value)
                box.draw(screen, theme)
                
                self.update_current_game_file(box.text, box.grid_coordinates)
                self.f_handler.draw_borders(screen, theme)
                
            else:
                print("back tracking was false") # pop up "No solution this puzzle right now"
        
             
    def handle_input(self, event, screen, theme):
        for box in self.text_boxes:
            if event.type == pygame.KEYDOWN and box.is_active():
                if not self.notes_on:
                    if hasattr(event, 'key') and event.key == pygame.K_BACKSPACE:
                        # Handle backspace key
                        box.text = box.text[:-1]
                    elif event.unicode.isdigit() and (int(event.unicode) != 0):
                        # Append the pressed key to the text 
                        if self.__valid_digit(event.unicode, box.grid_coordinates, self.rows):
                            box.text = event.unicode
                            self.rows[box.grid_coordinates[0]][box.grid_coordinates[1]] = box.text
                        else:
                            self.mistakes += 1
                    box.draw(screen, theme)
                    self.update_current_game_file(box.text, box.grid_coordinates)
                    self.f_handler.draw_borders(screen, theme)
                    box.deactivate()
                    
                else:
                    if hasattr(event, 'key') and event.key == pygame.K_BACKSPACE:
                        # Handle backspace key
                        box.notes = []
                        box.draw(screen, theme)
                        self.f_handler.draw_borders(screen, theme)
                        box.deactivate()
                    elif event.unicode.isdigit() and (int(event.unicode) != 0):
                        # Append the pressed key to the text
                        box.notes.append(event.unicode)
                        box.draw_notes(screen, theme)
        empty_boxes = [box for box in self.text_boxes if box.text == ""]
        if not len(empty_boxes):
            self.completed = True
                        
    def fill_table(self, game_id, time, conn):
        cursor = conn.cursor()
        command = "UPDATE game_data SET hints = {h}, mistakes = {m}, time = {t}, completed = {c} WHERE id = {id}".format(h=self.hint_count, m=self.mistakes, t=time, c=self.completed, id=game_id)
        cursor.execute(command)
        conn.commit()
        conn.close()