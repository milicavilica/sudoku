import pygame
import random

from button import Button
from label import Label
from screen import ScreenHandler
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, BACKDROUND_COLOR
from file_handler import FileHandler

pygame.init()


# screen
screen_handler = ScreenHandler(SCREEN_WIDTH, SCREEN_HEIGHT, "Pink Sudoku", BACKDROUND_COLOR)

# main menu
# main title
main_title = Label("SUDOKU", "Oswald", 100, (105, 110))
main_title.display_label(screen_handler.screen)
# new game button
new_game_button = Button("New Game", "Oswald", 50, (50, 8), (115, 230), (270, 50))
new_game_button.display_button(screen_handler.screen)
# continue game
continue_button = Button("Continue Game", "Oswald", 50, (5, 8), (115, 300), (270, 50))
continue_button.display_button(screen_handler.screen)
# themes button
themes_button = Button("Change theme", "Oswald", 50, (16, 8), (115, 370), (270, 50))
themes_button.display_button(screen_handler.screen)
# statistics button
statistics_button = Button("Statistics", "Oswald", 50, (55, 8), (115, 440), (270, 50))
statistics_button.display_button(screen_handler.screen)
# picture sudoku button
pic_sudoku_button = Button("Picture Sudoku", "Oswald", 50, (7, 8), (115, 510), (270, 50))
pic_sudoku_button.display_button(screen_handler.screen)
main_menu_buttons = (new_game_button, continue_button, themes_button, statistics_button, pic_sudoku_button)


# new game menu
new_game_menu_title = Label("NEW GAME", "Oswald", 90, (85, 110))
easy_mode = Button("Easy", "Oswald", 50, (90, 13), (115, 250), (270, 60))
medium_mode = Button("Medium", "Oswald", 50, (70, 13), (115, 330), (270, 60))
hard_mode = Button("Hard", "Oswald", 50, (90, 13), (115, 410), (270, 60))
back_button = Button("Back to main", "Oswald", 50, (8, 5), (140, 530), (230,40))
new_game_buttons = (easy_mode, medium_mode, hard_mode, back_button)

# easy game mode 
back_to_new_game = Button("Back", "Oswald", 35, (5, 8), (52, 508), (70, 40))
easy_mode_buttons = (back_to_new_game,)

# game modes
menu_state = "main"
theme = "pink"


pygame.display.update()

run = True
while run:
    # check which menu 
    if menu_state == "main":
        main_title.display_label(screen_handler.screen)
        for button in main_menu_buttons:
            button.display_button(screen_handler.screen)

    if menu_state == "new game":
        new_game_menu_title.display_label(screen_handler.screen)
        for button in new_game_buttons:
            button.display_button(screen_handler.screen)

    if menu_state == "easy mode":
        for button in easy_mode_buttons:
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
            
            # check if in easy mode
            elif menu_state == "easy mode":
                for button in easy_mode_buttons:
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
                elif statistics_button.collide_point(position):
                    print("statistics_button clicked")
                # if picture sdoku pressed
                elif pic_sudoku_button.collide_point(position):
                    print("pic_sudoku_button clicked")
                    
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
                    menu_state = "easy mode"
                    screen_handler.clear_screen(theme)
                    for button in easy_mode_buttons:
                        button.change_theme(theme)
    
                    files = ("sudoku easy 1.csv", "sudoku easy 2.csv", "sudoku easy 3.csv")
                    file_number = random.randint(0, 2)
                    file_handler = FileHandler(files[file_number])
                    file_handler.open_file()
                    file_handler.draw_rows(screen_handler.screen, theme)
                    file_handler.close_file()
                elif medium_mode.collide_point(position):
                    pass
                elif hard_mode.collide_point(position):
                    pass
                    
            # if in easy game mode 
            elif menu_state == "easy mode":
                menu_state = "new game"
                screen_handler.clear_screen(theme)
                new_game_menu_title.change_theme(theme)
                for button in new_game_buttons:
                    button.change_theme(theme)
                
                
                    
    pygame.time.delay(100)


pygame.quit()