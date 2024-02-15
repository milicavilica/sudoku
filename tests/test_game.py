import unittest
import sys
import os
import csv
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pygame
from unittest.mock import patch
from screen import ScreenHandler
from button import Button
from label import Label
from text_box import TextBox
from file_handler import FileHandler
from game_logic import GameLogic
from stats_handler import StatsHandler
from utils import (BACKDROUND_COLOR, BLUE_BG_COLOR, def_font, LABEL_COLOR,
                   BUTTON_BG_COLOR, BLUE_LABEL, BLUE_BUTTON_BG_COLOR, BUTTON_HOVERED, BLUE_HOVERED, SEL_SQUARE)

class TestScreen(unittest.TestCase):
    
    def setUp(self):
        pygame.init()
        
    def tearDown(self):
        pygame.quit()
    
    def test_singleton_behavior(self):
        screen_handler1 = ScreenHandler(800, 600, "Test Screen 1", BLUE_BG_COLOR)
        screen_handler2 = ScreenHandler(800, 600, "Test Screen 2", BLUE_BG_COLOR)
        
        assert screen_handler1 is screen_handler2
        
    def test_pop_up_message(self):
        screen_handler = ScreenHandler(500, 600, "Test Screen", BACKDROUND_COLOR)
        pygame.display.update()
        buttons = (Button("ok", def_font, 50, (210, 300), (80, 60)),)
        screen_handler.pop_up_message("pink", "Test message", buttons)
        assert screen_handler.background_color == BACKDROUND_COLOR
        assert screen_handler.screen.get_at((210, 300)) == BUTTON_BG_COLOR
        

class TestButton(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 600))
        pygame.display.set_caption("Test Window")

    def tearDown(self):
        pygame.quit()
        
    def test_initialization(self):
        button = Button("TestButton", "Arial", 20, (100, 100), (150, 50))
        
        self.assertEqual(button.name, "TestButton")
        self.assertEqual(button.name, "TestButton") 
        self.assertEqual(button.button_coordinates, (100, 100))
        self.assertEqual(button.dimensions, (150, 50))
        self.assertEqual(button.background_color, BUTTON_BG_COLOR)
        
    def test_set_text(self):
        button = Button("TestButton", "Arial", 20, (100, 100), (150, 50))

        button.set_text("NewText")
        self.assertEqual(button.name, "NewText")
        
    def test_change_background_hovered(self):
        button = Button("TestButton", def_font, 20, (100, 100), (150, 50))

        button.change_background(True)
        assert button.button.get_at((1,1)) == BUTTON_HOVERED
        button.change_background(False)
        assert button.button.get_at((1,1)) == BUTTON_BG_COLOR

    def test_collide_point(self):
        button = Button("TestButton", def_font, 20, (100, 100), (150, 50))

        self.assertTrue(button.collide_point((125, 125))) # inside the button
        self.assertFalse(button.collide_point((90, 90))) # outside the button

    def test_change_theme(self):
        button = Button("TestButton", def_font, 20, (100, 100), (150, 50))

        # Change theme to blue
        button.change_theme("blue")
        self.assertEqual(button.name, "TestButton")
        self.assertEqual(button.background_color, BLUE_BUTTON_BG_COLOR)
        self.assertEqual(button.background_hovered, BLUE_HOVERED)

        # Change theme back to pink 
        button.change_theme("pink")
        self.assertEqual(button.name, "TestButton")
        self.assertEqual(button.background_color, BUTTON_BG_COLOR)
        self.assertEqual(button.background_hovered, BUTTON_HOVERED)
        

class TestLabel(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        pygame.display.set_caption("Test Window")

    def tearDown(self):
        pygame.quit()
        
    def test_set_text(self):
        label = Label("TestLabel", def_font, 20, (100, 100))

        label.set_text("NewText")
        self.assertEqual(label.name_text, "NewText")
        
    def test_display_label(self):
        label = Label("TestLabel", def_font, 100, (1, 1))

        label.display_label(self.screen)
        assert self.screen.get_at((10, 10)) == label.color
        
    def test_change_theme(self):
        label = Label("TestLabel", "Arial", 20, (100, 100))

        # Change theme to blue
        label.change_theme("blue")
        self.assertEqual(label.color, BLUE_LABEL)

        # Change theme back to pink 
        label.change_theme("pink")
        self.assertEqual(label.color, LABEL_COLOR)


class TestTextBox(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 600))
        pygame.display.set_caption("Test Window")

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        textbox = TextBox((100, 100), (0, 0))
        
        self.assertEqual(textbox.coordinates, (100, 100))
        self.assertEqual(textbox.grid_coordinates, (0, 0))
        self.assertEqual(textbox.box, pygame.Rect(100, 100, 44, 44))
        self.assertFalse(textbox.is_active())
        self.assertEqual(textbox.text, "")
        self.assertEqual(textbox.notes, [])

    def test_collide_point(self):
        textbox = TextBox((100, 100), (0, 0))

        self.assertTrue(textbox.collide_point((125, 125))) # inside the textbox
        self.assertFalse(textbox.collide_point((90, 90)))  # outside the textbox

    def test_activate_deactivate(self):
        textbox = TextBox((100, 100), (0, 0))

        # Test activation and deactivation
        self.assertFalse(textbox.is_active())
        textbox.activate()
        self.assertTrue(textbox.is_active())
        textbox.deactivate()
        self.assertFalse(textbox.is_active())

    def test_draw(self):
        textbox = TextBox((100, 100), (0, 0))

        textbox.draw(self.screen, "pink")
        pygame.display.update()

        assert self.screen.get_at((101, 101)) == BUTTON_BG_COLOR

        textbox.text = "TestText"
        textbox.draw(self.screen, "blue")
        pygame.display.update()

        assert self.screen.get_at((101, 101)) == BLUE_BUTTON_BG_COLOR
        assert self.screen.get_at((101, 122)) == (0,0,0) # black

    def check_text_in_region(self, region):
        x, y, width, height = region
        for i in range(width):
            for j in range(height):
                pixel_color = self.screen.get_at((x + i, y + j))
                if pixel_color == (105, 105, 105):
                    return True
        return False
    
    def test_draw_notes(self):
        textbox = TextBox((100, 100), (0, 0))

        # Test drawing notes
        textbox.notes = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        textbox.draw_notes(self.screen, "pink")
        pygame.display.update()

        assert self.check_text_in_region((100, 100, 50, 50))
        assert self.check_text_in_region((120, 100, 50, 50))
        assert self.check_text_in_region((140, 100, 50, 50))


class TestFileHandler(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test Window")

    def tearDown(self):
        pygame.quit()
        
    def test_initialization(self):
        file_handler = FileHandler("test_file.csv")
        self.assertEqual(file_handler.file_name, "test_file.csv")
        self.assertIsNone(file_handler.file)
        self.assertIsNone(file_handler.file_contents)

    def test_open_close_file(self):
        file_handler = FileHandler("C:/Users/HP/python projects/Final/tests/test_file.csv")

        file_handler.open_file()
        self.assertIsNotNone(file_handler.file)
        self.assertIsNotNone(file_handler.file_contents)
        self.assertIsNotNone(file_handler.reader)

        file_handler.close_file()
        self.assertTrue(file_handler.file.closed)
        self.assertIsNotNone(file_handler.file)
        self.assertIsNotNone(file_handler.file_contents)
        self.assertIsNotNone(file_handler.reader)

    def test_get_rows(self):
        file_handler = FileHandler("C:/Users/HP/python projects/Final/tests/test_file.csv")
        file_handler.open_file()
        rows = file_handler.get_rows()
        file_handler.close_file()

        self.assertTrue(isinstance(rows, list))

    def test_draw_borders(self):
        file_handler = FileHandler("C:/Users/HP/python projects/Final/tests/test_file.csv")
        file_handler.open_file()
        file_handler.draw_borders(self.screen, "pink")
        pygame.display.update()
        file_handler.close_file()
        for i in range(3):
            for j in range(3):
                assert self.screen.get_at((52+j*132, 52+i*132)) == LABEL_COLOR

    def test_draw_rows(self):
        file_handler = FileHandler("C:/Users/HP/python projects/Final/tests/test_file.csv")
        file_handler.open_file()

        # Test drawing rows
        file_handler.draw_rows(self.screen, "pink")
        pygame.display.update()
        file_handler.close_file()
        for i in range(3):
            for j in range(3):
                assert self.screen.get_at((52+j*132, 52+i*132)) == LABEL_COLOR
                
        assert self.screen.get_at((55, 55)) == BUTTON_BG_COLOR
        assert self.screen.get_at((122, 70)) == LABEL_COLOR


class MockDatabase:
    
    def __init__(self):
        self.data = {}
        self.closed = False

    def execute(self, command):
        parts = command.split()
        if parts[0] == "UPDATE":
            table_name = parts[1]
            self.data[table_name] = {'1':{'hints':0}}
            set_index = parts.index("SET")
            where_index = parts.index("WHERE")
            h_field = parts[set_index + 1]
            h_value = parts[set_index + 3]
            m_field = parts[set_index + 4]
            m_value = parts[set_index + 6]
            condition_value = parts[where_index + 3]

            self.data[table_name][condition_value][h_field] = h_value
            self.data[table_name][condition_value][m_field] = m_value

    def cursor(self):
        return self
    
    def commit(self):
        pass

    def close(self):
        self.closed = True

    def fetchall(self):
        return self.data[0]
    
    def retrieve_updated_data(self):
        return self.data

class TestGameLogic(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 600))
        pygame.display.set_caption("Test Window")

        text_boxes = [TextBox((52 + j * 44, 52 + i * 44), (i, j)) for i in range(9) for j in range(9)]
        f_handler = FileHandler("C:/Users/HP/python projects/Final/tests/test_file.csv")
        f_handler.open_file()
        text_boxes = f_handler.draw_rows(self.screen, "pink")
        current_game_path = "C:/Users/HP/python projects/Final/tests/test_current_file.csv"
        with open(current_game_path, mode='w') as current_game:
            current_game.write(f_handler.file_contents)
        self.game_logic = GameLogic(text_boxes, f_handler, current_game_path)

    def tearDown(self):
        pygame.quit()

    def test_select_deselect_text_box(self):
        box = TextBox((52, 52), (0, 0))
        color_normal = LABEL_COLOR
        color_selected = SEL_SQUARE

        # test select box
        self.game_logic._select_text_box(box, self.screen, color_selected)
        pygame.display.update()
        assert self.screen.get_at((52, 55)) == SEL_SQUARE

        # test deselect_text_box
        self.game_logic._deselect_text_box(box, self.screen, color_normal)
        pygame.display.update()
        assert self.screen.get_at((52, 55)) == LABEL_COLOR
        
    def test_notes_switch(self):
        self.game_logic.notes_switch(True)
        self.assertTrue(self.game_logic.notes_on)
        self.game_logic.notes_switch(False)
        self.assertFalse(self.game_logic.notes_on)

    def test_activate_box(self):
        box = TextBox((52, 52), (0, 0))
        theme = "pink"

        # Test activate_box
        self.game_logic.activate_box((54, 54), theme, self.screen)
        self.assertTrue(box.is_active)
        assert self.screen.get_at((52, 55)) == SEL_SQUARE
        
    def test_update_current_game_file(self):
        digit = "2"
        position = (0, 0)

        self.game_logic.update_current_game_file(digit, position)

        file_path = "C:/Users/HP/python projects/Final/tests/test_current_file.csv"
        rows = []
        with open(file_path, mode="r") as curr_file:
            reader = csv.reader(curr_file)
            rows = list(reader)
        self.assertEqual(rows[position[0]][position[1]], digit)

    def test_valid_digit(self):
        digit = "1"
        grid_coordinates = (0, 0)
        
        result = self.game_logic._GameLogic__valid_digit(digit, grid_coordinates, self.game_logic.rows)
        self.assertFalse(result)

    def test_back_track(self):
        temp_rows_possible = [row[:] for row in self.game_logic.rows]
        temp_rows_impossible = [row[:] for row in self.game_logic.rows]
        temp_rows_impossible[0][2] = '1'
        i, j = 0, 0

        result1 = self.game_logic.back_track(temp_rows_possible, i, j)
        result2 = self.game_logic.back_track(temp_rows_impossible, i, j)
        self.assertTrue(result1)
        self.assertFalse(result2)

    def test_give_hint(self):
        theme = "pink"
        file_path = "C:/Users/HP/python projects/Final/tests/test_current_file.csv"
        rows = []
        with open(file_path, mode="r") as curr_file:
            reader = csv.reader(curr_file)
            rows = list(reader)
        self.game_logic.give_hint(self.screen, theme)
        
        new_rows = []
        with open(file_path, mode="r") as curr_file:
            reader = csv.reader(curr_file)
            new_rows = list(reader)
        
        self.assertNotEqual(rows, new_rows)

    def test_handle_input(self):
        event = pygame.event.Event(pygame.KEYDOWN, unicode="1")
        theme = "pink"
        self.game_logic.text_boxes[12].activate()
        self.game_logic.handle_input(event, self.screen, theme)
        self.assertTrue(self.game_logic.text_boxes[12].text)
        
        self.game_logic.text_boxes[0].activate()
        self.game_logic.handle_input(event, self.screen, theme)
        self.assertFalse(self.game_logic.text_boxes[0].text)

    def test_fill_table(self):
        game_id = 1
        time = 10
        conn = MockDatabase()
        self.game_logic.hint_count = 2
        
        self.game_logic.fill_table(game_id, time, conn)
        updated_data = conn.retrieve_updated_data()
        self.assertEqual(int(updated_data['game_data']['1']['hints'][0]), self.game_logic.hint_count)
        self.assertEqual(int(updated_data['game_data']['1']['mistakes'][0]), self.game_logic.mistakes)
        
        self.assertTrue(conn.closed)
        

if __name__ == '__main__':
    unittest.main()