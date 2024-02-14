import pygame
import random
import sqlite3

from button import Button
from label import Label
from screen import ScreenHandler
from utils import (SCREEN_WIDTH, SCREEN_HEIGHT, BACKDROUND_COLOR,
                   easy_files, medium_files, hard_files, def_font,
                   current_game_path, continue_game_path, game_id)
from file_handler import FileHandler
from game_logic import GameLogic

pygame.init()

# screen
screen_handler = ScreenHandler(SCREEN_WIDTH, SCREEN_HEIGHT, "Pink Sudoku", BACKDROUND_COLOR)
clock = pygame.time.Clock()
seconds,minutes = (0,0)
timer = Label("", def_font, 25, (52, 20))

# main menu
# main title
main_title = Label("SUDOKU", def_font, 100, (105, 110))
main_title.display_label(screen_handler.screen)
# new game button
new_game_button = Button("New Game", def_font, 50, (115, 230), (270, 50))
new_game_button.display_button(screen_handler.screen)
# continue game
continue_button = Button("Continue Game", def_font, 50, (115, 300), (270, 50))
continue_button.display_button(screen_handler.screen)
# themes button
themes_button = Button("Change theme", def_font, 50, (115, 370), (270, 50))
themes_button.display_button(screen_handler.screen)
# statistics button
statistics_button = Button("Statistics", def_font, 50, (115, 440), (270, 50))
statistics_button.display_button(screen_handler.screen)
main_menu_buttons = (new_game_button, continue_button, themes_button, statistics_button)

# new game menu
new_game_menu_title = Label("NEW GAME", def_font, 90, (85, 110))
easy_mode = Button("Easy", def_font, 50, (115, 250), (270, 60))
medium_mode = Button("Medium", def_font, 50, (115, 330), (270, 60))
hard_mode = Button("Hard", def_font, 50, (115, 410), (270, 60))
back_button = Button("Back to main", def_font, 50, (140, 530), (230,40))
new_game_buttons = (easy_mode, medium_mode, hard_mode, back_button)

# game mode 
notes_on = False
back_to_new_game = Button("Back", def_font, 35, (52, 508), (70, 40))
notes = Button("Notes On", def_font, 35, (240, 508), (120, 40))
hint = Button("Hint", def_font, 35, (380, 508), (70,40))
game_mode_buttons = (back_to_new_game, notes, hint)

#pop up message
yes_b = Button("Yes", def_font, 50 ,(140, 300), (100, 50))
no_b = Button("No", def_font, 50 ,(260, 300), (100, 50))
pop_up_buttons = (yes_b, no_b)

def create_new_row():
    conn = sqlite3.connect('stats.db')
    cursor = conn.cursor()
    command = "INSERT INTO game_data (id, mode) VALUES ({}, '{}');".format(game_id, game_mode)
    cursor.execute(command)
    conn.commit()
    conn.close()

# game modes
menu_state = "main"
theme = "pink"
game_mode = None


# game logic handler
game_logic_handler = None

def draw_playing_field(file):
    screen_handler.clear_screen(theme)
    for button in game_mode_buttons:
        button.change_theme(theme)
    
    file_handler = FileHandler(file)
    file_handler.open_file()
    text_boxes = file_handler.draw_rows(screen_handler.screen, theme)
    file_handler.close_file()
    
    with open(current_game_path, mode='w') as current_game:
        current_game.write(file_handler.file_contents)
    return GameLogic(text_boxes, file_handler, current_game_path)

pygame.display.update()

game_mode_entered = False
run = True
while run:
    # check which menu 
    if menu_state == "main":
        main_title.display_label(screen_handler.screen)
        for button in main_menu_buttons:
            button.display_button(screen_handler.screen)
    
    # check if in new game menu
    if menu_state == "new game":
        new_game_menu_title.display_label(screen_handler.screen)
        for button in new_game_buttons:
            button.display_button(screen_handler.screen)
    
    #check if in game mode
    if menu_state == "game mode":
        if notes_on:
            notes.set_text("Notes Off")
        else: 
            notes.set_text("Notes On")
        for button in game_mode_buttons:
            button.display_button(screen_handler.screen)
        if not game_mode_entered:
            start_time = pygame.time.get_ticks()
            game_mode_entered = True

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        seconds = elapsed_time // 1000
        minutes = seconds // 60
        seconds %= 60
        if seconds >= 60:
            minutes += 1
            seconds = 0
        
        screen_handler.clear_rect(theme, (60, 20), timer.coordinates)
        
        timer_text = f'{int(minutes):02d}:{int(seconds):02d}'.format(minutes, seconds)
        timer.change_theme(theme)
        timer.set_text(timer_text)
        timer.display_label(screen_handler.screen)
        pygame.display.update()
    else:
        game_mode_entered = False
    
    # check if pop up message
    if menu_state == "pop up message":
        for button in pop_up_buttons:
            button.display_button(screen_handler.screen)
    # check events
    for event in pygame.event.get():
        #check if exit button is pressed
        if event.type == pygame.QUIT:
            run = False
            
        # check if hovered over a button
        if event.type == pygame.MOUSEMOTION:
            position = pygame.mouse.get_pos()
            # check if in main menu
            if menu_state == "main":
                for button in main_menu_buttons:
                    button.change_background(button.collide_point(position))
                
            # check if in new game menu
            elif menu_state == "new game":
                for button in new_game_buttons:
                    button.change_background(button.collide_point(position))
            
            # check if in game mode
            elif menu_state == "game mode":
                for button in game_mode_buttons:
                    button.change_background(button.collide_point(position))
            
            # check if pop up message
            elif menu_state == "pop up message":
                for button in pop_up_buttons:
                    button.change_background(button.collide_point(position))
                
        # check if a button is pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            
            # if in main menu
            if menu_state == "main":
                #if new game pressed
                if new_game_button.collide_point(position):
                    menu_state = "new game"
                    screen_handler.clear_screen(theme)
                    new_game_menu_title.change_theme(theme)
                    for button in new_game_buttons:
                        button.change_theme(theme)
                # if continue game button pressed
                elif continue_button.collide_point(position):
                    menu_state = "game mode"
                    game_logic_handler = draw_playing_field(continue_game_path)
                #if change theme pressed
                elif themes_button.collide_point(position):
                    if theme == "pink":
                        theme = "blue"
                        screen_handler.clear_screen(theme)
                        main_title.change_theme(theme)
                        main_title.display_label(screen_handler.screen)
                        for mm_button in main_menu_buttons:
                                mm_button.change_theme(theme)
                        pygame.display.set_caption("Blue Sudoku")
                                
                    elif theme == "blue":
                        theme = "pink"
                        screen_handler.clear_screen(theme)
                        main_title.change_theme(theme)
                        main_title.display_label(screen_handler.screen)
                        for mm_button in main_menu_buttons:
                                mm_button.change_theme(theme)
                        pygame.display.set_caption("Pink Sudoku")
                # if statistics pressed                
                elif statistics_button.collide_point(position): # TODO
                    print("statistics_button clicked")
                    
            # if in new game menu
            elif menu_state == "new game":
                # if back to main button pressed
                if back_button.collide_point(position):
                    menu_state = "main"
                    screen_handler.clear_screen(theme)
                    new_game_menu_title.change_theme(theme)
                    for button in new_game_buttons:
                        button.change_theme(theme)
                # if easy button pressed
                elif easy_mode.collide_point(position):
                    menu_state = "game mode"
                    game_mode = "easy_mode"
                    game_id += 1
                    create_new_row()
                    file_num = random.randint(0,2)
                    game_logic_handler = draw_playing_field(easy_files[file_num])
                # if medium button pressed
                elif medium_mode.collide_point(position):
                    menu_state = "game mode"
                    game_mode = "medium_mode"
                    game_id += 1
                    create_new_row()
                    file_num = random.randint(0,2)
                    game_logic_handler = draw_playing_field(medium_files[file_num])
                # if hard button pressed
                elif hard_mode.collide_point(position):
                    menu_state = "game mode"
                    game_mode = "hard_mode"
                    game_id += 1
                    create_new_row()
                    file_num = random.randint(0,2)
                    game_logic_handler = draw_playing_field(hard_files[file_num])
                    
            # if in game mode 
            elif menu_state == "game mode":
                game_logic_handler.activate_box(position, theme, screen_handler.screen)
                # if back is pressed
                if back_to_new_game.collide_point(position):
                    menu_state = "pop up message"
                    for button in pop_up_buttons:
                        button.change_theme(theme)
                    screen_handler.pop_up_message(theme, "Save progress?", yes_b, no_b)
                    time_played = minutes*60 + seconds
                    conn = sqlite3.connect('stats.db')
                    game_logic_handler.fill_table(game_id, time_played, conn)
                # if notes button is pressed
                elif notes.collide_point(position):
                    notes_on = not notes_on
                    game_logic_handler.notes_switch(notes_on)
                # if hint button is presssed
                elif hint.collide_point(position):
                    game_logic_handler.give_hint(screen_handler.screen, theme)
            elif menu_state == "pop up message":
                if yes_b.collide_point(position):
                    with open(current_game_path, mode="r") as cur_file:
                        contents = cur_file.read()
                    with open(continue_game_path, mode="w") as cont_game:
                        cont_game.write(contents)
                
                menu_state = "new game"
                screen_handler.clear_screen(theme)
                new_game_menu_title.change_theme(theme)
                for button in new_game_buttons:
                    button.change_theme(theme)
        # check if a key has been pressed
        elif event.type == pygame.KEYDOWN:
            if menu_state == "game mode":
                game_logic_handler.handle_input(event, screen_handler.screen, theme)
                
    pygame.time.delay(100)

pygame.quit()