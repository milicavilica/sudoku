import sqlite3

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
def_font = "Oswald"
current_game_path = 'C:/Users/HP/python projects/Final/resources/current game.csv'
continue_game_path = 'C:/Users/HP/python projects/Final/resources/continue game.csv'

# color for blue theme
BLUE_LABEL = (0,0,205)
BLUE_BG_COLOR = (135,206,250)
BLUE_BUTTON_BG_COLOR = (0,191,255)
BLUE_HOVERED = (30,144,255)
BLUE_SEL_SQUARE = (255,255,255)

#default color theme
BACKDROUND_COLOR = (250, 222, 247)
LABEL_COLOR = (74, 2, 125)
BUTTON_BG_COLOR = (218, 173, 247)
BUTTON_HOVERED = (195, 118, 245)
SEL_SQUARE = (255,255,255)

easy_files = ('C:/Users/HP/python projects/Final/resources/sudoku easy 1.csv',
              'C:/Users/HP/python projects/Final/resources/sudoku easy 2.csv',
              'C:/Users/HP/python projects/Final/resources/sudoku easy 3.csv')
medium_files = ('C:/Users/HP/python projects/Final/resources/sudoku medium 1.csv',
                'C:/Users/HP/python projects/Final/resources/sudoku medium 2.csv',
              'C:/Users/HP/python projects/Final/resources/sudoku medium 3.csv')
hard_files = ('C:/Users/HP/python projects/Final/resources/sudoku hard 1.csv',
                'C:/Users/HP/python projects/Final/resources/sudoku hard 2.csv',
              'C:/Users/HP/python projects/Final/resources/sudoku hard 3.csv')


# db
conn = sqlite3.connect('stats.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS game_data (id INTEGER PRIMARY KEY,mode VARCHAR,hints INTEGER, mistakes INTEGER, time INTEGER, completed BOOL)")
conn.commit()
cursor.execute("SELECT MAX(id) FROM game_data")
res = cursor.fetchall()
game_id = res[0][0] if res[0][0] else 1
conn.close()
